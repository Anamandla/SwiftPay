# DOMAIN_MODEL.md — Domain Model Documentation
## SwiftPay Mobile Payment App

> **Assignment 9 | Domain Model**
> Identifies core domain entities, their attributes, responsibilities, relationships, and business rules.
> Aligned with SRD.md (Assignment 4), USE_CASES.md (Assignment 5), and STATE_DIAGRAMS.md (Assignment 8).

---

## 1. Domain Overview

SwiftPay operates in the **mobile banking / digital payments** domain. The core domain revolves around the movement of money between users via digital wallets, with supporting entities managing identity, security, notifications, and compliance. The domain is governed by strict business rules around atomicity, balance integrity, and audit traceability.

---

## 2. Domain Entities

### Entity 1 — User

| Field | Detail |
|---|---|
| **Description** | A registered individual who holds a SwiftPay account and wallet. The central actor in all financial operations. |
| **Attributes** | `userId: UUID`, `name: String`, `email: String`, `phone: String`, `passwordHash: String`, `status: Enum(UNVERIFIED, ACTIVE, SUSPENDED, DELETED)`, `createdAt: DateTime`, `updatedAt: DateTime` |
| **Methods** | `register()`, `login()`, `logout()`, `resetPassword()`, `updateProfile()`, `suspend()`, `reactivate()`, `delete()` |
| **Relationships** | Owns one `Wallet` (composition); initiates many `Transactions`; generates many `Notifications`; has many `Sessions`; subject of many `AuditLog` entries |

**Business Rules:**
- A user must have a unique email AND a unique phone number
- A user cannot transact while status = SUSPENDED or UNVERIFIED
- Deleting a user triggers POPIA-compliant PII scrubbing but retains anonymised transaction records

---

### Entity 2 — Wallet

| Field | Detail |
|---|---|
| **Description** | A digital ZAR wallet owned by exactly one User. The financial ledger for all debits and credits. |
| **Attributes** | `walletId: UUID`, `userId: UUID`, `balance: Decimal(10,2)`, `currency: String = "ZAR"`, `status: Enum(ACTIVE, FROZEN, CLOSED)`, `createdAt: DateTime`, `updatedAt: DateTime` |
| **Methods** | `credit(amount)`, `debit(amount)`, `freeze()`, `unfreeze()`, `close()`, `getBalance()`, `validateSufficientFunds(amount)` |
| **Relationships** | Belongs to one `User` (composition); referenced by many `Transactions` as sender or recipient wallet |

**Business Rules:**
- Balance can never go below R0.00 (no overdraft)
- `debit()` must call `validateSufficientFunds()` before modifying balance
- A wallet is automatically FROZEN when its owner's account is SUSPENDED
- All balance modifications must occur inside a database transaction (ACID)

---

### Entity 3 — Transaction

| Field | Detail |
|---|---|
| **Description** | An immutable record of every financial event in SwiftPay — transfers, top-ups, and bill payments. The financial audit trail. |
| **Attributes** | `transactionId: UUID`, `senderWalletId: UUID`, `recipientWalletId: UUID (nullable)`, `type: Enum(TRANSFER, TOP_UP, BILL_PAYMENT)`, `amount: Decimal(10,2)`, `currency: String`, `status: Enum(INITIATED, VALIDATING, PROCESSING, COMPLETED, FAILED, ROLLED_BACK, DISPUTED, REFUNDED)`, `gatewayReference: String`, `failureReason: String`, `createdAt: DateTime`, `completedAt: DateTime` |
| **Methods** | `initiate()`, `validate()`, `process()`, `complete()`, `fail(reason)`, `rollback()`, `dispute()`, `refund()`, `getStatus()` |
| **Relationships** | References two `Wallet` objects (sender and recipient); triggers `Notification` objects; appears in `AuditLog` on dispute/refund; processed via `PaymentGateway` |

**Business Rules:**
- A Transaction record is immutable once status = COMPLETED — no updates, only new records
- `rollback()` can only be called if status is PROCESSING or PENDING_GATEWAY
- Amount must be > R0.00 and ≤ the sender's current balance at time of initiation
- Every transaction must have a `gatewayReference` before status can become COMPLETED

---

### Entity 4 — Notification

| Field | Detail |
|---|---|
| **Description** | A push notification dispatched to a User's registered device via Firebase FCM following a transaction event. |
| **Attributes** | `notificationId: UUID`, `userId: UUID`, `transactionId: UUID`, `type: Enum(TRANSFER_SENT, TRANSFER_RECEIVED, BILL_PAID, TOP_UP_SUCCESS, ACCOUNT_SUSPENDED)`, `title: String`, `body: String`, `status: Enum(QUEUED, SENDING, DELIVERED, FAILED, READ, EXPIRED)`, `fcmToken: String`, `retryCount: Integer`, `createdAt: DateTime`, `deliveredAt: DateTime` |
| **Methods** | `send()`, `retry()`, `markRead()`, `expire()`, `getStatus()` |
| **Relationships** | Belongs to one `User`; associated with one `Transaction`; dispatched via `NotificationService` |

