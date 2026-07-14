import sys

from PySide6.QtWidgets import QApplication

from app_setup import create_tracker_and_storage
from frontend.desktop_ui import DesktopUI


def main():
    tracker, storage = create_tracker_and_storage()

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    ui = DesktopUI(tracker, storage)
    ui.run()

    return app.exec()


if __name__ == "__main__":
    main()
