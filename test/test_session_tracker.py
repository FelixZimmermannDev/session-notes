from backend.backend import CodingSession, SessionTracker


def test_get_or_create_session_creates_session_when_missing():
    tracker = SessionTracker()

    session = tracker.get_or_create_session("2026-07-07")

    assert session.get_date() == "2026-07-07"
    assert tracker.get_sessions() == [session]


def test_get_or_create_session_reuses_existing_session():
    tracker = SessionTracker()
    existing_session = CodingSession("2026-07-07")
    tracker.add_session(existing_session)

    session = tracker.get_or_create_session("2026-07-07")

    assert session is existing_session
    assert tracker.get_sessions() == [existing_session]


def test_mark_day_coded_creates_session_and_marks_coded():
    tracker = SessionTracker()

    tracker.mark_day_coded("2026-07-07")

    session = tracker.get_session_by_date("2026-07-07")
    assert session.is_coded() is True


def test_mark_day_coded_reuses_existing_session():
    tracker = SessionTracker()
    existing_session = CodingSession("2026-07-07")
    tracker.add_session(existing_session)

    tracker.mark_day_coded("2026-07-07")

    assert existing_session.is_coded() is True
    assert tracker.get_sessions() == [existing_session]


def test_mark_day_not_coded_creates_session_and_marks_not_coded():
    tracker = SessionTracker()

    tracker.mark_day_not_coded("2026-07-07")

    session = tracker.get_session_by_date("2026-07-07")
    assert session.is_coded() is False


def test_mark_day_not_coded_reuses_existing_session():
    tracker = SessionTracker()
    existing_session = CodingSession("2026-07-07")
    existing_session.mark_coded()
    tracker.add_session(existing_session)

    tracker.mark_day_not_coded("2026-07-07")

    assert existing_session.is_coded() is False
    assert tracker.get_sessions() == [existing_session]


def test_update_note_for_date_creates_session_and_updates_note():
    tracker = SessionTracker()

    session = tracker.update_note_for_date("2026-07-07", "Worked on backend")

    assert session.note == "Worked on backend"
    assert session.get_date() == "2026-07-07"
    assert tracker.get_sessions() == [session]


def test_update_note_for_date_reuses_existing_session():
    tracker = SessionTracker()
    existing_session = CodingSession("2026-07-07")
    tracker.add_session(existing_session)

    session = tracker.update_note_for_date("2026-07-07", "Updated existing note")

    assert session is existing_session
    assert existing_session.note == "Updated existing note"
    assert tracker.get_sessions() == [existing_session]


def test_log_session_creates_coded_session_with_note():
    tracker = SessionTracker()

    session = tracker.log_session("2026-07-07", True, "Built backend feature")

    assert session.get_date() == "2026-07-07"
    assert session.is_coded() is True
    assert session.note == "Built backend feature"
    assert tracker.get_sessions() == [session]


def test_log_session_creates_not_coded_session_with_note():
    tracker = SessionTracker()

    session = tracker.log_session("2026-07-07", False, "Rest day")

    assert session.get_date() == "2026-07-07"
    assert session.is_coded() is False
    assert session.note == "Rest day"
    assert tracker.get_sessions() == [session]


def test_log_session_reuses_existing_session():
    tracker = SessionTracker()
    existing_session = CodingSession("2026-07-07")
    tracker.add_session(existing_session)

    session = tracker.log_session("2026-07-07", True, "Updated through log_session")

    assert session is existing_session
    assert existing_session.is_coded() is True
    assert existing_session.note == "Updated through log_session"
    assert tracker.get_sessions() == [existing_session]