**Business Rules:**
- Maximum 3 retry attempts before status transitions to FAILED
- A FAILED notification does not affect the associated transaction's status
- FCM tokens must be refreshed on every app launch; stale tokens trigger automatic re-registration

---

### Entity 5 — OTP (One-Time Password)

| Field | Detail |
|---|---|
| **Description** | A short-lived 6-digit code stored in Redis, used exclusively for password reset verification. |
| **Attributes** | `otpId: UUID`, `userId: UUID`, `code: String (hashed)`, `attemptCount: Integer`, `status: Enum(GENERATED, SENT, PENDING, VERIFIED, EXPIRED, INVALIDATED)`, `expiresAt: DateTime`, `createdAt: DateTime` |
| **Methods** | `generate()`, `send()`, `verify(inputCode)`, `expire()`, `invalidate()`, `incrementAttempt()` |
| **Relationships** | Belongs to one `User`; stored in `RedisCache`; triggers `EmailService` on generation |

**Business Rules:**
- OTP expires automatically after 10 minutes (Redis TTL)
- After 3 incorrect `verify()` attempts, status transitions to INVALIDATED regardless of time remaining
- Only one active OTP may exist per user at a time — generating a new one invalidates the previous

---

### Entity 6 — AuditLog

| Field | Detail |
|---|---|
| **Description** | An immutable record of every privileged administrative action taken on the platform. Supports compliance and regulatory review. |
| **Attributes** | `logId: UUID`, `adminId: UUID`, `targetUserId: UUID`, `action: Enum(SUSPEND, REACTIVATE, DELETE, REFUND, ESCALATE)`, `reason: String`, `previousStatus: String`, `newStatus: String`, `ipAddress: String`, `createdAt: DateTime` |
| **Methods** | `create()`, `getByAdmin()`, `getByUser()`, `archive()`, `flag()` |
| **Relationships** | References one admin `User` (actor); references one target `User` (subject); optionally references a `Transaction` (for refund actions) |

**Business Rules:**
- AuditLog entries are immutable — no update or delete operations are permitted
- Every admin action on User or Transaction objects must produce an AuditLog entry atomically
- Entries older than 90 days are archived to cold storage; retained for a minimum of 12 months (POPIA)

---

### Entity 7 — Session (JWT)

| Field | Detail |
|---|---|
| **Description** | Represents an authenticated user session backed by a JWT access token and a refresh token stored in Redis. |
| **Attributes** | `sessionId: UUID`, `userId: UUID`, `accessTokenHash: String`, `refreshTokenHash: String`, `deviceInfo: String`, `ipAddress: String`, `status: Enum(ACTIVE, EXPIRED, REVOKED)`, `issuedAt: DateTime`, `accessExpiresAt: DateTime`, `refreshExpiresAt: DateTime` |
| **Methods** | `issue()`, `validate()`, `refresh()`, `revoke()`, `isExpired()` |
| **Relationships** | Belongs to one `User`; stored/validated against `RedisCache` |

**Business Rules:**
- Access token TTL = 24 hours; refresh token TTL = 30 days
- Suspending a User must immediately revoke all their active Sessions
- A refresh token can only be used once — it is rotated on each use

---

## 3. Entity Relationship Summary

```
User ─────────────── Wallet          (1 to 1, composition)
User ─────────────── Transaction     (1 to many, as sender)
User ─────────────── Notification    (1 to many)
User ─────────────── Session         (1 to many)
User ─────────────── OTP             (1 to 0..1, at most one active)
User ─────────────── AuditLog        (1 to many, as subject)
Wallet ───────────── Transaction     (1 to many, as sender or recipient wallet)
Transaction ──────── Notification    (1 to many)
Transaction ──────── AuditLog        (1 to 0..1, on dispute/refund)
```

---

## 4. Business Rules Summary

| Rule ID | Entity | Rule |
|---|---|---|
| BR-01 | User | Email and phone must be unique across all users |
| BR-02 | User | SUSPENDED or UNVERIFIED users cannot initiate transactions |
| BR-03 | Wallet | Balance cannot go below R0.00 |
| BR-04 | Wallet | All balance changes must be ACID-compliant database transactions |
| BR-05 | Wallet | Wallet is auto-frozen when owner is suspended |
| BR-06 | Transaction | Amount must be > R0.00 and ≤ sender balance at initiation time |
| BR-07 | Transaction | COMPLETED transactions are immutable |
| BR-08 | Transaction | Rollback only valid from PROCESSING or PENDING_GATEWAY states |
| BR-09 | OTP | Expires after 10 minutes; invalidated after 3 failed attempts |
| BR-10 | OTP | Only one active OTP per user at a time |
| BR-11 | Session | Access token = 24hr TTL; refresh token = 30 days |
| BR-12 | Session | All sessions revoked immediately on account suspension |
| BR-13 | AuditLog | Every admin action must produce an AuditLog entry atomically |
| BR-14 | AuditLog | AuditLog entries are immutable; retained ≥ 12 months |
| BR-15 | Notification | Max 3 retry attempts; failure does not affect transaction status |

---

*SwiftPay — DOMAIN_MODEL.md | Software Engineering Assignment 9*
