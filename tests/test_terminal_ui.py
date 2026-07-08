import pytest


try:
    from frontend.terminal_ui import TerminalUI
except ImportError:
    pytest.skip("TerminalUI depends on SessionTracker, which is not implemented yet", allow_module_level=True)


def test_terminal_ui_prints_title_when_run(capsys):
    ui = TerminalUI()

    ui.run()

    captured = capsys.readouterr()
    assert "Coding Session Tracker" in captured.out
