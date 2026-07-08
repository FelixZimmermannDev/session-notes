from backend.session_tracker import SessionTracker
from frontend.terminal_ui import TerminalUI


def test_terminal_ui_logs_session_note(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt: "Worked on terminal UI")

    ui = TerminalUI(SessionTracker())
    ui.run()

    captured = capsys.readouterr()
    assert "Saved Session 1" in captured.out
    assert "Note: Worked on terminal UI" in captured.out


def test_terminal_ui_shows_error_for_empty_note(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt: "")

    ui = TerminalUI(SessionTracker())
    ui.run()

    captured = capsys.readouterr()
    assert "Error: Session note cannot be empty." in captured.out
