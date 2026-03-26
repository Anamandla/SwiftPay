# TEST_CASES.md — Test Case Development
## SwiftPay Mobile Payment App

> **Assignment 5 | Test Cases**
> Validates functional requirements (FR) and non-functional requirements (NFR) defined in SRD.md (Assignment 4).

---

## 1. Functional Test Cases

| Test Case ID | Requirement ID | Use Case | Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|---|---|
| TC-001 | FR-01 | UC-01 | Successful user registration | App is open; email and phone not previously registered | 1. Open app. 2. Tap "Create Account." 3. Enter valid name, email, SA phone, password (8+ chars). 4. Tap "Register." | Account created in ≤ 3 seconds; wallet provisioned with R0.00; success message shown; redirect to Login screen. | — | Pending |
| TC-002 | FR-01 | UC-01 | Registration with duplicate email | An account already exists with the test email | 1. Attempt registration with an already-registered email. 2. Submit form. | HTTP 422 returned; error message: "This email is already in use."; no duplicate record created in DB. | — | Pending |
| TC-003 | FR-01 | UC-01 | Registration with password under 8 characters | App is open | 1. Enter all valid details. 2. Enter password "abc123" (6 chars). 3. Tap "Register." | Form not submitted; inline error: "Password must be at least 8 characters." | — | Pending |
| TC-004 | FR-02 | UC-02 | Successful login with valid credentials | User account exists and is active | 1. Enter registered email and correct password. 2. Tap "Login." | JWT access token issued; refresh token issued; user navigated to Home Dashboard within 2 seconds. | — | Pending |
| TC-005 | FR-02 | UC-02 | Login with incorrect password | User account exists | 1. Enter registered email and wrong password. 2. Tap "Login." | HTTP 401 returned; message: "Invalid credentials. Please try again."; no token issued. | — | Pending |
| TC-006 | FR-02 | UC-02 | Login attempt on suspended account | User account exists but status = SUSPENDED | 1. Enter valid credentials for a suspended account. 2. Tap "Login." | HTTP 403 returned; message: "Your account has been suspended. Please contact support."; no token issued. | — | Pending |
| TC-007 | FR-03 | UC-03 | Password reset with valid OTP | User has a registered account and email access | 1. Tap "Forgot Password." 2. Enter registered email. 3. Enter OTP received by email. 4. Enter new password. 5. Confirm. | Password updated; OTP invalidated in Redis; user prompted to log in with new password. | — | Pending |
| TC-008 | FR-03 | UC-03 | Password reset with expired OTP | OTP was issued more than 10 minutes ago | 1. Request OTP. 2. Wait 11 minutes. 3. Enter OTP. | Error: "OTP has expired. Please request a new one."; password unchanged. | — | Pending |
| TC-009 | FR-07 | UC-05 | Successful P2P money transfer | Sender authenticated; sender balance ≥ transfer amount; recipient account exists | 1. Navigate to "Send Money." 2. Enter valid recipient phone and amount (e.g. R50). 3. Tap "Confirm Transfer." | Sender wallet debited by R50; recipient wallet credited by R50; transaction logged; push notifications sent to both parties; operation completes in ≤ 5 seconds. | — | Pending |
| TC-010 | FR-07 | UC-05 | P2P transfer with insufficient balance | Sender wallet balance = R20; transfer amount = R100 | 1. Attempt to send R100. 2. Tap "Confirm Transfer." | HTTP 422 returned; message displays shortfall (R80 needed); sender wallet balance unchanged; no transaction record created. | — | Pending |
| TC-011 | FR-08 | UC-05 | Atomic rollback on gateway failure | Sender authenticated; balance sufficient; gateway configured to return timeout | 1. Initiate transfer. 2. Gateway returns timeout. | Sender wallet debit rolled back; balance restored to original value; no transaction record created; error displayed: "Transfer failed. Please try again." | — | Pending |
| TC-012 | FR-09 | UC-05 | Push notification delivered to recipient | Sender completes a successful transfer | 1. Complete a P2P transfer. 2. Check recipient device for notification. | FCM push notification received on recipient device within 3 seconds; notification contains amount and sender's name. | — | Pending |
| TC-013 | FR-10 | UC-07 | Successful bill payment | User authenticated; wallet balance ≥ payment amount; valid service provider selected | 1. Navigate to "Pay Bill." 2. Select provider. 3. Enter valid reference and amount. 4. Tap "Pay Now." | Wallet debited; provider receives payment confirmation via gateway; transaction record created (type: BILL_PAYMENT); success message shown. | — | Pending |
| TC-014 | FR-11 | UC-07 | Bill payment blocked due to insufficient balance | User wallet balance < payment amount | 1. Attempt bill payment exceeding balance. | HTTP 422; shortfall displayed; wallet unchanged; no gateway call made. | — | Pending |
| TC-015 | FR-12 | UC-08 | View transaction history — default load | User has 25+ transactions on record | 1. Navigate to "Transaction History." | First 20 transactions returned, sorted by date descending; each entry shows type, amount, counterparty, status, timestamp; loads within 2 seconds. | — | Pending |
| TC-016 | FR-13 | UC-08 | Filter transaction history by type | User has a mix of SEND, RECEIVE, and BILL_PAYMENT transactions | 1. Open Transaction History. 2. Apply filter: Type = "Bill Payment." | Only BILL_PAYMENT transactions displayed; results load within 2 seconds. | — | Pending |
| TC-017 | FR-15 | UC-10 | Admin suspends a user account | Admin authenticated; target user account is active | 1. Navigate to Admin Dashboard → User Management. 2. Search for user. 3. Tap "Suspend Account." 4. Enter reason. 5. Confirm. | User status updated to SUSPENDED in DB; audit log entry created; suspended user receives HTTP 403 on next login attempt. | — | Pending |
| TC-018 | FR-15 | UC-10 | Admin reactivates a suspended account | Admin authenticated; target user account is suspended | 1. Find suspended user. 2. Tap "Reactivate Account." 3. Enter reason. 4. Confirm. | User status updated to ACTIVE; user can log in immediately; audit log entry created. | — | Pending |

