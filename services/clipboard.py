from PySide6.QtGui import QGuiApplication

class ClipboardService:
    """Helper service to interface with the system clipboard using PySide6."""

    @staticmethod
    def get_text() -> str:
        """Retrieves plain text from the system clipboard."""
        clipboard = QGuiApplication.clipboard()
        return clipboard.text()

    @staticmethod
    def set_text(text: str) -> None:
        """Copies plain text to the system clipboard."""
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(text)

    @staticmethod
    def clear() -> None:
        """Clears the system clipboard."""
        clipboard = QGuiApplication.clipboard()
        clipboard.clear()
