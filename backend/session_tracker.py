from datetime import date

from backend.coding_session import CodingSession


class SessionTracker:
    def __init__(self):
        self.sessions = []

    def add_session(self, note):
        session_number = len(self.sessions) + 1
        today = date.today().isoformat()

        session = CodingSession(session_number, today, note)

        self.sessions.append(session)
        return session

    def get_sessions(self):
        return self.sessions

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
