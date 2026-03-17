# SRD.md — System Requirements Document (SRD)
## SwiftPay Mobile Payment App

> **Assignment 4 | Functional & Non-Functional Requirements**
> Version 1.0 | Built on top of Assignment 3 Specification

---

## 1. Document Purpose

This System Requirements Document (SRD) defines the complete functional and non-functional requirements for SwiftPay. Each requirement is traceable to at least one stakeholder identified in `STAKEHOLDERS.md`, ensuring that every capability and quality attribute serves a real user or business need.

---

## 2. Functional Requirements

Functional requirements describe **what the system shall do** — its features and capabilities.

### 2.1 User Authentication & Account Management

| ID | Requirement | Acceptance Criteria | Linked Stakeholder(s) |
|---|---|---|---|
| FR-01 | The system shall allow users to register using their full name, email address, South African mobile number, and a password of at least 8 characters. | Registration completes in ≤ 3 seconds; duplicate email/phone rejected with clear error message. | End User, Compliance Officer |
| FR-02 | The system shall authenticate users via email/phone and password, issuing a JWT access token valid for 24 hours and a refresh token valid for 30 days. | Successful login returns tokens within 2 seconds; invalid credentials return HTTP 401 with no token issued. | End User, IT Engineer |
| FR-03 | The system shall allow users to reset their password by requesting a 6-digit OTP sent to their registered email address, valid for 10 minutes. | OTP delivered within 30 seconds; expired OTP rejected with prompt to resend. | End User, Customer Support |
| FR-04 | The system shall automatically create a ZAR digital wallet for each newly registered user with a starting balance of R0.00. | Wallet record exists in the database within 1 second of registration completion. | End User, Business Owner |

### 2.2 Wallet & Balance Management

| ID | Requirement | Acceptance Criteria | Linked Stakeholder(s) |
|---|---|---|---|
| FR-05 | The system shall display the user's current wallet balance on the home dashboard, refreshed every time the screen is loaded. | Balance reflects the latest confirmed transaction; stale data older than 5 seconds must not be displayed. | End User (Sender/Recipient), Customer Support |
| FR-06 | The system shall allow users to top up their wallet via the integrated payment gateway using a debit or credit card. | Top-up reflects in wallet balance within 10 seconds of payment gateway confirmation; failed top-ups trigger a clear error message and no balance change. | End User, Payment Gateway |

### 2.3 Peer-to-Peer (P2P) Money Transfers

| ID | Requirement | Acceptance Criteria | Linked Stakeholder(s) |
|---|---|---|---|
| FR-07 | The system shall allow a logged-in user to transfer funds to another registered SwiftPay user by entering their mobile phone number and an amount. | Transfer completes (debit + credit + notification) in ≤ 5 seconds under normal load; insufficient balance returns HTTP 422 with no debit applied. | End User (Sender/Recipient) |
| FR-08 | The system shall process all P2P transfers as atomic database transactions, ensuring that if the credit step fails, the debit is automatically rolled back. | Simulated credit failure results in sender balance unchanged and no transaction record created; confirmed via database state check. | IT Engineer, Compliance Officer |
| FR-09 | The system shall send a real-time push notification to both the sender and recipient within 3 seconds of a successful transfer, including the amount and the other party's name. | Firebase FCM delivery receipt received within 3 seconds; notification includes transfer amount and counterparty name. | End User (Recipient), Customer Support |

### 2.4 Bill Payments

| ID | Requirement | Acceptance Criteria | Linked Stakeholder(s) |
|---|---|---|---|
| FR-10 | The system shall allow users to pay registered service providers (electricity, water, airtime) by selecting the provider, entering a reference number, and specifying an amount. | Payment reflected in transaction history within 5 seconds; provider receives payment confirmation via gateway webhook. | End User, Payment Gateway |
| FR-11 | The system shall prevent bill payments if the user's wallet balance is less than the requested payment amount, displaying the shortfall to the user. | Wallet balance below payment amount returns HTTP 422; balance unchanged; shortfall amount displayed in UI. | End User, Business Owner |

### 2.5 Transaction History

| ID | Requirement | Acceptance Criteria | Linked Stakeholder(s) |
|---|---|---|---|
| FR-12 | The system shall display a paginated list of all transactions (sent, received, bill payments) for the authenticated user, sorted by date descending, with 20 items per page. | History loads within 2 seconds; each entry shows type, amount, counterparty, status, and timestamp. | End User, Customer Support |
| FR-13 | The system shall allow users to filter their transaction history by date range, transaction type (sent / received / bill payment), and status (completed / pending / failed). | Filtered results load within 2 seconds; filters are combinable; results accurately reflect applied criteria. | End User, Customer Support |

### 2.6 Admin Capabilities

| ID | Requirement | Acceptance Criteria | Linked Stakeholder(s) |
|---|---|---|---|
| FR-14 | The system shall provide an admin-only dashboard that displays total registered users, total transaction volume (ZAR), and number of active sessions, updated every 60 seconds. | Dashboard data refreshes automatically; accessible only to users with the ADMIN role; non-admins receive HTTP 403. | System Administrator, Business Owner |
| FR-15 | The system shall allow admins to suspend or reactivate user accounts, preventing suspended users from logging in or initiating transactions. | Suspended user receives HTTP 403 on login attempt within 1 second of suspension; reactivation restores access immediately. | System Administrator, Compliance Officer |

---

## 3. Non-Functional Requirements

Non-functional requirements describe **how well the system shall perform** — its quality attributes.

### 3.1 Usability

