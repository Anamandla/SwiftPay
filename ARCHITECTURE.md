# ARCHITECTURE.md — SwiftPay Mobile Payment App

This document describes the software architecture of SwiftPay using the **C4 Model**, which organises diagrams into four levels of abstraction: **Context → Container → Component → Code**. Diagrams are written in **Mermaid**, a text-based diagramming language supported natively by GitHub.

> **C4 Model Quick Reference:**
> - **Level 1 – Context:** Who uses the system and what external systems does it interact with?
> - **Level 2 – Container:** What are the major deployable units (apps, databases, APIs)?
> - **Level 3 – Component:** What are the key building blocks inside each container?
> - **Level 4 – Code:** Class/module level detail (out of scope for this phase)

---
 * 
## Level 1 — System Context Diagram

> Shows SwiftPay as a black box and illustrates all external actors and systems that interact with it.

```mermaid
graph TD
    User["👤 End User\n(Mobile App User)\nSends & receives money,\npays bills, views history"]
    Admin["🛠️ Admin\n(System Operator)\nManages users & monitors\ntransactions"]
    SwiftPay["💸 SwiftPay\n(Mobile Payment System)\nProvides digital wallet,\nP2P transfers, bill payments"]
    PayGateway["🏦 Payment Gateway\n(e.g. Peach Payments)\nProcesses real money movement\nbetween financial institutions"]
    FCM["🔔 Firebase Cloud Messaging\n(Google FCM)\nDelivers push notifications\nto mobile devices"]
    EmailService["📧 Email Service\n(e.g. SendGrid)\nSends OTP and\ntransaction confirmation emails"]

    User -- "Uses via mobile app\n(HTTPS)" --> SwiftPay
    Admin -- "Manages via admin portal\n(HTTPS)" --> SwiftPay
    SwiftPay -- "Processes payments via\nREST API (HTTPS)" --> PayGateway
    SwiftPay -- "Sends push notifications\nvia FCM API" --> FCM
    FCM -- "Delivers notifications to" --> User
    SwiftPay -- "Sends emails via\nSMTP/API" --> EmailService
    EmailService -- "Delivers emails to" --> User
```
![Click Here](System-Context-Diagram.png)
---

## Level 2 — Container Diagram

> Zooms into SwiftPay and shows the major containers (deployable units): the mobile app, backend API, database, and cache.

```mermaid
graph TD
    User["👤 End User"]
    Admin["🛠️ Admin"]

    subgraph SwiftPay System
        MobileApp["📱 Mobile App\n(React Native)\nUser-facing interface for\nlogin, transfers, history,\nbill payments"]
        AdminPortal["🖥️ Admin Web Portal\n(React.js)\nAdmin dashboard for\nuser & transaction management"]
        APIServer["⚙️ Backend API Server\n(Node.js + Express)\nHandles all business logic:\nauthentication, wallet operations,\ntransaction processing"]
        DB["🗄️ Primary Database\n(PostgreSQL)\nStores users, wallets,\ntransactions, and audit logs"]
        Cache["⚡ Cache Layer\n(Redis)\nStores session tokens\nand temporary OTPs"]
    end

    PayGateway["🏦 Payment Gateway\n(External)"]
    FCM["🔔 Firebase FCM\n(External)"]
    EmailService["📧 Email Service\n(External)"]

    User -- "Uses (HTTPS)" --> MobileApp
    Admin -- "Uses (HTTPS)" --> AdminPortal
    MobileApp -- "REST API calls\n(JSON over HTTPS)" --> APIServer
    AdminPortal -- "REST API calls\n(JSON over HTTPS)" --> APIServer
    APIServer -- "Reads & writes\n(SQL)" --> DB
    APIServer -- "Reads & writes\n(Redis protocol)" --> Cache
    APIServer -- "Payment requests\n(REST/HTTPS)" --> PayGateway
    APIServer -- "Push notifications\n(FCM SDK)" --> FCM
    APIServer -- "Email dispatch\n(SMTP/API)" --> EmailService
```
![Click Here](Container-Diagram.png)
---

## Level 3 — Component Diagram (Backend API Server)

> Zooms into the Backend API Server container and shows its internal components (modules/services).