---

## 2. Non-Functional Test Cases

### 2.1 Performance Tests

| Test Case ID | NFR ID | Category | Description | Test Setup | Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|---|---|
| TC-NFR-01 | NFR-07 | Performance / Scalability | System handles 1,000 concurrent users | Load testing tool (k6 or JMeter) configured with 1,000 virtual users; backend deployed on staging server | 1. Configure k6 script simulating 1,000 concurrent users each performing login + view balance. 2. Run load test for 5 minutes. 3. Capture P95 response time and error rate. | P95 response time ≤ 3 seconds; zero HTTP 5xx errors; no database connection pool exhaustion. | — | Pending |
| TC-NFR-02 | NFR-12 | Performance | Transaction history loads within 2 seconds for large datasets | Database seeded with 10,000 transaction records for a single test user | 1. Authenticate test user. 2. Call GET /transactions endpoint. 3. Measure response time. | Response returned in ≤ 2 seconds; correct pagination (20 items); all records accounted for across pages. | — | Pending |
| TC-NFR-03 | NFR-13 | Performance | Mobile app cold start ≤ 3 seconds | Mid-range Android device (2GB RAM, Android 10); 4G network connection | 1. Force-close the app. 2. Clear memory. 3. Tap app icon. 4. Measure time from tap to Home Dashboard fully rendered. | App renders Home Dashboard within 3 seconds of cold start. | — | Pending |

### 2.2 Security Tests

| Test Case ID | NFR ID | Category | Description | Test Setup | Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|---|---|
| TC-NFR-04 | NFR-09 | Security | Passwords stored as bcrypt hash | Access to PostgreSQL database; test user registered | 1. Register a new user with password "TestPass123!". 2. Query the users table directly. 3. Inspect the password field. | Password field contains a bcrypt hash string (starts with `$2b$`); plaintext password "TestPass123!" not present anywhere in the database. | — | Pending |
| TC-NFR-05 | NFR-10 | Security | HTTP connections rejected; HTTPS enforced | Backend deployed with TLS certificate | 1. Send a request to `http://api.swiftpay.app/health`. 2. Observe response. | HTTP request returns HTTP 301 redirect to `https://`; SSL Labs scan on the domain returns grade A or higher. | — | Pending |
| TC-NFR-06 | NFR-02 (FR-02) | Security | Unauthenticated API access rejected | No JWT token available | 1. Send GET /transactions request with no Authorization header. 2. Send with expired JWT. | Both requests return HTTP 401 Unauthorized; no transaction data exposed. | — | Pending |
| TC-NFR-07 | NFR-11 | Security | Sensitive data encrypted at rest | Direct access to database storage | 1. Stop the database server. 2. Inspect raw database files on disk. 3. Attempt to read wallet balance and transaction records without the decryption key. | Raw database files are unreadable without the AES-256 decryption key; no plaintext financial data visible. | — | Pending |

---

## 3. Test Coverage Summary

| Category | Total Test Cases | Requirements Covered |
|---|---|---|
| User Auth & Registration | 6 (TC-001 to TC-006) | FR-01, FR-02 |
| Password Reset | 2 (TC-007, TC-008) | FR-03 |
| P2P Transfers | 4 (TC-009 to TC-012) | FR-07, FR-08, FR-09 |
| Bill Payments | 2 (TC-013, TC-014) | FR-10, FR-11 |
| Transaction History | 2 (TC-015, TC-016) | FR-12, FR-13 |
| Admin Management | 2 (TC-017, TC-018) | FR-15 |
| Performance | 3 (TC-NFR-01 to TC-NFR-03) | NFR-07, NFR-12, NFR-13 |
| Security | 4 (TC-NFR-04 to TC-NFR-07) | NFR-09, NFR-10, NFR-11 |
| **TOTAL** | **25** | **15 FR + 5 NFR** |

---

*SwiftPay — TEST_CASES.md | Software Engineering Assignment 5*