| ID | Category | Requirement | Measurable Criterion |
|---|---|---|---|
| NFR-01 | Usability | The mobile UI shall follow Material Design 3 guidelines to ensure consistency and intuitive navigation across Android and iOS. | New users shall complete their first money transfer within 3 minutes of registration without external guidance. |
| NFR-02 | Usability | All error messages shall be written in plain, non-technical language and suggest a corrective action. | 90% of usability test participants correctly identify the fix for a displayed error without assistance. |

### 3.2 Deployability

| ID | Category | Requirement | Measurable Criterion |
|---|---|---|---|
| NFR-03 | Deployability | The backend shall be containerised using Docker and deployable via a single `docker-compose up` command on any Linux server (Ubuntu 22.04+). | A fresh deployment on a clean Ubuntu 22.04 server completes successfully in under 10 minutes. |
| NFR-04 | Deployability | The mobile application shall be deployable to both the Google Play Store (Android 10+) and Apple App Store (iOS 14+). | Automated build pipeline produces valid APK and IPA artifacts with zero manual configuration steps. |

### 3.3 Maintainability

| ID | Category | Requirement | Measurable Criterion |
|---|---|---|---|
| NFR-05 | Maintainability | All backend API endpoints shall be documented in an OpenAPI 3.0 specification file (`openapi.yaml`) included in the repository. | 100% of public endpoints appear in the OpenAPI spec; a new developer can call any endpoint using only the spec within 30 minutes. |
| NFR-06 | Maintainability | The codebase shall maintain a minimum of 70% unit test coverage across all backend service modules. | Jest coverage report shows ≥ 70% line coverage on every CI pipeline run; pipeline fails below this threshold. |

### 3.4 Scalability

| ID | Category | Requirement | Measurable Criterion |
|---|---|---|---|
| NFR-07 | Scalability | The backend API shall support horizontal scaling and handle a minimum of 1,000 concurrent users without degradation in response time. | Load test (e.g. k6) simulating 1,000 concurrent users shows P95 response time ≤ 3 seconds and zero 5xx errors. |
| NFR-08 | Scalability | The PostgreSQL database shall use indexed queries on all high-frequency lookup fields (user_id, phone_number, transaction_date). | Query execution plan for indexed fields shows index scan (not sequential scan); query time ≤ 50ms for 1 million rows. |

### 3.5 Security

| ID | Category | Requirement | Measurable Criterion |
|---|---|---|---|
| NFR-09 | Security | All user passwords shall be hashed using bcrypt with a minimum cost factor of 12 before being stored in the database. | Database inspection confirms no plaintext passwords; bcrypt hash format verified on all user records. |
| NFR-10 | Security | All data transmitted between the mobile app and backend shall use TLS 1.2 or higher; HTTP connections shall be rejected. | SSL Labs scan returns grade A or higher; HTTP requests return HTTP 301 redirect to HTTPS. |
| NFR-11 | Security | All sensitive user data at rest (wallet balances, transaction records, personal details) shall be encrypted using AES-256. | Database encryption verification confirms AES-256 applied; raw database files unreadable without decryption key. |

### 3.6 Performance

| ID | Category | Requirement | Measurable Criterion |
|---|---|---|---|
| NFR-12 | Performance | The transaction history API endpoint shall return paginated results within 2 seconds for a user with up to 10,000 transaction records. | Automated test with a seeded dataset of 10,000 records confirms P99 response time ≤ 2 seconds. |
| NFR-13 | Performance | The mobile application shall launch and display the home dashboard within 3 seconds on a mid-range Android device (2GB RAM, Android 10) over a 4G connection. | Manual and automated test on reference device confirms cold start to dashboard render ≤ 3 seconds. |

---

## 4. Requirements Traceability Matrix

| Requirement ID | Type | Stakeholder(s) | Priority |
|---|---|---|---|
| FR-01 | Functional | End User, Compliance Officer | Must Have |
| FR-02 | Functional | End User, IT Engineer | Must Have |
| FR-03 | Functional | End User, Customer Support | Must Have |
| FR-04 | Functional | End User, Business Owner | Must Have |
| FR-05 | Functional | End User, Customer Support | Must Have |
| FR-06 | Functional | End User, Payment Gateway | Should Have |
| FR-07 | Functional | End User | Must Have |
| FR-08 | Functional | IT Engineer, Compliance Officer | Must Have |
| FR-09 | Functional | End User (Recipient), Customer Support | Must Have |
| FR-10 | Functional | End User, Payment Gateway | Should Have |
| FR-11 | Functional | End User, Business Owner | Must Have |
| FR-12 | Functional | End User, Customer Support | Must Have |
| FR-13 | Functional | End User, Customer Support | Should Have |
| FR-14 | Functional | System Administrator, Business Owner | Should Have |
| FR-15 | Functional | System Administrator, Compliance Officer | Must Have |
| NFR-01 | Non-Functional | End User | Must Have |
| NFR-02 | Non-Functional | End User, Customer Support | Should Have |
| NFR-03 | Non-Functional | IT Engineer | Must Have |
| NFR-04 | Non-Functional | IT Engineer, Business Owner | Must Have |
| NFR-05 | Non-Functional | IT Engineer | Should Have |
| NFR-06 | Non-Functional | IT Engineer | Should Have |
| NFR-07 | Non-Functional | IT Engineer, Business Owner | Should Have |
| NFR-08 | Non-Functional | IT Engineer | Should Have |
| NFR-09 | Non-Functional | Compliance Officer, IT Engineer | Must Have |
| NFR-10 | Non-Functional | Compliance Officer, IT Engineer | Must Have |
| NFR-11 | Non-Functional | Compliance Officer | Must Have |
| NFR-12 | Non-Functional | End User, IT Engineer | Should Have |
| NFR-13 | Non-Functional | End User | Should Have |

---

*SwiftPay — SRD.md | Software Engineering Assignment 4*
