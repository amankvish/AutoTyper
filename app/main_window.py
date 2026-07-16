import logging
import os
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QMenu
from PySide6.QtGui import QAction, QKeySequence, QShortcut, QIcon
from PySide6.QtCore import Qt, QPoint, QSize
from app.ui import AutoTyperUI
from core.typing_engine import TypingWorker
from core.formatter import TextFormatter
from services.settings import SettingsService
from services.file_loader import FileLoaderService, UnsupportedFileTypeError, FileLoadError
from services.clipboard import ClipboardService
import config

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """
    Main Controller window representing the interface and binding UI components
    to underlying logic and worker threads.
    """
    def __init__(self, settings_service: SettingsService):
        super().__init__()
        self.settings = settings_service
        self.worker = None
        self.current_file_path = ""

        # Enable Drag & Drop
        self.setAcceptDrops(True)

        # 1. Setup UI Layout
        self.ui = AutoTyperUI()
        self.ui.setup_ui(self)

        # 2. Restore User Settings & Last Session
        self.restore_settings()

        # 3. Connect UI Event Handlers
        self.connect_signals()

        # 4. Initialize Recent Files Dropdown Menu
        self.update_recent_files_menu()

        # 5. Trigger initial stats and time update
        self.handle_text_changed()

        # 6. First launch welcome dialog
        if self.settings.get("first_launch"):
            self.show_instructions_page()
            self.settings.set("first_launch", False)

    def connect_signals(self) -> None:
        """Connects interactive UI controls to logical actions."""
        # Toolbar actions
        self.load_btn.clicked.connect(self.handle_load_file)
        self.copy_btn.clicked.connect(self.handle_copy_text)
        self.paste_btn.clicked.connect(self.handle_paste_text)
        self.clear_btn.clicked.connect(self.handle_clear_text)
        self.instructions_btn.clicked.connect(self.show_instructions_page)
        self.back_btn.clicked.connect(self.show_dashboard_page)
        self.help_btn.clicked.connect(self.show_help_page)
        self.help_back_btn.clicked.connect(self.show_dashboard_page)
        self.settings_btn.clicked.connect(self.show_preferences_dialog)
        # Keyboard Shortcuts
        QShortcut(QKeySequence("Ctrl+O"), self, self.handle_load_file)
        QShortcut(QKeySequence("Ctrl+T"), self, self.handle_start_typing)
        QShortcut(QKeySequence("Ctrl+W"), self, self.handle_clear_text)
        QShortcut(QKeySequence("F1"), self, self.show_help_page)
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
        
        # Editor Shortcuts
        QShortcut(QKeySequence("Ctrl+F"), self, self.toggle_find_replace)
        QShortcut(QKeySequence("Ctrl+H"), self, self.focus_replace)
        QShortcut(QKeySequence.ZoomIn, self, self.zoom_in)
        QShortcut(QKeySequence("Ctrl+="), self, self.zoom_in)
        QShortcut(QKeySequence.ZoomOut, self, self.zoom_out)
        QShortcut(QKeySequence("Ctrl+0"), self, self.zoom_reset)
        QShortcut(QKeySequence("Ctrl+G"), self, self.handle_goto_line)

        # Editor Buttons
        self.word_wrap_btn.clicked.connect(self.handle_word_wrap)
        self.find_next_btn.clicked.connect(self.handle_find_next)
        self.find_prev_btn.clicked.connect(self.handle_find_prev)
        self.replace_btn.clicked.connect(self.handle_replace)
        self.replace_all_btn.clicked.connect(self.handle_replace_all)
        self.close_find_btn.clicked.connect(self.find_replace_widget.hide)

        # Editor text changed (for auto save, stats counter, and typing time)
        self.editor.textChanged.connect(self.handle_text_changed)

        # Speed slider
        self.speed_slider.valueChanged.connect(self.handle_speed_change)

        # Random delay checkbox & inputs
        self.random_delay_cb.toggled.connect(self.handle_delay_cb_toggled)
        self.min_delay_spin.valueChanged.connect(self.handle_delay_spin_change)
        self.max_delay_spin.valueChanged.connect(self.handle_delay_spin_change)

        # Execute buttons
        self.start_btn.clicked.connect(self.handle_start_typing)
        self.stop_btn.clicked.connect(self.handle_stop_typing)
        
        # Favorites
        self.fav_btn.clicked.connect(self.handle_favorite_toggle)

        # Profile Selection
        self.profile_combo.currentTextChanged.connect(self.handle_profile_change)
        self.mode_normal_radio.toggled.connect(self.handle_mode_toggled)
        self.mode_human_radio.toggled.connect(self.handle_mode_toggled)

    def restore_settings(self) -> None:
        """Restores all settings into the UI elements."""
        profiles = self.settings.get("typing_profiles", {})
        
        # Select Profile
        current_profile = self.settings.get("current_profile")
        self.profile_combo.blockSignals(True)
        self.profile_combo.clear()
        self.profile_combo.addItems(list(profiles.keys()) + ["Custom (Unsaved)"])
        self.profile_combo.setCurrentText(current_profile)
        self.profile_combo.blockSignals(False)
        
        # Speed & Mode
        wpm = self.settings.get("wpm")
        self.speed_slider.setValue(wpm)
        self.speed_val_label.setText(f"{wpm} WPM")

        mode = self.settings.get("typing_mode")
        if mode == "normal":
            self.mode_normal_radio.setChecked(True)
        else:
            self.mode_human_radio.setChecked(True)

        # Random Delay Checkbox & Spinners
        delay_enabled = self.settings.get("random_delay_enabled")
        self.random_delay_cb.setChecked(delay_enabled)
        self.handle_delay_cb_toggled(delay_enabled)

        self.min_delay_spin.setValue(self.settings.get("min_delay_ms"))
        self.max_delay_spin.setValue(self.settings.get("max_delay_ms"))
        
        # Window Size & Geometry
        width = self.settings.get("window_width")
        height = self.settings.get("window_height")
        self.resize(width, height)

        x = self.settings.get("window_x")
        y = self.settings.get("window_y")
        if x != -1 and y != -1:
            self.move(x, y)

        # Theme Styling
        theme = self.settings.get("theme")
        self.apply_theme(theme)

        # Restore Unsaved text from crash (autosave.txt takes priority)
        restored = False
        from config import AUTOSAVE_FILE_PATH
        if os.path.exists(AUTOSAVE_FILE_PATH):
            try:
                with open(AUTOSAVE_FILE_PATH, 'r', encoding='utf-8') as f:
                    unsaved_text = f.read()
                if unsaved_text:
                    self.editor.setPlainText(unsaved_text)
                    self.status_msg_label.setText("Restored unsaved session text after crash.")
                    logger.info("Restored unsaved session text from autosave.txt")
                    restored = True
            except Exception as e:
                logger.error(f"Failed to load autosave file: {e}")

        # If not restored from crash, restore last session text & cursor position
        if not restored and self.settings.get("restore_session"):
            last_text = self.settings.get("editor_text") or ""
            if last_text:
                self.editor.setPlainText(last_text)
                
                # Restore cursor position and selection
                cursor = self.editor.textCursor()
                from PySide6.QtGui import QTextCursor
                
                sel_start = self.settings.get("editor_selection_start", -1)
                sel_end = self.settings.get("editor_selection_end", -1)
                cursor_pos = self.settings.get("editor_cursor_position", 0)
                
                if sel_start != -1 and sel_end != -1:
                    cursor.setPosition(sel_start)
                    cursor.setPosition(sel_end, QTextCursor.KeepAnchor)
                else:
                    cursor.setPosition(min(cursor_pos, len(last_text)))
                    
                self.editor.setTextCursor(cursor)
                
                # Restore scroll position
                scroll_val = self.settings.get("editor_scroll_value", 0)
                self.editor.verticalScrollBar().setValue(scroll_val)
                
                logger.info("Restored editor session text, cursor position, selection, and scroll.")

        # Restore last opened file path
        self.current_file_path = self.settings.get("last_opened_file") or ""

    def save_current_state(self) -> None:
        """Saves current widget values and window geometry back to SettingsService."""
        self.settings.set("wpm", self.speed_slider.value())
        self.settings.set("typing_mode", "normal" if self.mode_normal_radio.isChecked() else "human")
        self.settings.set("random_delay_enabled", self.random_delay_cb.isChecked())
        self.settings.set("min_delay_ms", self.min_delay_spin.value())
        self.settings.set("max_delay_ms", self.max_delay_spin.value())
        
        # Save window sizes
        self.settings.set("window_width", self.width())
        self.settings.set("window_height", self.height())
        self.settings.set("window_x", self.x())
        self.settings.set("window_y", self.y())
        
        # Save session text, cursor position, selection, and scroll
        self.settings.set("editor_text", self.editor.toPlainText())
        cursor = self.editor.textCursor()
        self.settings.set("editor_cursor_position", cursor.position())
        
        if cursor.hasSelection():
            self.settings.set("editor_selection_start", cursor.selectionStart())
            self.settings.set("editor_selection_end", cursor.selectionEnd())
        else:
            self.settings.set("editor_selection_start", -1)
            self.settings.set("editor_selection_end", -1)
            
        self.settings.set("editor_scroll_value", self.editor.verticalScrollBar().value())
        self.settings.set("last_opened_file", self.current_file_path)

    def apply_theme(self, theme: str) -> None:
        """Applies stylesheet styling to the window."""
        self.setStyleSheet(config.DARK_THEME)
        self.settings.set("theme", "dark")

    # ==========================================
    # Styled Dialog Box Helpers
    # ==========================================

    def show_styled_message(self, title: str, text: str, icon_type: str = "info") -> QMessageBox.StandardButton:
        """Displays a theme-compliant styled QMessageBox for Windows OS integration."""
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setTextFormat(Qt.RichText)
        msg.setStyleSheet(self.styleSheet())
        
        # Apply window icon
        icon_path = config.get_resource_path("autotyper_icon.png")
        if os.path.exists(icon_path):
            msg.setWindowIcon(QIcon(icon_path))

        if icon_type == "info":
            msg.setIcon(QMessageBox.Information)
        elif icon_type == "warning":
            msg.setIcon(QMessageBox.Warning)
        elif icon_type == "error":
            msg.setIcon(QMessageBox.Critical)
        elif icon_type == "question":
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            
        return msg.exec()

    def show_dashboard_page(self) -> None:
        self.stacked_widget.setCurrentIndex(0)

    def show_instructions_page(self) -> None:
        self.stacked_widget.setCurrentIndex(1)

    def show_help_page(self) -> None:
        self.stacked_widget.setCurrentIndex(2)
        
    def show_preferences_dialog(self) -> None:
        """Shows the new lightweight preferences dialog."""
        from app.preferences import PreferencesDialog
        dialog = PreferencesDialog(self, self.settings)
        dialog.exec()

    # ==========================================
    # Drag and Drop System Overrides
    # ==========================================

    def dragEnterEvent(self, event) -> None:
        """Verifies dropped files are supported extensions before accepting."""
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0].toLocalFile()
            _, ext = os.path.splitext(url.lower())
            if ext in ('.txt', '.md', '.docx'):
                event.acceptProposedAction()

    def dropEvent(self, event) -> None:
        """Loads accepted file drop contents directly into the editor."""
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0].toLocalFile()
            self.load_file_from_path(url)
            event.acceptProposedAction()

    # ==========================================
    def handle_word_wrap(self) -> None:
        if self.word_wrap_btn.isChecked():
            from PySide6.QtWidgets import QPlainTextEdit
            self.editor.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        else:
            from PySide6.QtWidgets import QPlainTextEdit
            self.editor.setLineWrapMode(QPlainTextEdit.NoWrap)

    def toggle_find_replace(self) -> None:
        if self.find_replace_widget.isVisible():
            self.find_replace_widget.hide()
            self.editor.setFocus()
        else:
            self.find_replace_widget.show()
            self.find_input.setFocus()
            self.find_input.selectAll()

    def focus_replace(self) -> None:
        self.find_replace_widget.show()
        self.replace_input.setFocus()
        self.replace_input.selectAll()

    def handle_find_next(self) -> None:
        text = self.find_input.text()
        if not text:
            return
        # Find next occurrence
        found = self.editor.find(text)
        if not found:
            # Wrap around
            cursor = self.editor.textCursor()
            from PySide6.QtGui import QTextCursor
            cursor.movePosition(QTextCursor.Start)
            self.editor.setTextCursor(cursor)
            self.editor.find(text)

    def handle_find_prev(self) -> None:
        text = self.find_input.text()
        if not text:
            return
        from PySide6.QtGui import QTextDocument
        found = self.editor.find(text, QTextDocument.FindBackward)
        if not found:
            cursor = self.editor.textCursor()
            from PySide6.QtGui import QTextCursor
            cursor.movePosition(QTextCursor.End)
            self.editor.setTextCursor(cursor)
            self.editor.find(text, QTextDocument.FindBackward)

    def handle_replace(self) -> None:
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.replace_input.text())
        self.handle_find_next()

    def handle_replace_all(self) -> None:
        text = self.find_input.text()
        if not text:
            return
        replace_text = self.replace_input.text()
        
        cursor = self.editor.textCursor()
        from PySide6.QtGui import QTextCursor
        cursor.beginEditBlock()
        
        # Reset to start
        cursor.movePosition(QTextCursor.Start)
        self.editor.setTextCursor(cursor)
        count = 0
        while self.editor.find(text):
            self.editor.textCursor().insertText(replace_text)
            count += 1
            
        cursor.endEditBlock()
        self.show_styled_message("Replace All", f"Replaced {count} occurrences.", "info")

    def zoom_in(self) -> None:
        font = self.editor.font()
        size = font.pointSize()
        if size < 72:
            font.setPointSize(size + 2)
            self.editor.setFont(font)

    def zoom_out(self) -> None:
        font = self.editor.font()
        size = font.pointSize()
        if size > 6:
            font.setPointSize(size - 2)
            self.editor.setFont(font)

    def zoom_reset(self) -> None:
        font = self.editor.font()
        font.setPointSize(10) # default monospace point size is usually around 10
        self.editor.setFont(font)

    def handle_goto_line(self) -> None:
        """Prompts the user for a line number and scrolls to it."""
        from PySide6.QtWidgets import QInputDialog
        line_num, ok = QInputDialog.getInt(self, "Go To Line", "Line number:", 1, 1, self.editor.blockCount())
        if ok:
            block = self.editor.document().findBlockByNumber(line_num - 1)
            cursor = self.editor.textCursor()
            cursor.setPosition(block.position())
            self.editor.setTextCursor(cursor)
            self.editor.centerCursor()

    # ==========================================
    # Toast Notifications
    # ==========================================

    def show_toast(self, message: str, theme: str = "info") -> None:
        """Displays a non-intrusive toast notification."""
        from app.toast import ToastNotification
        toast = ToastNotification(self, message, duration_ms=2500, theme=theme)
        toast.show_toast()

    # ==========================================
    # File Operations
    # ==========================================

    def handle_copy_text(self) -> None:
        """Copies the text inside the editor to the clipboard."""
        text = self.editor.toPlainText()
        ClipboardService.set_text(text)

    def handle_paste_text(self) -> None:
        """Pastes plain text from the clipboard into the editor."""
        text = ClipboardService.get_text()
        if text:
            self.editor.insertPlainText(text)

    def handle_clear_text(self) -> None:
        """Clears text inside the editor."""
        self.editor.clear()

    def load_file_from_path(self, file_path: str) -> None:
        """Loads and formats a document from a specific absolute path."""
        if not file_path:
            return
        try:
            text = FileLoaderService.load_file(file_path)
            self.editor.setPlainText(text)
            self.status_msg_label.setText(f"Loaded: {os.path.basename(file_path)}")
            # Add to recent list and update session
            self.current_file_path = file_path
            self.settings.set("last_opened_file", file_path)
            self.settings.add_recent_file(file_path)
            self.update_recent_files_menu()
            
            # Update fav_btn state
            self.fav_btn.blockSignals(True)
            self.fav_btn.setChecked(self.settings.is_favorite(file_path))
            self.fav_btn.blockSignals(False)
        except FileNotFoundError:
            self.show_styled_message("Error", f"The file could not be found:\n{file_path}", "error")
        except PermissionError:
            self.show_styled_message("Error", f"Permission denied. Unable to access the file:\n{file_path}", "error")
        except UnsupportedFileTypeError as e:
            self.show_styled_message("Unsupported File Format", str(e), "warning")
        except FileLoadError as e:
            self.show_styled_message("Error", str(e), "error")
        except Exception as e:
            self.show_styled_message("Error", f"An unexpected error occurred:\n{str(e)}", "error")

    def handle_load_file(self) -> None:
        """Opens a file dialog, loads and sets text to the editor."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Document",
            "",
            "Supported Files (*.txt *.docx *.md);;Text Files (*.txt);;Word Documents (*.docx);;Markdown Files (*.md)"
        )
        if not file_path:
            return
        self.load_file_from_path(file_path)

    def handle_favorite_toggle(self) -> None:
        """Toggles favorite status for the currently loaded file."""
        current_file = self.settings.get("last_opened_file")
        if not current_file or not os.path.exists(current_file):
            self.fav_btn.setChecked(False)
            self.show_styled_message("Favorites", "Load a valid file first before starring it.", "warning")
            return
            
        is_fav = self.settings.toggle_favorite(current_file)
        self.fav_btn.setChecked(is_fav)
        self.update_recent_files_menu()

    def update_recent_files_menu(self) -> None:
        """Populates the Load File dropdown button menu with favorites and recent files."""
        menu = QMenu(self)
        menu.setStyleSheet(self.styleSheet())
        
        # Favorites Section
        favorites = self.settings.get("favorite_files") or []
        valid_favs = []
        for path in favorites:
            if os.path.exists(path):
                valid_favs.append(path)
                
        if valid_favs:
            if len(valid_favs) != len(favorites):
                self.settings.set("favorite_files", valid_favs) # Prune missing
                
            fav_menu = menu.addMenu("⭐ Favorites")
            for path in valid_favs:
                filename = os.path.basename(path)
                action = fav_menu.addAction(filename)
                action.setToolTip(path)
                action.triggered.connect(lambda checked=False, p=path: self.load_file_from_path(p))
            menu.addSeparator()
        
        # Recent Files Section
        recent_list = self.settings.get("recent_files") or []
        valid_recents = []
        
        for path in recent_list:
            if os.path.exists(path):
                valid_recents.append(path)
                
        if len(valid_recents) != len(recent_list):
            self.settings.set("recent_files", valid_recents)
        
        if valid_recents:
            recent_menu = menu.addMenu("🕒 Recent Files")
            for path in valid_recents:
                filename = os.path.basename(path)
                action = recent_menu.addAction(filename)
                action.setToolTip(path)
                action.triggered.connect(lambda checked=False, p=path: self.load_file_from_path(p))
            menu.addSeparator()
            
        browse_action = menu.addAction("Browse...")
        browse_action.triggered.connect(self.handle_load_file)
        
        current = self.settings.get("last_opened_file")
        if current and os.path.exists(current):
            menu.addSeparator()
            open_folder_action = menu.addAction("📂 Open Containing Folder")
            open_folder_action.triggered.connect(lambda: self.open_containing_folder(current))
        
        self.load_btn.setMenu(menu)

    def open_containing_folder(self, file_path: str) -> None:
        import subprocess
        import platform
        folder_path = os.path.dirname(file_path)
        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", folder_path])
        else:
            subprocess.Popen(["xdg-open", folder_path])

    def handle_text_changed(self) -> None:
        """Autosaves text to autosave.txt, updates stats counters, and updates estimated duration."""
        text = self.editor.toPlainText()

        # 1. Autosave to disk (if enabled)
        if self.settings.get("autosave_enabled", True):
            from config import AUTOSAVE_FILE_PATH
            try:
                with open(AUTOSAVE_FILE_PATH, 'w', encoding='utf-8') as f:
                    f.write(text)
            except Exception as e:
                logger.error(f"Autosave failed: {e}")

        # 2. Update Stats Counter
        chars = len(text)
        words = len(text.split())
        lines = text.count("\n") + 1 if chars > 0 else 0
        self.status_stats_label.setText(f"Chars: {chars} | Words: {words} | Lines: {lines}")

        # 3. Update Estimated Time
        self.update_estimated_time()

    def update_estimated_time(self) -> None:
        """Updates the status bar with the estimated typing time."""
        text = self.editor.toPlainText()
        if not text.strip():
            self.status_time_label.setText("Est. Time: 0s")
            return
            
        wpm = self.speed_slider.value()
        mode = "normal" if self.mode_normal_radio.isChecked() else "human"
        
        # Approximate time
        from core.delay_engine import DelayEngine
        base_delay = DelayEngine.calculate_base_delay(wpm)
        
        chars = len(text)
        total_sec = chars * base_delay
        
        if mode == "human":
            # Add estimated extra pause time (roughly 30% more for human pauses)
            total_sec *= 1.3
            
        # Format time
        if total_sec < 60:
            time_str = f"{int(total_sec)}s"
        else:
            mins = int(total_sec // 60)
            secs = int(total_sec % 60)
            time_str = f"{mins}m {secs}s"
            
        self.status_time_label.setText(f"Est. Time: ~{time_str}")

    def _mark_custom_profile(self) -> None:
        """Helper to mark the profile as Custom if the user manually tweaks a setting."""
        if self.profile_combo.currentText() != "Custom (Unsaved)":
            self.profile_combo.blockSignals(True)
            self.profile_combo.setCurrentText("Custom (Unsaved)")
            self.settings.set("current_profile", "Custom (Unsaved)")
            self.profile_combo.blockSignals(False)

    def handle_profile_change(self, profile_name: str) -> None:
        """Applies the selected profile's settings to the UI."""
        self.settings.set("current_profile", profile_name)
        if profile_name == "Custom (Unsaved)":
            return
            
        profiles = self.settings.get("typing_profiles")
        if not profiles or profile_name not in profiles:
            return
            
        prof = profiles[profile_name]
        
        # Block signals to prevent recursive custom marking
        self.speed_slider.blockSignals(True)
        self.mode_normal_radio.blockSignals(True)
        self.mode_human_radio.blockSignals(True)
        self.random_delay_cb.blockSignals(True)
        self.min_delay_spin.blockSignals(True)
        self.max_delay_spin.blockSignals(True)
        
        # Apply profile values
        self.speed_slider.setValue(prof["wpm"])
        self.settings.set("wpm", prof["wpm"])
        self.update_estimated_time()
        
        mode = prof["typing_mode"]
        self.settings.set("typing_mode", mode)
        if mode == "normal":
            self.mode_normal_radio.setChecked(True)
        else:
            self.mode_human_radio.setChecked(True)
            
        delay_enabled = prof["random_delay_enabled"]
        self.random_delay_cb.setChecked(delay_enabled)
        self.settings.set("random_delay_enabled", delay_enabled)
        self.min_delay_spin.setEnabled(delay_enabled)
        self.max_delay_spin.setEnabled(delay_enabled)
        
        self.min_delay_spin.setValue(prof["min_delay_ms"])
        self.max_delay_spin.setValue(prof["max_delay_ms"])
        self.settings.set("min_delay_ms", prof["min_delay_ms"])
        self.settings.set("max_delay_ms", prof["max_delay_ms"])
        
        # Unblock signals
        self.speed_slider.blockSignals(False)
        self.mode_normal_radio.blockSignals(False)
        self.mode_human_radio.blockSignals(False)
        self.random_delay_cb.blockSignals(False)
        self.min_delay_spin.blockSignals(False)
        self.max_delay_spin.blockSignals(False)

    def handle_mode_toggled(self) -> None:
        """Updates the active typing mode and marks profile as Custom."""
        if self.mode_normal_radio.isChecked():
            logger.debug("Typing mode toggled to NORMAL")
            self.status_mode_label.setText("Mode: Normal")
        else:
            logger.debug("Typing mode toggled to HUMAN")
            self.status_mode_label.setText("Mode: Human")
        self._mark_custom_profile()
        self.update_estimated_time()

    def handle_speed_change(self, value: int) -> None:
        """Updates WPM label and settings."""
        self.speed_val_label.setText(f"{value} WPM")
        self._mark_custom_profile()
        self.update_estimated_time()

    def handle_delay_cb_toggled(self, checked: bool) -> None:
        """Disables delay spinner inputs if random delay is unchecked."""
        self.settings.set("random_delay_enabled", checked)
        self.min_delay_spin.setEnabled(checked)
        self.max_delay_spin.setEnabled(checked)
        self._mark_custom_profile()

    def handle_delay_spin_change(self) -> None:
        """Ensures that the minimum delay is never larger than the maximum delay."""
        min_val = self.min_delay_spin.value()
        max_val = self.max_delay_spin.value()
        if min_val > max_val:
            self.max_delay_spin.setValue(min_val)
        
        self.settings.set("min_delay_ms", self.min_delay_spin.value())
        self.settings.set("max_delay_ms", self.max_delay_spin.value())
        self._mark_custom_profile()

    # ==========================================
    # Execution Logic / Thread control
    # ==========================================

    def handle_start_typing(self) -> None:
        """Prepares configuration, locks GUI inputs, and starts the typing worker thread."""
        raw_text = self.editor.toPlainText()
        if not raw_text.strip():
            self.show_styled_message("Empty Editor", "Please paste or load some text before starting!", "warning")
            return

        # Prepare Text - normalize newlines to preserve indentation format accurately
        formatted_text = TextFormatter.format_for_typing(raw_text)

        wpm = self.speed_slider.value()
        mode = "normal" if self.mode_normal_radio.isChecked() else "human"
        logger.info(f"Initiating auto typing: WPM={wpm}, Mode={mode}, Characters={len(formatted_text)}")

        # UI Input Locking
        self.set_controls_enabled(False)
        self.status_progress_bar.setVisible(True)
        self.status_progress_bar.setValue(0)

        # Extract profile-specific hidden settings
        current_profile = self.settings.get("current_profile", "Human")
        profiles = self.settings.get("typing_profiles", {})
        
        # Fallback to Human profile defaults if Custom (Unsaved) or invalid
        prof = profiles.get(current_profile, profiles.get("Human", {}))
        punctuation_pause = prof.get("punctuation_pause", 0.3)
        line_break_pause = prof.get("line_break_pause", 0.5)
        
        # Countdown logic (Phase 5 will add custom global countdown, for now use profile countdown or 5)
        countdown_sec = self.settings.get("custom_countdown", prof.get("countdown", 5))

        # Worker initialization
        self.worker = TypingWorker(
            text=formatted_text,
            wpm=wpm,
            mode=mode,
            random_enabled=self.random_delay_cb.isChecked(),
            min_delay_ms=self.min_delay_spin.value(),
            max_delay_ms=self.max_delay_spin.value(),
            punctuation_pause=punctuation_pause,
            line_break_pause=line_break_pause,
            countdown_sec=countdown_sec
        )

        # Connect Worker signals to GUI update methods
        self.worker.status_changed.connect(self.on_worker_status_changed)
        self.worker.progress_changed.connect(self.on_worker_progress_changed)
        self.worker.countdown_tick.connect(self.on_worker_countdown_tick)
        self.worker.finished.connect(self.on_worker_finished)

        # Start thread
        self.worker.start()

    def handle_stop_typing(self) -> None:
        """Triggers the cancellation flag in the running typing thread worker."""
        if self.worker and self.worker.isRunning():
            logger.info("Emergency typing stop requested by user.")
            self.status_msg_label.setText("Stopping...")
            self.worker.stop()

    def set_controls_enabled(self, enabled: bool) -> None:
        """Toggles enabling of input widgets while typing is executing."""
        self.editor.setReadOnly(not enabled)
        self.load_btn.setEnabled(enabled)
        self.copy_btn.setEnabled(enabled)
        self.paste_btn.setEnabled(enabled)
        self.clear_btn.setEnabled(enabled)
        self.instructions_btn.setEnabled(enabled)
        self.help_btn.setEnabled(enabled)
        
        self.speed_slider.setEnabled(enabled)
        self.mode_normal_radio.setEnabled(enabled)
        self.mode_human_radio.setEnabled(enabled)
        self.random_delay_cb.setEnabled(enabled)
        
        # Keep spinner lock synchronized
        if enabled:
            self.handle_delay_cb_toggled(self.random_delay_cb.isChecked())
        else:
            self.min_delay_spin.setEnabled(False)
            self.max_delay_spin.setEnabled(False)

        # Execution buttons toggle
        self.start_btn.setEnabled(enabled)
        self.stop_btn.setEnabled(not enabled)

    # ==========================================
    # Worker Thread Callback Slots
    # ==========================================

    def on_worker_status_changed(self, status: str) -> None:
        """Updates status messages displayed in the status bar."""
        if status == "Countdown":
            self.status_msg_label.setText("Starting shortly... Get ready!")
            self.status_msg_label.setStyleSheet("color: #ff9500; font-weight: 500;")
        elif status == "Typing":
            self.status_msg_label.setText("Auto typing in progress...")
            self.status_msg_label.setStyleSheet("color: #0a84ff; font-weight: 500;")
        elif status == "Stopped":
            self.status_msg_label.setText("Auto typing stopped.")
            self.status_msg_label.setStyleSheet("color: #ff3b30; font-weight: 500;")
        elif status == "Completed":
            self.status_msg_label.setText("Typing sequence finished successfully.")
            self.status_msg_label.setStyleSheet("color: #34c759; font-weight: 500;")
        elif status == "Error":
            self.status_msg_label.setText("Execution Error.")
            self.status_msg_label.setStyleSheet("color: #ff3b30; font-weight: 700;")
        elif status == "Ready":
            self.status_msg_label.setText("Ready")
            self.status_msg_label.setStyleSheet("color: #8e8e93;")

    def on_worker_countdown_tick(self, count: int) -> None:
        """Updates the countdown label during the initial start sequence."""
        self.countdown_label.setText(f"Typing in {count}s...")

    def on_worker_progress_changed(self, current: int, total: int, remaining_sec: int) -> None:
        """Updates the visual progress bar and remaining time during keystroke execution."""
        if total > 0:
            percentage = int((current / total) * 100)
            self.status_progress_bar.setValue(percentage)
            self.status_progress_bar.setFormat(f"{current}/{total} ({percentage}%)")
            
            # Format remaining seconds nicely
            if remaining_sec < 60:
                time_str = f"{remaining_sec}s"
            else:
                mins = remaining_sec // 60
                secs = remaining_sec % 60
                time_str = f"{mins}m {secs}s"
            
            self.status_msg_label.setText(f"Auto typing in progress... (Remaining: {time_str})")

    def on_worker_finished(self, success: bool, message: str) -> None:
        """Cleans up the worker thread, unlocks inputs, and displays completion dialogs."""
        self.set_controls_enabled(True)
        self.status_progress_bar.setVisible(False)
        self.countdown_label.setText("Ready")

        if success:
            logger.info("Typing execution succeeded.")
            self.show_styled_message("Completed", message, "info")
            self.on_worker_status_changed("Ready")
        else:
            logger.info(f"Typing execution stopped/failed. Message: {message}")
            if "cancelled" in message.lower() or "stopped" in message.lower() or "interrupted" in message.lower():
                self.on_worker_status_changed("Stopped")
                self.show_styled_message("Interrupted", message, "warning")
            else:
                self.on_worker_status_changed("Error")
                self.show_styled_message("Error", message, "error")

        # Cleanup thread
        if self.worker:
            self.worker.wait()  # Ensure C++ thread is fully dead before resetting reference
            self.worker = None

    # ==========================================
    # Window System Overrides
    # ==========================================

    def closeEvent(self, event) -> None:
        """Saves current state, stops threads, prompts exits, and shuts down safely."""
        logger.info("Application close event requested.")
        
        # 1. If typing thread is active, confirm termination
        if self.worker and self.worker.isRunning():
            reply = self.show_styled_message(
                "Typing in Progress",
                "Auto typing is currently active. Are you sure you want to stop typing and exit?",
                "question"
            )
            if reply != QMessageBox.Yes:
                event.ignore()
                return
            else:
                self.worker.stop()
                self.worker.wait()

        # 2. If editor contains unsaved text, prompt exit confirmation
        elif self.editor.toPlainText().strip():
            reply = self.show_styled_message(
                "Confirm Exit",
                "Are you sure you want to exit AutoTyper?",
                "question"
            )
            if reply != QMessageBox.Yes:
                event.ignore()
                return

        # 3. Clean exit: Save current state
        self.save_current_state()

        # 4. Clean exit: Delete autosave.txt
        from config import AUTOSAVE_FILE_PATH
        if os.path.exists(AUTOSAVE_FILE_PATH):
            try:
                os.remove(AUTOSAVE_FILE_PATH)
                logger.info("Clean shutdown: cleared autosave.txt")
            except Exception as e:
                logger.error(f"Failed to clear autosave file: {e}")

        event.accept()
