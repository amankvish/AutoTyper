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

DARK_THEME = ""
LIGHT_THEME = ""
