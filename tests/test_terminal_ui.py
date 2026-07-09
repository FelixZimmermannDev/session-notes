from backend.session_tracker import SessionTracker
from frontend.terminal_ui import TerminalUI


class FakeStorage:
    def __init__(self):
        self.saved_sessions = None
        self.save_call_count = 0

    def save_sessions(self, sessions):
        self.saved_sessions = list(sessions)
        self.save_call_count += 1


def test_terminal_ui_logs_session_note(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt: "Worked on terminal UI")
    storage = FakeStorage()

    ui = TerminalUI(SessionTracker(), storage)
    ui.run()

    captured = capsys.readouterr()
    assert "Saved Session 1" in captured.out
    assert "Note: Worked on terminal UI" in captured.out


def test_terminal_ui_saves_sessions_to_storage(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "Stored terminal note")
    storage = FakeStorage()

    ui = TerminalUI(SessionTracker(), storage)
    ui.run()

    assert storage.save_call_count == 1
    assert len(storage.saved_sessions) == 1
    assert storage.saved_sessions[0].get_note() == "Stored terminal note"


def test_terminal_ui_shows_error_for_empty_note(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt: "")
    storage = FakeStorage()

    ui = TerminalUI(SessionTracker(), storage)
    ui.run()

    captured = capsys.readouterr()
    assert "Please enter a session note" in captured.out


def test_terminal_ui_does_not_save_empty_note(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "")
    storage = FakeStorage()

    ui = TerminalUI(SessionTracker(), storage)
    ui.run()

    assert storage.save_call_count == 0
    assert storage.saved_sessions is None
