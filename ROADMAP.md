# Product Roadmap - AutoTyper

AutoTyper by **The IoT Labs** is designed as a lightweight, safe, and offline-first typing simulation tool.

---

## 🌟 Version 1.1 (Quality of Life Release) - Current
* **Windows 11 Zinc Theme**: Sleek, borderless dark mode interface with Sky Blue accent rings.
* **Typing Profiles**: Switch between Built-in Profiles (Normal, Fast, Slow, Human) or custom.
* **Enhanced Editor**: Find/Replace toolbar, line numbers, word wrap, and 16px Consolas font.
* **File Favorites**: Star (⭐) important files to pin them at the top of the Recent Files dropdown.
* **Settings Manager**: Dedicated UI to configure Auto-Save, Startup Profile, Session Restore.

---

## 🚀 Version 1.2 (Planned)
* **Custom Punctuation Pause Schedulers**: Allow power-users to customize punctuation sleep multipliers inside the settings panel.
* **Auto-Indent Safety Toggles**: Introduce an option inside settings that dynamically inserts backspaces after enters to counteract IDE auto-indent behaviors automatically.
* **Pause/Resume Trigger Key**: Enable pausing and resuming the typing process dynamically via a global hotkey (e.g. `Pause` or `F8`), maintaining the same QThread worker lifecycle.

---

## 🛡️ Out of Scope
* **Cloud Sync & AI Assistants**: We are committed to keeping AutoTyper offline-first and safe. No cloud syncing or AI integrations will be added to preserve local security.
* **Automation macro recorder**: AutoTyper is an automated typing tool, not an automation macro recorder. Unnecessary complexity like recorder hooks will not be implemented.
