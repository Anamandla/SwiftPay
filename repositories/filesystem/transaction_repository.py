"""
FileSystemTransactionRepositoryStub — stores data in JSON file.

TODO: Full implementation should:
- Load transaction data from JSON file on init
- Append new transactions to JSON file
- Support filtering by user_id, date range from JSON
"""
import os

from repositories.inmemory.transaction_repository import InMemoryTransactionRepository


class FileSystemTransactionRepositoryStub(InMemoryTransactionRepository):
    """Stub: inherits InMemoryTransactionRepository, stores _file_path for future JSON persistence.

    TODO: Override create(), get_by_user_id(), etc. to read/write JSON file.
    """

    def __init__(self, file_path: str = "data/transactions.json"):
        super().__init__()
        self._file_path = file_path
        # TODO: self._load_from_json()

    # TODO: Implement _load_from_json() and _flush_to_json()
