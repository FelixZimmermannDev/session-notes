import main


def test_main_creates_and_runs_terminal_ui(monkeypatch):
    tracker = object()
    storage = object()
    calls = {}

    monkeypatch.setattr(
        main,
        "create_tracker_and_storage",
        lambda: (tracker, storage),
    )

    class FakeTerminalUI:
        def __init__(self, received_tracker, received_storage):
            calls["dependencies"] = (received_tracker, received_storage)

        def run(self):
            calls["ran"] = True

    monkeypatch.setattr(main, "TerminalUI", FakeTerminalUI)

    main.main()

    assert calls["dependencies"] == (tracker, storage)
    assert calls["ran"] is True
