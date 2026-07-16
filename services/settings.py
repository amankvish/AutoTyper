import json
import logging
import os
from typing import Any, Dict
from config import CONFIG_FILE_PATH, DEFAULT_WPM, DEFAULT_MIN_DELAY_MS, DEFAULT_MAX_DELAY_MS

logger = logging.getLogger(__name__)

class SettingsService:
    """Manages application settings persistence to config.json."""
    
    _defaults: Dict[str, Any] = {
        "theme": "dark",
        "wpm": DEFAULT_WPM,
        "random_delay_enabled": True,
        "min_delay_ms": DEFAULT_MIN_DELAY_MS,
        "max_delay_ms": DEFAULT_MAX_DELAY_MS,
        "typing_mode": "human",
        "window_width": 800,
        "window_height": 650,
        "window_x": -1,
        "window_y": -1,
        "recent_files": [],
        "last_opened_file": "",
        "editor_cursor_position": 0,
        "editor_text": "",
        "first_launch": True
    }

    def __init__(self):
        self.settings: Dict[str, Any] = self._defaults.copy()
        self.load()

    def load(self) -> None:
        """Loads settings from config.json. If missing/invalid, falls back to defaults."""
        if not os.path.exists(CONFIG_FILE_PATH):
            logger.info("Config file not found. Initializing with defaults.")
            self.settings = self._defaults.copy()
            self.save()
            return

        try:
            with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    # Merge loaded data with defaults to ensure all keys exist
                    for key, val in self._defaults.items():
                        self.settings[key] = data.get(key, val)
                else:
                    logger.warning("Corrupted config structure. Using defaults.")
                    self.settings = self._defaults.copy()
                    self.save()
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}. Resetting to defaults.")
            self.settings = self._defaults.copy()
            self.save()

    def save(self) -> None:
        """Saves current settings to config.json."""
        try:
            os.makedirs(os.path.dirname(CONFIG_FILE_PATH), exist_ok=True)
            with open(CONFIG_FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")

    def get(self, key: str) -> Any:
        """Gets a setting value by key."""
        return self.settings.get(key, self._defaults.get(key))

    def set(self, key: str, value: Any) -> None:
        """Sets a setting value and saves the configuration."""
        if key in self._defaults:
            # Ensure type safety
            expected_type = type(self._defaults[key])
            is_valid = False
            if expected_type is bool:
                is_valid = isinstance(value, bool)
            elif expected_type in (int, float):
                is_valid = isinstance(value, (int, float)) and not isinstance(value, bool)
            else:
                is_valid = isinstance(value, expected_type)

            if is_valid:
                self.settings[key] = value
                self.save()
            else:
                logger.warning(f"Type mismatch for key '{key}'. Expected {expected_type}, got {type(value)}")
        else:
            logger.warning(f"Attempted to set unrecognized setting key: {key}")

    def add_recent_file(self, file_path: str) -> None:
        """Adds a file path to the recent files list (capped at last 5, unique, newest first)."""
        if not file_path:
            return
            
        recent = self.get("recent_files")
        if not isinstance(recent, list):
            recent = []
            
        # Standardize path slashes
        normalized_path = os.path.normpath(file_path)
        
        # Remove if already exists to place it first
        if normalized_path in recent:
            recent.remove(normalized_path)
            
        recent.insert(0, normalized_path)
        
        # Cap at MAX_RECENT_FILES
        from config import MAX_RECENT_FILES
        recent = recent[:MAX_RECENT_FILES]
        
        # Use direct dict assignment to avoid calling save() twice, then save manually
        self.settings["recent_files"] = recent
        self.save()
