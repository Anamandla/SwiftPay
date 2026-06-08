"""
DatabaseUserRepositoryStub — stores data in PostgreSQL via psycopg2/SQLAlchemy.

TODO: Full implementation should:
- Connect to PostgreSQL using connection string
- Create users table if not exists (CREATE TABLE IF NOT EXISTS)
- Implement all CRUD operations using parameterized SQL queries
- Use connection pooling (SQLAlchemy or psycopg2 pool)
- Handle transactions with commit/rollback
"""
from typing import Optional
from datetime import datetime

from repositories.interfaces import UserRepositoryInterface


class DatabaseUserRepositoryStub(UserRepositoryInterface):
    """Stub: stores _conn_str, inherits interface. No real DB connection yet.

    TODO: Replace all methods with actual psycopg2/SQLAlchemy implementations.
    TODO: Add connection pool management.
    """

    def __init__(self, conn_str: str = "postgresql://user:pass@localhost:5432/swiftpay"):
        self._conn_str = conn_str
        # TODO: self._pool = create_connection_pool(conn_str)
        # TODO: self._create_tables_if_not_exists()

    def save(self, user: dict) -> dict:
        """TODO: INSERT INTO users ... RETURNING *"""
        raise NotImplementedError(
            "DatabaseUserRepositoryStub: save() not yet implemented. "
            "Use psycopg2 or SQLAlchemy to insert into users table."
        )

    def get_by_id(self, user_id: str) -> Optional[dict]:
        """TODO: SELECT * FROM users WHERE id = $1"""
        raise NotImplementedError(
            "DatabaseUserRepositoryStub: get_by_id() not yet implemented. "
            "Use psycopg2 or SQLAlchemy to query users table."
        )

    def get_by_email(self, email: str) -> Optional[dict]:
        """TODO: SELECT * FROM users WHERE email = $1"""
        raise NotImplementedError(
            "DatabaseUserRepositoryStub: get_by_email() not yet implemented."
        )

    def get_all(self) -> list:
        """TODO: SELECT * FROM users"""
        raise NotImplementedError(
            "DatabaseUserRepositoryStub: get_all() not yet implemented."
        )

    def update(self, user_id: str, data: dict) -> Optional[dict]:
        """TODO: UPDATE users SET ... WHERE id = $1 RETURNING *"""
        raise NotImplementedError(
            "DatabaseUserRepositoryStub: update() not yet implemented."
        )

    def delete(self, user_id: str) -> bool:
        """TODO: DELETE FROM users WHERE id = $1"""
        raise NotImplementedError(
            "DatabaseUserRepositoryStub: delete() not yet implemented."
        )
