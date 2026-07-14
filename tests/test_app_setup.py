import json
from datetime import date
from pathlib import Path

import app_setup


def test_get_sessions_file_path_uses_project_data_folder(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = app_setup.get_sessions_file_path()

    expected = (
        Path(app_setup.__file__).resolve().parent
        / "data"
        / "sessions.json"
    )
    assert result == expected


def test_create_tracker_and_storage_loads_existing_sessions(tmp_path):
    session_file = tmp_path / "sessions.json"
    session_file.write_text(
        json.dumps([
            {
                "session_number": 5,
                "date": date.today().isoformat(),
                "note": "Loaded by application setup",
                "is_archived": False,
            }
        ]),
        encoding="utf-8",
    )

    tracker, storage = app_setup.create_tracker_and_storage(session_file)

    assert storage.file_path == session_file
    assert len(tracker.get_sessions()) == 1
    assert tracker.get_sessions()[0].get_session_number() == 5
    assert tracker.get_sessions()[0].get_note() == "Loaded by application setup"
