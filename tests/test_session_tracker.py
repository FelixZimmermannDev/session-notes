from backend.coding_session import CodingSession
from backend.session_tracker import SessionTracker


def test_tracker_starts_with_empty_session_list():
    tracker = SessionTracker()

    assert tracker.get_sessions() == []


def test_add_session_adds_session_to_list():
    tracker = SessionTracker()
    session = CodingSession("2026-07-08")

    tracker.add_session(session)

    assert tracker.get_sessions() == [session]


def test_get_session_by_date_returns_matching_session():
    tracker = SessionTracker()
    session = CodingSession("2026-07-08")
    tracker.add_session(session)

    result = tracker.get_session_by_date("2026-07-08")

    assert result is session


def test_get_session_by_date_returns_none_when_missing():
    tracker = SessionTracker()

    result = tracker.get_session_by_date("2026-07-08")

    assert result is None


def test_has_session_for_date_returns_true_when_session_exists():
    tracker = SessionTracker()
    session = CodingSession("2026-07-08")
    tracker.add_session(session)

    assert tracker.has_session_for_date("2026-07-08") is True


def test_has_session_for_date_returns_false_when_session_is_missing():
    tracker = SessionTracker()

    assert tracker.has_session_for_date("2026-07-08") is False


def test_get_or_create_session_creates_session_when_missing():
    tracker = SessionTracker()

    session = tracker.get_or_create_session("2026-07-08")

    assert session.get_date() == "2026-07-08"
    assert tracker.get_sessions() == [session]


def test_get_or_create_session_reuses_existing_session():
    tracker = SessionTracker()
    existing_session = CodingSession("2026-07-08")
    tracker.add_session(existing_session)

    session = tracker.get_or_create_session("2026-07-08")

    assert session is existing_session
    assert tracker.get_sessions() == [existing_session]
