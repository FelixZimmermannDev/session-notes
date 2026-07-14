from datetime import date
import pytest
from backend.coding_session import EmptyNoteError

from backend.session_tracker import SessionTracker
from backend.coding_session import CodingSession

def test_tracker_starts_with_empty_session_list():
    tracker = SessionTracker()

    assert tracker.get_sessions() == []


def test_get_next_session_number_returns_one_when_empty():
    tracker = SessionTracker()

    assert tracker.get_next_session_number() == 1


def test_get_next_session_number_uses_highest_existing_number():
    tracker = SessionTracker()
    tracker.set_sessions([
        CodingSession(1, "2026-07-08", "First session"),
        CodingSession(2, "2026-07-09", "Second session"),
        CodingSession(5, "2026-07-10", "Fifth session"),
    ])

    assert tracker.get_next_session_number() == 6


def test_get_next_session_number_does_not_modify_sessions():
    tracker = SessionTracker()
    tracker.set_sessions([
        CodingSession(1, "2026-07-08", "First session"),
        CodingSession(2, "2026-07-09", "Second session"),
        CodingSession(5, "2026-07-10", "Fifth session"),
    ])
    sessions_before = list(tracker.get_sessions())

    tracker.get_next_session_number()

    assert tracker.get_sessions() == sessions_before


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

def test_update_session_note_changes_existing_session():
    tracker = SessionTracker()
    session = tracker.add_session("Old note")

    result = tracker.update_session_note(
        session.get_session_number(),
        "New note"
    )

    assert result is session
    assert session.get_note() == "New note"

def test_update_session_note_changes_session_inside_tracker():
    tracker = SessionTracker()
    tracker.add_session("Old note")

    tracker.update_session_note(1, "New note")

    stored_session = tracker.get_session_by_number(1)

    assert stored_session.get_note() == "New note"

def test_update_session_note_returns_none_when_session_is_missing():
    tracker = SessionTracker()

    result = tracker.update_session_note(
        99,
        "New note"
    )

    assert result is None

def test_update_session_note_does_not_modify_sessions_when_session_is_missing():
    tracker = SessionTracker()
    first_session = tracker.add_session("First note")
    second_session = tracker.add_session("Second note")
    sessions_before_update = list(tracker.get_sessions())

    result = tracker.update_session_note(99, "New note")

    assert result is None
    assert tracker.get_sessions() == sessions_before_update
    assert first_session.get_note() == "First note"
    assert second_session.get_note() == "Second note"


def test_update_session_note_rejects_empty_note():
    tracker = SessionTracker()
    session = tracker.add_session("Old note")

    with pytest.raises(EmptyNoteError):
        tracker.update_session_note(1, "   ")

    assert session.get_note() == "Old note"


def test_archive_session_archives_and_returns_existing_session():
    tracker = SessionTracker()
    session = tracker.add_session("Archive me")

    result = tracker.archive_session(1)

    assert result is session
    assert session.is_archived() is True
    assert tracker.get_sessions() == [session]
    assert tracker.get_active_sessions() == []
    assert tracker.get_session_by_number(1) is None


def test_archive_session_returns_none_without_modifying_other_sessions():
    tracker = SessionTracker()
    session = tracker.add_session("Keep active")

    result = tracker.archive_session(99)

    assert result is None
    assert session.is_archived() is False
    assert tracker.get_active_sessions() == [session]


def test_searches_exclude_archived_sessions():
    tracker = SessionTracker()
    archived_session = CodingSession(1, "2026-07-08", "Backend work")
    active_session = CodingSession(2, "2026-07-08", "Backend tests")
    tracker.set_sessions([archived_session, active_session])
    tracker.archive_session(1)

    assert tracker.get_session_by_number(1) is None
    assert tracker.get_sessions_by_date("2026-07-08") == [active_session]
    assert tracker.get_sessions_by_note("backend") == [active_session]


def test_archived_session_cannot_be_updated():
    tracker = SessionTracker()
    session = tracker.add_session("Original note")
    tracker.archive_session(1)

    result = tracker.update_session_note(1, "New note")

    assert result is None
    assert session.get_note() == "Original note"
