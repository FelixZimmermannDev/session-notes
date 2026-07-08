from backend.coding_session import CodingSession


def test_new_session_stores_date_and_starts_unset_with_empty_note():
    session = CodingSession("2026-07-08")

    assert session.get_date() == "2026-07-08"
    assert session.get_status() == "unset"
    assert session.get_note() == ""
    assert session.is_unset() is True
    assert session.is_coded() is False
    assert session.is_uncoded() is False


def test_mark_coded_sets_status_to_coded():
    session = CodingSession("2026-07-08")

    session.mark_coded()

    assert session.get_status() == "coded"
    assert session.is_coded() is True
    assert session.is_uncoded() is False
    assert session.is_unset() is False


def test_mark_uncoded_sets_status_to_uncoded():
    session = CodingSession("2026-07-08")

    session.mark_uncoded()

    assert session.get_status() == "uncoded"
    assert session.is_uncoded() is True
    assert session.is_coded() is False
    assert session.is_unset() is False


def test_mark_uncoded_can_override_coded_status():
    session = CodingSession("2026-07-08")
    session.mark_coded()

    session.mark_uncoded()

    assert session.get_status() == "uncoded"
    assert session.is_uncoded() is True


def test_update_note_stores_note_text():
    session = CodingSession("2026-07-08")

    session.update_note("Worked on tests")

    assert session.get_note() == "Worked on tests"
