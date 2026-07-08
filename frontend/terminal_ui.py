from datetime import date

from backend.session_tracker import SessionTracker


class TerminalUI:

    def __init__(self, session_tracker: SessionTracker):
        self.session_tracker = session_tracker




    def run(self):
        today = date.today().isoformat()

        coded_answer = input("Did you code today? (y/n) ")
        note = input("Note: ")

        if coded_answer.lower() == "y":
            session = self.session_tracker.mark_day_coded(today)
        else:
            session = self.session_tracker.mark_day_not_coded(today)

        session = self.session_tracker.update_note_for_date(today, note)

        print("Saved session:")
        print(f"Date: {session.get_date()}")
        print(f"Status: {session.get_status().value}")
        print(f"Note: {session.get_note()}")
