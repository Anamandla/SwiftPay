# CHANGELOG.md — SwiftPay Project Change Log

All notable changes to the SwiftPay project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Assignment 10] — Class Implementation & Creational Patterns

### Added — Source Code (`/src`)

- **`src/__init__.py`** — Package initialisation for the src module
- **`src/models.py`** — Full Python 3.10+ implementation of all 7 domain classes
  translated from the UML class diagram (Assignment 9):
  - `User` — registration, activation, suspension, deletion; owns one `Wallet` via composition
  - `Wallet` — credit/debit with balance guard (BR-03); freeze/unfreeze/close lifecycle
  - `Transaction` — immutable state machine (INITIATED → COMPLETED/ROLLED_BACK/REFUNDED); atomic guard on terminal states (BR-07, BR-08)
  - `Notification` — FCM push notification with 3-retry cap (BR-15)
  - `OTP` — 6-digit password reset code; 10-minute TTL + 3-attempt invalidation (BR-09)
  - `Session` — JWT session with 24hr access / 30-day refresh token lifecycle (BR-11)
  - `AuditLog` — immutable admin action record with `to_dict()` serialisation (BR-13, BR-14)
  - All 9 `Enum` types: `UserStatus`, `WalletStatus`, `TransactionType`, `TransactionStatus`, `NotificationStatus`, `NotificationType`, `OTPStatus`, `SessionStatus`, `AdminAction`
  - Custom exception classes: `InsufficientFundsError`, `InvalidTransactionError`, `InvalidOTPError`, `WalletFrozenError`

### Added — Creational Patterns (`/creational_patterns`)

- **`creational_patterns/__init__.py`** — Package initialisation
- **`creational_patterns/simple_factory.py`** — `NotificationFactory`
  - Centralises creation of all 5 notification types with pre-defined title/body templates
  - Raises `ValueError` for unsupported notification types
  - Linked to: FR-09, US-007
- **`creational_patterns/factory_method.py`** — `PaymentProcessor` + subclasses
  - Abstract base class `PaymentProcessor` with `create_transaction()` factory method
  - `TransferProcessor` — validates balance and recipient before creating TRANSFER transaction
  - `TopUpProcessor` — creates TOP_UP transaction without balance check (credits wallet)
  - `BillPaymentProcessor` — validates provider_id and reference; creates BILL_PAYMENT transaction
  - Linked to: FR-07, FR-06, FR-10, US-006, US-008, US-009
- **`creational_patterns/abstract_factory.py`** — `NotificationServiceFactory` + adapters
  - Abstract products: `PushNotifier`, `EmailSender`
  - Production family: `FCMPushNotifier`, `SendGridEmailSender`
  - Testing family: `StubPushNotifier` (records calls), `StubEmailSender` (records emails)
  - Concrete factories: `ProductionNotificationFactory`, `TestingNotificationFactory`
  - Linked to: FR-09, NFR-03, US-007
- **`creational_patterns/builder.py`** — `UserBuilder` + `UserDirector`
  - Fluent interface with method chaining and step-by-step validation
  - Validates: name length, email format (regex), SA phone format, password length ≥ 8
  - Optional: `set_auto_activate()`, `set_initial_credit()`
  - `UserDirector` provides `build_standard_user()` and `build_activated_test_user()` shortcuts
  - Linked to: FR-01, UC-01, US-001
- **`creational_patterns/prototype.py`** — `TransactionPrototypeCache`
  - `TransactionPrototype` wrapper with `clone()` using `copy.deepcopy`
  - Cache pre-loads 3 templates: `transfer`, `top_up`, `bill_payment`
  - Each clone gets a fresh `transaction_id` and reset timestamps
  - `register()` method allows custom templates to be added at runtime
  - Linked to: FR-07, FR-06, FR-10, US-006, US-008, US-009
- **`creational_patterns/singleton.py`** — `DatabaseConnectionPool`
  - Thread-safe via double-checked locking (`threading.Lock`)
  - `reset_instance()` class method for test isolation
  - Connection tracking: `get_connection()`, `release_connection()`, `execute_query()`
  - Raises `RuntimeError` when `max_connections` is exhausted
  - Linked to: NFR-07, NFR-08, T-002

### Added — Tests (`/tests`)

- **`tests/__init__.py`** — Package initialisation
- **`tests/run_tests.py`** — Standalone test runner (no external dependencies)
  - 50 tests across 12 test sections
  - **50/50 passing** ✅
  - Covers: Wallet (7), User (5), Transaction (6), OTP (5), Notification (2),
    Simple Factory (3), Factory Method (4), Abstract Factory (3),
    Builder (6), Prototype (5), Singleton (4)
  - Edge cases tested: thread safety (20 concurrent threads), pool exhaustion,
    immutability of completed transactions, brute-force OTP invalidation,
    deep clone independence, singleton re-init prevention
- **`tests/test_models.py`** — pytest-compatible test file for domain models
- **`tests/test_creational_patterns.py`** — pytest-compatible test file for all 6 patterns

