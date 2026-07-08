from backend.session_tracker import SessionTracker


class TerminalUI:

    def __init__(self, session_tracker: SessionTracker):
        self.session_tracker = session_tracker

    def run(self):
        note = input("Session note: ")

        try:
            session = self.session_tracker.add_session(note)
            self.show_saved_session(session)

        except ValueError as error:
            print(f"Error: {error}")

    def show_saved_session(self, session):
        print()
        print(f"Saved Session {session.get_session_number()}")
        print(f"Date: {session.get_date()}")
        print(f"Note: {session.get_note()}")
