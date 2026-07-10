import json
import os
from pathlib import Path

from backend.coding_session import CodingSession


class JsonStorage:

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def save_sessions(self, sessions):
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        data = []

        for session in sessions:
            session_as_dict = session.to_dict()
            data.append(session_as_dict)

        # Create a temporary .tmp file before replacing the original.
        temporary_file_path = self.file_path.with_name(
            self.file_path.name + ".tmp"
        )

        with open(
            temporary_file_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(data, file, indent=4)

        os.replace(
            temporary_file_path,
            self.file_path
        )

    def load_sessions(self):
        if not self.file_path.exists():
            return []

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        sessions = []

        for item in data:
            session = CodingSession.from_dict(item)
            sessions.append(session)

        return sessions