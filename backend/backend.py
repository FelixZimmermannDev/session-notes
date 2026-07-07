#Ein Eintrag. Eine Session. Hat Date, coded, note

class CodingSession:

    def __init__(self, date):
        self.date = date
        self.coded = False
        self.note = ""

    def mark_coded(self):
        self.coded = True
        return self.coded

    def mark_not_coded(self):
        self.coded = False
        return self.coded

    def update_note(self, note):
        self.note = note

    def is_coded(self):
        return self.coded

    def get_date(self):
        return self.date
        #Muss man spaeter per Kalender oder dergleichen input holen und nicht per userinput

class SessionTracker:

    def __init__(self):
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)

    def get_sessions(self):
        return self.sessions

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

    def mark_day_coded(self, date):
        session = self.get_or_create_session(date)
        return session.mark_coded()

    def mark_day_not_coded(self, date):
        session = self.get_or_create_session(date)
        return session.mark_not_coded()

    def update_note_for_date(self, date, note):
        session = self.get_or_create_session(date)
        session.update_note(note)
        return session
