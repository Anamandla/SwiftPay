"""
DatabaseWalletRepositoryStub — stores data in PostgreSQL via psycopg2/SQLAlchemy.

TODO: Full implementation should:
- Connect to PostgreSQL using shared connection pool
- Implement wallet CRUD with SQL queries
- Handle balance updates with row-level locking (SELECT ... FOR UPDATE)
"""
from typing import Optional

from repositories.interfaces import WalletRepositoryInterface


class DatabaseWalletRepositoryStub(WalletRepositoryInterface):
    """Stub: stores _conn_str, inherits interface. No real DB connection yet.

    TODO: Replace all methods with actual psycopg2/SQLAlchemy implementations.
    TODO: Use SELECT ... FOR UPDATE for balance mutations.
    """

    def __init__(self, conn_str: str = "postgresql://user:pass@localhost:5432/swiftpay"):
        self._conn_str = conn_str
        # TODO: self._pool = create_connection_pool(conn_str)

    def create(self, wallet: dict) -> dict:
        """TODO: INSERT INTO wallets ... RETURNING *"""
        raise NotImplementedError("DatabaseWalletRepositoryStub: create() not yet implemented.")

    def get_by_id(self, wallet_id: str) -> Optional[dict]:
        """TODO: SELECT * FROM wallets WHERE id = $1"""
        raise NotImplementedError("DatabaseWalletRepositoryStub: get_by_id() not yet implemented.")

    def get_by_user_id(self, user_id: str) -> Optional[dict]:
        """TODO: SELECT * FROM wallets WHERE user_id = $1"""
        raise NotImplementedError("DatabaseWalletRepositoryStub: get_by_user_id() not yet implemented.")

    def update_balance(self, wallet_id: str, amount: float) -> dict:
        """TODO: UPDATE wallets SET balance = balance + $1 WHERE id = $2 RETURNING *"""
        raise NotImplementedError("DatabaseWalletRepositoryStub: update_balance() not yet implemented.")
