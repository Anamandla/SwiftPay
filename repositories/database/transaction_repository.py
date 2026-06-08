"""
DatabaseTransactionRepositoryStub — stores data in PostgreSQL via psycopg2/SQLAlchemy.

TODO: Full implementation should:
- Connect to PostgreSQL using shared connection pool
- Implement transaction CRUD with SQL queries
- Support filtering by user_id, type, date range
"""
from typing import Optional

from repositories.interfaces import TransactionRepositoryInterface


class DatabaseTransactionRepositoryStub(TransactionRepositoryInterface):
    """Stub: stores _conn_str, inherits interface. No real DB connection yet.

    TODO: Replace all methods with actual psycopg2/SQLAlchemy implementations.
    """

    def __init__(self, conn_str: str = "postgresql://user:pass@localhost:5432/swiftpay"):
        self._conn_str = conn_str
        # TODO: self._pool = create_connection_pool(conn_str)

    def create(self, transaction: dict) -> dict:
        """TODO: INSERT INTO transactions ... RETURNING *"""
        raise NotImplementedError("DatabaseTransactionRepositoryStub: create() not yet implemented.")

    def get_by_id(self, transaction_id: str) -> Optional[dict]:
        """TODO: SELECT * FROM transactions WHERE id = $1"""
        raise NotImplementedError("DatabaseTransactionRepositoryStub: get_by_id() not yet implemented.")

    def get_by_user_id(self, user_id: str) -> list:
        """TODO: SELECT * FROM transactions WHERE user_id = $1 ORDER BY created_at DESC"""
        raise NotImplementedError("DatabaseTransactionRepositoryStub: get_by_user_id() not yet implemented.")
