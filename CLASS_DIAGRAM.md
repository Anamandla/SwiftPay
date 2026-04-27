# CLASS_DIAGRAM.md — Class Diagram
## SwiftPay Mobile Payment App

> **Assignment 9 | Class Diagram in Mermaid.js**
> Full UML class diagram including attributes, methods, relationships, multiplicity, and design notes.

---

## Class Diagram

```mermaid
classDiagram

    %% ─────────────────────────────────────────
    %% CORE DOMAIN CLASSES
    %% ─────────────────────────────────────────

    class User {
        -userId : UUID
        -name : String
        -email : String
        -phone : String
        -passwordHash : String
        -status : UserStatus
        -createdAt : DateTime
        -updatedAt : DateTime
        +register(name, email, phone, password) User
        +login(credential, password) Session
        +logout(sessionId) void
        +resetPassword(otpCode, newPassword) void
        +updateProfile(name, phone) void
        +suspend(adminId, reason) void
        +reactivate(adminId, reason) void
        +delete() void
        +getWallet() Wallet
        +getTransactionHistory(filters) List~Transaction~
    }

    class Wallet {
        -walletId : UUID
        -userId : UUID
        -balance : Decimal
        -currency : String
        -status : WalletStatus
        -createdAt : DateTime
        -updatedAt : DateTime
        +credit(amount) void
        +debit(amount) void
        +freeze() void
        +unfreeze() void
        +close() void
        +getBalance() Decimal
        +validateSufficientFunds(amount) Boolean
    }

    class Transaction {
        -transactionId : UUID
        -senderWalletId : UUID
        -recipientWalletId : UUID
        -type : TransactionType
        -amount : Decimal
        -currency : String
        -status : TransactionStatus
        -gatewayReference : String
        -failureReason : String
        -createdAt : DateTime
        -completedAt : DateTime
        +initiate() void
        +validate() Boolean
        +process() void
        +complete(gatewayRef) void
        +fail(reason) void
        +rollback() void
        +dispute() void
        +refund() void
        +getStatus() TransactionStatus
    }

    class Notification {
        -notificationId : UUID
        -userId : UUID
        -transactionId : UUID
        -type : NotificationType
        -title : String
        -body : String
        -status : NotificationStatus
        -fcmToken : String
        -retryCount : Integer
        -createdAt : DateTime
        -deliveredAt : DateTime
        +send() void
        +retry() void
        +markRead() void
        +expire() void
        +getStatus() NotificationStatus
    }

    class OTP {
        -otpId : UUID
        -userId : UUID
        -codeHash : String
        -attemptCount : Integer
        -status : OTPStatus
        -expiresAt : DateTime
        -createdAt : DateTime
        +generate() String
        +send(email) void
        +verify(inputCode) Boolean
        +expire() void
        +invalidate() void
        +incrementAttempt() void
        +isExpired() Boolean
    }

    class AuditLog {
        -logId : UUID
        -adminId : UUID
        -targetUserId : UUID
        -transactionId : UUID
        -action : AdminAction
        -reason : String
        -previousStatus : String
        -newStatus : String
        -ipAddress : String
        -createdAt : DateTime
        +create(adminId, targetId, action, reason) AuditLog
        +getByAdmin(adminId) List~AuditLog~
        +getByUser(userId) List~AuditLog~
        +archive() void
        +flag(reason) void
    }

    class Session {
        -sessionId : UUID
        -userId : UUID
        -accessTokenHash : String
        -refreshTokenHash : String
        -deviceInfo : String
        -ipAddress : String
        -status : SessionStatus
        -issuedAt : DateTime
        -accessExpiresAt : DateTime
        -refreshExpiresAt : DateTime
        +issue(userId) Session
        +validate(token) Boolean
        +refresh(refreshToken) Session
        +revoke() void
        +isExpired() Boolean
    }

    %% ─────────────────────────────────────────
    %% EXTERNAL SERVICE INTERFACES
    %% ─────────────────────────────────────────

    class PaymentGateway {
        <<interface>>
        +processTransfer(amount, senderId, recipientId) GatewayResponse
        +processTopUp(amount, cardDetails) GatewayResponse
        +processBillPayment(amount, providerId, reference) GatewayResponse
        +getSettlementStatus(gatewayRef) GatewayResponse
    }

    class PeachPaymentsAdapter {
        -apiKey : String
        -baseUrl : String
        -timeoutMs : Integer
        +processTransfer(amount, senderId, recipientId) GatewayResponse
        +processTopUp(amount, cardDetails) GatewayResponse
        +processBillPayment(amount, providerId, reference) GatewayResponse
        +getSettlementStatus(gatewayRef) GatewayResponse
        -buildRequest(payload) HttpRequest
        -parseResponse(response) GatewayResponse
        -handleTimeout() GatewayResponse
    }

    class NotificationService {
        <<interface>>
        +sendPush(userId, title, body, fcmToken) void
        +queueNotification(notification) void
        +retryFailed() void
    }

    class FCMAdapter {
        -fcmApiKey : String
        -maxRetries : Integer
        -retryDelayMs : Integer
        +sendPush(userId, title, body, fcmToken) void
        +queueNotification(notification) void
        +retryFailed() void
        -callFCMApi(payload) FCMResponse
        -handleInvalidToken(fcmToken) void
    }

    class EmailService {
        <<interface>>
        +sendOTP(email, otpCode) void
        +sendWelcome(email, name) void
        +sendTransactionAlert(email, transaction) void
    }

    class SendGridAdapter {
        -apiKey : String
        -fromAddress : String
        +sendOTP(email, otpCode) void
        +sendWelcome(email, name) void
        +sendTransactionAlert(email, transaction) void
        -buildEmailPayload(to, subject, body) EmailPayload
    }

    %% ─────────────────────────────────────────
    %% ENUMERATIONS
    %% ─────────────────────────────────────────

    class UserStatus {
        <<enumeration>>
        UNVERIFIED
        ACTIVE
        SUSPENDED
        DELETED
    }

    class WalletStatus {
        <<enumeration>>
        ACTIVE
        FROZEN
        CLOSED
    }

    class TransactionType {
        <<enumeration>>
        TRANSFER
        TOP_UP
        BILL_PAYMENT
    }

    class TransactionStatus {
        <<enumeration>>
        INITIATED
        VALIDATING
        PROCESSING
        PENDING_GATEWAY
        COMPLETED
        FAILED
        ROLLED_BACK
        DISPUTED
        REFUNDED
    }

    class NotificationStatus {
        <<enumeration>>
        QUEUED
        SENDING
        DELIVERED
        FAILED
        READ
        EXPIRED
    }

    class NotificationType {
        <<enumeration>>
        TRANSFER_SENT
        TRANSFER_RECEIVED
        BILL_PAID
        TOP_UP_SUCCESS
        ACCOUNT_SUSPENDED
    }

    class OTPStatus {
        <<enumeration>>
        GENERATED
        SENT
        PENDING
        VERIFIED
        EXPIRED
        INVALIDATED
    }

    class SessionStatus {
        <<enumeration>>
        ACTIVE
        EXPIRED
        REVOKED
    }

    class AdminAction {
        <<enumeration>>
        SUSPEND
        REACTIVATE
        DELETE
        REFUND
        ESCALATE
    }

    %% ─────────────────────────────────────────
    %% RELATIONSHIPS
    %% ─────────────────────────────────────────

    %% Composition — Wallet cannot exist without User
    User "1" *-- "1" Wallet : owns

    %% Association — User initiates many Transactions
    User "1" --> "0..*" Transaction : initiates

    %% Association — User receives many Notifications
    User "1" --> "0..*" Notification : receives

    %% Association — User has many Sessions
    User "1" --> "0..*" Session : authenticates via

    %% Association — User has at most one active OTP
    User "1" --> "0..1" OTP : has

    %% Association — User is subject of many AuditLog entries
    User "1" --> "0..*" AuditLog : subject of

    %% Association — Wallet is referenced in Transactions
    Wallet "1" --> "0..*" Transaction : senderWallet
    Wallet "1" --> "0..*" Transaction : recipientWallet

    %% Association — Transaction triggers Notifications
    Transaction "1" --> "0..*" Notification : triggers

    %% Association — Transaction optionally appears in AuditLog
    Transaction "0..1" --> "0..1" AuditLog : logged in

    %% Inheritance — Adapters implement interfaces
    PaymentGateway <|.. PeachPaymentsAdapter : implements
    NotificationService <|.. FCMAdapter : implements
    EmailService <|.. SendGridAdapter : implements

    %% Dependency — OTP uses EmailService
    OTP ..> EmailService : sends via

    %% Dependency — Transaction uses PaymentGateway
    Transaction ..> PaymentGateway : settled via

    %% Dependency — Notification uses NotificationService
    Notification ..> NotificationService : dispatched via

    %% Enum associations
    User ..> UserStatus : status
    Wallet ..> WalletStatus : status
    Transaction ..> TransactionType : type
    Transaction ..> TransactionStatus : status
    Notification ..> NotificationStatus : status
    Notification ..> NotificationType : type
    OTP ..> OTPStatus : status
    Session ..> SessionStatus : status
    AuditLog ..> AdminAction : action
```

