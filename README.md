# SwiftPay

A modern payment management system for peer-to-peer transactions and digital wallets.

[![CI](https://github.com/Anamandla/SwiftPay/actions/workflows/ci.yml/badge.svg)](https://github.com/Anamandla/SwiftPay/actions/workflows/ci.yml)

---

## Features

- User authentication and wallet management
- Real-time transaction processing
- RESTful API with comprehensive documentation
- Modular architecture following clean code principles

## Getting Started

### Prerequisites

- **Python 3.10+** — required for the core application and API server
- **Git** — for cloning the repository and version control
- **pip** — Python package manager for installing dependencies

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/Anamandla/SwiftPay.git
cd SwiftPay

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run tests
python tests/run_all_tests.py

# 4. Start the API server
python api/main.py
```

## Project Structure

| Directory | Description |
|-----------|-------------|
| `api/` | REST API endpoints and request handlers |
| `services/` | Business logic and service layer |
| `repositories/` | Data access layer (InMemory, FileSystem, Database stubs) |
| `src/` | Core application modules |
| `tests/` | Unit and integration test suites |
| `docs/` | Project documentation and design artifacts |
| `creational_patterns/` | Factory and creational design pattern implementations |

## Contribution Roadmap

| Feature | Label | Difficulty | Issue |
|---------|-------|------------|-------|
| README Enhancement | `documentation` | Beginner | [#59](https://github.com/Anamandla/SwiftPay/issues/59) |
| FileSystem/DB Repository Stubs | `repository` | Beginner | [#41](https://github.com/Anamandla/SwiftPay/issues/41) |

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contributor guide and [ROADMAP.md](ROADMAP.md) for upcoming milestones.

## Architecture

SwiftPay follows a layered architecture pattern:

```
Presentation Layer (API)
    ↓
Service Layer (Business Logic)
    ↓
Repository Layer (Data Access)
    ↓
Storage (InMemory / FileSystem / Database)
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design documentation.

---

*Built with clean code principles and designed for extensibility.*