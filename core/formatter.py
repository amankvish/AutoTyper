class TextFormatter:
    """Formats and sanitizes input text to ensure it is typed accurately."""

    @staticmethod
    def normalize_line_endings(text: str) -> str:
        """
        Normalizes line endings to '\n'.
        Prevents duplicate enters when typing text with Windows style '\r\n'.
        """
        if not text:
            return ""
        # Convert carriage returns + newlines to just newlines
        text = text.replace("\r\n", "\n")
        # Convert standalone carriage returns to newlines
        text = text.replace("\r", "\n")
        return text

    @staticmethod
    def format_for_typing(text: str) -> str:
        """
        Performs sanitization of the text for the typing simulation.
        Ensures exact spaces, tabs, and indentation structure are preserved.
        """
        # Right now, normalizing newlines is the core preparation step.
        return TextFormatter.normalize_line_endings(text)
