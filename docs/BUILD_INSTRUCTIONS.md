# Build & Compilation Instructions

This guide documents how to compile the **AutoTyper** source files into a single, standalone Windows `.exe` executable using **PyInstaller**.

---

## 🛠️ Step 1: Development Environment Setup

Ensure you have Python 3.12+ (64-bit) installed and have set up your virtual environment:

```bash
# 1. Activate your virtual environment
.venv\Scripts\activate

# 2. Install PyInstaller and dependencies
pip install -r requirements.txt
```

---

## 📦 Step 2: Packaging the Application

We compile the project using PyInstaller and the provided specification file **`autotyper.spec`**:

```bash
pyinstaller autotyper.spec
```

### What this command does:
1. Compiles the main entry point `main.py` without terminal outputs (`console=False` / `--noconsole`).
2. Packages dependencies (`PySide6`, `pyautogui`, `python-docx`, `pynput`).
3. Embeds the application icon (`autotyper_icon.ico`) to show on File Explorer.
4. Packs static assets (`autotyper_splash.png` and `autotyper_icon.png`) into the executable's internal resource bundle.

---

## 🔬 Step 3: Executable Verification

Once compilation completes, the packaged executable will be generated inside the **`dist/`** directory:

```text
AutoTyper Project/
└── dist/
    └── autotyper.exe     # Standalone application
```

To verify the build:
1. Double-click `dist/autotyper.exe` in Windows File Explorer.
2. Verify that the **Splash Screen** appears for 1.5 seconds.
3. Verify that the Main Window launches, restores session parameters, and connects file/stats listeners.
4. Try drag-and-drop loading of a text file and verify that the stats display correctly.
