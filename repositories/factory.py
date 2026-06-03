"""
RepositoryFactory — Assignment 11
Factory Pattern for switching storage backends via a string key.
Supports: MEMORY (default), FILE (stub), DATABASE (stub).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from repositories.interfaces import UserRepository, WalletRepository, TransactionRepository
from repositories.inmemory.user_repository import InMemoryUserRepository
from repositories.inmemory.wallet_repository import InMemoryWalletRepository
from repositories.inmemory.transaction_repository import InMemoryTransactionRepository


class RepositoryFactory:
    """
    Central factory that returns the correct repository implementation
    based on the requested storage backend type.

    Current backends:
      - "MEMORY" : In-memory HashMap (default, used for tests and dev)
      - "FILE"   : JSON filesystem stub (future implementation)
      - "DATABASE": PostgreSQL stub (future implementation)
    """

    MEMORY = "MEMORY"
    FILE = "FILE"
    DATABASE = "DATABASE"

    @staticmethod
    def get_user_repository(storage_type: str = "MEMORY") -> UserRepository:
        if storage_type == RepositoryFactory.MEMORY:
            return InMemoryUserRepository()
        if storage_type == RepositoryFactory.FILE:
            return FileSystemUserRepositoryStub()
        if storage_type == RepositoryFactory.DATABASE:
            return DatabaseUserRepositoryStub()
        raise ValueError(f"Unknown storage type: '{storage_type}'. "
                         f"Valid options: MEMORY, FILE, DATABASE")

    @staticmethod
    def get_wallet_repository(storage_type: str = "MEMORY") -> WalletRepository:
        if storage_type == RepositoryFactory.MEMORY:
            return InMemoryWalletRepository()
        if storage_type == RepositoryFactory.FILE:
            return FileSystemWalletRepositoryStub()
        if storage_type == RepositoryFactory.DATABASE:
            return DatabaseWalletRepositoryStub()
        raise ValueError(f"Unknown storage type: '{storage_type}'")

    @staticmethod
    def get_transaction_repository(storage_type: str = "MEMORY") -> TransactionRepository:
        if storage_type == RepositoryFactory.MEMORY:
            return InMemoryTransactionRepository()
        if storage_type == RepositoryFactory.FILE:
            return FileSystemTransactionRepositoryStub()
        if storage_type == RepositoryFactory.DATABASE:
            return DatabaseTransactionRepositoryStub()
        raise ValueError(f"Unknown storage type: '{storage_type}'")


# ── Future-Proof Stubs ────────────────────────────────────────────────────────

class FileSystemUserRepositoryStub(InMemoryUserRepository):
    """
    STUB — Filesystem JSON backend (Assignment 11 future-proofing).
    Inherits InMemory for now; a real implementation would:
      1. Load JSON on __init__ from self._file_path
      2. Persist to JSON on every save/delete
      3. Use file locking for concurrent access safety
    """
    def __init__(self, file_path: str = "data/users.json"):
        super().__init__()
        self._file_path = file_path
        # TODO: self._load_from_file()

    def save(self, entity):
        result = super().save(entity)
        # TODO: self._persist_to_file()
        return result


class FileSystemWalletRepositoryStub(InMemoryWalletRepository):
    def __init__(self, file_path: str = "data/wallets.json"):
        super().__init__(); self._file_path = file_path


class FileSystemTransactionRepositoryStub(InMemoryTransactionRepository):
    def __init__(self, file_path: str = "data/transactions.json"):
        super().__init__(); self._file_path = file_path


class DatabaseUserRepositoryStub(InMemoryUserRepository):
    """
    STUB — PostgreSQL backend (Assignment 11 future-proofing).
    A real implementation would use psycopg2 / SQLAlchemy:
      save()        → INSERT INTO users ... ON CONFLICT DO UPDATE
      find_by_id()  → SELECT * FROM users WHERE user_id = %s
      find_all()    → SELECT * FROM users
      delete()      → UPDATE users SET status='DELETED' WHERE user_id = %s
    """
    def __init__(self, connection_string: str = None):
        super().__init__()
        self._conn_str = connection_string
        # TODO: self._pool = DatabaseConnectionPool(conn_str)


class DatabaseWalletRepositoryStub(InMemoryWalletRepository):
    def __init__(self, connection_string: str = None):
        super().__init__(); self._conn_str = connection_string


class DatabaseTransactionRepositoryStub(InMemoryTransactionRepository):
    def __init__(self, connection_string: str = None):
        super().__init__(); self._conn_str = connection_string
