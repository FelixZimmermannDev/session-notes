from pathlib import Path

from backend.json_storage import JsonStorage
from backend.session_tracker import SessionTracker


def get_sessions_file_path():
    project_folder = Path(__file__).resolve().parent
    return project_folder / "data" / "sessions.json"


def create_tracker_and_storage(session_file=None):
    if session_file is None:
        session_file = get_sessions_file_path()

    storage = JsonStorage(session_file)
    tracker = SessionTracker()
    tracker.set_sessions(storage.load_sessions())

    return tracker, storage
