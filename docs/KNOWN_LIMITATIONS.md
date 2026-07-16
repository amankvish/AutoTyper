# AutoTyper v1.1 Known Limitations

While AutoTyper v1.1 is highly stable and optimized, the following environmental limitations exist by design or due to backend technical constraints:

## 1. Rich Text Formatting (RTE) Drop
AutoTyper is designed to transcribe raw text (Plain Text). While it can ingest `.docx` files, it will explicitly strip bold, italics, font colors, and embedded images, converting the document strictly into UTF-8 characters. It types raw strings, not clipboard objects.

## 2. Protected OS Windows
AutoTyper relies on the `Win32 SendInput` API. It cannot inject keystrokes into:
- UAC (User Account Control) Admin Prompts.
- Ctrl+Alt+Delete screens.
- Certain high-security DRM-protected games (e.g., Vanguard anti-cheat engines) that hook the keyboard driver at the kernel level.
- Sandboxed Windows Store Apps (UWP) under specific tight security constraints.

## 3. High WPM Thread Yielding
At extremely high Custom WPMs (e.g., >800 WPM) with Human Mode disabled, the typing thread operates so quickly that the Win32 message queue might struggle to dispatch `ESC` cancel events instantaneously. A delay of ~200ms might occur between pressing `ESC` and the thread finally yielding.

## 4. Mac / Linux Incompatibility
AutoTyper is strictly bound to Windows due to deep integration with the `ctypes.windll.user32.SendInput` architecture for Unicode payload delivery. There are no plans for Mac or Linux support in the Community Edition roadmap.
