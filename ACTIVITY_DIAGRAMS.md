# ACTIVITY_DIAGRAMS.md — Activity Workflow Modeling
## SwiftPay Mobile Payment App

> **Assignment 8 | Activity Diagrams**
> Models 8 complex SwiftPay workflows using UML activity diagrams in Mermaid.
> Includes swimlanes, decision nodes, parallel actions, and start/end nodes.

---

## 1. User Registration Workflow

```mermaid
flowchart TD
    Start([🟢 Start]) --> A

    subgraph User ["👤 User"]
        A[Open SwiftPay app] --> B[Tap 'Create Account']
        B --> C[Fill in name, email, phone, password]
        C --> D[Tap Register]
        J[Correct errors and resubmit] --> D
        P[Confirm account active] --> Stop2([🔴 End])
    end

    subgraph System ["⚙️ System"]
        E{Validate inputs}
        F[Display inline field errors]
        G[Hash password — bcrypt cost 12]
        H[(Write user record to DB)]
        I[(Create wallet — R0.00 balance)]
        K[Send welcome email]
        L[Return success response]
    end

    subgraph EmailService ["📧 Email Service"]
        M[Deliver welcome email to user]
    end

    D --> E
    E -->|Invalid| F
    F --> J
    E -->|Valid| G
    G --> H
    H --> I
    I --> K
    I --> L
    K --> M
    L --> P
    M --> Stop([🔴 End])
```

**Explanation:**
The parallel branches after wallet creation (`Send welcome email` and `Return success response`) ensure the user is not blocked waiting for email delivery. The system responds immediately while the email dispatches asynchronously — addressing the End User's need for fast registration (≤ 3 seconds, FR-01) while still fulfilling the Compliance Officer's requirement for onboarding communication.

| Element | Requirement |
|---|---|
| bcrypt hashing step | NFR-09 |
| Wallet auto-creation | FR-04 |
| Async email dispatch | NFR-05 (reliability) |
| Inline validation errors | NFR-01 (usability) |

---

## 2. Login and Authentication Workflow

```mermaid
flowchart TD
    Start([🟢 Start]) --> A

    subgraph User ["👤 User"]
        A[Open Login screen] --> B[Enter email/phone and password]
        B --> C[Tap Login]
        L[View error message] --> B
        O[Access Home Dashboard] --> Stop2([🔴 End])
    end

    subgraph System ["⚙️ System"]
        D{Account exists?}
        E{Password matches bcrypt hash?}
        F{Account status = Active?}
        G[Return HTTP 401 — Invalid credentials]
        H[Return HTTP 403 — Account suspended]
        I[Issue JWT access token — 24hr]
        J[Issue refresh token — 30 days]
        K[Store refresh token hash in Redis]
        N[Return tokens to app]
    end

    subgraph MobileApp ["📱 Mobile App"]
        M[Store tokens in AsyncStorage]
        P[Navigate to Home Dashboard]
    end

    C --> D
    D -->|No| G
    G --> L
    D -->|Yes| E
    E -->|No| G
    E -->|Yes| F
    F -->|Suspended| H
    H --> L
    F -->|Active| I
    I --> J
    J --> K
    K --> N
    N --> M
    M --> P
    P --> O
```

**Explanation:**
The deliberate ambiguity of the HTTP 401 response (returned for both "account not found" and "wrong password") is a security design decision — it prevents user enumeration attacks. This workflow directly serves the End User's concern for secure access and the Compliance Officer's security baseline requirements.

| Element | Requirement |
|---|---|
| bcrypt comparison | NFR-09 |
| JWT issuance | FR-02 |
| Suspended account guard | FR-15 |
| Token storage in AsyncStorage | NFR-02 |

---

## 3. P2P Money Transfer Workflow

```mermaid
flowchart TD
    Start([🟢 Start]) --> A

    subgraph User ["👤 Sender"]
        A[Navigate to Send Money] --> B[Enter recipient phone and amount]
        B --> C[Tap Confirm Transfer]
        N[View error — insufficient balance] --> B
        O[View error — recipient not found] --> B
        T[View Transfer Successful screen] --> Stop2([🔴 End])
    end

    subgraph System ["⚙️ System"]
        D{Recipient exists?}
        E{Sender balance ≥ amount?}
        F[Begin DB transaction]
        G[Debit sender wallet]
        H[Call Payment Gateway]
        I{Gateway response?}
        J[Credit recipient wallet]
        K[Commit DB transaction]
        L[Write transaction log — COMPLETED]
        P[Rollback DB transaction]
        Q[Write transaction log — FAILED]
        R[Return HTTP 503 / 402]
    end

    subgraph Notifications ["🔔 Notification Service"]
        S1[Send push to sender: Transfer sent]
        S2[Send push to recipient: Money received]
    end

    subgraph Gateway ["🏦 Payment Gateway"]
        GW[Process fund settlement]
    end

    C --> D
    D -->|No| O
    D -->|Yes| E
    E -->|No| N
    E -->|Yes| F
    F --> G
    G --> H
    H --> GW
    GW --> I
    I -->|Success| J
    J --> K
    K --> L
    L --> S1
    L --> S2
    S1 --> T
    S2 --> Stop3([🔴 End — Recipient notified])
    I -->|Failure/Timeout| P
    P --> Q
    Q --> R
    R --> Stop4([🔴 End — Transfer failed])
```

