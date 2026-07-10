from pathlib import Path

from backend.json_storage import JsonStorage
from backend.session_tracker import SessionTracker
from frontend.terminal_ui import TerminalUI


def get_sessions_file_path():
    project_folder = Path(__file__).resolve().parent
    return project_folder / "data" / "sessions.json"


if __name__ == "__main__":
    session_file = get_sessions_file_path()

    storage = JsonStorage(session_file)
    tracker = SessionTracker()

    loaded_coding_sessions = storage.load_sessions()
    tracker.set_sessions(loaded_coding_sessions)

    ui = TerminalUI(tracker, storage)
    ui.run()
