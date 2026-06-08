"""
FileSystemUserRepositoryStub — stores data in JSON file.

TODO: Full implementation should:
- Load user data from JSON file on init
- Save changes back to JSON file after each mutation
- Handle file locking for concurrent access
- Use atomic writes (write to .tmp, then rename)
"""
import json
import os
from typing import Optional
from datetime import datetime

from repositories.inmemory.user_repository import InMemoryUserRepository


class FileSystemUserRepositoryStub(InMemoryUserRepository):
    """Stub: inherits InMemoryUserRepository, stores _file_path for future JSON persistence.

    TODO: Override save(), update(), delete() to write to JSON file.
    TODO: Add load_from_json() method to hydrate _users from file on init.
    """

    def __init__(self, file_path: str = "data/users.json"):
        super().__init__()
        self._file_path = file_path
        # TODO: self._load_from_json()

    def save(self, user: dict) -> dict:
        """Save user to in-memory store (and TODO: persist to JSON file)."""
        result = super().save(user)
        # TODO: self._flush_to_json()
        return result

    # TODO: def _load_from_json(self) -> None:
    #     if os.path.exists(self._file_path):
    #         with open(self._file_path, 'r') as f:
    #             users = json.load(f)
    #             self._users = {u['id']: u for u in users}

    # TODO: def _flush_to_json(self) -> None:
    #     os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
    #     tmp_path = self._file_path + '.tmp'
    #     with open(tmp_path, 'w') as f:
    #         json.dump(list(self._users.values()), f, indent=2, default=str)
    #     os.replace(tmp_path, self._file_path)
