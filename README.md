# AutoTyper Project

An automated keyboard typing simulation utility designed and developed by **The IoT Labs**. This production-grade Windows desktop application is built using Python 3.12+, PySide6 (Qt6), and native Windows SendInput APIs (with PyAutoGUI fallback). It provides a simple, safe, and highly reliable text typing automation experience.

---

## 🚀 Key Features

* **Typing Profiles (v1.1)**: Switch between Built-in Profiles (Normal, Fast, Slow, Human) or save your custom speeds and delays.
* **Code Editor (v1.1)**: Monospaced editor featuring dynamic Line Numbers, Word Wrap toggle, Go To Line (`Ctrl+G`), Duplicate/Delete lines (`Ctrl+D`/`Ctrl+L`), and an inline Find/Replace bar (`Ctrl+F`).
* **Session Restore (v1.1)**: Automatically restores your unsaved text, cursor location, selection, and scroll position on restart.
* **File Favorites (v1.1)**: Star (⭐) important files to pin them at the top of the Recent Files dropdown.
* **Settings Manager (v1.1)**: Dedicated UI to configure Auto-Save, Startup Profile, Session Restore, and Export/Import config backups.
* **Background Threading**: Keystroke emulation runs on a separate worker thread (`QThread`), keeping the GUI responsive and letting you abort instantly.
* **Emergency Stop**: Press the global **`ESC`** key at any point to stop typing immediately, even if the application is not currently focused.
* **Document File Loader**: Load and parse text directly from Plain Text (`.txt`), Markdown (`.md`), and Microsoft Word (`.docx` via `python-docx`) files.
* **Keyboard Shortcuts**: Mapped shortcuts (Ctrl+O, Ctrl+T, Ctrl+W, F1, Ctrl+Q, Ctrl+F) for power users.
* **Document Drag & Drop**: Drag `.txt`, `.md`, or `.docx` files directly onto the app window to import them instantly.
* **Themed Dialogs & Toast Notifications**: Sleek notifications that fade out automatically without interrupting your workflow.
* **Character Stats Counter**: Shows live counts of Characters, Words, and Lines inside the status bar.
* **Estimated Typing Time**: Calculates and displays total estimated typing time next to the profile and mode status.
* **Typing Simulation Modes**:
  * **Normal Mode**: Consistent, uniform typing speed.
  * **Human Mode**: Introduces natural micro-pauses between letters and longer delays after punctuation (`.`, `,`, `!`, `?`, etc.) and newlines.
* **Optional Random Delay**: Enable random delays with customizable minimum and maximum delay limits (in milliseconds).
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