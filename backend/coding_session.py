class CodingSession:

    def __init__(self, session_number, date, note):
        self.session_number = session_number
        self.date = date
        self.note = self._clean_note(note)

    #Note
    def update_note(self, note):
        self.note = self._clean_note(note)

    def _clean_note(self, note):
        if not note or not note.strip():
            raise ValueError("Session note cannot be empty.")

        return note.strip()

    def get_note(self):
        return self.note

    #Session Number
    def get_session_number(self):
        return self.session_number

    #Date
    def get_date(self):
        return self.date

    #JSON
    def to_dict(self):
        return {
            "session_number": self.session_number,
            "date": self.date,
            "note": self.note
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["session_number"],
            data["date"],
            data["note"]
        )
    