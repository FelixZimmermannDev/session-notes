import json

from backend.coding_session import CodingSession
from backend.json_storage import JsonStorage


def test_load_sessions_returns_empty_list_when_file_does_not_exist(tmp_path):
    storage = JsonStorage(tmp_path / "missing_sessions.json")

    assert storage.load_sessions() == []


def test_save_sessions_creates_json_file_with_session_data(tmp_path):
    file_path = tmp_path / "sessions.json"
    storage = JsonStorage(file_path)
    sessions = [CodingSession(1, "2026-07-08", "Stored note")]

    storage.save_sessions(sessions)

    assert json.loads(file_path.read_text(encoding="utf-8")) == [
        {
            "session_number": 1,
            "date": "2026-07-08",
            "note": "Stored note",
        }
    ]


def test_load_sessions_recreates_coding_session_objects(tmp_path):
    file_path = tmp_path / "sessions.json"
    file_path.write_text(
        json.dumps(
            [
                {
                    "session_number": 1,
                    "date": "2026-07-08",
                    "note": "Loaded note",
                }
            ]
        ),
        encoding="utf-8",
    )
    storage = JsonStorage(file_path)

    sessions = storage.load_sessions()

    assert len(sessions) == 1
    assert isinstance(sessions[0], CodingSession)
    assert sessions[0].get_session_number() == 1
    assert sessions[0].get_date() == "2026-07-08"
    assert sessions[0].get_note() == "Loaded note"


def test_save_sessions_creates_parent_folder_when_missing(tmp_path):
    file_path = tmp_path / "data" / "sessions.json"
    storage = JsonStorage(file_path)

    storage.save_sessions([CodingSession(1, "2026-07-08", "Nested data note")])

    assert file_path.exists()


def test_save_then_load_round_trip_preserves_multiple_sessions(tmp_path):
    storage = JsonStorage(tmp_path / "sessions.json")
    original_sessions = [
        CodingSession(1, "2026-07-08", "First note"),
        CodingSession(2, "2026-07-09", "Second note"),
    ]

    storage.save_sessions(original_sessions)
    loaded_sessions = storage.load_sessions()

    assert [session.to_dict() for session in loaded_sessions] == [
        session.to_dict() for session in original_sessions
    ]
