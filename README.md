# AutoTyper Project

An automated keyboard typing simulation utility designed and developed by **The IoT Labs**. This production-grade Windows desktop application is built using Python 3.12+, PySide6 (Qt6), and native Windows SendInput APIs (with PyAutoGUI fallback). It provides a simple, safe, and highly reliable text typing automation experience.

---

## 🚀 Key Features

* **Background Threading**: Keystroke emulation runs on a separate worker thread (`QThread`), keeping the GUI responsive and letting you abort instantly.
* **Emergency Stop**: Press the global **`ESC`** key at any point to stop typing immediately, even if the application is not currently focused.
* **Smart Text Editor**: Monospaced text box styled after Windows 11 Fluent UI, preserving tabs, spacing, and indentations exactly.
* **Document File Loader**: Load and parse text directly from Plain Text (`.txt`), Markdown (`.md`), and Microsoft Word (`.docx` via `python-docx`) files.
* **Splash Screen Loader**: Premium graphic screen displayed dynamically for 1.5 seconds on application boot.
* **First Launch Welcome Panel**: Helpful quick-start tips shown automatically on first launch to guide new users.
* **Keyboard Shortcuts**: Mapped shortcuts (Ctrl+O, Ctrl+T, Ctrl+W, Ctrl+H, F1, Ctrl+Q) for power users.
* **Document Drag & Drop**: Drag `.txt`, `.md`, or `.docx` files directly onto the app window to import them instantly.
* **Themed Dialogs**: Styled message boxes (errors, warnings, and prompts) matching the active Dark/Light stylesheet.
* **Exit Safety Checks**: Double-checks with the user before stopping active typing execution or discarding current text edits.
* **Character Stats Counter**: Shows live counts of Characters, Words, and Lines inside the status bar.
* **Estimated Typing Time**: Calculates and displays total estimated typing time next to WPM slider, and remaining duration during execution in the status bar.
* **Recent Files Dropdown**: Accessible menu associated with the Load File button that lists the last 5 files opened.
* **Session Memory**: Remembers and restores window positions, sizes, editor text, cursor location, theme mode, and typing configurations automatically.
* **Typing Speed Slider**: Fine-tune your typing speed between `20 WPM` and `200 WPM`.
* **Typing Simulation Modes**:
  * **Normal Mode**: Consistent, uniform typing speed.
  * **Human Mode**: Introduces natural micro-pauses between letters and longer delays after punctuation (`.`, `,`, `!`, `?`, etc.) and newlines.
* **Optional Random Delay**: Enable random delays with customizable minimum and maximum delay limits (in milliseconds).
* **Settings Persistence**: Saves your WPM speed, typing mode, delay ranges, theme choices, and window size/position inside a local `config.json` file.
* **Dark / Light Modes**: A modern, sleek user interface with support for Windows 11 style rounded corners and high-contrast styling.

---

## 📁 Repository Structure

The codebase is organized following clean architectural guidelines, separating user interfaces from backend business logic:

```text
AutoTyper Project/
│
├── main.py                 # Application entry point
├── config.py               # Constants, limitations, & Windows 11 stylesheet templates
├── requirements.txt        # Python dependency list
├── autotyper.spec          # PyInstaller packaging configuration
├── file_version_info.txt   # Windows executable version details
├── test_core.py            # Unit and integration test suite
│
├── app/                    # User Interface Package
│   ├── ui.py               # Widget declarations and visual layout
│   └── main_window.py      # Main window controller (signals, threading, file triggers)
│
├── core/                   # Core Typing Simulation Logic
│   ├── typing_engine.py    # Emulation thread worker and global key hook listener
│   ├── delay_engine.py     # Speed formulas and punctuation pause multipliers
│   └── formatter.py        # Carriage return normalization utility
│
├── services/               # Services Package
│   ├── settings.py         # Read/write configuration JSON schema
│   ├── file_loader.py      # Multi-format document parser (.txt, .md, .docx)
│   └── clipboard.py        # System clipboard interface
│
├── docs/                   # Quality Control and Release Documentation
│   ├── ARCHITECTURE_GUIDE.md # Architectural overview and class diagrams
│   ├── BUILD_INSTRUCTIONS.md # Step-by-step PyInstaller compilation guide
│   ├── DEVELOPER_GUIDE.md    # API documentation and testing conventions
│   ├── INSTALLER_GUIDE.md    # SmartScreen warnings and packaging details
│   ├── RELEASE_CHECKLIST.md  # Final Release QA Verification Checklist
│   ├── GITHUB_RELEASE_NOTES.md # Releases details template
│   ├── QC_REPORT.md        # Final Quality Control audit report
│   ├── CHANGELOG.md        # Change log details for Version 1.0
│   ├── RELEASE_NOTES.md    # Release notes & instructions
│   ├── KNOWN_ISSUES.md     # Environmental constraints & workarounds
│   └── TEST_REPORT.md      # Automated testing suite log
│
├── LICENSE                 # MIT License file
├── SECURITY.md             # Security disclosures policy
├── CONTRIBUTING.md         # Contributor guidelines
├── CODE_OF_CONDUCT.md      # Contributor Covenant Code of Conduct
└── ROADMAP.md              # Product release roadmap
```

