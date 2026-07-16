# AutoTyper Version 1.0.0 Final Changelog

All notable changes that transitioned the **AutoTyper** desktop application from a Phase 1 MVP prototype to a stable Gold Master public release are documented in this file.

---

## [1.0.0] - 2026-07-16

This is the Gold Master release of AutoTyper v1.0.0.

### Added
* **Windows Native Character Typing**: Integrated ctypes-wrapped native `SendInput` dispatcher with `KEYEVENTF_UNICODE` inside `core/typing_engine.py` for robust, layout-independent typing of Unicode/UTF-8 character sets (e.g. emojis, Cyrillic, accented symbols).
* **Safe Thread Synchronization**: Connected QThread joins using `.wait()` in window controllers to prevent GC race conditions and application termination warnings.
* **Auto Save Recovery**: Auto-writes editor plain text changes to `autosave.txt` and recovers session text after unexpected crashes.
* **Settings Validation**: Adds strict validation checks (bool vs int/float) inside settings service to prevent configuration corruption.
* **Config Corruption Recovery**: Settings service catches JSON errors and overwrites corrupted config files with defaults on boot.
* **Character Stats Counter**: Shows live counts of Characters, Words, and Lines inside the status bar.
* **Estimated Typing Duration**: Computes estimated total typing time next to WPM slider and remaining time inside the status bar during typing.
* **Recent Files History**: Displays the last 5 opened files in a dropdown popup associated with the Load File button.
* **Session Restoration**: Restores window sizing/position, editor text, cursor indexes, last opened file paths, themes, and speed settings.
* **Splash Screen Loader**: Custom graphics splash screen rendered for 1.5 seconds on application boot.
* **First Launch Welcome Tips**: Custom welcome dialog showing quick start tips on the initial app startup.
* **Help / About Dialog**: Themed details panel containing software specifications and copyrights.
* **Local Keyboard Shortcuts**: Maps Ctrl+O (Load), Ctrl+T (Start), Ctrl+W (Clear), Ctrl+H / F1 (Help/About), and Ctrl+Q (Exit) shortcuts.
* **File Drag & Drop**: Enable direct document importing by dragging and dropping `.txt`, `.md`, or `.docx` files onto the editor.
* **Themed MessageBox Dialogs**: Styled message boxes (errors, warnings, prompts) to match active stylesheets.
* **Double-Check Exit Confirmations**: Intercepts close events to warn users if typing is running or if the editor has unsaved text.
* **Robust File Load Encodings**: Sequential tries for `utf-8-sig` (stripping BOM), `utf-16`, and `latin-1` fallbacks to prevent loading crashes.
* **Expanded Automated Tests**: Added 14 unit and integration tests inside `test_core.py` covering WPM math, random delay distributions, formatting, Unicode loading, corrupted config recovery, recent files queue FIFO behavior, and large file parses.

### Changed
* **Styling**: Standardized Dark and Light themes to use Windows 11 Fluent UI style guidelines and applied styling to QToolButton dropdown menus.
* **Load File Controls**: Converted the Load File button to a `QToolButton` with `MenuButtonPopup` mode to display recent file history.
* **Status Updates**: Centralized status message state changes (Ready, Countdown, Typing, Stopped, Completed, Error) to be emitted directly from the Typing Engine.

### Removed
* **PDF Document Loader**: Removed `PyPDF2` dependency and PDF loader since extracting text from PDF destroys original indentations and tabs.
* **Markdown Parsing Library**: Removed the unused `markdown` library from `requirements.txt`.
* **Legacy Prototypes**: Deleted `test.py` and `autotyper.py` prototype mockups to clean up the repository.
