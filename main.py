from backend.json_storage import JsonStorage
from backend.session_tracker import SessionTracker
from frontend.terminal_ui import TerminalUI


if __name__ == "__main__":

    storage = JsonStorage("data/sessions.json")
    tracker = SessionTracker()

    loaded_coding_sessions = storage.load_sessions()

    tracker.set_sessions(loaded_coding_sessions)

    ui = TerminalUI(tracker, storage)
    ui.run()

