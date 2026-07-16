# Release Notes - AutoTyper Version 1.0.0 (Gold Master)

**AutoTyper** is the easiest, safest, and most reliable auto-typing utility suite for Windows, developed by **The IoT Labs**.

---

## 🌟 Version Overview
Version 1.0.0 is the official release of AutoTyper. Built with PySide6 (Qt6) and native Windows SendInput APIs (with PyAutoGUI fallback), this application provides desktop users with an automated typing experience that preserves formatting, handles special character sets, and simulates natural human variations.

### Core Value Proposition
> "Paste or load text, click Start, and type naturally, accurately, and safely."

---

## 🚀 Key Features

1. **Smart Monospaced Editor**: Monospaced font display preserving space indentations, tabs, and blank lines exactly.
2. **Multi-Format Loader**: One-click import for Plain Text (`.txt`), Markdown (`.md`), and Word (`.docx`) files with support for UTF-8 with BOM, UTF-16, and Latin-1 fallbacks.
3. **Splash Screen Loader**: Premium graphics screen displayed dynamically for 1.5 seconds on application boot.
4. **First Launch Welcome Panel**: Helpful quick-start tips shown automatically on first launch to guide new users.
5. **Help / About Panel**: Custom help details containing native capabilities and copyright info.
6. **Local Keyboard Shortcuts**: Map Ctrl+O (Load), Ctrl+T (Start), Ctrl+W (Clear), Ctrl+H / F1 (Help/About), and Ctrl+Q (Exit) for power-user control.
7. **Document Drag & Drop**: Drag `.txt`, `.md`, or `.docx` files directly onto the app window to import them instantly.
8. **Themed MessageBox Dialogs**: All errors, warnings, and prompts are rendered inside custom widgets matching the active Dark/Light stylesheet.
9. **Exit Safety Triggers**: Prompts exit confirmation when the user closes the app with active text or during typing execution.
10. **Auto Save & Crash Recovery**: Keeps a live copy of editor text in `autosave.txt` and automatically restores it in the event of an unexpected application crash.
11. **Character Stats Counter**: Shows live counts of Characters, Words, and Lines inside the status bar.
12. **Estimated Typing Time**: Calculates and displays total estimated typing time next to WPM slider, and remaining duration during execution in the status bar.
13. **Recent Files Dropdown**: Accessible menu associated with the Load File button that lists the last 5 files opened.
14. **Session Memory**: Remembers and restores window positions, sizes, editor text, cursor location, theme mode, and typing configurations automatically.
15. **Typing Simulation Profiles**:
   * **Normal Mode**: Emulates keys at a uniform, consistent speed.
   * **Human Mode**: Automatically varies the speed organically and adds realistic pauses after punctuations and carriage returns.
16. **Millisecond Random Delays**: Add optional speed variability with customizable minimum and maximum character delay thresholds.
17. **Global Emergency Stop**: Hold down **`ESC`** at any time to abort typing instantly, even if the application window is minimized or out of focus.
18. **Windows 11 UI Styling**: Rounded corners, clean spacing, and immediate Dark/Light theme toggling.
19. **Offline-First Security**: Runs entirely locally with zero database allocations, cloud APIs, accounts, or telemetry.

---

## 💻 System Requirements

* **Operating System**: Windows 10 or 11 (64-bit).
* **Python runtime**: Python 3.12+ (for running from source).
* **RAM footprint**: < 45 MB.
* **Storage footprint**: < 100 MB.

---

## 🛠️ Installation & Setup

Ensure your virtual environment is activated, then run:

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

To compile into a standalone `.exe`:
```bash
pyinstaller autotyper.spec
```
The compiled executable will be placed under the `dist/` directory.
