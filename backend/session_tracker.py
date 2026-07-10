from datetime import date

from backend.coding_session import CodingSession


class SessionTracker:

    def __init__(self):
        self.sessions = []

    #Add Session
    def add_session(self, note):
        highest_session_number = 0

        for session in self.sessions:
            if session.get_session_number() > highest_session_number:
                highest_session_number = session.get_session_number()

        session_number = highest_session_number + 1
        today = date.today().isoformat()

        session = CodingSession(session_number, today, note)

        self.sessions.append(session)

        return session

    def get_sessions(self):
        return self.sessions

    #Find Sessions
    def get_session_by_number(self, session_number):
        for session in self.sessions:
            if session.get_session_number() == session_number:
                return session

        return None

    def get_sessions_by_date(self, target_date):
        matching_sessions = []

        for session in self.sessions:
            if session.get_date() == target_date:
                matching_sessions.append(session)

        return matching_sessions

    def get_sessions_by_note(self, keyword):
        matching_sessions = []
        cleaned_keyword = keyword.lower().strip()

        if not cleaned_keyword:
            return []

        for session in self.sessions:
            note = session.get_note().lower()

            if cleaned_keyword in note:
                matching_sessions.append(session)

        return matching_sessions

    #JSON
    def set_sessions(self, sessions):
        self.sessions = sessions
