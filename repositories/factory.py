"""
Repository factory — creates repository instances based on backend type.

Backend types:
- "inmemory" — In-memory repositories (current default, fully implemented)
- "filesystem" — JSON file-based repositories (stubs, TODO: implement)
- "database" — PostgreSQL repositories (stubs, TODO: implement)

Design choice: Factory pattern (not Dependency Injection)
- Pros: Simple, centralized creation, easy to switch backends
- Cons: Factory needs to know about all backend types
- Why chosen: SwiftPay is a student project; Factory is easier to understand
  and extend than setting up a full DI container.
"""
from enum import Enum
from typing import Optional

from repositories.inmemory.user_repository import InMemoryUserRepository
from repositories.inmemory.wallet_repository import InMemoryWalletRepository
from repositories.inmemory.transaction_repository import InMemoryTransactionRepository


class BackendType(Enum):
    INMEMORY = "inmemory"
    FILESYSTEM = "filesystem"
    DATABASE = "database"


class RepositoryFactory:
    """Creates repository instances based on the configured backend type."""

    _backend: BackendType = BackendType.INMEMORY
    _conn_str: Optional[str] = None
    _data_dir: Optional[str] = None

    @classmethod
    def configure(cls, backend: str = "inmemory", conn_str: Optional[str] = None,
                  data_dir: Optional[str] = None) -> None:
        """Configure the factory with a backend type and optional connection params.

        Args:
            backend: One of "inmemory", "filesystem", "database"
            conn_str: PostgreSQL connection string (required for database backend)
            data_dir: Directory for JSON files (required for filesystem backend)
        """
        cls._backend = BackendType(backend)
        cls._conn_str = conn_str
        cls._data_dir = data_dir

    @classmethod
    def create_user_repository(cls):
        """Create a user repository for the configured backend."""
        if cls._backend == BackendType.INMEMORY:
            return InMemoryUserRepository()
        elif cls._backend == BackendType.FILESYSTEM:
            from repositories.filesystem.user_repository import FileSystemUserRepositoryStub
            path = f"{cls._data_dir}/users.json" if cls._data_dir else "data/users.json"
            return FileSystemUserRepositoryStub(file_path=path)
        elif cls._backend == BackendType.DATABASE:
            from repositories.database.user_repository import DatabaseUserRepositoryStub
            return DatabaseUserRepositoryStub(conn_str=cls._conn_str or "")
        raise ValueError(f"Unknown backend: {cls._backend}")

    @classmethod
    def create_wallet_repository(cls):
        """Create a wallet repository for the configured backend."""
        if cls._backend == BackendType.INMEMORY:
            return InMemoryWalletRepository()
        elif cls._backend == BackendType.FILESYSTEM:
            from repositories.filesystem.wallet_repository import FileSystemWalletRepositoryStub
            path = f"{cls._data_dir}/wallets.json" if cls._data_dir else "data/wallets.json"
            return FileSystemWalletRepositoryStub(file_path=path)
        elif cls._backend == BackendType.DATABASE:
            from repositories.database.wallet_repository import DatabaseWalletRepositoryStub
            return DatabaseWalletRepositoryStub(conn_str=cls._conn_str or "")
        raise ValueError(f"Unknown backend: {cls._backend}")

    @classmethod
    def create_transaction_repository(cls):
        """Create a transaction repository for the configured backend."""
        if cls._backend == BackendType.INMEMORY:
            return InMemoryTransactionRepository()
        elif cls._backend == BackendType.FILESYSTEM:
            from repositories.filesystem.transaction_repository import FileSystemTransactionRepositoryStub
            path = f"{cls._data_dir}/transactions.json" if cls._data_dir else "data/transactions.json"
            return FileSystemTransactionRepositoryStub(file_path=path)
        elif cls._backend == BackendType.DATABASE:
            from repositories.database.transaction_repository import DatabaseTransactionRepositoryStub
            return DatabaseTransactionRepositoryStub(conn_str=cls._conn_str or "")
        raise ValueError(f"Unknown backend: {cls._backend}")
