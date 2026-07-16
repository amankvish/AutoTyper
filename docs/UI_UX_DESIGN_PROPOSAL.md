# AutoTyper UI/UX Design Proposal

This document outlines the design philosophy, visual systems, and user experience patterns implemented in **AutoTyper v1.0.0**, designed by **The IoT Labs**.

---

## 🎨 1. Design System & Style Tokens

To fit natively on modern Windows 10 & 11 environments, AutoTyper adheres to the **Windows Fluent Design System**:

| Style Token | Dark Theme Value | Light Theme Value |
|---|---|---|
| **Background** | `#1c1c1e` (Fluent Base) | `#f5f5f7` (Fluent Base Light) |
| **Cards & Panels** | `#2c2c2e` | `#ffffff` |
| **Borders** | `1px solid #3a3a3c` | `1px solid #d1d1d6` |
| **Brand Accent** | `#0a84ff` (Windows Blue) | `#007aff` (iOS/Windows Royal Blue) |
| **Critical Stop** | `#ff3b30` (Alert Red) | `#ff3b30` (Alert Red Light) |
| **Fonts** | `'Segoe UI', -apple-system, sans-serif` | `'Segoe UI', -apple-system, sans-serif` |
| **Code Fonts** | `'Consolas', 'Courier New', monospace` | `'Consolas', 'Courier New', monospace` |
| **Corners** | `8px` rounded (Layout) / `6px` (Controls) | `8px` rounded (Layout) / `6px` (Controls) |

---

## 🚀 2. Application Flow & Interactive States

### Phase 1: Splash Screen Loading
* **Design**: 400x250 centered splash screen (`autotyper_splash.png`) containing a glowing cyan keyboard key with a sleek letter 'A' and a small lightning bolt.
* **UX**: Renders immediately on boot for 1.5 seconds while background settings are restored in the event loop, preventing visual lockups or Windows "Not Responding" alerts.

### Phase 2: Main Window & Workspace
* **Layout**: Uses vertical stack grids with clean `20px` margins to avoid cramped elements.
* **Editor**: Uses a monospaced font with a distinct `1px` border that transitions to `2px solid #0a84ff` on focus, providing clear input targeting.
* **Speed Card**: Houses sliders and simulation radios. Features dynamic total duration calculation labels (e.g. `60 WPM (Est: 2m 14s)`) next to the speed title.

### Phase 3: Active Simulation & Countdown
* **Action Buttons**: Big, highly clickable `Start Typing` and `Stop Typing` buttons (`44px` height).
* **Countdown Overlay**: A prominent ticking delay countdown (e.g. `Typing in 5s...`) next to the buttons.
* **Input Locking**: When started, all editing blocks, file load menus, and settings are disabled (`setEnabled(False)`) to prevent concurrent modification issues during execution. Only the "Stop Typing" button remains clickable.

### Phase 4: Clean Exit & Confirmation
* **Closing Prompt**: Double-checks with the user if there are active text files loaded or if typing is currently in progress, avoiding accidental data loss.

---

## 🏷️ 3. Footer Branding Integration

To maintain proper alignment and brand attribution, the footer includes a centered label containing a clickable link:
```text
AutoTyper by The IoT Labs (https://theiotlabs.in/)
```
* **Implementation**: Uses a clickable rich-text `QLabel` with `setOpenExternalLinks(True)`. Clicking the link redirects the user directly to the official homepage in their default web browser.
