# A9_REFLECTION.md — Reflection on Domain Modeling and Class Diagram Design
## SwiftPay Mobile Payment App

> **Assignment 9 | Reflection (~500+ words)**

---

## Reflection

### 1. Challenges in Designing the Domain Model and Class Diagram

The most significant challenge in domain modeling was deciding what constitutes a **domain entity** versus a **value object** versus an **implementation detail**. Early drafts of the domain model included classes like `CardDetails`, `FCMToken`, and `RedisKey`. These felt important because they appear in the code, but they are not domain entities — they carry no independent identity, have no lifecycle of their own, and impose no business rules. Removing them and treating them as attributes of other classes (e.g., `fcmToken` as a field on `Notification`, `cardDetails` as a parameter to `PaymentGateway.processTopUp()`) produced a cleaner model that better reflected the business domain rather than the implementation.

Defining methods was equally difficult. The temptation was to map methods directly to API endpoints — `POST /auth/register` becomes `register()`, `POST /transactions/transfer` becomes `transfer()`, and so on. This produces a class diagram that looks like a route map rather than an object model. The more useful approach was to ask: *what does this object know how to do?* A `Wallet` knows how to `debit()`, `credit()`, and `validateSufficientFunds()`. It does not know how to "process a transfer" — that orchestration belongs to the `Transaction` class and the service layer. Making this distinction forced a clearer separation of concerns that will make the eventual implementation more maintainable.

The most technically complex part was the **multiplicity on Transaction wallet references**. A single `Wallet` is referenced as the sender in many transactions and as the recipient in many other transactions. Modelling this accurately required two separate associations (`senderWallet` and `recipientWallet`) rather than a single generic association — a subtle but important distinction that prevents the diagram from misrepresenting the data model.

### 2. Alignment with Previous Assignments

The class diagram did not emerge from a vacuum — it is a synthesis of every prior assignment. The `UserStatus`, `TransactionStatus`, `OTPStatus`, and `SessionStatus` enumerations are a direct translation of the state transition diagrams from Assignment 8: every named state in those diagrams becomes a value in the corresponding enumeration. This is the most direct and verifiable form of traceability between behavioral models and structural models.

The use cases from Assignment 5 drove method definition. UC-05 (Send Money) requires that `Transaction` can `initiate()`, `validate()`, `process()`, `complete()`, `fail()`, and `rollback()` — each step in the use case's basic and alternative flows becomes a method. UC-10 (Admin: Manage Users) requires that `User` can `suspend()` and `reactivate()`, and that every such action produces an `AuditLog` entry. The class diagram makes both of these requirements structurally explicit.

The functional requirements from Assignment 4 drove the business rules documented in the domain model. FR-08 (atomic rollback) is reflected in the absence of an `update()` method on `Transaction` — immutability enforces atomicity at the design level. NFR-06 (maintainability) is reflected in the interface + adapter pattern for external services — the domain is protected from third-party API changes.

### 3. Trade-offs Made

The most deliberate trade-off was **favouring composition over inheritance** throughout the diagram. An early draft explored an inheritance hierarchy where `Transfer`, `TopUp`, and `BillPayment` were subclasses of an abstract `Transaction`. This is a valid OO design, but it introduces complexity: three database tables (or a complex single-table inheritance scheme), three sets of methods to maintain, and three separate state machines to test. The chosen approach uses a single `Transaction` class with a `type` enumeration. This is simpler, easier to query (one table, one set of indexes), and adequate for SwiftPay's current scale. If the system grows to require fundamentally different behaviour per transaction type, refactoring to inheritance remains possible — but premature inheritance is harder to remove than to add.

The second trade-off was **interface granularity for external services**. A single `ExternalService` interface covering payment, notification, and email would have been simpler. But collapsing three distinct third-party integrations into one interface would force any adapter to implement methods it does not need — violating the Interface Segregation Principle. Three separate interfaces (`PaymentGateway`, `NotificationService`, `EmailService`) each with their own adapter is more verbose but is far more maintainable and testable.

### 4. Lessons Learned About Object-Oriented Design

The most important lesson from this assignment is that **a class diagram is a design decision document, not a description of code**. The choices made here — what is a class versus an attribute, what is composition versus association, which methods belong where — will constrain the implementation for the rest of the semester. Decisions that seem neutral in a diagram (like making `AuditLog` a separate class from `Transaction`) have real consequences in the database schema, the API design, and the test strategy.

The second lesson is that **immutability is a design pattern, not just a constraint**. Making `Transaction` and `AuditLog` effectively immutable (no `update()` methods, only forward state transitions) is not just a business rule — it is an architectural choice that makes the system easier to reason about, easier to audit, and easier to scale. Immutable records can be cached aggressively, replicated safely, and queried without locks. This is a principle borrowed from functional programming that applies directly to financial systems where data integrity is non-negotiable.

Finally, the process of building the class diagram made concrete something that requirements and use cases leave abstract: **the system has to actually hold this data somewhere**. Every attribute in the diagram is a database column. Every association is a foreign key or a join table. Thinking at the class level forced a more rigorous consideration of the data model than any of the prior assignments had required.

---

*SwiftPay — A9_REFLECTION.md | Software Engineering Assignment 9*
