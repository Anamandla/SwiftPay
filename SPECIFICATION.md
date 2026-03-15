# SPECIFICATION.md — SwiftPay Mobile Payment App

---

## 1. Introduction

### 1.1 Project Title
**SwiftPay** — A Mobile Payment Application

### 1.2 Domain
**Finance / Mobile Banking**

The finance and banking domain encompasses systems that manage the movement, storage, and tracking of money. Mobile banking, a sub-domain, focuses on delivering financial services through smartphone applications. This domain is governed by strict regulations around data security, user authentication, and transaction integrity. Examples of systems in this domain include mobile wallets (like M-Pesa and PayPal), online banking portals, and digital payment platforms.

SwiftPay operates within the mobile banking sub-domain, targeting everyday consumers who require fast, accessible, and secure digital payment capabilities without relying on physical bank branches.

---

### 1.3 Problem Statement

Millions of people face friction when transferring money — slow bank processes, high fees, limited accessibility in remote areas, and reliance on physical infrastructure. Existing solutions are either too complex, too costly, or require a formal bank account.

SwiftPay solves this by providing a lightweight, mobile-first application that allows users to:
- Send and receive money instantly
- Pay bills and service providers directly
- Track all transactions in real time
- Operate with minimal banking infrastructure required

The system aims to make digital payments fast, affordable, and accessible to a wide range of users.

---

### 1.4 Individual Scope (Feasibility Justification)

SwiftPay is designed as a single-developer project feasible within one semester. The scope is constrained to:

- A mobile frontend (React Native) supporting iOS and Android
- A REST API backend (Node.js/Express) handling business logic
- A relational database (PostgreSQL) for persistence
- JWT-based authentication (no biometrics in Phase 1)
- Core features: registration, login, wallet balance, P2P transfer, transaction history
- Basic admin view for monitoring

Features **excluded from scope** (future phases):
- Physical card integration
- International/cross-currency transfers
- Investment or savings products
- Full regulatory compliance (KYC/AML integration)

This scope is achievable individually using well-documented, open-source tools and standard REST API patterns.

---

## 2. Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| End User | Primary user of the mobile app | Send/receive money, view balance, pay bills |
| Admin | System operator | Monitor transactions, manage users, flag fraud |
| Developer | System builder and maintainer | Implement and deploy the system |
| Payment Gateway | External service provider | Process actual money movement |
| Bank / Financial Institution | Backend financial partner | Hold and settle funds |

---

## 3. Functional Requirements

### 3.1 User Management
- FR-01: Users shall be able to register with their name, email, phone number, and password.
- FR-02: Users shall be able to log in using email/phone and password.
- FR-03: Users shall be able to reset their password via email OTP.
- FR-04: The system shall assign each user a unique wallet upon registration.

### 3.2 Wallet & Transactions
- FR-05: Users shall be able to view their current wallet balance.
- FR-06: Users shall be able to transfer funds to another registered user by phone number.
- FR-07: The system shall deduct the transferred amount from the sender's wallet and credit the recipient's wallet atomically.
- FR-08: Users shall be able to view a history of all their transactions (sent and received).

### 3.3 Bill Payments
- FR-09: Users shall be able to pay registered service providers (e.g., electricity, water).
- FR-10: The system shall confirm payment and update balance upon successful processing.

### 3.4 Notifications
- FR-11: Users shall receive a push notification upon every transaction (sent, received, or failed).
- FR-12: Users shall receive an in-app notification for low balance alerts.

### 3.5 Admin
- FR-13: Admins shall be able to view all registered users.
- FR-14: Admins shall be able to view all transactions across the system.
- FR-15: Admins shall be able to suspend or reactivate user accounts.

---

## 4. Non-Functional Requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-01 | Security | All passwords must be hashed using bcrypt before storage |
| NFR-02 | Security | All API endpoints must be protected with JWT authentication |
| NFR-03 | Security | All data in transit must use HTTPS/TLS encryption |
| NFR-04 | Performance | Transaction processing must complete within 3 seconds under normal load |
| NFR-05 | Availability | The system shall target 99.5% uptime |
| NFR-06 | Scalability | The backend shall support horizontal scaling |
| NFR-07 | Usability | The mobile UI shall be operable with one hand on a standard smartphone |
| NFR-08 | Reliability | Failed transactions must be rolled back completely (ACID compliance) |

---

## 5. Use Cases (Summary)

| Use Case | Actor | Description |
|---|---|---|
| UC-01: Register Account | User | User signs up with personal details and gets a wallet |
| UC-02: Login | User | User authenticates and receives a session token |
| UC-03: Send Money | User | User transfers funds to another user by phone number |
| UC-04: View Balance | User | User checks current wallet balance |
| UC-05: View History | User | User views list of past transactions |
| UC-06: Pay Bill | User | User pays a registered service provider |
| UC-07: Manage Users | Admin | Admin views, suspends, or reactivates user accounts |
| UC-08: Monitor Transactions | Admin | Admin views system-wide transaction activity |

---

## 6. System Constraints

- The system requires an active internet connection to function.
- Phase 1 supports only single-currency transactions (ZAR).
- The mobile application targets Android 10+ and iOS 14+.
- External payment gateway integration depends on third-party API availability.

---

*SwiftPay — SPECIFICATION.md | Software Engineering Assignment 3*