**Explanation:**
The parallel notification branches after a successful transfer (sender notification and recipient notification) ensure both parties are informed simultaneously without either waiting for the other. The atomic DB transaction wrapping debit + gateway + credit is the most critical path in the entire system — the rollback branch directly addresses the Compliance Officer's requirement for no partial transactions.

| Element | Requirement |
|---|---|
| Balance guard | FR-07 |
| Atomic DB transaction + rollback | FR-08 |
| Parallel push notifications | FR-09 |
| Gateway integration | FR-07 |

---

## 4. Password Reset via OTP Workflow

```mermaid
flowchart TD
    Start([🟢 Start]) --> A

    subgraph User ["👤 User"]
        A[Tap 'Forgot Password'] --> B[Enter registered email]
        B --> C[Tap Send OTP]
        F[Check email inbox] --> G[Enter 6-digit OTP]
        G --> H[Enter new password]
        H --> I[Tap Confirm Reset]
        N[View error: OTP expired] --> C
        O[View error: OTP incorrect] --> G
        P[View error: Too many attempts] --> C
        Q[View success: Password reset] --> Stop2([🔴 End])
    end

    subgraph System ["⚙️ System"]
        D{Email registered?}
        E[Generate 6-digit OTP]
        J{OTP valid and not expired?}
        K{Attempt count < 3?}
        L[Hash new password]
        M[Update user record in DB]
        R[Invalidate OTP in Redis]
        S[Return generic response]
    end

    subgraph Redis ["⚡ Redis Cache"]
        Store[Store OTP with 10-min TTL]
    end

    subgraph EmailService ["📧 Email Service"]
        Send[Send OTP email to user]
    end

    C --> D
    D -->|No| S
    S --> F
    D -->|Yes| E
    E --> Store
    Store --> Send
    Send --> F
    I --> K
    K -->|No — max attempts| P
    K -->|Yes| J
    J -->|Expired| N
    J -->|Incorrect| O
    J -->|Valid| L
    L --> M
    M --> R
    R --> Q
```

**Explanation:**
The generic response for unregistered emails prevents user enumeration — an attacker cannot determine whether an email is registered by testing the reset flow. The Redis TTL and attempt counter are parallel security controls that protect against both time-based and brute-force attacks.

| Element | Requirement |
|---|---|
| OTP generation + Redis TTL | FR-03 |
| 3-attempt limit | NFR-09 (brute force protection) |
| Generic response for unknown email | NFR-09 (no info leak) |
| bcrypt on new password | NFR-09 |

---

## 5. Bill Payment Workflow

```mermaid
flowchart TD
    Start([🟢 Start]) --> A

    subgraph User ["👤 User"]
        A[Navigate to Pay Bill] --> B[Select service provider]
        B --> C[Enter reference number and amount]
        C --> D[Tap Pay Now]
        I[View error: invalid input or low balance] --> C
        O[View Payment Successful screen] --> Stop2([🔴 End])
        P[View Payment Failed screen] --> Stop3([🔴 End])
    end

    subgraph System ["⚙️ System"]
        E{Validate: balance sufficient AND reference valid?}
        F[Display confirmation screen]
        G[Debit user wallet]
        H[Call Payment Gateway]
        J{Gateway + Provider response?}
        K[Write transaction — COMPLETED]
        L[Reverse wallet debit — rollback]
        M[Write transaction — FAILED]
    end

    subgraph Gateway ["🏦 Payment Gateway"]
        GW[Forward payment to provider]
        GW2{Provider confirms receipt?}
    end

    D --> E
    E -->|Invalid| I
    E -->|Valid| F
    F --> G
    G --> H
    H --> GW
    GW --> GW2
    GW2 -->|Confirmed| J
    GW2 -->|Rejected| J
    J -->|Success| K
    K --> O
    J -->|Failure| L
    L --> M
    M --> P
```

**Explanation:**
The two-step flow (validation → confirmation screen → payment) gives the user a final chance to review before funds move — directly addressing the End User's pain point of accidental payments. The rollback on gateway failure mirrors the P2P transfer pattern for consistency.

| Element | Requirement |
|---|---|
| Balance guard | FR-11 |
| Confirmation screen | NFR-01 (usability) |
| Provider webhook confirmation | FR-10 |
| Rollback on failure | FR-08 |

---

## 6. Admin: Suspend User Account Workflow

