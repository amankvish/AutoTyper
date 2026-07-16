import os
import sys

# Application Metadata
APP_NAME = "AutoTyper"
COMPANY_NAME = "The IoT Labs"
VERSION = "1.0.0 (Gold Master)"

# Paths
def get_app_dir() -> str:
    """Returns the base directory of the app."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_resource_path(relative_path: str) -> str:
    """Gets absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    # Dev: Look inside the resources directory
    dev_path = os.path.join(get_app_dir(), "resources", relative_path)
    if os.path.exists(dev_path):
        return dev_path
    return os.path.join(get_app_dir(), relative_path)

CONFIG_FILE_PATH = os.path.join(get_app_dir(), "config.json")
AUTOSAVE_FILE_PATH = os.path.join(get_app_dir(), "autosave.txt")
# App Limits
MAX_RECENT_FILES = 10

# Typing Constants
MIN_WPM = 20
MAX_WPM = 200
DEFAULT_WPM = 60

DEFAULT_MIN_DELAY_MS = 10
DEFAULT_MAX_DELAY_MS = 100

# Human mode delay configurations (seconds)
HUMAN_PAUSE_PUNCTUATION = {
    '.': 0.35,
    ',': 0.15,
    '!': 0.35,
    '?': 0.35,
    ';': 0.20,
    ':': 0.20
}
HUMAN_PAUSE_ENTER = 0.50

# ==========================================
# SOLARIZED MILD STYLESHEET (GENTLE MID-TONE)
# ==========================================

DARK_THEME = """
QMainWindow {
    background-color: #073642;
}
QWidget {
    color: #eee8d5;
    font-family: 'Segoe UI', -apple-system, sans-serif;
    font-size: 13px;
}
QLabel {
    color: #eee8d5;
}
QLabel#header_label {
    font-size: 20px;
    font-weight: 700;
    color: #b58900;
}
QLabel#brand_label {
    font-size: 11px;
    color: #93a1a1;
}
QLabel#footer_label {
    font-size: 11px;
    color: #93a1a1;
}
QPlainTextEdit {
    background-color: #eee8d5;
    color: #073642;
    border: 2px solid #586e75;
    border-radius: 8px;
    padding: 8px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 14px;
}
QPlainTextEdit:focus {
    border: 2px solid #b58900;
    background-color: #eee8d5;
}
QPushButton, QToolButton {
    background-color: #002b36;
    color: #eee8d5;
    border: 1px solid #586e75;
    border-radius: 6px;
    padding: 6px 12px;
    font-weight: 500;
}
QPushButton:hover, QToolButton:hover {
    background-color: #073642;
    border-color: #93a1a1;
}
QPushButton:pressed, QToolButton:pressed {
    background-color: #586e75;
}
QPushButton#start_btn {
    background-color: #b58900;
    color: #002b36;
    border: none;
    font-weight: 700;
    font-size: 14px;
    padding: 10px 20px;
}
QPushButton#start_btn:hover {
    background-color: #cb4b16;
    color: #eee8d5;
}
QPushButton#start_btn:pressed {
    background-color: #b58900;
}
QPushButton#stop_btn {
    background-color: #dc322f;
    color: #ffffff;
    border: none;
    font-weight: 700;
    font-size: 14px;
    padding: 10px 20px;
}
QPushButton#stop_btn:hover {
    background-color: #cb4b16;
}
QPushButton#stop_btn:pressed {
    background-color: #901a1e;
}
QSlider::groove:horizontal {
    border: 1px solid #586e75;
    height: 4px;
    background: #002b36;
    border-radius: 2px;
}
QSlider::sub-page:horizontal {
    background: #b58900;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #eee8d5;
    border: 1px solid #586e75;
    width: 14px;
    height: 14px;
    margin-top: -5px;
    margin-bottom: -5px;
    border-radius: 7px;
}
QSlider::handle:horizontal:hover {
    background: #ffffff;
    border-color: #b58900;
}
QRadioButton {
    spacing: 6px;
}
QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 1px solid #586e75;
    background: #002b36;
}
QRadioButton::indicator:checked {
    background: #b58900;
    border: 4px solid #002b36;
}
QCheckBox {
    spacing: 6px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #586e75;
    background: #002b36;
    border-radius: 4px;
}
QCheckBox::indicator:checked {
    background: #b58900;
    border: 1px solid #b58900;
    image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzA3MzY0MiIgd2lkdGg9IjEycHgiIGhlaWdodD0iMTJweCI+PHBhdGggZD0iTTAgMGgyNHYyNEgweiIgZmlsbD0ibm9uZSIvPjxwYXRoIGQ9Ik05IDE2LjE3TDQuODMgMTJsLTEuNDIgMS40MUw5IDE5IDIxIDdsLTEuNDEtMS40MXoiLz48L3N2Zz4=);
}
QSpinBox {
    background-color: #002b36;
    color: #eee8d5;
    border: 1px solid #586e75;
    border-radius: 6px;
    padding: 4px 6px;
}
QSpinBox:focus {
    border: 1px solid #b58900;
}
QStatusBar {
    background-color: #002b36;
    border-top: 1px solid #073642;
}
QStatusBar QLabel {
    color: #93a1a1;
    font-size: 11px;
}
QGroupBox {
    border: 1px solid #002b36;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: 500;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 8px;
    padding: 0 3px;
}
"""

