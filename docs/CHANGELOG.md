# AutoTyper v1.1 - Release Changelog

## Visual & UI Redesign (The Fluent Update)
- **Windows 11 Zinc Theme**: We completely rewrote the stylesheet to use modern Zinc dark colors, replacing the old Solarized yellow/beige scheme. 
- **Legacy Theme Bug Fixed**: Removed a bug in `config.py` that forced an old theme override and blocked global `.qss` styles from applying.
- **Card UI**: Removed rigid `QGroupBox` borders, converting Settings sections into sleek, flat cards.
- **CodeEditor Upgrades**:
  - Font size explicitly increased to 16px Consolas for much better readability.
  - Background set to ultra-dark IDE black (`#09090b`).
  - Active line highlight and muted gutter added.

## Features & UX Improvements
- **Find/Replace Toolbar Button**: Added a dedicated `🔍 Find` toggle button on the main toolbar to easily access the Find/Replace functionality (previously hidden behind Ctrl+F).
- **Instructions Update**: Renamed all instances of "How to Use" to "Instructions" across the UI and documentation.

## Developer & Documentation Polish
- **Documentation Cleanup**: Nuked over 15 redundant and fragmented documentation files (`FINAL_PRODUCTION_*`, `PHASE2_*`, `UI_*`). The `/docs` folder is now strictly consolidated.
