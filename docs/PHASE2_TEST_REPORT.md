# Phase 2 (v1.1) Test Report

This report outlines the automated unit tests and manual verifications for the Phase 2 (v1.1) Quality of Life update.

---

## 📊 Summary of Test Execution
* **Test Date**: 2026-07-16
* **Environment**: Windows 11, Python 3.12+ (activated `.venv`)
* **Test Tool**: `pytest`
* **Status**: **PASS (100% Successful)**
* **Total Automated Tests Executed**: 14
* **Total Failures / Errors**: 0

---

## 🧪 Phase 2 Verification Checks

### Removed Constraints Validated
- Verified `settings_page` index is fully removed; no orphaned memory references.
- Verified `Ctrl+D` and `Ctrl+L` do not duplicate/delete lines (Power-user limits respected).
- Verified Export/Import configs are fully disabled.
- Verified Toasts do not spam on Copy/Paste/Clear operations.

### New Additions Validated
- **Preferences Dialog**: Spawns correctly as a modal `QDialog`. Settings reset successfully writes defaults to `config.json`.
- **Open Folder**: The "Open Containing Folder" action natively executes Explorer on Windows.
- **Typing Profiles**: Adjusting custom WPM/Delay seamlessly detaches from built-in presets and displays "Custom (Unsaved)".
- **File Validation**: Recent Files dynamically prunes paths that have been deleted externally upon dropdown render.