---

## 🛠️ Installation & Setup

### Prerequisites
Make sure you have **Python 3.12+** installed on your system.

### Step 1: Set up a Virtual Environment
We recommend running this application in a virtual environment to avoid dependency conflicts:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows (PowerShell):
.venv\Scripts\activate
# On Windows (CMD):
.venv\Scripts\activate.bat
```

### Step 2: Install Dependencies
Install all required libraries using `requirements.txt`:

```bash
pip install -r requirements.txt
```

This installs:
* `PySide6` (>=6.6.0) - For building the cross-platform GUI.
* `pyautogui` (>=0.9.53) - For simulating keyboard keypresses.
* `python-docx` (>=1.2.0) - For loading and parsing Microsoft Word files.
* `pynput` (>=1.7.6) - For registering the global `ESC` key listener thread.
* `pyinstaller` (>=6.3.0) - For packaging the standalone executable.

---

## 💻 Running the Application

Ensure your virtual environment is activated before running the script.

```bash
python main.py
```

---

## 📦 Compiling to Standalone Executable (.exe)

You can package this Python application into a standalone executable file for Windows using PyInstaller, so users do not need Python installed to run it.

1. Ensure PyInstaller is installed:
   ```bash
   pip install pyinstaller
   ```

2. Compile using the existing specification file:
   ```bash
   pyinstaller autotyper.spec
   ```

3. The output executable `autotyper.exe` will be created in the `dist/` directory.

---

## 🧪 Running Tests

A complete unit test suite has been built to test formatting, settings, delays, and file loaders.

```bash
python test_core.py
```

---

## 📚 Quality Control and Release Documentation

More details about the release can be found in the **[docs/](file:///d:/IoT%20Labs/AutoTyper%20Project/docs)** folder:
* **[docs/QC_REPORT.md](file:///d:/IoT%20Labs/AutoTyper%20Project/docs/QC_REPORT.md)**: Product Quality Control audit details and readiness score.
* **[docs/CHANGELOG.md](file:///d:/IoT%20Labs/AutoTyper%20Project/docs/CHANGELOG.md)**: Version history, additions, changes, and removals.
* **[docs/RELEASE_REPORT.md](file:///d:/IoT%20Labs/AutoTyper%20Project/docs/RELEASE_REPORT.md)**: Final pre-release audit, verification, and code sign parameters.
* **[docs/RELEASE_NOTES.md](file:///d:/IoT%20Labs/AutoTyper%20Project/docs/RELEASE_NOTES.md)**: Target users, features, and deployment parameters.
* **[docs/KNOWN_ISSUES.md](file:///d:/IoT%20Labs/AutoTyper%20Project/docs/KNOWN_ISSUES.md)**: Workarounds for auto-indentation and admin privileges.
* **[docs/TEST_REPORT.md](file:///d:/IoT%20Labs/AutoTyper%20Project/docs/TEST_REPORT.md)**: Expanded unit test suite results.
* **[docs/RELEASE_CHECKLIST.md](file:///d:/IoT%20Labs/AutoTyper%20Project/docs/RELEASE_CHECKLIST.md)**: Quality Assurance verification checklist.
* **[docs/BUILD_INSTRUCTIONS.md](file:///d:/IoT%20Labs/AutoTyper%20Project/docs/BUILD_INSTRUCTIONS.md)**: PyInstaller compilation steps.
* **[docs/DEVELOPER_GUIDE.md](file:///d:/IoT%20Labs/AutoTyper%20Project/docs/DEVELOPER_GUIDE.md)**: Core components documentation and design styles.
* **[docs/ARCHITECTURE_GUIDE.md](file:///d:/IoT%20Labs/AutoTyper%20Project/docs/ARCHITECTURE_GUIDE.md)**: Class maps, threading synchronization, and crash prevention structures.
* **[docs/INSTALLER_GUIDE.md](file:///d:/IoT%20Labs/AutoTyper%20Project/docs/INSTALLER_GUIDE.md)**: Windows SmartScreen workarounds, executable signing details, and Inno Setup integration.
* **[docs/GITHUB_RELEASE_NOTES.md](file:///d:/IoT%20Labs/AutoTyper%20Project/docs/GITHUB_RELEASE_NOTES.md)**: Release tags summary.
* **[docs/UI_UX_DESIGN_PROPOSAL.md](file:///d:/IoT%20Labs/AutoTyper%20Project/docs/UI_UX_DESIGN_PROPOSAL.md)**: Design philosophy, visual tokens, and interface guides.

---

## 🛡️ Legal and Community Policies
* **[LICENSE](LICENSE)**: MIT License details.
* **[SECURITY.md](SECURITY.md)**: Security vulnerability disclosures and offline policy details.
* **[CONTRIBUTING.md](CONTRIBUTING.md)**: Development guidelines, setup, and PR conventions.
* **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)**: Contributor Covenant Code of Conduct.
* **[ROADMAP.md](ROADMAP.md)**: Product release roadmap.