import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from backend.json_storage import JsonStorage
from backend.session_tracker import SessionTracker
from frontend.desktop_ui import DesktopUI


def get_sessions_file_path():
    project_folder = Path(__file__).resolve().parent
    return project_folder / "data" / "sessions.json"


def main():
    session_file = get_sessions_file_path()

    storage = JsonStorage(session_file)

    tracker = SessionTracker()
    tracker.set_sessions(storage.load_sessions())

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    ui = DesktopUI(tracker, storage)
    ui.run()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

