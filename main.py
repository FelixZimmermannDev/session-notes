from backend.session_tracker import SessionTracker
from frontend.terminal_ui import TerminalUI


if __name__ == "__main__":
    tracker = SessionTracker()
    ui = TerminalUI(tracker)
    ui.run()