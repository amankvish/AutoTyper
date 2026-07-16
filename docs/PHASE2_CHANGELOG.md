# Phase 2 (v1.1) Changelog

All Phase 2 Quality of Life changes are documented here.

## Added
* **Typing Profiles System**: Added static `Normal`, `Fast`, `Slow`, and `Human` profile presets. Moving sliders manually transitions state to `Custom (Unsaved)`.
* **Code Editor Widget**: Replaced basic text editor with `CodeEditor` featuring dynamic line numbers.
* **Inline Search & Replace**: Press `Ctrl+F` or `Ctrl+H` to access search bar with Find Next, Find Prev, Replace, and Replace All capabilities.
* **Favorites System**: Click ⭐ to favorite files. Favorites pinned to top of Load File dropdown.
* **Open Containing Folder**: Added native OS folder opener to the Load File dropdown.
* **Session Restore**: Automatically restores unsaved text, exact cursor position, and scroll location.
* **Preferences Dialog**: A lightweight QDialog to configure Countdown, Autosave, Session Restore, Default Profile, and Factory Resets.

## Changed
* **Recent Files Limit**: Increased capacity from 5 to 10. Automatically prunes deleted files.
* **Toast Notifications**: Stripped spammy notifications. Now reserved strictly for File Loaded, Settings Saved, and Typing bounds.
* **Human Mode**: Upgraded delay engine with nuanced punctuation pauses.

## Removed
* **Settings Page**: Full settings page index completely removed in favor of lightweight dialog.
* **Export/Import Config**: Backup mechanics removed to simplify user experience.
* **Save/Restore Profiles**: Removed persistent profile modifications to keep built-in presets static.
* **IDE Editor Shortcuts**: Removed `Ctrl+D` (Duplicate) and `Ctrl+L` (Delete line) to maintain text-editor focus.
