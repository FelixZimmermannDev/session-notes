from datetime import date

class EmptyNoteError(ValueError):
    def __init__(self):
        super().__init__("Please enter a session note")


class InvalidDateError(ValueError):
    def __init__(self):
        super().__init__("Please enter a valid date in YYYY-MM-DD format")


class FutureDateError(ValueError):
    def __init__(self):
        super().__init__("Please enter today's date or an earlier date")


class CodingSession:

    # INITIALIZATION
    def __init__(self, session_number, date, note, is_archived=False):
        self._session_number = session_number
        self._date = self._clean_date(date)
        self._note = self._clean_note(note)
        self._is_archived = is_archived

    # NOTE
    def get_note(self):
        return self._note

    def update_note(self, new_note):
        self._note = self._clean_note(new_note)

    def _clean_note(self, note):
        if note is None:
            raise EmptyNoteError()

        cleaned_note = note.strip()

        if not cleaned_note:
            raise EmptyNoteError()

        return cleaned_note

    # SESSION NUMBER
    def get_session_number(self):
        return self._session_number

    # DATE
    def get_date(self):
        return self._date

    @staticmethod
    def _clean_date(date_value):
        if not isinstance(date_value, str):
            raise InvalidDateError()

        cleaned_date = date_value.strip()

        try:
            parsed_date = date.fromisoformat(cleaned_date)
        except ValueError:
            raise InvalidDateError() from None

        if parsed_date.isoformat() != cleaned_date:
            raise InvalidDateError()

        if parsed_date > date.today():
            raise FutureDateError()

        return cleaned_date

    # ARCHIVE
    def archive(self):
        self._is_archived = True

    def is_archived(self):
        return self._is_archived

    # SERIALIZATION
    def to_dict(self):
        return {
            "session_number": self._session_number,
            "date": self._date,
            "note": self._note,
            "is_archived": self._is_archived
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["session_number"],
            data["date"],
            data["note"],
            data.get("is_archived", False)
        )
