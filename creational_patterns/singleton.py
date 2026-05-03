"""
Pattern 6: Singleton
─────────────────────────────────────────────────────────────────────────────
Use case: DatabaseConnectionPool — ensures exactly one connection pool
instance exists across the entire application lifetime.
Justification: Multiple connection pool instances would exhaust database
connections and cause race conditions on shared state. The Singleton
guarantees one pool is created once and reused everywhere, directly
supporting NFR-07 (scalability) and NFR-08 (indexed queries).
Thread-safety is ensured via a threading.Lock double-checked locking pattern.
Linked to: NFR-07, NFR-08, T-002 (DB schema setup)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import threading
from typing import Optional


class DatabaseConnectionPool:
    """
    Singleton — thread-safe database connection pool.
    Uses double-checked locking to avoid lock overhead after initialisation.
    """

    _instance: Optional["DatabaseConnectionPool"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        # First check without lock (fast path for already-created instances)
        if cls._instance is None:
            with cls._lock:
                # Second check inside lock (prevents race condition)
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, host: str = "localhost", port: int = 5432,
                 database: str = "swiftpay", max_connections: int = 20):
        # Guard against re-initialisation on subsequent __init__ calls
        if self._initialized:
            return
        self._host = host
        self._port = port
        self._database = database
        self._max_connections = max_connections
        self._active_connections: int = 0
        self._query_count: int = 0
        self._initialized = True
        print(f"[DB Pool] Initialised: {host}:{port}/{database} "
              f"(max_connections={max_connections})")

    @classmethod
    def reset_instance(cls) -> None:
        """
        Test-only method — resets the singleton so tests can create
        a fresh instance with different parameters.
        Should never be called in production code.
        """
        with cls._lock:
            cls._instance = None

    @property
    def host(self) -> str:
        return self._host

    @property
    def database(self) -> str:
        return self._database

    @property
    def max_connections(self) -> int:
        return self._max_connections

    @property
    def active_connections(self) -> int:
        return self._active_connections

    def get_connection(self) -> dict:
        """Simulate acquiring a connection from the pool."""
        if self._active_connections >= self._max_connections:
            raise RuntimeError("Connection pool exhausted. No available connections.")
        self._active_connections += 1
        conn_id = f"conn-{self._active_connections}"
        print(f"[DB Pool] Connection acquired: {conn_id} "
              f"({self._active_connections}/{self._max_connections} active)")
        return {"connection_id": conn_id, "pool": self}

    def release_connection(self, connection: dict) -> None:
        """Simulate releasing a connection back to the pool."""
        if self._active_connections > 0:
            self._active_connections -= 1
        print(f"[DB Pool] Connection released: {connection.get('connection_id')} "
              f"({self._active_connections}/{self._max_connections} active)")

    def execute_query(self, sql: str) -> dict:
        """Simulate query execution with pool tracking."""
        self._query_count += 1
        return {"rows": [], "query_count": self._query_count, "sql": sql}

    @property
    def query_count(self) -> int:
        return self._query_count

    def __repr__(self) -> str:
        return (f"DatabaseConnectionPool(host={self._host}, "
                f"db={self._database}, active={self._active_connections}/"
                f"{self._max_connections})")


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    pool1 = DatabaseConnectionPool(host="db.swiftpay.app", database="swiftpay_prod")
    pool2 = DatabaseConnectionPool(host="other-host", database="other_db")

    print(f"pool1 is pool2: {pool1 is pool2}")    # True — same instance
    print(f"pool2.host: {pool2.host}")             # db.swiftpay.app — not overwritten

    conn = pool1.get_connection()
    pool1.release_connection(conn)