---

## Key Design Decisions

### 1. Composition vs. Association for User → Wallet
The `User` to `Wallet` relationship is modelled as **composition** (filled diamond) rather than association. This reflects the business rule that a Wallet cannot exist independently of a User — if the User is deleted, the Wallet is closed and archived. Every other relationship is a standard association because the referenced objects have independent lifecycles.

### 2. Interface + Adapter Pattern for External Services
`PaymentGateway`, `NotificationService`, and `EmailService` are modelled as **interfaces** with concrete adapter implementations (`PeachPaymentsAdapter`, `FCMAdapter`, `SendGridAdapter`). This design decision decouples the domain from specific third-party providers — if SwiftPay switches from Peach Payments to Stripe, only the adapter changes. The domain classes (`Transaction`, `Notification`, `OTP`) depend on the interface, never the concrete class. This maps directly to NFR-06 (maintainability).

### 3. Enumerations for All Status Fields
Every status field (`UserStatus`, `TransactionStatus`, etc.) is modelled as a named enumeration rather than a raw string. This prevents invalid state values at the application layer and maps directly to the state transition diagrams in Assignment 8 — every enumeration value corresponds to a named state in those diagrams.

### 4. Transaction as an Immutable Audit Record
`Transaction` has no `update()` method. Once created, transaction records can only move forward through states via specific methods (`complete()`, `fail()`, `rollback()`). This immutability is a deliberate design decision reflecting BR-07 (COMPLETED transactions cannot be modified) and the financial industry's requirement for tamper-proof ledgers.