```mermaid
flowchart TD
    Start([🟢 Start]) --> A

    subgraph Admin ["🛠️ System Administrator"]
        A[Navigate to User Management] --> B[Search for user by name/email/phone]
        B --> C{User found?}
        C -->|No| D[Display: No account found]
        D --> B
        C -->|Yes| E[View user profile and current status]
        E --> F{Account already suspended?}
        F -->|Yes| G[Display: Already suspended]
        G --> Stop2([🔴 End])
        F -->|No| H[Tap Suspend Account]
        H --> I[Enter mandatory reason text]
        I --> J[Tap Confirm]
        J --> K{Confirm action?}
        K -->|Cancel| Stop3([🔴 End — No change])
        K -->|Confirm| L[System applies suspension]
    end

    subgraph System ["⚙️ System"]
        L --> M[Update user status = SUSPENDED in DB]
        M --> N[Freeze associated wallet]
        N --> O[Revoke all active JWT tokens]
        O --> P[Write audit log entry]
        P --> Q[Display: Account suspended successfully]
    end

    subgraph AuditLog ["📋 Audit Log"]
        P --> R[(Store: admin ID, user ID, reason, timestamp)]
    end

    Q --> Stop4([🔴 End])
```

**Explanation:**
The parallel actions of freezing the wallet and revoking JWT tokens happen together after the DB status update — ensuring the user cannot complete an in-flight transaction during the suspension window. The mandatory reason field and audit log write directly address the Compliance Officer's requirement for traceable admin actions.

| Element | Requirement |
|---|---|
| Status update | FR-15 |
| JWT revocation | NFR-02 |
| Wallet freeze | FR-15 (side effect) |
| Audit log write | FR-15, NFR-11 |

---

## 7. Top Up Wallet Workflow

```mermaid
flowchart TD
    Start([🟢 Start]) --> A

    subgraph User ["👤 User"]
        A[Navigate to Top Up Wallet] --> B[Enter card details and amount]
        B --> C[Tap Proceed]
        J[View error: Card declined] --> B
        K[View error: Service unavailable] --> B
        L[View updated balance] --> Stop2([🔴 End])
    end

    subgraph System ["⚙️ System"]
        D{Validate amount > 0?}
        E[Call Payment Gateway with card details]
        F{Gateway response?}
        G[Credit wallet balance]
        H[Write transaction record — TOP_UP]
        I[Return success + new balance]
        M[Return error — no balance change]
    end

    subgraph Gateway ["🏦 Payment Gateway"]
        GW[Process card charge]
        GW2{Card authorised?}
    end

    subgraph Notifications ["🔔 Notification Service"]
        N[Send push: Wallet topped up — R amount]
    end

    C --> D
    D -->|Invalid| J
    D -->|Valid| E
    E --> GW
    GW --> GW2
    GW2 -->|Authorised| F
    GW2 -->|Declined| F
    F -->|Success| G
    G --> H
    H --> I
    H --> N
    I --> L
    F -->|Declined| J
    F -->|Timeout| K
    K --> M
    J --> M
```

**Explanation:**
The push notification after a successful top-up runs in parallel with returning the updated balance to the UI — consistent with the notification pattern used in P2P transfers, ensuring the user is always informed regardless of which screen they are on. This addresses the End User's need for real-time balance awareness.

| Element | Requirement |
|---|---|
| Gateway card processing | FR-06 |
| Balance credit on confirmation only | FR-06 (acceptance criteria) |
| Transaction record | FR-12 (history) |
| Push notification | FR-09 pattern |

---

## 8. View and Filter Transaction History Workflow

```mermaid
flowchart TD
    Start([🟢 Start]) --> A

    subgraph User ["👤 User"]
        A[Navigate to Transaction History] --> B[System loads default view]
        B --> C{Apply filters?}
        C -->|No| D[View paginated list — 20 items]
        C -->|Yes| E[Select filter: type / date range / status]
        E --> F[Tap Apply Filters]
        F --> G{Results found?}
        G -->|No| H[Display: No transactions match filters]
        G -->|Yes| D
        D --> I{Load more?}
        I -->|Yes — tap next page| J[Fetch next 20 transactions]
        J --> D
        I -->|No| K{Tap transaction?}
        K -->|Yes| L[View full transaction detail screen]
        L --> D
        K -->|No| Stop([🔴 End])
        H --> Stop2([🔴 End])
    end

    subgraph System ["⚙️ System"]
        B --> Q[Query DB: SELECT * FROM transactions WHERE user_id = ? ORDER BY created_at DESC LIMIT 20]
        F --> R[Query DB with filter predicates applied]
        J --> S[Query DB: OFFSET paginated]
        Q --> T{Query time ≤ 2 seconds?}
        T -->|Yes| D
        T -->|No| U[Log slow query alert for DevOps]
        U --> D
    end
```

**Explanation:**
The slow query detection branch (> 2 seconds) does not block the user — the data still returns, but a DevOps alert is raised for investigation. This balances the End User's need for responsiveness (NFR-12) with the IT Engineer's need for observability. The pagination loop ensures large datasets never cause memory or performance issues on the mobile client.

| Element | Requirement |
|---|---|
| Default paginated load | FR-12 |
| Filter application | FR-13 |
| ≤ 2 second target | NFR-12 |
| Slow query alert | NFR-07 (observability) |

---

*SwiftPay — ACTIVITY_DIAGRAMS.md | Software Engineering Assignment 8*
