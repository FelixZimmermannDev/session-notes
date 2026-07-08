from backend.coding_session import CodingSession
#Verwaltung mehrerer Sessions

class SessionTracker:

    def __init__(self):
        self.sessions = []

    #Add Session
    def add_session(self, session):
        self.sessions.append(session)

    #Zugriff auf Liste
    def get_sessions(self):
        return self.sessions

    #For Each Day
    def get_session_by_date(self, date):
        for session in self.sessions:
            if session.get_date() == date:
                return session

        return None

    def has_session_for_date(self, date):
        return self.get_session_by_date(date) is not None

    def get_or_create_session(self, date):
        session = self.get_session_by_date(date)

        if session is None:
            session = CodingSession(date)
            self.add_session(session)

        return session
