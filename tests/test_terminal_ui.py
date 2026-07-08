from backend.session_tracker import SessionTracker
from frontend.terminal_ui import TerminalUI


def test_terminal_ui_logs_todays_session(monkeypatch, capsys):
    answers = iter(["y", "Worked on terminal UI"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))

    ui = TerminalUI(SessionTracker())
    ui.run()

    captured = capsys.readouterr()
    assert "Saved session:" in captured.out
    assert "Status: coded" in captured.out
    assert "Note: Worked on terminal UI" in captured.out
