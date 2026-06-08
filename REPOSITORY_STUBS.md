# Repository Stubs (Issue #41 — A11)

This document explains the repository layer design and future-proofing strategy.

## Architecture Pattern: Factory (Not Dependency Injection)

SwiftPay uses the **Factory pattern** to create repository instances.

### Why Factory?

1. **Simplicity** — A single `RepositoryFactory` class handles all backend creation
2. **Easy to understand** — Student project; Factory is more intuitive than DI containers
3. **Centralized switching** — Change backend in one place (`RepositoryFactory.configure()`)
4. **Extensible** — Add new backend types by extending the factory

### Why Not DI?

- DI requires a framework (e.g., `injector`, `dependency-injector`)
- Adds complexity without clear benefit for a small project
- Can be migrated to DI later if the project grows

## Backend Types

| Backend | Status | Description |
|---------|--------|-------------|
| `inmemory` | ✅ Implemented | Stores data in Python dicts; default for development |
| `filesystem` | 🔧 Stub | Will persist to JSON files; inherits InMemory, adds `_file_path` |
| `database` | 🔧 Stub | Will use PostgreSQL via psycopg2/SQLAlchemy; implements interface directly |

## How to Switch Backends

```python
from repositories.factory import RepositoryFactory

# Default: in-memory (no config needed)
user_repo = RepositoryFactory.create_user_repository()

# Switch to filesystem
RepositoryFactory.configure(backend="filesystem", data_dir="data")
user_repo = RepositoryFactory.create_user_repository()

# Switch to PostgreSQL
RepositoryFactory.configure(backend="database", conn_str="postgresql://...")
user_repo = RepositoryFactory.create_user_repository()
```

## File Structure

```
repositories/
├── __init__.py
├── interfaces.py          # Abstract interfaces (type hints)
├── factory.py             # RepositoryFactory (backend switcher)
├── inmemory/              # ✅ Fully implemented
│   ├── user_repository.py
│   ├── wallet_repository.py
│   └── transaction_repository.py
├── filesystem/            # 🔧 Stubs (this PR)
│   ├── __init__.py
│   ├── user_repository.py
│   ├── wallet_repository.py
│   └── transaction_repository.py
└── database/              # 🔧 Stubs (this PR)
    ├── __init__.py
    ├── user_repository.py
    ├── wallet_repository.py
    └── transaction_repository.py
```

## Stub Implementation Details

### FileSystem Stubs
- Inherit from `InMemory*Repository` classes
- Store `_file_path` attribute for future JSON persistence
- All methods delegate to parent (in-memory) — data is NOT persisted to disk yet
- TODO comments describe the JSON load/save implementation path

### Database Stubs
- Implement `*RepositoryInterface` directly (no inheritance from InMemory)
- Store `_conn_str` attribute for future PostgreSQL connection
- All methods raise `NotImplementedError` with descriptive messages
- TODO comments describe the SQL queries needed for each method

## Future Work

1. Implement FileSystem `_load_from_json()` and `_flush_to_json()` methods
2. Add file locking (`fcntl` on Linux, `msvcrt` on Windows) for concurrent safety
3. Implement Database stubs using `psycopg2` or `SQLAlchemy`
4. Add connection pooling for Database backend
5. Write integration tests for each backend type
