import sys
import os
import time
import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QPixmap
from app.main_window import MainWindow
from services.settings import SettingsService
import config

def setup_logging() -> None:
    """Configures application-wide logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def main() -> None:
    """Main application entry point."""
    # 1. Initialize logging
    setup_logging()
    logger = logging.getLogger("AutoTyper")
    logger.info("Initializing AutoTyper Application...")

    # 2. Create the Qt Application
    app = QApplication(sys.argv)
    app.setApplicationName("AutoTyper")
    app.setOrganizationName("The IoT Labs")

    # 3. Initialize Splash Screen
    splash_path = config.get_resource_path("autotyper_splash.png")
    splash = None
    if os.path.exists(splash_path):
        pixmap = QPixmap(splash_path)
        scaled_pixmap = pixmap.scaled(
            pixmap.width() // 2,
            pixmap.height() // 2,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        splash = QSplashScreen(scaled_pixmap)
        splash.show()
        app.processEvents()
        logger.info("Splash screen displayed.")

    # 4. Initialize Settings Service
    settings_service = SettingsService()

    # 5. Initialize MainWindow
    window = MainWindow(settings_service)

    # 6. Smoothly fade/finish splash screen
    if splash:
        start_time = time.time()
        # Keep splash for 1.5s, processing UI events to prevent freezes
        while time.time() - start_time < 1.5:
            app.processEvents()
            time.sleep(0.02)
        splash.finish(window)

    window.show()

    # 7. Execute Event Loop
    logger.info("AutoTyper UI visible. Running event loop...")
    exit_code = app.exec()
    logger.info(f"AutoTyper Application shutting down with code {exit_code}.")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