```mermaid
graph TD
    MobileApp["📱 Mobile App"]
    AdminPortal["🖥️ Admin Portal"]

    subgraph Backend API Server - Node.js + Express
        AuthModule["🔐 Auth Module\nHandles registration, login,\nJWT issuance, OTP verification,\npassword reset"]
        UserModule["👤 User Module\nManages user profiles,\naccount status (active/suspended),\nuser lookup by phone"]
        WalletModule["💰 Wallet Module\nManages wallet balances,\ncredit/debit operations,\nbalance enquiry"]
        TransactionModule["💳 Transaction Module\nOrchestrates P2P transfers,\nbill payments, transaction\nrecording and rollback"]
        NotificationModule["🔔 Notification Module\nTriggers push notifications\nvia FCM and email alerts\nvia Email Service"]
        AdminModule["🛠️ Admin Module\nExposes admin-only endpoints:\nuser management, transaction\nmonitoring, account suspension"]
        APIGateway["🚪 API Gateway / Router\n(Express Router)\nRoutes incoming HTTP requests\nto the correct module,\napplies JWT middleware"]
    end

    DB["🗄️ PostgreSQL Database"]
    Cache["⚡ Redis Cache"]
    PayGateway["🏦 Payment Gateway"]
    FCM["🔔 Firebase FCM"]
    EmailService["📧 Email Service"]

    MobileApp -- "HTTP Requests" --> APIGateway
    AdminPortal -- "HTTP Requests" --> APIGateway

    APIGateway --> AuthModule
    APIGateway --> UserModule
    APIGateway --> WalletModule
    APIGateway --> TransactionModule
    APIGateway --> AdminModule

    AuthModule -- "Store/retrieve OTPs" --> Cache
    AuthModule -- "Read/write users" --> DB
    UserModule -- "Read/write users" --> DB
    WalletModule -- "Read/write wallets" --> DB
    TransactionModule -- "Record transactions" --> DB
    TransactionModule -- "Update wallet balance" --> WalletModule
    TransactionModule -- "Send payment to gateway" --> PayGateway
    TransactionModule -- "Trigger notification" --> NotificationModule
    NotificationModule -- "Push alerts" --> FCM
    NotificationModule -- "Email alerts" --> EmailService
    AdminModule -- "Query users & transactions" --> DB
```
![Click Here](Component-Diagram(Backend-API-Server).png)
---

## Level 3 — Component Diagram (Mobile App)

> Zooms into the React Native Mobile App and shows its internal screens and service components.

```mermaid
graph TD
    User["👤 End User"]

    subgraph Mobile App - React Native
        AuthScreen["🔐 Auth Screens\nLogin, Registration,\nForgot Password, OTP Verify"]
        HomeScreen["🏠 Home / Dashboard Screen\nWallet balance display,\nquick action buttons"]
        TransferScreen["💸 Transfer Screen\nSend money by phone number,\namount entry, confirmation"]
        HistoryScreen["📋 Transaction History Screen\nList of past transactions\nwith status and details"]
        BillScreen["🧾 Bill Payment Screen\nSelect provider, enter\nreference & amount"]
        NotifScreen["🔔 Notifications Screen\nIn-app notification\nlist and alerts"]
        APIService["🌐 API Service Layer\n(Axios)\nCentralised HTTP client,\nJWT token attachment,\nerror handling"]
        AuthStore["💾 Auth Store\n(AsyncStorage + Context)\nStores JWT token\nand user session locally"]
    end

    BackendAPI["⚙️ Backend API Server"]
    FCM["🔔 Firebase FCM\n(Push Notifications)"]

    User --> AuthScreen
    User --> HomeScreen
    User --> TransferScreen
    User --> HistoryScreen
    User --> BillScreen
    User --> NotifScreen

    AuthScreen --> APIService
    HomeScreen --> APIService
    TransferScreen --> APIService
    HistoryScreen --> APIService
    BillScreen --> APIService

    AuthScreen --> AuthStore
    APIService --> AuthStore

    APIService -- "REST calls (HTTPS)" --> BackendAPI
    FCM -- "Delivers push alerts" --> NotifScreen
```
![Click Here](Component-Diagram(Mobile-App).png)
---

## End-to-End Flow Summary

The diagram below illustrates a complete P2P money transfer from a user's perspective, end to end:

```mermaid
sequenceDiagram
    participant U as 👤 User (Mobile App)
    participant API as ⚙️ Backend API
    participant DB as 🗄️ PostgreSQL
    participant GW as 🏦 Payment Gateway
    participant FCM as 🔔 Firebase FCM

    U->>API: POST /transactions/transfer (JWT, amount, recipient phone)
    API->>DB: Validate sender wallet balance
    DB-->>API: Balance confirmed
    API->>DB: Debit sender wallet (atomic transaction)
    API->>GW: Request fund settlement
    GW-->>API: Settlement confirmed
    API->>DB: Credit recipient wallet (atomic transaction)
    API->>DB: Record transaction log
    API->>FCM: Trigger push notification (sender + recipient)
    FCM-->>U: "Transfer successful" push notification
    API-->>U: 200 OK — Transaction complete
```
![Click Here](End-to-End-Flow-Summary.png)
---

*SwiftPay — ARCHITECTURE.md | Software Engineering Assignment 3*
