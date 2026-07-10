import pytest

from backend.coding_session import CodingSession, EmptyNoteError


def test_create_coding_session():
    session = CodingSession(1, "2026-07-08", "OOP gelernt")

    assert session.get_session_number() == 1
    assert session.get_date() == "2026-07-08"
    assert session.get_note() == "OOP gelernt"


def test_note_is_stripped_on_create():
    session = CodingSession(1,
                            "2026-07-08",
                            "  OOP gelernt  ")

    assert session.get_note() == "OOP gelernt"


def test_empty_note_is_not_allowed():
    with pytest.raises(EmptyNoteError, match="Please enter a session note"):
        CodingSession(1, "2026-07-08", "")


def test_whitespace_note_is_not_allowed():
    with pytest.raises(EmptyNoteError):
        CodingSession(1, "2026-07-08", "     ")


def test_none_note_is_not_allowed():
    with pytest.raises(EmptyNoteError):
        CodingSession(1, "2026-07-08", None)

def test_to_dict_returns_session_data():

    session = CodingSession(1, "2026-07-08", "OOP gelernt")

    result = session.to_dict()

    assert result == {
        "session_number": 1,
        "date": "2026-07-08",
        "note": "OOP gelernt"
    }

def test_from_dict_creates_coding_session():
    data = {
        "session_number": 1,
        "date": "2026-07-08",
        "note": "OOP gelernt"
    }

    session = CodingSession.from_dict(data)

    assert isinstance(session, CodingSession)
    assert session.get_session_number() == 1
    assert session.get_date() == "2026-07-08"
    assert session.get_note() == "OOP gelernt"
