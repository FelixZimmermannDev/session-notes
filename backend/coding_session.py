from enum import Enum
class SessionStatus(Enum):
    UNSET = 'unset'
    CODED = 'coded'
    UNCODED = 'uncoded'


class CodingSession:

    def __init__(self, date):
        self.date = date
        self.status = SessionStatus.UNSET
        self.note = ''

    #Status feature
    def mark_coded(self):
        self.status = SessionStatus.CODED

    def mark_uncoded(self):
        self.status = SessionStatus.UNCODED

    def is_coded(self):
        return self.status == SessionStatus.CODED

    def is_uncoded(self):
        return self.status == SessionStatus.UNCODED

    def is_unset(self):
        return self.status == SessionStatus.UNSET

    #Note Feature
    def update_note(self, note):
        self.note = note

    #Read Methods
    def get_date(self):
        return self.date

    def get_status(self):
        return self.status

    def get_note(self):
        return self.note

