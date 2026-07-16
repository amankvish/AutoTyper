# AutoTyper v1.1 Build Guide

## Overview
This guide details the steps required to compile the AutoTyper Python source code into a standalone `.exe` using PyInstaller.

## 1. Environment Setup
1. Ensure Python 3.12+ is installed on Windows.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: AutoTyper intentionally uses minimal dependencies. Primarily `PySide6`)*

## 2. Preparing Resources
Ensure the following files are present in the `resources/` folder before compiling:
- `autotyper_splash.png` (Used during boot)
- `autotyper_icon.ico` (Used for the executable and window title bar)

## 3. PyInstaller Compilation
We compile AutoTyper as a single, windowed executable (no console window).

Run the following command from the root project directory:
```bash
pyinstaller --noconfirm --onedir --windowed --icon "resources/autotyper_icon.ico" --add-data "resources;resources/"  "main.py"
```

## 4. Verification
1. Navigate to the generated `dist/main/` folder.
2. Double click `main.exe` (can be renamed to `AutoTyper.exe`).
3. Verify that the Splash Screen appears and the application boots in under 2 seconds.
4. Verify that `config.json` is generated successfully in the same directory upon closure.

## 5. Output Packaging
Zip the contents of the `dist/main` folder and distribute as `AutoTyper_v1.1_Portable.zip`.