LIGHT_THEME = """
QMainWindow {
    background-color: #fdf6e3;
}
QWidget {
    color: #073642;
    font-family: 'Segoe UI', -apple-system, sans-serif;
    font-size: 13px;
}
QLabel {
    color: #073642;
}
QLabel#header_label {
    font-size: 20px;
    font-weight: 700;
    color: #b58900;
}
QLabel#brand_label {
    font-size: 11px;
    color: #586e75;
}
QLabel#footer_label {
    font-size: 11px;
    color: #586e75;
}
QPlainTextEdit {
    background-color: #073642;
    color: #eee8d5;
    border: 2px solid #93a1a1;
    border-radius: 8px;
    padding: 8px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 14px;
}
QPlainTextEdit:focus {
    border: 2px solid #b58900;
    background-color: #073642;
}
QPushButton, QToolButton {
    background-color: #eee8d5;
    color: #073642;
    border: 1px solid #93a1a1;
    border-radius: 6px;
    padding: 6px 12px;
    font-weight: 500;
}
QPushButton:hover, QToolButton:hover {
    background-color: #fdf6e3;
    border-color: #586e75;
}
QPushButton:pressed, QToolButton:pressed {
    background-color: #93a1a1;
}
QPushButton#start_btn {
    background-color: #b58900;
    color: #eee8d5;
    border: none;
    font-weight: 700;
    font-size: 14px;
    padding: 10px 20px;
}
QPushButton#start_btn:hover {
    background-color: #cb4b16;
    color: #eee8d5;
}
QPushButton#start_btn:pressed {
    background-color: #b58900;
}
QPushButton#stop_btn {
    background-color: #dc322f;
    color: #ffffff;
    border: none;
    font-weight: 700;
    font-size: 14px;
    padding: 10px 20px;
}
QPushButton#stop_btn:hover {
    background-color: #cb4b16;
}
QPushButton#stop_btn:pressed {
    background-color: #901a1e;
}
QSlider::groove:horizontal {
    border: 1px solid #93a1a1;
    height: 4px;
    background: #eee8d5;
    border-radius: 2px;
}
QSlider::sub-page:horizontal {
    background: #b58900;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #073642;
    border: 1px solid #93a1a1;
    width: 14px;
    height: 14px;
    margin-top: -5px;
    margin-bottom: -5px;
    border-radius: 7px;
}
QSlider::handle:horizontal:hover {
    background: #002b36;
    border-color: #b58900;
}
QRadioButton {
    spacing: 6px;
}
QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 1px solid #93a1a1;
    background: #eee8d5;
}
QRadioButton::indicator:checked {
    background: #b58900;
    border: 4px solid #eee8d5;
}
QCheckBox {
    spacing: 6px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #93a1a1;
    background: #eee8d5;
    border-radius: 4px;
}
QCheckBox::indicator:checked {
    background: #b58900;
    border: 1px solid #b58900;
    image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iI2ZkZjZlMyIgd2lkdGg9IjEycHgiIGhlaWdodD0iMTJweCI+PHBhdGggZD0iTTAgMGgyNHYyNEgweiIgZmlsbD0ibm9uZSIvPjxwYXRoIGQ9Ik05IDE2LjE3TDQuODMgMTJsLTEuNDIgMS40MUw5IDE5IDIxIDdsLTEuNDEtMS40MXoiLz48L3N2Zz4=);
}
QSpinBox {
    background-color: #eee8d5;
    color: #073642;
    border: 1px solid #93a1a1;
    border-radius: 6px;
    padding: 4px 6px;
}
QSpinBox:focus {
    border: 1px solid #b58900;
}
QStatusBar {
    background-color: #eee8d5;
    border-top: 1px solid #fdf6e3;
}
QStatusBar QLabel {
    color: #586e75;
    font-size: 11px;
}
QGroupBox {
    border: 1px solid #eee8d5;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: 500;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 8px;
    padding: 0 3px;
}
"""
