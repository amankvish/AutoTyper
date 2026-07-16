from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit,
    QSlider, QRadioButton, QCheckBox, QSpinBox, QGroupBox, QStatusBar,
    QProgressBar, QToolButton, QStackedWidget, QScrollArea, QTextBrowser,
    QComboBox, QLineEdit
)
from app.code_editor import CodeEditor
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import os

class AutoTyperUI:
    """Sets up the layout and widgets for the AutoTyper main window."""

    def setup_ui(self, window) -> None:
        window.setWindowTitle("AutoTyper")
        window.resize(850, 700)

        # Set Window Icon
        import config
        icon_path = config.get_resource_path("autotyper_icon.png")
        if os.path.exists(icon_path):
            window.setWindowIcon(QIcon(icon_path))

        # Central Widget
        central_widget = QWidget(window)
        window.setCentralWidget(central_widget)

        # Root Layout
        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ==========================================
        # Stacked Widget (Page 0 = Dashboard, Page 1 = Instructions)
        # ==========================================
        window.stacked_widget = QStackedWidget(central_widget)
        root_layout.addWidget(window.stacked_widget)

        # ==========================================
        # PAGE 0: Main Dashboard
        # ==========================================
        dashboard_page = QWidget()
        main_layout = QVBoxLayout(dashboard_page)
        main_layout.setContentsMargins(20, 20, 20, 10)
        main_layout.setSpacing(15)

        # 1. Header (Logo & Brand Info)
        header_layout = QHBoxLayout()
        title_block = QVBoxLayout()

        window.header_label = QLabel("AutoTyper", dashboard_page)
        window.header_label.setObjectName("header_label")

        window.brand_label = QLabel("Designed by The IoT Labs", dashboard_page)
        window.brand_label.setObjectName("brand_label")

        title_block.addWidget(window.header_label)
        title_block.addWidget(window.brand_label)
        header_layout.addLayout(title_block)

        header_layout.addStretch()

        # How to Use & Help Buttons
        window.instructions_btn = QPushButton("📖 How to Use", dashboard_page)
        window.instructions_btn.setMinimumWidth(110)
        header_layout.addWidget(window.instructions_btn)

        window.help_btn = QPushButton("❓ Help", dashboard_page)
        window.help_btn.setMinimumWidth(80)
        header_layout.addWidget(window.help_btn)

        window.settings_btn = QPushButton("⚙ Settings", dashboard_page)
        window.settings_btn.setMinimumWidth(90)
        header_layout.addWidget(window.settings_btn)

        main_layout.addLayout(header_layout)

        # 2. Toolbar (File Actions & Clipboard)
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(8)

        window.load_btn = QToolButton(dashboard_page)
        window.load_btn.setText("📁 Load File")
        window.load_btn.setPopupMode(QToolButton.MenuButtonPopup)
        
        window.fav_btn = QPushButton("⭐", dashboard_page)
        window.fav_btn.setCheckable(True)
        window.fav_btn.setToolTip("Toggle Favorite")
        window.fav_btn.setFixedWidth(30)
        
        window.copy_btn = QPushButton("📋 Copy", dashboard_page)
        window.copy_btn.setToolTip("Copy text to clipboard")
        window.copy_btn.setAccessibleName("Copy")
        window.copy_btn.setAccessibleDescription("Copies the editor text to your clipboard")
        
        window.paste_btn = QPushButton("📥 Paste", dashboard_page)
        window.paste_btn.setToolTip("Paste text from clipboard")
        window.paste_btn.setAccessibleName("Paste")
        window.paste_btn.setAccessibleDescription("Pastes text from your clipboard into the editor")
        
        window.clear_btn = QPushButton("🧹 Clear", dashboard_page)
        window.clear_btn.setToolTip("Clear the editor")
        window.clear_btn.setAccessibleName("Clear")
        window.clear_btn.setAccessibleDescription("Clears all text from the editor")

        window.word_wrap_btn = QPushButton("Wrapping", dashboard_page)
        window.word_wrap_btn.setCheckable(True)
        window.word_wrap_btn.setChecked(True)
        window.word_wrap_btn.setToolTip("Toggle Word Wrap")
        window.word_wrap_btn.setAccessibleName("Toggle Word Wrap")
        window.word_wrap_btn.setAccessibleDescription("Toggles line wrapping in the editor")

        toolbar_layout.addWidget(window.load_btn)
        toolbar_layout.addWidget(window.fav_btn)
        toolbar_layout.addWidget(window.copy_btn)
        toolbar_layout.addWidget(window.paste_btn)
        toolbar_layout.addWidget(window.clear_btn)
        toolbar_layout.addWidget(window.word_wrap_btn)
        toolbar_layout.addStretch()

        main_layout.addLayout(toolbar_layout)

        # 3. Editor (Custom CodeEditor with Line Numbers)
        window.editor = CodeEditor(dashboard_page)
        window.editor.setPlaceholderText("Paste your code or text here, or click 'Load File' to import...")
        window.editor.setAccessibleName("Text Editor")
        window.editor.setAccessibleDescription("Main editor where you paste or load the text you want to auto-type")
        main_layout.addWidget(window.editor)
        
        # Find/Replace Bar (hidden by default)
        window.find_replace_widget = QWidget(dashboard_page)
        find_replace_layout = QHBoxLayout(window.find_replace_widget)
        find_replace_layout.setContentsMargins(0, 5, 0, 0)
        
        window.find_input = QLineEdit(window.find_replace_widget)
        window.find_input.setPlaceholderText("Find...")
        window.find_next_btn = QPushButton("Find Next", window.find_replace_widget)
        window.find_prev_btn = QPushButton("Find Prev", window.find_replace_widget)
        
        window.replace_input = QLineEdit(window.find_replace_widget)
        window.replace_input.setPlaceholderText("Replace with...")
        window.replace_btn = QPushButton("Replace", window.find_replace_widget)
        window.replace_all_btn = QPushButton("Replace All", window.find_replace_widget)
        window.close_find_btn = QPushButton("❌", window.find_replace_widget)
        window.close_find_btn.setFixedWidth(30)
        
        find_replace_layout.addWidget(window.find_input)
        find_replace_layout.addWidget(window.find_prev_btn)
        find_replace_layout.addWidget(window.find_next_btn)
        find_replace_layout.addWidget(window.replace_input)
        find_replace_layout.addWidget(window.replace_btn)
        find_replace_layout.addWidget(window.replace_all_btn)
        find_replace_layout.addWidget(window.close_find_btn)
        
        window.find_replace_widget.hide()
        main_layout.addWidget(window.find_replace_widget)

        # 4. Settings Panel
        settings_layout = QHBoxLayout()
        settings_layout.setSpacing(15)

        # Left Group: Speed and Typing Mode
        speed_group = QGroupBox("Speed & Mode Settings", dashboard_page)
        speed_layout = QVBoxLayout(speed_group)
        speed_layout.setSpacing(12)

        # Profile Selection Layout
        profile_layout = QHBoxLayout()
        profile_layout.addWidget(QLabel("Typing Profile:", speed_group))
        window.profile_combo = QComboBox(speed_group)
        window.profile_combo.addItems(["Normal", "Fast", "Slow", "Human", "Custom (Unsaved)"])
        profile_layout.addWidget(window.profile_combo, 1)
        
        speed_layout.addLayout(profile_layout)

        # WPM Slider Layout
        wpm_label_layout = QHBoxLayout()
        wpm_title = QLabel("Typing Speed:", speed_group)
        window.speed_val_label = QLabel("60 WPM", speed_group)
        window.speed_val_label.setObjectName("accent_label")
        wpm_label_layout.addWidget(wpm_title)
        wpm_label_layout.addStretch()
        wpm_label_layout.addWidget(window.speed_val_label)
        speed_layout.addLayout(wpm_label_layout)

        slider_container = QHBoxLayout()
        window.speed_slider = QSlider(Qt.Horizontal, speed_group)
        window.speed_slider.setRange(20, 200)
        window.speed_slider.setValue(60)
        slider_container.addWidget(QLabel("20 WPM", speed_group))
        slider_container.addWidget(window.speed_slider)
        slider_container.addWidget(QLabel("200 WPM", speed_group))
        speed_layout.addLayout(slider_container)

        # Mode Radio Buttons Layout
        mode_label = QLabel("Typing Simulation Mode:", speed_group)
        speed_layout.addWidget(mode_label)

        mode_btn_layout = QHBoxLayout()
        window.mode_normal_radio = QRadioButton("Normal (Uniform Speed)", speed_group)
        window.mode_human_radio = QRadioButton("Human (Natural pauses & variation)", speed_group)
        window.mode_human_radio.setChecked(True)
        mode_btn_layout.addWidget(window.mode_normal_radio)
        mode_btn_layout.addWidget(window.mode_human_radio)
        speed_layout.addLayout(mode_btn_layout)

        settings_layout.addWidget(speed_group, 5)

        # Right Group: Random Delays
        delay_group = QGroupBox("Random Delay Settings", dashboard_page)
        delay_layout = QVBoxLayout(delay_group)
        delay_layout.setSpacing(10)

        window.random_delay_cb = QCheckBox("Enable Random Char Delays", delay_group)
        window.random_delay_cb.setChecked(True)
        delay_layout.addWidget(window.random_delay_cb)

        delay_spin_layout = QHBoxLayout()

        # Min Delay
        min_vbox = QVBoxLayout()
        min_vbox.addWidget(QLabel("Minimum (ms):", delay_group))
        window.min_delay_spin = QSpinBox(delay_group)
        window.min_delay_spin.setRange(1, 5000)
        window.min_delay_spin.setValue(10)
        min_vbox.addWidget(window.min_delay_spin)

        # Max Delay
        max_vbox = QVBoxLayout()
        max_vbox.addWidget(QLabel("Maximum (ms):", delay_group))
        window.max_delay_spin = QSpinBox(delay_group)
        window.max_delay_spin.setRange(1, 5000)
        window.max_delay_spin.setValue(100)
        max_vbox.addWidget(window.max_delay_spin)

        delay_spin_layout.addLayout(min_vbox)
        delay_spin_layout.addLayout(max_vbox)
        delay_layout.addLayout(delay_spin_layout)

        # Vertical spacer to balance layout
        delay_layout.addStretch()

        settings_layout.addWidget(delay_group, 4)
        main_layout.addLayout(settings_layout)

        # 5. Countdown & Execution Controls
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(10, 5, 10, 5)

        countdown_layout = QVBoxLayout()
        countdown_title = QLabel("ETA / Countdown", dashboard_page)
        window.countdown_label = QLabel("Ready", dashboard_page)
        window.countdown_label.setObjectName("countdown_label")
        countdown_layout.addWidget(countdown_title)
        countdown_layout.addWidget(window.countdown_label)
        control_layout.addLayout(countdown_layout)

        control_layout.addStretch()

        # Action Buttons
        window.start_btn = QPushButton("▶ Start AutoTyping", dashboard_page)
        window.start_btn.setObjectName("primary_action")
        window.start_btn.setMinimumHeight(40)
        window.start_btn.setToolTip("Begin typing the text (Ctrl+T)")
        window.start_btn.setAccessibleName("Start Auto Typing")
        window.start_btn.setAccessibleDescription("Begins typing the text from the editor using the configured speed and mode")

        window.stop_btn = QPushButton("■ Stop / Cancel", dashboard_page)
        window.stop_btn.setObjectName("danger_action")
        window.stop_btn.setMinimumHeight(40)
        window.stop_btn.setToolTip("Stop typing immediately (Global ESC)")
        window.stop_btn.setAccessibleName("Stop Auto Typing")
        window.stop_btn.setAccessibleDescription("Immediately stops the active typing process")
        window.stop_btn.setMinimumWidth(150)

        control_layout.addWidget(window.start_btn)
        control_layout.addWidget(window.stop_btn)

        main_layout.addLayout(control_layout)

        # Footer
        window.footer_label = QLabel("Press 'Ctrl+T' to start typing instantly. Press 'ESC' at any time to panic stop.", dashboard_page)
        window.footer_label.setObjectName("footer_hint")
        window.footer_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(window.footer_label)

        window.stacked_widget.addWidget(dashboard_page)  # Index 0

        # ==========================================
        # PAGE 1: How to Use (Inline Instructions)
        # ==========================================
        instructions_page = QWidget()
        instr_layout = QVBoxLayout(instructions_page)
        instr_layout.setContentsMargins(20, 20, 20, 10)
        instr_layout.setSpacing(15)

        # Back button header
        instr_header = QHBoxLayout()
        window.back_btn = QPushButton("← Back to Dashboard", instructions_page)
        window.back_btn.setObjectName("back_btn")
        window.back_btn.setMinimumHeight(36)
        window.back_btn.setMinimumWidth(180)
        instr_header.addWidget(window.back_btn)
        instr_header.addStretch()
        instr_layout.addLayout(instr_header)

        # Scrollable instructions content
        scroll_area = QScrollArea(instructions_page)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        instr_content = QTextBrowser(scroll_area)
        instr_content.setOpenExternalLinks(True)
        instr_content.setStyleSheet(
            "QTextBrowser { border: none; background: transparent; font-size: 14px; padding: 10px; }"
        )
        instr_content.setHtml(
            "<h1 style='color: #b58900;'>📖 How to Use AutoTyper</h1>"
            "<hr style='border: 1px solid #586e75;'>"

            "<h2>Step 1 — Load Your Text</h2>"
            "<ul>"
            "  <li>Click <b>📁 Load File</b> to open a <code>.txt</code>, <code>.md</code>, or <code>.docx</code> file.</li>"
            "  <li>Or click <b>📥 Paste</b> to paste text from the clipboard.</li>"
            "  <li>Or <b>drag &amp; drop</b> a file directly onto the window.</li>"
            "</ul>"

            "<h2>Step 2 — Configure Settings</h2>"
            "<ul>"
            "  <li>Adjust the <b>Speed (WPM)</b> slider to control typing speed (20–200 WPM).</li>"
            "  <li>Select <b>Normal</b> mode for constant speed, or <b>Human</b> mode for natural pauses at punctuation.</li>"
            "  <li>Enable <b>Random Delay</b> to add realistic variation between keystrokes.</li>"
            "</ul>"

            "<h2>Step 3 — Start Typing</h2>"
            "<ul>"
            "  <li>Click <b>▶ Start Typing</b>. A <b>5-second countdown</b> begins.</li>"
            "  <li>During the countdown, <b>switch to your target application</b> (Notepad, Word, VS Code, browser, etc.).</li>"
            "  <li>AutoTyper will begin typing automatically into the focused window.</li>"
            "</ul>"

            "<h2>Step 4 — Stop / Emergency</h2>"
            "<ul>"
            "  <li>Press <b>ESC</b> on your keyboard at any time to <b>immediately stop typing</b>.</li>"
            "  <li>Or click <b>⏹ Stop Typing</b> in the AutoTyper window.</li>"
            "</ul>"

            "<hr style='border: 1px solid #586e75;'>"

            "<h2>⌨️ Keyboard Shortcuts</h2>"
            "<table cellpadding='8' cellspacing='0' style='border-collapse: collapse; width: 100%;'>"
            "<tr style='border-bottom: 1px solid #586e75;'>"
            "  <td style='font-weight: bold; width: 120px;'>Ctrl+O</td><td>Open File</td></tr>"
            "<tr style='border-bottom: 1px solid #586e75;'>"
            "  <td style='font-weight: bold;'>Ctrl+T</td><td>Start Typing</td></tr>"
            "<tr style='border-bottom: 1px solid #586e75;'>"
            "  <td style='font-weight: bold;'>Ctrl+W</td><td>Clear Editor</td></tr>"
            "<tr style='border-bottom: 1px solid #586e75;'>"
            "  <td style='font-weight: bold;'>Ctrl+H</td><td>About / Help</td></tr>"
            "<tr style='border-bottom: 1px solid #586e75;'>"
            "  <td style='font-weight: bold;'>F1</td><td>About / Help</td></tr>"
            "<tr>"
            "  <td style='font-weight: bold;'>ESC</td><td>Emergency Stop</td></tr>"
            "</table>"

            "<hr style='border: 1px solid #586e75;'>"

            "<h2>💡 Tips</h2>"
            "<ul>"
            "  <li>AutoTyper <b>auto-saves</b> your editor text. If the app crashes, your text is recovered on next launch.</li>"
            "  <li>Use <b>Recent Files</b> from the Load File dropdown to quickly re-open previously loaded files.</li>"
            "  <li>The status bar shows <b>character count</b>, <b>word count</b>, <b>line count</b>, and <b>estimated typing time</b>.</li>"
            "  <li>AutoTyper is <b>100% offline</b> — no data is sent anywhere. Your text stays on your machine.</li>"
            "</ul>"

            "<hr style='border: 1px solid #586e75;'>"
            "<p style='text-align: center;'>"
            "<i>AutoTyper by <b>The IoT Labs</b> — "
            "<a href='https://theiotlabs.in/' style='color: #b58900;'>theiotlabs.in</a></i></p>"
        )

        scroll_area.setWidget(instr_content)
        instr_layout.addWidget(scroll_area)

        window.stacked_widget.addWidget(instructions_page)  # Index 1

        # ==========================================
        # PAGE 2: Help / About (Inline)
        # ==========================================
        help_page = QWidget()
        help_layout = QVBoxLayout(help_page)
        help_layout.setContentsMargins(20, 20, 20, 10)
        help_layout.setSpacing(15)

        # Back button header
        help_header = QHBoxLayout()
        window.help_back_btn = QPushButton("← Back to Dashboard", help_page)
        window.help_back_btn.setObjectName("back_btn")
        window.help_back_btn.setMinimumHeight(36)
        window.help_back_btn.setMinimumWidth(180)
        help_header.addWidget(window.help_back_btn)
        help_header.addStretch()
        help_layout.addLayout(help_header)

        # Scrollable help content
        help_scroll = QScrollArea(help_page)
        help_scroll.setWidgetResizable(True)
        help_scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        help_content = QTextBrowser(help_scroll)
        help_content.setOpenExternalLinks(True)
        help_content.setStyleSheet(
            "QTextBrowser { border: none; background: transparent; font-size: 14px; padding: 10px; }"
        )
        help_content.setHtml(
            "<h1 style='color: #b58900;'>❓ About AutoTyper</h1>"
            "<hr style='border: 1px solid #586e75;'>"

            "<h2>AutoTyper v1.0.0</h2>"
            "<p><b>Developed by:</b> The IoT Labs</p>"
            "<p>AutoTyper is a professional, secure, and formatting-accurate "
            "Windows keyboard simulation utility.</p>"

            "<hr style='border: 1px solid #586e75;'>"

            "<h2>🔧 Key Capabilities</h2>"
            "<ul>"
            "  <li><b>Native Win32 SendInput</b> — Layout-independent Unicode character dispatch. "
            "Works with any keyboard layout, any language, and any special characters.</li>"
            "  <li><b>Human Rhythm Simulation</b> — Natural pauses at punctuation marks, "
            "paragraph breaks, and random keystroke delays for realistic typing.</li>"
            "  <li><b>Auto-Save & Crash Recovery</b> — Your editor text is continuously saved "
            "to <code>autosave.txt</code>. If the app closes unexpectedly, your work is restored on next launch.</li>"
            "  <li><b>Session Memory</b> — Remembers your window size, position, speed settings, "
            "typing mode, and last opened file across sessions.</li>"
            "  <li><b>Drag & Drop</b> — Drop <code>.txt</code>, <code>.md</code>, or <code>.docx</code> "
            "files directly onto the window to load them.</li>"
            "  <li><b>100% Offline</b> — No internet connection required. No telemetry. "
            "No cloud. No login. Your text never leaves your machine.</li>"
            "</ul>"

            "<hr style='border: 1px solid #586e75;'>"

            "<h2>📋 Supported File Formats</h2>"
            "<table cellpadding='8' cellspacing='0' style='border-collapse: collapse; width: 100%;'>"
            "<tr style='border-bottom: 1px solid #586e75;'>"
            "  <td style='font-weight: bold; width: 120px;'>.txt</td><td>Plain text files (UTF-8, UTF-16, Latin-1)</td></tr>"
            "<tr style='border-bottom: 1px solid #586e75;'>"
            "  <td style='font-weight: bold;'>.md</td><td>Markdown files</td></tr>"
            "<tr>"
            "  <td style='font-weight: bold;'>.docx</td><td>Microsoft Word documents (text content only)</td></tr>"
            "</table>"

            "<hr style='border: 1px solid #586e75;'>"

            "<h2>🛡️ Security & Privacy</h2>"
            "<ul>"
            "  <li>AutoTyper stores settings locally in <code>config.json</code> next to the executable.</li>"
            "  <li>No data is transmitted over the network — ever.</li>"
            "  <li>No analytics, tracking cookies, or telemetry.</li>"
            "  <li>Open source under the MIT License.</li>"
            "</ul>"

            "<hr style='border: 1px solid #586e75;'>"

            "<h2>🏢 About The IoT Labs</h2>"
            "<p>The IoT Labs is a technology company focused on building practical, "
            "reliable, and user-friendly desktop and IoT solutions.</p>"
            "<p>Visit us: <a href='https://theiotlabs.in/' style='color: #b58900;'>theiotlabs.in</a></p>"

            "<hr style='border: 1px solid #586e75;'>"
            "<p style='text-align: center;'>"
            "<i>Copyright © 2026 The IoT Labs. All rights reserved.</i></p>"
            "<p style='text-align: center; font-size: 12px; color: #586e75;'>Version 1.0.0 (Gold Master)</p>"
        )

        help_scroll.setWidget(help_content)
        help_layout.addWidget(help_scroll)

        window.stacked_widget.addWidget(help_page)  # Index 2

        # ==========================================
        # Status Bar (shared across all pages)
        # ==========================================
        window.status_bar = QStatusBar(window)
        window.setStatusBar(window.status_bar)

        window.status_msg_label = QLabel("Ready", window)
        window.status_bar.addWidget(window.status_msg_label, 1)

        # New Status Bar indicators
        window.status_time_label = QLabel("Est. Time: 0s", window)
        window.status_bar.addPermanentWidget(window.status_time_label)

        window.status_profile_label = QLabel("Profile: None", window)
        window.status_bar.addPermanentWidget(window.status_profile_label)

        window.status_mode_label = QLabel("Mode: Normal", window)
        window.status_bar.addPermanentWidget(window.status_mode_label)

        window.status_stats_label = QLabel("Chars: 0 | Words: 0 | Lines: 0", window)
        window.status_bar.addPermanentWidget(window.status_stats_label)

        window.status_progress_bar = QProgressBar(window)
        window.status_progress_bar.setRange(0, 100)
        window.status_progress_bar.setValue(0)
        window.status_progress_bar.setMaximumWidth(200)
        window.status_progress_bar.setTextVisible(True)
        window.status_progress_bar.setFormat("%p%")
        window.status_progress_bar.setVisible(False)
        window.status_bar.addPermanentWidget(window.status_progress_bar)
