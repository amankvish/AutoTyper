# Developer Guide - AutoTyper

Welcome to the AutoTyper Developer Guide. This document provides setup guidelines and design standards to help you contribute to the project.

---

## 🛠️ Environment Setup

1. **Python Versions**: We support Python 3.12+ on Windows.
2. **Virtual Environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. **Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔬 Core Components Reference

### 1. The Typing Engine (`core/typing_engine.py`)
The `TypingWorker` runs as a `QThread` to keep the main GUI event loop responsive.
* Keystrokes are triggered using a `ctypes`-wrapped Win32 `SendInput` dispatcher (`KEYEVENTF_UNICODE`). This allows typing characters independent of active keyboard layouts.
* Backspaces, tabs, and returns are sent using virtual key codes to interact correctly with target systems.
* A background listener (`pynput.keyboard.Listener`) intercepts global key presses. It calls `worker.stop()` immediately if the user presses `ESC`.

### 2. Speed Delay Models (`core/delay_engine.py`)
* Computes character delays ($12 / \text{WPM}$).
* Introduces natural human rhythms (80%–120% variation) and punctuation delays.

---

## 🧪 Testing Guidelines

All unit and integration tests are written in **`test_core.py`**.
* Execute the test suite using:
  ```bash
  python test_core.py
  ```
* When adding features, write corresponding tests in `test_core.py`.
* Ensure that no formatting, typing, or configuration recovery tests fail before submitting pull requests.

---

## 🎨 Stylesheets & Visual Guidelines

AutoTyper features a rounded, premium visual layout styled after the Windows 11 Fluent UI.
* Themes (Dark and Light) are declared as QSS (Qt Style Sheets) inside `config.py`.
* Do not apply hardcoded inline stylesheets directly on widgets; use selectors inside `config.py` to maintain style consistency.
* Margin and padding sizes should use `8px`/`12px`/`16px` boundaries.
