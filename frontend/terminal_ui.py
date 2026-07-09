from backend.session_tracker import SessionTracker


class TerminalUI:

    def __init__(self, session_tracker: SessionTracker, storage):
        self.session_tracker = session_tracker
        self.storage = storage

    def run(self):
        note = input("Session note: ")

        try:
            session = self.session_tracker.add_session(note)
            self.storage.save_sessions(self.session_tracker.get_sessions())
            self.show_saved_session(session)

        except ValueError as error:
            print(f"Error: {error}")

    def show_saved_session(self, session):
        print()
        print(f"Saved Session {session.get_session_number()}")
        print(f"Date: {session.get_date()}")
        print(f"Note: {session.get_note()}")
