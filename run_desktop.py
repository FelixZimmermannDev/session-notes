import sys

from PySide6.QtWidgets import QApplication

from backend.json_storage import JsonStorage
from backend.session_tracker import SessionTracker
from frontend.desktop_ui import DesktopUI


if __name__ == "__main__":
    storage = JsonStorage("data/sessions.json")
    tracker = SessionTracker()
    tracker.set_sessions(storage.load_sessions())

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    ui = DesktopUI(tracker, storage)
    ui.run()

    sys.exit(app.exec())

