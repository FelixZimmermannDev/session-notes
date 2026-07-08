from backend.session_tracker import SessionTracker


class TerminalUI:
    def __init__(self):
        self.tracker = SessionTracker()

    def run(self):
        print("Coding Session Tracker")
