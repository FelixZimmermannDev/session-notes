import pytest

from backend.coding_session import CodingSession


def test_create_coding_session():
    session = CodingSession(1, "2026-07-08", "OOP gelernt")

    assert session.get_session_number() == 1
    assert session.get_date() == "2026-07-08"
    assert session.get_note() == "OOP gelernt"


def test_note_is_stripped_on_create():
    session = CodingSession(1, "2026-07-08", "  OOP gelernt  ")

    assert session.get_note() == "OOP gelernt"


def test_empty_note_is_not_allowed():
    with pytest.raises(ValueError):
        CodingSession(1, "2026-07-08", "")


def test_whitespace_note_is_not_allowed():
    with pytest.raises(ValueError):
        CodingSession(1, "2026-07-08", "     ")


def test_update_note():
    session = CodingSession(1, "2026-07-08", "OOP gelernt")

    session.update_note("JSON gelernt")

    assert session.get_note() == "JSON gelernt"


def test_updated_note_is_stripped():
    session = CodingSession(1, "2026-07-08", "OOP gelernt")

    session.update_note("  JSON gelernt  ")

    assert session.get_note() == "JSON gelernt"


def test_update_note_cannot_be_empty():
    session = CodingSession(1, "2026-07-08", "OOP gelernt")

    with pytest.raises(ValueError):
        session.update_note("")