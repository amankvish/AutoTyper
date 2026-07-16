# AutoTyper v1.1 - UI Polish Sprint Changelog

## Visual System Updates
* **Global Theme Integration**: Deployed `app/style.qss`, establishing a strict CSS-based Fluent Design theme. 
* **Typography Refactoring**: Replaced erratic inline fonts with native "Segoe UI Variable" and a strict hierarchy system.
* **Inline Styles Removed**: All `setStyleSheet` calls completely eradicated from Python logic files, isolating UI behavior from presentation.

## Layout Changes
* **Card Flattening**: Removed 1990s-style `QGroupBox` borders in favor of modern, slightly elevated card foundations.
* **Component Hierarchy**: Flattened the screen into a direct top-down flow: Toolbar -> Expanded CodeEditor -> Compact Typing Controls -> Status Bar. 

## Component Styling
* **Action Buttons**: Applied color coding to primary interactive elements (Start = Blue, Stop = Red) to establish an instant visual hierarchy.
* **Inputs & Combos**: Rounded corners (4px radius) mapped perfectly to Windows 11 Fluent guidelines. Included subtle focus rings (Blue).
* **Scrollbars**: Designed sleek, transparent scrollbars with auto-hiding properties for massive documents.
