from pathlib import Path

import main


def test_get_sessions_file_path_uses_project_data_folder(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = main.get_sessions_file_path()

    expected = (
        Path(main.__file__).resolve().parent
        / "data"
        / "sessions.json"
    )

    assert result == expected
