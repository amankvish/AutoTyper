from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QCheckBox, QSpinBox, QComboBox, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from services.settings import SettingsService

class PreferencesDialog(QDialog):
    def __init__(self, parent, settings_service: SettingsService):
        super().__init__(parent)
        self.settings = settings_service
        self.setWindowTitle("Preferences")
        self.setMinimumWidth(350)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        group = QGroupBox("General Preferences", self)
        form = QVBoxLayout(group)
        
        self.autosave_cb = QCheckBox("Enable Auto Save", group)
        self.restore_session_cb = QCheckBox("Restore Last Session on Startup", group)
        self.remember_win_cb = QCheckBox("Remember Window Position & Size", group)
        
        form.addWidget(self.autosave_cb)
        form.addWidget(self.restore_session_cb)
        form.addWidget(self.remember_win_cb)
        
        # Default Profile
        def_prof_layout = QHBoxLayout()
        def_prof_layout.addWidget(QLabel("Default Profile:", group))
        self.default_profile_combo = QComboBox(group)
        self.default_profile_combo.addItems(["Normal", "Fast", "Slow", "Human"])
        def_prof_layout.addWidget(self.default_profile_combo)
        def_prof_layout.addStretch()
        form.addLayout(def_prof_layout)
        
        # Countdown Timer
        cd_layout = QHBoxLayout()
        cd_layout.addWidget(QLabel("Countdown (seconds):", group))
        self.custom_countdown_spin = QSpinBox(group)
        self.custom_countdown_spin.setRange(1, 60)
        cd_layout.addWidget(self.custom_countdown_spin)
        cd_layout.addStretch()
        form.addLayout(cd_layout)
        
        layout.addWidget(group)
        
        btn_layout = QHBoxLayout()
        self.reset_btn = QPushButton("Reset Settings", self)
        self.reset_btn.setObjectName("danger_action")
        self.close_btn = QPushButton("Close", self)
        
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.close_btn)
        
        layout.addLayout(btn_layout)
        
        # Connect signals
        self.close_btn.clicked.connect(self.accept)
        self.reset_btn.clicked.connect(self.handle_reset)
        
        self.autosave_cb.toggled.connect(lambda checked: self.settings.set("autosave_enabled", checked))
        self.restore_session_cb.toggled.connect(lambda checked: self.settings.set("restore_session", checked))
        self.remember_win_cb.toggled.connect(lambda checked: self.settings.set("remember_window_position", checked))
        self.default_profile_combo.currentTextChanged.connect(lambda text: self.settings.set("default_profile", text))
        self.custom_countdown_spin.valueChanged.connect(lambda val: self.settings.set("custom_countdown", val))
        
        self._load_values()
        
    def _load_values(self):
        self.autosave_cb.setChecked(self.settings.get("autosave_enabled", True))
        self.restore_session_cb.setChecked(self.settings.get("restore_session", True))
        self.remember_win_cb.setChecked(self.settings.get("remember_window_position", True))
        self.default_profile_combo.setCurrentText(self.settings.get("default_profile", "Normal"))
        self.custom_countdown_spin.setValue(self.settings.get("custom_countdown", 5))

    def handle_reset(self):
        reply = QMessageBox.question(self, 'Reset Settings', 'Are you sure you want to reset all preferences to default?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.settings.set("autosave_enabled", True)
            self.settings.set("restore_session", True)
            self.settings.set("remember_window_position", True)
            self.settings.set("default_profile", "Normal")
            self.settings.set("custom_countdown", 5)
            self._load_values()
            
            # Show a toast in the main window
            if self.parent() and hasattr(self.parent(), "show_toast"):
                self.parent().show_toast("Preferences reset to defaults.", "info")
