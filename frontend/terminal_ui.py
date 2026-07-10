from backend.coding_session import EmptyNoteError
from backend.session_tracker import SessionTracker


class TerminalUI:

    def __init__(self, session_tracker: SessionTracker, storage):
        self.session_tracker = session_tracker
        self.storage = storage

    def run(self):
        print("1 - Add session")
        print("2 - Search sessions")

        option = input("Enter option: ")

        if option == "1":
            self.add_session()
        elif option == "2":
            self.search_menu()
        else:
            print("Invalid option")

    def add_session(self):
        note = input("Session note: ")

        try:
            session = self.session_tracker.add_session(note)
            self.storage.save_sessions(
                self.session_tracker.get_sessions()
            )
            self.show_saved_session(session)

        except EmptyNoteError:
            print("Please enter a session note")

    def search_menu(self):
        print("1 - Search by number")
        print("2 - Search by note")
        print("3 - Search by date")

        option = input("Enter option: ")

        if option == "1":
            try:
                number = int(input("Enter session number: "))
            except ValueError:
                print("Invalid session number")
                return
            self.search_session_by_number(number)

        elif option == "2":
            keyword = input("Enter note keyword: ")
            self.search_sessions_by_note(keyword)

        elif option == "3":
            target_date = input("Enter session date: ")
            self.search_sessions_by_date(target_date)

        else:
            print("Invalid option")

    def search_session_by_number(self, number):
        session = self.session_tracker.get_session_by_number(number)

        if session is None:
            print("Session not found")
            return

        self.show_session(session)

    def search_sessions_by_note(self, keyword):
        sessions = self.session_tracker.get_sessions_by_note(keyword)
        self.show_sessions(sessions)

    def search_sessions_by_date(self, target_date):
        sessions = self.session_tracker.get_sessions_by_date(target_date)
        self.show_sessions(sessions)

    def show_sessions(self, sessions):
        if not sessions:
            print("No sessions found")
            return

        for session in sessions:
            self.show_session(session)

    def show_saved_session(self, session):
        print()
        print(f"Saved Session {session.get_session_number()}")
        print(f"Date: {session.get_date()}")
        print(f"Note: {session.get_note()}")

    def show_session(self, session):
        print()
        print(f"Session {session.get_session_number()}")
        print(f"Date: {session.get_date()}")
        print(f"Note: {session.get_note()}")
