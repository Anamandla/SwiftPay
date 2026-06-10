# 💸 SwiftPay — Mobile Payment App

[![CI](https://github.com/Anamandla/SwiftPay/actions/workflows/ci.yml/badge.svg)](https://github.com/Anamandla/SwiftPay/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

SwiftPay is a mobile-first payment application that enables users to send money, pay bills, and manage their finances securely and instantly — all from their smartphone. Once completed, SwiftPay will allow individuals to transfer funds between accounts, track spending, and receive real-time transaction notifications without needing a traditional bank branch.

---

## 📄 Project Documents

### Assignment 3 — System Specification & Architecture
| Document | Description |
|---|---|
| [SPECIFICATION.md](./SPECIFICATION.md) | Full system specification including domain, problem statement, stakeholders, functional and non-functional requirements |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | C4 architectural diagrams (Context, Container, Component) using Mermaid |

### Assignment 15 — Cross-Project Contributions
| Document | Description |
|---|---|
| [CONTRIBUTION_PLAN.md](./CONTRIBUTION_PLAN.md) | Strategy for contributing to 3 peer repositories — issue selection, phased approach, PR principles |
| [MERGED_PRS.md](./MERGED_PRS.md) | Log of all submitted and merged PRs to peer repositories |
| [REFLECTION_A15.md](./REFLECTION_A15.md) | Reflection on cross-project collaboration, CI failures, review cycles |

### Assignment 14 — Peer Review & Open-Source Preparation
| Document | Description |
|---|---|
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Full contributor guide: setup, coding standards, testing requirements, PR process |
| [ROADMAP.md](./ROADMAP.md) | 4-phase feature roadmap with `good-first-issue` and `feature-request` labels |
| [VOTING_RESULTS.md](./VOTING_RESULTS.md) | Peer star/fork tracking table and feedback log |
| [REFLECTION_A14.md](./REFLECTION_A14.md) | Reflection on onboarding contributors and open-source best practices |
| [LICENSE](./LICENSE) | MIT License |

### Assignment 13 — CI/CD with GitHub Actions
| Document | Description |
|---|---|
| [.github/workflows/ci.yml](./.github/workflows/ci.yml) | Full CI/CD pipeline: test automation on every push/PR + release artifact on merge to main |
| [PROTECTION.md](./PROTECTION.md) | Branch protection rules explanation and setup guide |

#### How to Run Tests Locally
```bash
git clone https://github.com/YOUR_USERNAME/SwiftPay.git
cd SwiftPay
python3 --version          # Requires Python 3.10+
python3 tests/run_all_tests.py   # Runs all 41 tests — no pip install needed
```

#### How the CI/CD Pipeline Works
Every push triggers the `test` job which runs all 4 test suites. If all pass, and the push is to `main`, the `release` job builds a zip artifact and creates a GitHub Release automatically. PRs to `main` are blocked from merging unless the `test` job passes.

### Assignment 12 — Service Layer & REST API
| Document | Description |
|---|---|
| [services/user_service.py](./services/user_service.py) | UserService — registration, auth, suspend/reactivate, profile update |
| [services/transaction_service.py](./services/transaction_service.py) | TransactionService — P2P transfer, top-up, history |
| [services/wallet_service.py](./services/wallet_service.py) | WalletService — balance retrieval |
| [api/app.py](./api/app.py) | REST API (stdlib http.server) — 13 endpoints across Users, Auth, Transactions, Wallet |
| [docs/openapi.yaml](./docs/openapi.yaml) | Full OpenAPI 3.0 specification |
| [tests/services/](./tests/services/) | Unit tests for UserService (11 tests) and TransactionService (7 tests) |
| [tests/api/test_api.py](./tests/api/test_api.py) | API integration tests (10 tests) |

#### API Endpoints Quick Reference
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| POST | `/api/auth/login` | Authenticate user |
| GET | `/api/users` | List all users |
| POST | `/api/users` | Register user |
| GET | `/api/users/{id}` | Get user by ID |
| PUT | `/api/users/{id}` | Update profile |
| GET | `/api/users/{id}/balance` | Get wallet balance |
| GET | `/api/users/{id}/transactions` | Transaction history |
| POST | `/api/users/{id}/suspend` | Suspend account (admin) |
| POST | `/api/users/{id}/reactivate` | Reactivate account (admin) |
| POST | `/api/transactions/transfer` | P2P money transfer |
| POST | `/api/transactions/topup` | Top up wallet |
| GET | `/api/transactions` | List all transactions (admin) |

### Assignment 11 — Repository Layer
| Document | Description |
|---|---|
| [repositories/base.py](./repositories/base.py) | Generic `Repository[T, ID]` interface with 6 CRUD operations |
| [repositories/interfaces.py](./repositories/interfaces.py) | Entity-specific interfaces: `UserRepository`, `WalletRepository`, `TransactionRepository` |
| [repositories/inmemory/](./repositories/inmemory/) | HashMap-backed implementations of all three repository interfaces |
| [repositories/factory.py](./repositories/factory.py) | `RepositoryFactory` — switches between MEMORY / FILE / DATABASE backends by string key; includes filesystem and PostgreSQL stubs for future-proofing |
| [tests/test_repositories.py](./tests/test_repositories.py) | 14 repository unit tests |

#### Repository Abstraction Choice: Factory Pattern
The `RepositoryFactory` was chosen over Dependency Injection frameworks because SwiftPay uses Python's stdlib only — no Spring, no FastAPI, no DI container. The factory provides the same decoupling benefit (storage backend swappable by changing one string) with zero external dependencies. The `SWIFTPAY_STORAGE` environment variable controls which backend is used at runtime.

### Assignment 10 — From Class Diagrams to Code + Creational Patterns
| Document | Description |
|---|---|
| [src/models.py](./src/models.py) | Full Python implementation of all 7 domain classes (User, Wallet, Transaction, Notification, OTP, Session, AuditLog) translated from the UML class diagram |
| [creational_patterns/simple_factory.py](./creational_patterns/simple_factory.py) | **Simple Factory** — `NotificationFactory` centralises creation of all 5 notification types |
| [creational_patterns/factory_method.py](./creational_patterns/factory_method.py) | **Factory Method** — `PaymentProcessor` abstract base with `TransferProcessor`, `TopUpProcessor`, `BillPaymentProcessor` subclasses |
| [creational_patterns/abstract_factory.py](./creational_patterns/abstract_factory.py) | **Abstract Factory** — `NotificationServiceFactory` creates matched families of push notifier + email sender for Production and Testing environments |
| [creational_patterns/builder.py](./creational_patterns/builder.py) | **Builder** — `UserBuilder` constructs Users step-by-step with validation; `UserDirector` provides convenience configurations |
| [creational_patterns/prototype.py](./creational_patterns/prototype.py) | **Prototype** — `TransactionPrototypeCache` stores and deep-clones pre-configured Transaction templates |
| [creational_patterns/singleton.py](./creational_patterns/singleton.py) | **Singleton** — `DatabaseConnectionPool` with thread-safe double-checked locking |
| [tests/run_tests.py](./tests/run_tests.py) | Standalone test runner — 50 tests, 50 passing, no external dependencies |
| [CHANGELOG.md](./CHANGELOG.md) | Full change log tracking all Assignment 10 progress |

#### Language Choice
**Python 3.10+** was chosen because:
- The class diagram maps cleanly to Python's `dataclass`-style classes and `Enum` types
- Python's `abc.ABC` and `@abstractmethod` support the Factory Method and Abstract Factory patterns natively
- `threading.Lock` provides the concurrency primitives needed for a thread-safe Singleton
- `copy.deepcopy` makes the Prototype pattern trivial to implement correctly
- No compilation step — tests run immediately with `python3 tests/run_tests.py`

#### Creational Pattern Rationale

| Pattern | Applied To | Justification |
|---|---|---|
| **Simple Factory** | `NotificationFactory` | 5 notification types share identical construction logic but differ only in title/body templates. Centralising creation eliminates copy-pasted template strings across the codebase. |
| **Factory Method** | `PaymentProcessor` → `TransferProcessor`, `TopUpProcessor`, `BillPaymentProcessor` | Each payment type has different validation rules (balance check, required fields). Delegating to subclasses keeps each processor focused without a monolithic if/else chain. |
| **Abstract Factory** | `NotificationServiceFactory` → `ProductionNotificationFactory`, `TestingNotificationFactory` | The system must swap the entire notification stack (FCM + SendGrid) between production and test environments. The Abstract Factory guarantees all products come from the same family — no accidental real FCM calls in unit tests. |
| **Builder** | `UserBuilder` | User creation involves mandatory field validation, optional activation, optional wallet credit, and password hashing. A builder enforces the construction sequence and prevents partially-built User objects from being used. |
| **Prototype** | `TransactionPrototypeCache` | Creating a Transaction with correct defaults (currency, type, initial status) is repetitive. The cache stores validated templates and produces independent deep-copied clones, guaranteeing each transaction starts from a known-good state. |
| **Singleton** | `DatabaseConnectionPool` | Multiple connection pool instances would exhaust database connections and cause race conditions. One pool, created once, reused everywhere — with thread-safe double-checked locking for concurrent access safety. |

### Assignment 9 — Domain Modeling & Class Diagram
| Document | Description |
|---|---|
| [DOMAIN_MODEL.md](./DOMAIN_MODEL.md) | Domain model for 7 entities: User, Wallet, Transaction, Notification, OTP, AuditLog, Session — with attributes, methods, relationships, and 15 business rules |
| [CLASS_DIAGRAM.md](./CLASS_DIAGRAM.md) | Full UML class diagram in Mermaid.js with 10 classes, 3 interfaces, 9 enumerations, composition/inheritance/association relationships, multiplicity, and design decision explanations |
| [A9_REFLECTION.md](./A9_REFLECTION.md) | Reflection on abstraction challenges, alignment with prior assignments, composition vs inheritance trade-offs, and OO design lessons |

### Assignment 8 — State & Activity Modeling
| Document | Description |
|---|---|
| [STATE_DIAGRAMS.md](./STATE_DIAGRAMS.md) | State transition diagrams for 8 objects: User Account, Wallet, Transaction, Push Notification, Bill Payment, JWT Session, OTP, Admin Action |
| [ACTIVITY_DIAGRAMS.md](./ACTIVITY_DIAGRAMS.md) | Activity workflow diagrams for 8 workflows: Registration, Login, P2P Transfer, Password Reset, Bill Payment, Admin Suspend, Top Up, Transaction History |
| [A8_REFLECTION.md](./A8_REFLECTION.md) | Reflection on granularity decisions, aligning diagrams with Agile stories, and state vs activity diagram comparison |

### Assignment 7 — Kanban Board & Template Analysis
| Document | Description |
|---|---|
| [template_analysis.md](./template_analysis.md) | Comparison of 4 GitHub project templates, justification for Automated Kanban selection, and 7-column customisation plan |
| [kanban_explanation.md](./kanban_explanation.md) | Definition of Kanban, full board structure, WIP limits, column definitions, label/milestone setup, and GitHub setup guide |
| [reflection.md](./reflection.md) | Reflection on template selection challenges and comparison with Trello and Jira |

### Assignment 6 — Agile Planning
| Document | Description |
|---|---|
| [AGILE_PLANNING.md](./AGILE_PLANNING.md) | 15 user stories (INVEST), MoSCoW prioritised product backlog with story points, Sprint 1 plan with 19 tasks, traceability matrix, and reflection |

### Assignment 5 — Use Case Modeling & Test Cases
| Document | Description |
|---|---|
| [USE_CASES.md](./USE_CASES.md) | Use case diagram (Mermaid), actor explanations, and 8 detailed use case specifications with flows and alternative paths |
| [TEST_CASES.md](./TEST_CASES.md) | 25 test cases covering 15 functional and 5 non-functional requirements, including performance and security tests |
| [REFLECTION_A5.md](./REFLECTION_A5.md) | Reflection on challenges translating requirements into use cases and tests |

### Assignment 4 — Stakeholder & System Requirements
| Document | Description |
|---|---|
| [STAKEHOLDERS.md](./STAKEHOLDERS.md) | Detailed stakeholder analysis: roles, concerns, pain points, and success metrics for 8 stakeholders |
| [SRD.md](./SRD.md) | System Requirements Document with 15 functional requirements and 13 non-functional requirements across 6 quality categories |
| [REFLECTION.md](./REFLECTION.md) | Reflection on challenges encountered when balancing competing stakeholder needs |

---

## 🚀 Project Overview

| Field | Detail |
|---|---|
| **Project Name** | SwiftPay |
| **Domain** | Finance / Mobile Banking |
| **Type** | Individual Project |
| **Course** | Software Engineering — Assignment 3 |

---

## ✨ Key Features (Planned)

- User registration and secure authentication (PIN / biometrics)
- Peer-to-peer (P2P) money transfers
- Bill payments and airtime top-up
- Real-time transaction history and notifications
- Wallet balance management
- Admin dashboard for monitoring and fraud detection

---

## 🛠️ Tech Stack (Planned)

- **Frontend:** React Native (iOS & Android)
- **Backend:** Node.js / Express REST API
- **Database:** PostgreSQL
- **Authentication:** JWT + OAuth 2.0
- **Notifications:** Firebase Cloud Messaging (FCM)

---

## 🏁 Getting Started

### Prerequisites
- Python 3.10 or higher
- Git
- A GitHub account

### Setup
```bash
git clone https://github.com/YOUR_USERNAME/SwiftPay.git
cd SwiftPay
python --version              # Verify Python 3.10+
python tests/run_all_tests.py # Run all tests — no pip install needed
```

### Start the API
```bash
cd api
python app.py                 # Starts on http://localhost:8080
```

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed setup instructions, coding standards, and the PR process. Check [ROADMAP.md](./ROADMAP.md) for planned features.

---

## 📋 Features Open for Contribution

| Feature | Label | Difficulty | Issue |
|---------|-------|------------|-------|
| FileSystem & Database repository stubs | `repository`, `good-first-issue` | Beginner | [#41](https://github.com/Anamandla/SwiftPay/issues/41) |
| Add requirements.txt and setup.py | `ci-cd`, `good-first-issue` | Beginner | [#54](https://github.com/Anamandla/SwiftPay/issues/54) |
| Write CONTRIBUTING.md | `documentation`, `good-first-issue` | Beginner | [#55](https://github.com/Anamandla/SwiftPay/issues/55) |
| Add MIT License | `documentation`, `good-first-issue` | Beginner | [#57](https://github.com/Anamandla/SwiftPay/issues/57) |
| Update README with Getting Started guide | `documentation`, `good-first-issue` | Beginner | [#59](https://github.com/Anamandla/SwiftPay/issues/59) |

---

*Submitted by: Anamandla Zweni - 223095435 | Software Engineering Assignment 3*
