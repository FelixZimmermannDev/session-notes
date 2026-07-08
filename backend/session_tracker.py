from backend.coding_session import CodingSession


# Verwaltet alle Coding-Sessions.
# Sucht Sessions nach Datum und stellt Feature-Methoden für die UI bereit.
class SessionTracker:

    def __init__(self):
        self.sessions = []

    # Session collection
    def add_session(self, session):
        self.sessions.append(session)

    def get_sessions(self):
        return self.sessions

    # Daily session lookup
    def get_session_by_date(self, date):
        for session in self.sessions:
            if session.get_date() == date:
                return session

        return None

    def has_session_for_date(self, date):
        return self.get_session_by_date(date) is not None

    # Daily session creation
    def get_or_create_session(self, date):
        session = self.get_session_by_date(date)

        if session is None:
            session = CodingSession(date)
            self.add_session(session)

        return session

    # Daily status feature
    def mark_day_coded(self, date):
        session = self.get_or_create_session(date)
        session.mark_coded()
        return session

    def mark_day_not_coded(self, date):
        session = self.get_or_create_session(date)
        session.mark_uncoded()
        return session