### 5. AuditLog Separation from Transaction
`AuditLog` is a separate class from `Transaction` rather than a field on `User`. This separation means that administrative actions (suspend, delete, escalate) and financial actions (transfer, payment) are tracked in different tables with different retention and access control policies — matching NFR-11 (12-month audit retention) and the Compliance Officer's concerns from Assignment 4.

---

## Traceability to Prior Assignments

| Class / Relationship | Assignment 4 (FR/NFR) | Assignment 5 (UC) | Assignment 8 (State) |
|---|---|---|---|
| `User` + `UserStatus` | FR-01, FR-02, FR-15 | UC-01, UC-02, UC-10 | User Account state diagram |
| `Wallet` + `WalletStatus` | FR-04, FR-05, FR-06 | UC-04, UC-06 | Wallet state diagram |
| `Transaction` + `TransactionStatus` | FR-07, FR-08, FR-10 | UC-05, UC-07 | Transaction state diagram |
| `Notification` + `NotificationStatus` | FR-09 | UC-09 | Push Notification state diagram |
| `OTP` + `OTPStatus` | FR-03 | UC-03 | OTP state diagram |
| `Session` + `SessionStatus` | FR-02, NFR-02 | UC-02 | JWT Session state diagram |
| `AuditLog` + `AdminAction` | FR-15, NFR-11 | UC-10 | Admin Action state diagram |
| `PaymentGateway` interface | FR-07, FR-10 | UC-05, UC-07 | Transaction activity diagram |
| `NotificationService` interface | FR-09 | UC-09 | Notification state diagram |
| `EmailService` interface | FR-03 | UC-03 | OTP state diagram |

---

*SwiftPay — CLASS_DIAGRAM.md | Software Engineering Assignment 9*
