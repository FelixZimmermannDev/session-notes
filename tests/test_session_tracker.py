from datetime import date

from backend.session_tracker import SessionTracker
from backend.coding_session import CodingSession

def test_tracker_starts_with_empty_session_list():
    tracker = SessionTracker()

    assert tracker.get_sessions() == []


def test_add_session_creates_numbered_session_for_today():
    tracker = SessionTracker()

    session = tracker.add_session("Worked on backend")

    assert session.get_session_number() == 1
    assert session.get_date() == date.today().isoformat()
    assert session.get_note() == "Worked on backend"
    assert tracker.get_sessions() == [session]


def test_add_session_increments_session_numbers():
    tracker = SessionTracker()

    first_session = tracker.add_session("First note")
    second_session = tracker.add_session("Second note")

    assert first_session.get_session_number() == 1
    assert second_session.get_session_number() == 2
    assert tracker.get_sessions() == [first_session, second_session]


def test_get_session_by_number_returns_matching_session():
    tracker = SessionTracker()
    session = tracker.add_session("Find me")

    result = tracker.get_session_by_number(1)

    assert result is session


def test_get_session_by_number_returns_none_when_missing():
    tracker = SessionTracker()

    assert tracker.get_session_by_number(99) is None


def test_get_sessions_by_date_returns_matching_sessions():
    tracker = SessionTracker()
    first_session = tracker.add_session("First today")
    second_session = tracker.add_session("Second today")

    result = tracker.get_sessions_by_date(date.today().isoformat())

    assert result == [first_session, second_session]


def test_get_sessions_by_date_returns_empty_list_when_missing():
    tracker = SessionTracker()

    assert tracker.get_sessions_by_date("1999-01-01") == []

def test_set_sessions_sets_loaded_sessions():
    tracker = SessionTracker()

    loaded_session = CodingSession(
        5,
        "2026-07-08",
        "Loaded session"
    )

    tracker.set_sessions([loaded_session])

    assert tracker.get_sessions() == [loaded_session]


def test_set_sessions_replaces_existing_sessions():
    tracker = SessionTracker()
    tracker.add_session("Existing session")
    loaded_session = CodingSession(5, "2026-07-08", "Loaded session")

    tracker.set_sessions([loaded_session])

    assert tracker.get_sessions() == [loaded_session]


def test_add_session_uses_highest_existing_session_number():
    tracker = SessionTracker()
    loaded_sessions = [
        CodingSession(5, "2026-07-08", "Higher numbered session"),
        CodingSession(2, "2026-07-07", "Lower numbered session"),
    ]
    tracker.set_sessions(loaded_sessions)

    new_session = tracker.add_session("New session")

    assert new_session.get_session_number() == 6

def test_get_sessions_by_note_returns_matching_sessions():
    tracker = SessionTracker()
    matching_session = tracker.add_session("Worked on backend")
    tracker.add_session("Learned JSON")

    result = tracker.get_sessions_by_note("backend")

    assert result == [matching_session]


def test_get_sessions_by_note_is_case_insensitive():
    tracker = SessionTracker()
    session = tracker.add_session("OOP gelernt")

    result = tracker.get_sessions_by_note("oop")

    assert result == [session]


def test_get_sessions_by_note_returns_empty_list_when_missing():
    tracker = SessionTracker()
    tracker.add_session("Worked on backend")

    result = tracker.get_sessions_by_note("desktop")

    assert result == []


def test_get_sessions_by_note_returns_empty_list_for_blank_keyword():
    tracker = SessionTracker()
    tracker.add_session("Worked on backend")

    result = tracker.get_sessions_by_note("   ")

    assert result == []
