# Product Roadmap - AutoTyper

AutoTyper by **The IoT Labs** is designed as a lightweight, safe, and offline-first typing simulation tool.

---

## 🌟 Version 1.0 (Gold Master Release) - Current
* Monospaced text box styled after Windows 11 Fluent UI, preserving tabs and spacing.
* Support for `.txt`, `.md`, and `.docx` document imports with multi-encoding fallbacks.
* Windows native layout-independent `SendInput` Unicode typing.
* Simulation modes: Normal (uniform WPM) and Human (organic delay variation + punctuation pauses).
* Live character, word, and line count statistics.
* Estimated total duration and dynamic remaining typing countdown.
* Last session auto-restoration and autosave crash prevention.
* Recent files history dropdown menu.
* 100% offline configuration storage.

---

## 🚀 Version 1.1 (Planned)
* **Custom Punctuation Pause Schedulers**: Allow power-users to customize punctuation sleep multipliers inside the settings panel.
* **Auto-Indent Safety Toggles**: Introduce an option inside settings that dynamically inserts backspaces after enters to counteract IDE auto-indent behaviors automatically.
* **Pause/Resume Trigger Key**: Enable pausing and resuming the typing process dynamically via a global hotkey (e.g. `Pause` or `F8`), maintaining the same QThread worker lifecycle.

---

## 🛡️ Out of Scope
* **Cloud Sync & AI Assistants**: We are committed to keeping AutoTyper offline-first and safe. No cloud syncing or AI integrations will be added to preserve local security.
* **Automation macro recorder**: AutoTyper is an automated typing tool, not an automation macro recorder. Unnecessary complexity like recorder hooks will not be implemented.
