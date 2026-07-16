# Changelog - AutoTyper

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-07-16
### Added
- **Typing Profiles System**: Added `Normal`, `Fast`, `Slow`, and `Human` profile presets. Custom profile state is automatically tracked when users adjust sliders manually.
- **Code Editor Widget**: Replaced the basic text editor with a robust `CodeEditor` featuring dynamic line numbers and intelligent block tracking.
- **Inline Search & Replace**: Press `Ctrl+F` or `Ctrl+H` to access a non-intrusive bottom search bar with Find Next, Find Prev, Replace, and Replace All capabilities.
- **Advanced Editor Shortcuts**: Added Word Wrap toggle, Zooming (`Ctrl++`, `Ctrl+-`), Go to Line (`Ctrl+G`), Duplicate Line (`Ctrl+D`), and Delete Line (`Ctrl+L`).
- **Favorites System**: Click the ⭐ icon to favorite files. Favorites are pinned to the top of the Load File dropdown.
- **Session Restore System**: AutoTyper now automatically restores your unsaved text, exact cursor position, active text selection, and vertical scroll location upon reboot.
- **Dynamic Status Bar**: Status bar now tracks: Estimated Total Typing Time, Active Profile, Typing Mode, Character Count, Word Count, and Line Count.
- **Toast Notifications**: Implemented custom floating auto-fading notifications to replace annoying dialogue popups for simple actions like copying, pasting, and starring files.
- **Dedicated Settings Page**: Added a new full-page settings menu to configure default preferences (auto-save, startup profile, restore session, countdown duration) and manage config backups.
- **Accessibility Attributes**: Screen readers can now properly identify all interactive UI elements via updated `setAccessibleName` properties.

### Changed
- Increased `MAX_RECENT_FILES` capacity from 5 to 10.
- Recent Files menu now automatically prunes deleted or moved files.
- Refactored UI connections in `main_window.py` to correctly block signals, eliminating recursive event loop bugs when changing profiles programmatically.
- Enhanced delay engine `Human` mode variance by abstracting `punctuation_pause` and `line_break_pause` directly into the Typing Profiles logic for finer control.

### Removed
- Removed intrusive message box alerts for non-critical confirmations.

---

## [1.0.0] - 2026-07-16
This is the Gold Master release of AutoTyper v1.0.0.

### Added
- **Windows Native Character Typing**: Integrated ctypes-wrapped native `SendInput` dispatcher with `KEYEVENTF_UNICODE` inside `core/typing_engine.py` for robust, layout-independent typing of Unicode/UTF-8 character sets.
- **Safe Thread Synchronization**: Connected QThread joins using `.wait()` in window controllers to prevent GC race conditions.
- **Auto Save Recovery**: Auto-writes editor plain text changes to `autosave.txt` and recovers session text after unexpected crashes.
- **Settings Validation**: Adds strict validation checks (bool vs int/float) inside settings service to prevent configuration corruption.
- **Config Corruption Recovery**: Settings service catches JSON errors and overwrites corrupted config files with defaults on boot.
- **Character Stats Counter**: Shows live counts of Characters, Words, and Lines inside the status bar.
- **Estimated Typing Duration**: Computes estimated total typing time next to WPM slider and remaining time inside the status bar during typing.
- **Recent Files History**: Displays the last 5 opened files in a dropdown popup associated with the Load File button.
- **Session Restoration**: Restores window sizing/position, editor text, cursor indexes, last opened file paths, themes, and speed settings.
- **Splash Screen Loader**: Custom graphics splash screen rendered for 1.5 seconds on application boot.
- **First Launch Welcome Tips**: Custom welcome dialog showing quick start tips on the initial app startup.
- **Help / About Dialog**: Themed details panel containing software specifications and copyrights.
- **Local Keyboard Shortcuts**: Maps Ctrl+O (Load), Ctrl+T (Start), Ctrl+W (Clear), Ctrl+H / F1 (Help/About), and Ctrl+Q (Exit) shortcuts.
- **File Drag & Drop**: Enable direct document importing by dragging and dropping `.txt`, `.md`, or `.docx` files onto the editor.
- **Themed MessageBox Dialogs**: Styled message boxes (errors, warnings, prompts) to match active stylesheets.
- **Double-Check Exit Confirmations**: Intercepts close events to warn users if typing is running or if the editor has unsaved text.
- **Robust File Load Encodings**: Sequential tries for `utf-8-sig` (stripping BOM), `utf-16`, and `latin-1` fallbacks to prevent loading crashes.
- **Expanded Automated Tests**: Added 14 unit and integration tests inside `test_core.py` covering WPM math, random delay distributions, formatting, Unicode loading, corrupted config recovery, recent files queue FIFO behavior, and large file parses.

### Changed
- **Styling**: Standardized Dark and Light themes to use Windows 11 Fluent UI style guidelines and applied styling to QToolButton dropdown menus.
- **Load File Controls**: Converted the Load File button to a `QToolButton` with `MenuButtonPopup` mode to display recent file history.
- **Status Updates**: Centralized status message state changes (Ready, Countdown, Typing, Stopped, Completed, Error) to be emitted directly from the Typing Engine.

### Removed
- **PDF Document Loader**: Removed `PyPDF2` dependency and PDF loader since extracting text from PDF destroys original indentations and tabs.
- **Markdown Parsing Library**: Removed the unused `markdown` library from `requirements.txt`.
- **Legacy Prototypes**: Deleted `test.py` and `autotyper.py` prototype mockups to clean up the repository.
