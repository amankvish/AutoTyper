# GitHub Release Notes - AutoTyper v1.0.0 (Gold Master)

We are proud to announce the Gold Master release of **AutoTyper v1.0.0**, the easiest, safest, and most reliable auto-typing utility suite for Windows!

Developed under the brand **The IoT Labs**, AutoTyper is designed from the ground up as a lightweight, secure, and formatting-accurate keyboard simulation tool.

---

## 🚀 Key Highlights

* **Windows Native Unicode Emulation**: Direct `SendInput` keyboard simulations bypass physical layouts to write accents, emojis, and special characters flawlessly.
* **Preserves Layout Formatting**: Guarantees spaces, tabs, and indentation structure preservation. normalizes newlines to avoid double-enter issues.
* **Human Emulation Engine**: Mimics natural human keystroke speed distributions and adds pauses after punctuations and returns.
* **Emergency Halt Key**: Press global **`ESC`** key at any point to stop typing instantly, even if the application window is out of focus.
* **Session Memory & Auto Save**: Automatically preserves settings, sizing, and cursor indices. Autowrites to `autosave.txt` to prevent text loss during crashes.
* **100% Offline-First**: Zero databases, web API connections, or telemetry tracking to ensure your local script files stay completely secure.

---

## 🛠️ Installation & Setup

1. Download and extract **`AutoTyper_v1.0.0.zip`**.
2. Run **`autotyper.exe`** to start the application (if Windows SmartScreen displays a warning, click *More Info* -> *Run Anyway*).
3. The configuration will be stored locally inside a generated `config.json` next to the executable.

---

## 🧪 Verification Logs
* **Automated Unit Tests**: 14/14 tests passed successfully (`python test_core.py`).
* **Active memory**: Consumes < 45 MB RAM during active execution loops.
* **Boot speed**: GUI renders in less than 1.0 second.
