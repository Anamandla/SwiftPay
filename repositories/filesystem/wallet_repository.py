"""
FileSystemWalletRepositoryStub — stores data in JSON file.

TODO: Full implementation should:
- Load wallet data from JSON file on init
- Save changes back to JSON file after each mutation
- Handle file locking for concurrent access
"""
import os

from repositories.inmemory.wallet_repository import InMemoryWalletRepository


class FileSystemWalletRepositoryStub(InMemoryWalletRepository):
    """Stub: inherits InMemoryWalletRepository, stores _file_path for future JSON persistence.

    TODO: Override create(), update_balance(), etc. to write to JSON file.
    """

    def __init__(self, file_path: str = "data/wallets.json"):
        super().__init__()
        self._file_path = file_path
        # TODO: self._load_from_json()

    # TODO: Implement _load_from_json() and _flush_to_json() as in user_repository.py
