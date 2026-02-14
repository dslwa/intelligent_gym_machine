import sys

from PyQt5.QtWidgets import QApplication

from config.logging_config import configure_logging
from src.gui.main_window import MainWindow
from src.gui.styles import create_app_font, create_dark_palette, APP_STYLESHEET
from src.services.fis_service import FISService


def main():
    configure_logging()
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setPalette(create_dark_palette())
    app.setFont(create_app_font())
    app.setStyleSheet(APP_STYLESHEET)

    window = MainWindow(FISService())
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
