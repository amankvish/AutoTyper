# Known Issues & Environmental Constraints

This document details known limitations and quirks of the **AutoTyper** desktop application on the Windows platform.

---

## 1. Destination Editor Auto-Indentation

### Symptom
When typing source code (such as Python, Java, or HTML) into advanced text editors or IDEs (like VS Code, PyCharm, or IntelliJ), lines may receive extra leading spaces or tabs, resulting in nested double-indentation.

### Cause
Many modern code editors have a "smart indent" or "auto-indent" feature enabled by default. When AutoTyper types a newline (`\n`), the target editor automatically indents the next line. When AutoTyper then types the original leading spaces/tabs from the source text, they are added to the auto-generated indent.

### Workaround
Before starting the typing sequence, temporarily disable **Auto Indent** in the target editor's settings. 
* *VS Code*: Set `"editor.autoIndent": "none"` in settings.
* *PyCharm / IntelliJ*: Disable "Smart indent" under Settings -> Editor -> General -> Smart Keys.

---

## 2. Windows Administrative Privileges

### Symptom
AutoTyper fails to type characters or trigger keystrokes when typing into specific application windows (such as Command Prompt, PowerShell, Task Manager, or programs run under Administrator mode).

### Cause
Windows User Account Control (UAC) security prevents standard, non-elevated applications from sending synthetic input events (like mouse clicks or keypresses) to elevated (Administrator) windows.

### Workaround
Right-click on the `autotyper.exe` (or your command prompt if running from source) and select **Run as Administrator** to grant AutoTyper the permissions required to send events to elevated target windows.

---

## 3. Remote Desktop Services (RDP) Safety Interruptions

### Symptom
When typing into a Remote Desktop or Virtual Machine window, the keyboard hook might fail to capture the `ESC` key, or PyAutoGUI might trigger its native fail-safe.

### Cause
UAC and Remote Desktop virtualization sometimes intercept global key hook mappings or cause artificial mouse coordinate shifts.

### Workaround
Run AutoTyper locally on the target machine inside the Remote Desktop window, or keep the focus active on the local machine when pressing `ESC`.
