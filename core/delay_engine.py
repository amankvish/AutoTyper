import random
from config import HUMAN_PAUSE_PUNCTUATION, HUMAN_PAUSE_ENTER

class DelayEngine:
    """Calculates characters delays depending on typing speed, mode, and random variation settings."""

    @staticmethod
    def calculate_base_delay(wpm: int) -> float:
        """
        Calculates character delay in seconds for a target WPM.
        A standard 'word' in typing speed measurement is 5 characters (including spaces).
        Formula: 
            Characters per min = WPM * 5
            Characters per sec = (WPM * 5) / 60 = WPM / 12
            Delay per char = 1 / (WPM / 12) = 12 / WPM
        """
        if wpm <= 0:
            return 0.2  # Safeguard fallback to 60 WPM
        return 12.0 / wpm

    @classmethod
    def get_delay(
        cls,
        char: str,
        wpm: int,
        mode: str,  # "normal" or "human"
        random_enabled: bool,
        min_delay_ms: int,
        max_delay_ms: int
    ) -> float:
        """
        Computes the delay for the given character.
        
        Args:
            char: The character about to be typed.
            wpm: The current typing speed in WPM.
            mode: "normal" or "human".
            random_enabled: Whether user-defined random delays are enabled.
            min_delay_ms: User-defined minimum delay in milliseconds.
            max_delay_ms: User-defined maximum delay in milliseconds.
            
        Returns:
            Delay in seconds to sleep before typing this character.
        """
        delay = 0.0

        # 1. Base Character Delay
        if random_enabled:
            # User defined random delay range in milliseconds
            min_sec = max(0.0, min_delay_ms / 1000.0)
            max_sec = max(min_sec, max_delay_ms / 1000.0)
            delay = random.uniform(min_sec, max_sec)
        else:
            base = cls.calculate_base_delay(wpm)
            if mode == "human":
                # Add natural human fluctuation (80% to 120% of base speed)
                delay = random.uniform(base * 0.8, base * 1.2)
            else:
                delay = base

        # 2. Human Mode Extra Pauses
        if mode == "human":
            # Extra pause after punctuation
            if char in HUMAN_PAUSE_PUNCTUATION:
                delay += HUMAN_PAUSE_PUNCTUATION[char]
            # Extra pause after newlines
            elif char in ('\n', '\r'):
                delay += HUMAN_PAUSE_ENTER

        return max(0.0, delay)
