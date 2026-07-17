import time
import logging
import sys
import ctypes
from ctypes import wintypes
import pyautogui
from PySide6.QtCore import QThread, Signal
from pynput import keyboard
from core.delay_engine import DelayEngine

# Windows-specific API definitions for native character typing
IS_WINDOWS = sys.platform == "win32"

if IS_WINDOWS:
    class KEYBDINPUT(ctypes.Structure):
        _fields_ = [
            ("wVk", wintypes.WORD),
            ("wScan", wintypes.WORD),
            ("dwFlags", wintypes.DWORD),
            ("time", wintypes.DWORD),
            ("dwExtraInfo", ctypes.c_size_t),
        ]

    class INPUT_UNION(ctypes.Union):
        _fields_ = [("ki", KEYBDINPUT)]

    class INPUT(ctypes.Structure):
        _fields_ = [
            ("type", wintypes.DWORD),
            ("ii", INPUT_UNION),
        ]

    INPUT_KEYBOARD = 1
    KEYEVENTF_UNICODE = 0x0004
    KEYEVENTF_KEYUP = 0x0002

    def send_unicode_char(char: str) -> bool:
        """Types a character using Windows SendInput API with KEYEVENTF_UNICODE."""
        try:
            codepoint = ord(char)
            # 1. Key Down Event
            input_down = INPUT()
            input_down.type = INPUT_KEYBOARD
            input_down.ii.ki.wVk = 0
            input_down.ii.ki.wScan = codepoint
            input_down.ii.ki.dwFlags = KEYEVENTF_UNICODE
            input_down.ii.ki.time = 0
            input_down.ii.ki.dwExtraInfo = 0

            # 2. Key Up Event
            input_up = INPUT()
            input_up.type = INPUT_KEYBOARD
            input_up.ii.ki.wVk = 0
            input_up.ii.ki.wScan = codepoint
            input_up.ii.ki.dwFlags = KEYEVENTF_UNICODE | KEYEVENTF_KEYUP
            input_up.ii.ki.time = 0
            input_up.ii.ki.dwExtraInfo = 0

            # Array of INPUT structures
            input_array = (INPUT * 2)(input_down, input_up)
            
            # Send events
            result = ctypes.windll.user32.SendInput(2, ctypes.byref(input_array), ctypes.sizeof(INPUT))
            return result > 0
        except Exception:
            return False
else:
    def send_unicode_char(char: str) -> bool:
        return False

# Disable PyAutoGUI's default pause to allow precise custom character delays
pyautogui.PAUSE = 0.0
# Enable PyAutoGUI fail-safe (moving mouse to corners aborts typing)
pyautogui.FAILSAFE = True

logger = logging.getLogger(__name__)

