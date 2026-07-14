from datetime import date

from backend.coding_session import CodingSession


class SessionTracker:

    def __init__(self):
        self.sessions = []

    #ADD SESSION
    def add_session(self, note):
        session_number = self.get_next_session_number()
        today = date.today().isoformat()

        session = CodingSession(session_number, today, note)
        self.sessions.append(session)

        return session

    #SESSION NUMBER
    def get_next_session_number(self):
        highest_session_number = 0

        for session in self.sessions:
            if session.get_session_number() > highest_session_number:
                highest_session_number = session.get_session_number()

        return highest_session_number + 1

    def get_sessions(self):
        return self.sessions

    #FIND SESSION
    def get_session_by_number(self, session_number):
        for session in self.sessions:
            if (
                session.get_session_number() == session_number
                and not session.is_archived()
            ):
                return session

        return None

    def get_sessions_by_date(self, target_date):
        matching_sessions = []

        for session in self.sessions:
            if session.is_archived():
                continue

            if session.get_date() == target_date:
                matching_sessions.append(session)

        return matching_sessions

    def get_sessions_by_note(self, keyword):
        matching_sessions = []
        cleaned_keyword = keyword.lower().strip()

        if not cleaned_keyword:
            return []

        for session in self.sessions:
            if session.is_archived():
                continue

            note = session.get_note().lower()

            if cleaned_keyword in note:
                matching_sessions.append(session)

        return matching_sessions

    #UPDATE SESSION
    def update_session_note(self, session_number, new_note):
        session = self.get_session_by_number(session_number)

        if session is None:
            return None

        session.update_note(new_note)

        return session

    #JSON
    def set_sessions(self, sessions):
        self.sessions = sessions

    #ARCHIVE
    def archive_session(self, session_number):
        session = self.get_session_by_number(session_number)

        if session is None:
            return None

        session.archive()

        return session

    def get_active_sessions(self):
        active_sessions = []

        for session in self.sessions:
            if not session.is_archived():
                active_sessions.append(session)

        return active_sessions
