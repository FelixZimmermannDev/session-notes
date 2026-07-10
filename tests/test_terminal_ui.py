from backend.session_tracker import SessionTracker
from frontend.terminal_ui import TerminalUI


class FakeStorage:
    def __init__(self):
        self.saved_sessions = None
        self.save_call_count = 0

    def save_sessions(self, sessions):
        self.saved_sessions = list(sessions)
        self.save_call_count += 1


def set_inputs(monkeypatch, *answers):
    answers_iterator = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers_iterator))


def test_terminal_ui_logs_session_note(monkeypatch, capsys):
    set_inputs(monkeypatch, "1", "Worked on terminal UI")
    storage = FakeStorage()

    ui = TerminalUI(SessionTracker(), storage)
    ui.run()

    captured = capsys.readouterr()
    assert "Saved Session 1" in captured.out
    assert "Note: Worked on terminal UI" in captured.out


def test_terminal_ui_saves_sessions_to_storage(monkeypatch):
    set_inputs(monkeypatch, "1", "Stored terminal note")
    storage = FakeStorage()

    ui = TerminalUI(SessionTracker(), storage)
    ui.run()

    assert storage.save_call_count == 1
    assert len(storage.saved_sessions) == 1
    assert storage.saved_sessions[0].get_note() == "Stored terminal note"


def test_terminal_ui_shows_error_for_empty_note(monkeypatch, capsys):
    set_inputs(monkeypatch, "1", "")
    storage = FakeStorage()

    ui = TerminalUI(SessionTracker(), storage)
    ui.run()

    captured = capsys.readouterr()
    assert "Please enter a session note" in captured.out


def test_terminal_ui_does_not_save_empty_note(monkeypatch):
    set_inputs(monkeypatch, "1", "")
    storage = FakeStorage()

    ui = TerminalUI(SessionTracker(), storage)
    ui.run()

    assert storage.save_call_count == 0
    assert storage.saved_sessions is None


def test_terminal_ui_searches_session_by_number(monkeypatch, capsys):
    tracker = SessionTracker()
    tracker.add_session("Find this session")
    set_inputs(monkeypatch, "2", "1", "1")

    TerminalUI(tracker, FakeStorage()).run()

    captured = capsys.readouterr()
    assert "Session 1" in captured.out
    assert "Note: Find this session" in captured.out


def test_terminal_ui_shows_error_for_invalid_session_number(monkeypatch, capsys):
    set_inputs(monkeypatch, "2", "1", "not-a-number")

    TerminalUI(SessionTracker(), FakeStorage()).run()

    captured = capsys.readouterr()
    assert "Invalid session number" in captured.out


def test_terminal_ui_searches_sessions_by_note(monkeypatch, capsys):
    tracker = SessionTracker()
    tracker.add_session("Worked on backend")
    tracker.add_session("Learned JSON")
    set_inputs(monkeypatch, "2", "2", "BACKEND")

    TerminalUI(tracker, FakeStorage()).run()

    captured = capsys.readouterr()
    assert "Note: Worked on backend" in captured.out
    assert "Learned JSON" not in captured.out


def test_terminal_ui_searches_sessions_by_date(monkeypatch, capsys):
    tracker = SessionTracker()
    session = tracker.add_session("Today session")
    set_inputs(monkeypatch, "2", "3", session.get_date())

    TerminalUI(tracker, FakeStorage()).run()

    captured = capsys.readouterr()
    assert "Note: Today session" in captured.out

def test_terminal_ui_shows_message_when_session_number_is_missing(
    monkeypatch,
    capsys,
):
    set_inputs(monkeypatch, "2", "1", "99")

    TerminalUI(SessionTracker(), FakeStorage()).run()

    captured = capsys.readouterr()

    assert "Session not found" in captured.out


def test_terminal_ui_shows_message_when_note_has_no_matches(
    monkeypatch,
    capsys,
):
    tracker = SessionTracker()
    tracker.add_session("Worked on backend")

    set_inputs(monkeypatch, "2", "2", "desktop")

    TerminalUI(tracker, FakeStorage()).run()

    captured = capsys.readouterr()

    assert "No sessions found" in captured.out


def test_terminal_ui_shows_message_when_date_has_no_matches(
    monkeypatch,
    capsys,
):
    tracker = SessionTracker()
    tracker.add_session("Today session")

    set_inputs(monkeypatch, "2", "3", "1999-01-01")

    TerminalUI(tracker, FakeStorage()).run()

    captured = capsys.readouterr()

    assert "No sessions found" in captured.out


def test_terminal_ui_shows_error_for_invalid_main_menu_option(
    monkeypatch,
    capsys,
):
    set_inputs(monkeypatch, "99")

    TerminalUI(SessionTracker(), FakeStorage()).run()

    captured = capsys.readouterr()

    assert "Invalid option" in captured.out


def test_terminal_ui_shows_error_for_invalid_search_menu_option(
    monkeypatch,
    capsys,
):
    set_inputs(monkeypatch, "2", "99")

    TerminalUI(SessionTracker(), FakeStorage()).run()

    captured = capsys.readouterr()

    assert "Invalid option" in captured.out