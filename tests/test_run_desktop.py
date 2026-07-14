import run_desktop


def test_main_creates_and_runs_desktop_ui(monkeypatch):
    tracker = object()
    storage = object()
    calls = {}

    monkeypatch.setattr(
        run_desktop,
        "create_tracker_and_storage",
        lambda: (tracker, storage),
    )

    class FakeApplication:
        def __init__(self, arguments):
            calls["arguments"] = arguments

        def setQuitOnLastWindowClosed(self, enabled):
            calls["quit_on_last_window"] = enabled

        def exec(self):
            calls["event_loop_started"] = True
            return 0

    class FakeDesktopUI:
        def __init__(self, received_tracker, received_storage):
            calls["dependencies"] = (received_tracker, received_storage)

        def run(self):
            calls["ui_ran"] = True

    monkeypatch.setattr(run_desktop, "QApplication", FakeApplication)
    monkeypatch.setattr(run_desktop, "DesktopUI", FakeDesktopUI)

    result = run_desktop.main()

    assert calls["arguments"] is run_desktop.sys.argv
    assert calls["quit_on_last_window"] is False
    assert calls["dependencies"] == (tracker, storage)
    assert calls["ui_ran"] is True
    assert calls["event_loop_started"] is True
    assert result == 0
