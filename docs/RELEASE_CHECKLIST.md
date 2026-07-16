# Release QA & Verification Checklist

Use this checklist to perform final Quality Assurance (QA) before publishing the **AutoTyper v1.0.0** release.

---

## 🛠️ Phase 1: Environment & Setup Verification
- `[ ]` Ensure virtual environment `.venv` contains only the packages specified in `requirements.txt`.
- `[ ]` Run the automated test suite `python test_core.py` and verify all 14 tests pass successfully.
- `[ ]` Verify that no dead prototypes (`test.py`, `autotyper.py`) or obsolete configurations exist in the workspace.

---

## 💻 Phase 2: Manual Quality Assurance (QA)

### 1. Startup & Splash Screen
- `[ ]` Launch the application and verify that the splash screen appears for 1.5 seconds.
- `[ ]` Confirm the application main window renders with correct Dark or Light stylesheets and rounded corners.
- `[ ]` Verify that a first-launch welcome dialog appears when launching the app with no pre-existing configuration.

### 2. File Loading & Formatting
- `[ ]` Drag and drop a `.txt` file onto the editor and confirm it loads successfully.
- `[ ]` Load a `.docx` file using the "Browse..." menu action and verify spacing and paragraphs are maintained.
- `[ ]` Drag and drop an unsupported file format (like `.exe` or `.bin`) and confirm that a warning appears and the app does not crash.
- `[ ]` Check that the character stats label dynamically updates with correct Character, Word, and Line counts.

### 3. Simulation & Interruption
- `[ ]` Load a sample text, set typing speed to 60 WPM, and click "Start Typing".
- `[ ]` Confirm that a countdown ticker appears and locks UI inputs.
- `[ ]` Focus a target window (e.g. Notepad) and verify character typing starts after the countdown.
- `[ ]` Test typing simulation in both "Normal" and "Human" modes. Verify human mode pauses after periods and commas.
- `[ ]` Press the **`ESC`** key during active typing and verify that execution halts immediately.

### 4. Exit Safety Confirmations
- `[ ]` Click the Close button while typing is active and confirm that a confirmation dialog appears.
- `[ ]` Confirm that closing the application with text in the editor prompts the exit warning.
- `[ ]` Verify that `autosave.txt` is successfully cleared from the directory on a clean exit.

---

## 📦 Phase 3: Compilation & Packaging
- `[ ]` Run PyInstaller compilation using `pyinstaller autotyper.spec`.
- `[ ]` Double-click the compiled `dist/autotyper.exe` binary and verify it launches.
- `[ ]` Right-click `dist/autotyper.exe` -> select Properties -> verify File Version metadata matches `1.0.0.0` and Company metadata matches "The IoT Labs".
