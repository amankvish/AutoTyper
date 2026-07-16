# Installer & Distribution Guide

This document describes how to distribute the compiled **AutoTyper** application to Windows users.

---

## 📦 1. Standalone Executable Distribution

Because AutoTyper is compiled as a single-file executable (`onefile` mode in PyInstaller), you can distribute the standalone `autotyper.exe` binary directly to end-users.

### Distribution Package Files:
```text
AutoTyper_v1.0.0/
├── autotyper.exe           # The compiled standalone executable
└── LICENSE                 # MIT License details
```

---

## 🛠️ 2. Creating a Windows Installer (Optional)

If you prefer to provide users with a standard Windows Setup Wizard (`Setup.exe` with desktop icons, registry keys, and uninstaller programs), you can package the compiled `autotyper.exe` using third-party installer packages like **Inno Setup** or **NSIS**.

### Using Inno Setup:
1. Download and install [Inno Setup Compiler](https://jrsoftware.org/isinfo.php).
2. Create a new Inno Setup script (`.iss`) mapping the source file to your compiled `dist/autotyper.exe`.
3. Configure the setup to:
   * Copy the executable to `{autopf}\The IoT Labs\AutoTyper`.
   * Create a desktop and start menu shortcut pointing to `autotyper.exe`.
   * Include the application icon (`autotyper_icon.ico`) for the installer package.
4. Compile the script to generate `AutoTyper_Setup.exe`.

---

## 🛡️ 3. Handling Windows SmartScreen Warnings

When compiling a standalone `.exe` using PyInstaller, Windows SmartScreen may flag the executable as an "Unknown Publisher" upon first download or run.

### Why this happens:
Windows requires executable binaries to be signed with a trusted digital certificate (Code Signing Certificate) to verify the publisher's identity.

### How to resolve:
1. **Self-Signing / Code Signing Certificate**: Purchase a standard OV/EV Code Signing Certificate from standard authorities (like SSL.com, Sectigo, or DigiCert) and sign the binary using `signtool.exe`:
   ```bash
   signtool sign /tr http://timestamp.digicert.com /td sha256 /fd sha256 /a dist/autotyper.exe
   ```
2. **User Workaround**: Instruct users to click "More Info" -> "Run Anyway" when Windows SmartScreen presents the default block dialog. As the binary accumulates downloads and positive reputation, SmartScreen warnings will disappear automatically.