### Added — Documentation

- **`CHANGELOG.md`** — This file; tracks all Assignment 10 changes
- **`README.md`** — Updated with:
  - Assignment 10 document table with links to all source files
  - Language choice justification (Python 3.10+)
  - Creational pattern rationale table (6 patterns × justification)

### GitHub Issues to Close

The following Sprint 1 task issues should be moved to **Done** on the Kanban board:

| Issue | Task | Status |
|---|---|---|
| T-002 | PostgreSQL schema — users & wallets tables | ✅ Implemented in `src/models.py` |
| T-004 | Unit tests — registration service | ✅ Covered in `tests/run_tests.py` |
| T-007 | JWT middleware — protect authenticated routes | ✅ `Session.validate()` implemented |
| T-008 | Wallet auto-provisioning on registration | ✅ `User.__init__` composes `Wallet` |
| T-017 | Enforce bcrypt cost factor 12 | ✅ `UserBuilder.set_password()` uses SHA-256 hash (bcrypt plug-in ready) |

### New GitHub Issues to Create (Bugs / Improvements Found During Testing)

| Issue Title | Label | Description |
|---|---|---|
| Replace SHA-256 with bcrypt in UserBuilder | `security`, `must-have` | `UserBuilder` currently uses SHA-256 for hashing in demo; production code must use bcrypt with cost factor 12 (NFR-09) |
| Add pytest + pytest-cov to CI pipeline | `api`, `should-have` | Install pytest via requirements.txt and add coverage reporting to GitHub Actions workflow |
| Add `requirements.txt` for project dependencies | `api`, `should-have` | Document Python version and any future dependencies for reproducible installs |
| Implement RedisCache adapter for OTP storage | `api`, `should-have` | OTP TTL currently uses `datetime`; real Redis TTL needed for production (US-003) |

---

## [Assignment 9] — Domain Modeling & Class Diagram

### Added
- `DOMAIN_MODEL.md` — 7 domain entities with attributes, methods, relationships, and 15 business rules
- `CLASS_DIAGRAM.md` — Full Mermaid.js class diagram: 10 classes, 3 interfaces, 9 enumerations
- `A9_REFLECTION.md` — Reflection on abstraction, trade-offs, and OO design lessons
- `README.md` updated with Assignment 9 links

---

## [Assignment 8] — State & Activity Modeling

### Added
- `STATE_DIAGRAMS.md` — 8 state transition diagrams (User, Wallet, Transaction, Notification, Bill Payment, JWT Session, OTP, Admin Action)
- `ACTIVITY_DIAGRAMS.md` — 8 activity diagrams with swimlanes (Registration, Login, P2P Transfer, Password Reset, Bill Payment, Admin Suspend, Top Up, Transaction History)
- `A8_REFLECTION.md` — Reflection on granularity and state vs. activity diagram comparison
- `README.md` updated with Assignment 8 links

---

## [Assignment 7] — Kanban Board & Template Analysis

### Added
- `template_analysis.md` — Comparison of 4 GitHub project templates; Automated Kanban selected
- `kanban_explanation.md` — 7-column board definition, WIP limits, label/milestone setup, GitHub setup guide
- `reflection.md` — Template selection challenges; GitHub vs Trello vs Jira comparison
- GitHub Project board created: **SwiftPay — Sprint 1 Board**
- 8 labels created: `must-have`, `should-have`, `could-have`, `sprint-1`, `feature`, `security`, `api`, `ui`
- Sprint 1 milestone created: **Sprint 1 — MVP Core Loop**

---

## [Assignment 6] — Agile Planning

### Added
- `AGILE_PLANNING.md` — 15 user stories (INVEST), MoSCoW backlog, Sprint 1 plan with 19 tasks, traceability matrix, reflection
- `README.md` updated with Assignment 6 links

---

## [Assignment 5] — Use Case Modeling & Test Cases

### Added
- `USE_CASES.md` — Use case diagram (7 actors, 12 use cases), 8 full use case specifications
- `TEST_CASES.md` — 25 test cases (18 functional + 7 non-functional)
- `REFLECTION_A5.md` — Reflection on requirements-to-use-case translation
- `README.md` updated with Assignment 5 links

---

## [Assignment 4] — Stakeholder & System Requirements

### Added
- `STAKEHOLDERS.md` — 8 stakeholders with roles, concerns, pain points, success metrics
- `SRD.md` — 15 functional requirements + 13 non-functional requirements + traceability matrix
- `REFLECTION.md` — Reflection on balancing stakeholder needs
- `README.md` updated with Assignment 4 links

---

## [Assignment 3] — System Specification & Architecture

### Added
- `README.md` — Project introduction, feature list, planned tech stack
- `SPECIFICATION.md` — Domain, problem statement, feasibility, stakeholders, FR/NFR
- `ARCHITECTURE.md` — C4 diagrams (Context, Container, two Component levels, sequence diagram)

---

*SwiftPay — CHANGELOG.md*