class TypingWorker(QThread):
    """
    Background worker thread that handles the typing simulation.
    Uses native Windows SendInput API (with PyAutoGUI fallback for tabs/enters)
    for layout-independent typing, and listens globally for the ESC key to stop.
    """
    status_changed = Signal(str)      # Emits status texts (e.g. "Countdown", "Typing", "Completed", etc.)
    progress_changed = Signal(int, int, int) # Emits (current_char_index, total_chars, remaining_seconds)
    countdown_tick = Signal(int)      # Emits remaining seconds during startup countdown
    finished = Signal(bool, str)      # Emits (success_status, message)

    def __init__(
        self,
        text: str,
        wpm: int,
        mode: str,
        random_enabled: bool,
        min_delay_ms: int,
        max_delay_ms: int,
        punctuation_pause: float = 0.3,
        line_break_pause: float = 0.5,
        countdown_sec: int = 5
    ):
        super().__init__()
        self.text = text
        self.wpm = wpm
        self.mode = mode
        self.random_enabled = random_enabled
        self.min_delay_ms = min_delay_ms
        self.max_delay_ms = max_delay_ms
        self.punctuation_pause = punctuation_pause
        self.line_break_pause = line_break_pause
        self.countdown_sec = countdown_sec
        
        self._is_running = True
        self._listener = None

    def run(self) -> None:
        """Main thread loop."""
        logger.info("Typing thread started.")
        self.status_changed.emit("Countdown")

        # 1. Start global ESC key listener
        self._start_esc_listener()

        try:
            # 2. Countdown phase
            for remaining in range(self.countdown_sec, 0, -1):
                if not self._is_running:
                    logger.info("Typing cancelled during countdown.")
                    self.status_changed.emit("Stopped")
                    self.finished.emit(False, "Typing cancelled during countdown.")
                    return
                self.countdown_tick.emit(remaining)
                time.sleep(1)

            if not self._is_running:
                logger.info("Typing cancelled.")
                self.status_changed.emit("Stopped")
                self.finished.emit(False, "Typing cancelled.")
                return

            # 3. Typing phase
            self.status_changed.emit("Typing")
            total_chars = len(self.text)
            
            for idx, char in enumerate(self.text):
                if not self._is_running:
                    logger.info("Typing stopped by user.")
                    self.status_changed.emit("Stopped")
                    self.finished.emit(False, "Typing stopped by user.")
                    return

                # Calculate specific delay for this character
                delay = DelayEngine.get_delay(
                    char=char,
                    wpm=self.wpm,
                    mode=self.mode,
                    random_enabled=self.random_enabled,
                    min_delay_ms=self.min_delay_ms,
                    max_delay_ms=self.max_delay_ms,
                    punctuation_pause=self.punctuation_pause,
                    line_break_pause=self.line_break_pause
                )
                
                # Dynamic sleeping
                if delay > 0:
                    time.sleep(delay)

                # Safe keystroke execution
                if char == '\n':
                    pyautogui.press('enter')
                elif char == '\t':
                    pyautogui.press('tab')
                else:
                    # Attempt Windows SendInput first for layout-independent Unicode typing
                    if not send_unicode_char(char):
                        pyautogui.typewrite(char)

                remaining_chars = total_chars - (idx + 1)
                remaining_sec = int((12 * remaining_chars) / self.wpm) if self.wpm > 0 else 0
                self.progress_changed.emit(idx + 1, total_chars, remaining_sec)

            # 4. Completion
            logger.info("Typing completed successfully.")
            self.status_changed.emit("Completed")
            self.finished.emit(True, "Typing completed successfully!")

        except pyautogui.FailSafeException:
            logger.warning("PyAutoGUI fail-safe triggered by mouse movement.")
            self.status_changed.emit("Stopped")
            self.finished.emit(False, "Interrupted: Mouse moved to a screen corner.")
        except Exception as e:
            logger.error(f"Error in typing process: {e}")
            self.status_changed.emit("Error")
            self.finished.emit(False, f"Error: {str(e)}")
        finally:
            self._stop_esc_listener()
            logger.info("Typing thread finished.")

    def stop(self) -> None:
        """Cancels the typing operation."""
        self._is_running = False

    def _start_esc_listener(self) -> None:
        """Starts the global key listener for the ESC emergency stop key."""
        last_esc_time = [0.0]
        
        def on_press(key):
            if key == keyboard.Key.esc:
                current_time = time.time()
                if current_time - last_esc_time[0] <= 1.0:
                    logger.info("Double ESC key detected. Triggering emergency stop.")
                    self.stop()
                    return False  # Stops the keyboard listener thread
                else:
                    logger.debug("First ESC key detected. Waiting for second press...")
                    last_esc_time[0] = current_time

        try:
            self._listener = keyboard.Listener(on_press=on_press)
            self._listener.start()
            logger.info("Global ESC listener started.")
        except Exception as e:
            logger.error(f"Failed to start global ESC keyboard listener: {e}")

    def _stop_esc_listener(self) -> None:
        """Stops the global key listener thread safely."""
        if self._listener:
            try:
                self._listener.stop()
            except Exception as e:
                logger.debug(f"Error stopping key listener: {e}")
            self._listener = None
            logger.info("Global ESC listener stopped.")
