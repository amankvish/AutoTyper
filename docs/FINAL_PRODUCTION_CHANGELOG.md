# AutoTyper v1.1 Production Changelog

## Added
* **Preferences Dialog**: Replaced the heavy full-screen settings page with a lightweight modal `QDialog`.
* **Typing Profiles**: Integrated `Normal`, `Fast`, `Slow`, and `Human` static built-in profiles.
* **Code Editor Widget**: Upgraded the main text box with a `CodeEditor` supporting line numbers.
* **Inline Search & Replace**: Added bottom bar search (`Ctrl+F` and `Ctrl+H`) with Find Next/Prev and Replace capability.
* **Favorites System**: Click ⭐ to favorite a file. Favorites are pinned to the top of the Load File menu.
* **Open Containing Folder**: Added a right-click/menu action to natively launch the OS folder containing the loaded file.
* **Session Restore Memory**: Added strict tracking for exact text cursor placement, active selection ranges, and precise vertical scrollbar positioning on boot.

## Changed
* **Recent Files Validation**: The recent files dropdown now actively checks `os.path.exists` on render and silently prunes any deleted documents.
* **Recent Files Limit**: Expanded capacity from 5 to 10.
* **Notification System**: Stripped toast notification spam. Toasts only fire on major status boundaries (File Loaded, Typing Started, Settings Saved) rather than basic clipboard operations.
* **Typing Human Mode**: Nuanced punctuation and line break pauses decoupled from raw WPM math for more organic delays.

## Removed
* **Settings Page Index**: Unhooked the full `settings_page` widget from the main `QStackedWidget` for UI speed and reduced memory payload.
* **Export / Import Config**: Scrapped backup system entirely to enforce raw, lightweight JSON reliability.
* **Profile Saving**: Removed profile editing logic. Users select a preset or tweak sliders to silently transition into an unsaved "Custom" state.
* **Coding Shortcuts**: Removed `Ctrl+D` (Duplicate Line) and `Ctrl+L` (Delete Line) to preserve the pure typing workflow over IDE feature creep.
