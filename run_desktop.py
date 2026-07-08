import sys

from PySide6.QtWidgets import QApplication

from frontend.desktop_ui import DesktopUI


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    ui = DesktopUI()
    ui.run()

    sys.exit(app.exec())
