from backend.coding_session import EmptyNoteError
from backend.session_tracker import SessionTracker


class TerminalUI:

    def __init__(self, session_tracker: SessionTracker, storage):
        self.session_tracker = session_tracker
        self.storage = storage

    def run(self):
        print("1 - Add session")
        print("2 - Search sessions")
        print("3 - Update session note")
        print("4 - Archive session")

        option = input("Enter option: ")

        if option == "1":
            self.add_session()
        elif option == "2":
            self.search_menu()
        elif option == "3":
            self.handle_update_session()
        elif option == "4":
            self.handle_archive_session()
        else:
            print("Invalid option")

    #ADD SESSION
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

    #MENU
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

    #SEARCH
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

    #SHOW
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

    #UPDATE
    def handle_update_session(self):
        try:
            session_number = int(
                input("Enter session number: ")
            )
        except ValueError:
            print("Invalid session number")
            return
        session = self.session_tracker.get_session_by_number(
            session_number
        )

        if session is None:
            print("Session not found")
            return

        print("Current session:")
        self.show_session(session)

        new_note = input("Enter new note: ")

        try:
            session = self.session_tracker.update_session_note(
                session_number,
                new_note
            )
        except EmptyNoteError:
            print("Please enter a session note")
            return

        if session is None:
            print("Session not found")
            return

        self.storage.save_sessions(
            self.session_tracker.get_sessions()
        )

        print("Session updated")
        self.show_session(session)

    def handle_archive_session(self):
        try:
            session_number = int(
                input("Enter session number: ")
            )
        except ValueError:
            print("Invalid session number")
            return

        session = self.session_tracker.get_session_by_number(
            session_number
        )

        if session is None:
            print("Session not found")
            return

        print("Selected session:")
        self.show_session(session)

        confirmation = input(
            "Archive this session? (y/n): "
        ).strip().lower()

        if confirmation != "y":
            print("Archive cancelled")
            return

        archived_session = self.session_tracker.archive_session(
            session_number
        )

        self.storage.save_sessions(
            self.session_tracker.get_sessions()
        )

        print("Session archived")
        self.show_session(archived_session)
