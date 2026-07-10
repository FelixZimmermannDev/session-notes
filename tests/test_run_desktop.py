from pathlib import Path

import run_desktop


def test_get_sessions_file_path_uses_project_data_folder(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = run_desktop.get_sessions_file_path()

    expected = (
        Path(run_desktop.__file__).resolve().parent
        / "data"
        / "sessions.json"
    )

    assert result == expected
