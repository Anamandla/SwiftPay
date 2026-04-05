# AGILE_PLANNING.md — Agile User Stories, Backlog & Sprint Planning
## SwiftPay Mobile Payment App

> **Assignment 6 | Agile Planning Document**
> Builds directly on functional requirements (SRD.md / Assignment 4) and use cases (USE_CASES.md / Assignment 5).

---

## 1. User Stories

User stories follow the format: **"As a [role], I want [action] so that [benefit]."**
All stories satisfy the **INVEST** criteria: Independent, Negotiable, Valuable, Estimable, Small, Testable.

| Story ID | Linked FR / UC | User Story | Acceptance Criteria | Priority |
|---|---|---|---|---|
| US-001 | FR-01 / UC-01 | As a **new user**, I want to register an account with my name, email, phone, and password so that I can access SwiftPay services. | Registration completes in ≤ 3 seconds; duplicate email/phone rejected with clear error; wallet provisioned at R0.00. | High |
| US-002 | FR-02 / UC-02 | As a **registered user**, I want to log in with my email and password so that I can securely access my account and wallet. | JWT token issued within 2 seconds; invalid credentials return a clear error; suspended accounts blocked with explanation. | High |
| US-003 | FR-03 / UC-03 | As a **user who forgot their password**, I want to receive a one-time PIN via email so that I can reset my password without losing access to my account. | OTP delivered within 30 seconds; OTP expires after 10 minutes; password updated on valid OTP submission. | High |
| US-004 | FR-04 / UC-01 | As a **new user**, I want a digital wallet automatically created when I register so that I can immediately start sending and receiving money. | Wallet created within 1 second of registration; starting balance is R0.00; wallet linked to user account. | High |
| US-005 | FR-05 / UC-04 | As a **logged-in user**, I want to see my current wallet balance on the home screen so that I always know how much money I have available. | Balance displayed on dashboard load; reflects latest confirmed transaction; never shows data older than 5 seconds. | High |
| US-006 | FR-07, FR-08 / UC-05 | As a **sender**, I want to transfer money to another SwiftPay user using their phone number so that I can pay people quickly without needing their bank details. | Transfer completes in ≤ 5 seconds; sender debited and recipient credited atomically; failed gateway triggers full rollback. | High |
| US-007 | FR-09 / UC-05 | As a **recipient**, I want to receive a push notification immediately when money is sent to me so that I know funds have arrived without opening the app. | FCM notification delivered within 3 seconds of transfer; notification shows amount and sender name. | High |
| US-008 | FR-06 / UC-06 | As a **user**, I want to top up my wallet using my debit or credit card so that I can add funds to SwiftPay without going to a bank. | Top-up reflects in balance within 10 seconds of gateway confirmation; failed card shows clear error; balance unchanged on failure. | Medium |
| US-009 | FR-10, FR-11 / UC-07 | As a **user**, I want to pay my electricity or water bill directly from my SwiftPay wallet so that I can settle utility bills without visiting a payment centre. | Bill payment processes within 5 seconds; insufficient balance blocked with shortfall shown; gateway confirmation recorded. | Medium |
| US-010 | FR-12, FR-13 / UC-08 | As a **user**, I want to view and filter my full transaction history so that I can track my spending and verify past payments. | History loads in ≤ 2 seconds; paginated at 20 items; filterable by type, date, and status; each entry shows type, amount, party, and timestamp. | Medium |
| US-011 | FR-15 / UC-10 | As a **system administrator**, I want to suspend or reactivate user accounts so that I can protect the platform from fraudulent or policy-violating users. | Suspension takes effect immediately; suspended user blocked on next login; audit log entry created with reason and timestamp. | High |
| US-012 | FR-14 / UC-11 | As a **system administrator**, I want a dashboard showing total users, transaction volume, and active sessions so that I can monitor platform health in real time. | Dashboard data refreshes every 60 seconds; accessible only to ADMIN role; non-admins receive HTTP 403. | Medium |
| US-013 | NFR-09, NFR-10 | As a **compliance officer**, I want all passwords hashed and all data transmitted over HTTPS so that user data is protected from interception and breach. | Bcrypt hash (cost 12) confirmed in DB; HTTP requests redirected to HTTPS; SSL Labs grade A or higher. | High |
| US-014 | NFR-07 | As a **DevOps engineer**, I want the backend to handle 1,000 concurrent users without performance degradation so that the system remains responsive during peak usage. | Load test (k6) with 1,000 virtual users shows P95 response time ≤ 3 seconds; zero HTTP 5xx errors. | Medium |
| US-015 | NFR-03, NFR-04 | As a **DevOps engineer**, I want the backend containerised with Docker and the mobile app deployable to both app stores so that releases are fast, repeatable, and environment-independent. | `docker-compose up` deploys full backend on clean Ubuntu 22.04 in ≤ 10 minutes; CI pipeline produces valid APK and IPA. | Medium |

---

## 2. Product Backlog (MoSCoW Prioritisation)

Stories are prioritised using **MoSCoW** and estimated using **Fibonacci story points** (1, 2, 3, 5, 8).

| Story ID | User Story (Summary) | MoSCoW | Story Points | Dependencies | Justification |
|---|---|---|---|---|---|
| US-001 | Register account | Must-have | 3 | None | Entry point to entire system; no other story is possible without it. Directly addresses End User and Compliance Officer concerns. |
| US-002 | Login / Authenticate | Must-have | 2 | US-001 | All authenticated features depend on this. JWT infrastructure is foundational. |
| US-003 | Reset password via OTP | Must-have | 3 | US-001, US-002 | Critical for user retention — locked-out users abandon apps. Redis OTP infrastructure needed early. |
| US-004 | Auto-provision wallet on registration | Must-have | 2 | US-001 | The wallet is the core financial object; all transfer and balance features depend on it. |
| US-005 | View wallet balance | Must-have | 2 | US-002, US-004 | First thing users see after login; directly maps to End User success metric of knowing their balance. |
| US-006 | Send money (P2P transfer) | Must-have | 8 | US-002, US-004, US-005 | The primary value proposition of SwiftPay. Highest complexity — requires atomic DB transaction, gateway call, and rollback logic. |
| US-007 | Push notification on receipt | Must-have | 3 | US-006 | Recipient awareness is inseparable from the transfer experience. FCM integration needed for MVP. |
| US-013 | Password hashing + HTTPS enforcement | Must-have | 2 | US-001, US-002 | Security baseline — non-negotiable before any real user data is processed. Compliance Officer requirement. |
| US-008 | Top up wallet via card | Should-have | 5 | US-002, US-004 | Needed for sustained usage but wallet can initially be funded manually by admin for MVP testing. |
| US-009 | Pay utility bills | Should-have | 5 | US-008, US-006 | Valuable but not core to MVP; requires provider registry and gateway extension. |
| US-010 | View and filter transaction history | Should-have | 3 | US-006, US-007 | Important for trust and transparency but does not block MVP launch. |
| US-011 | Admin: suspend / reactivate users | Should-have | 3 | US-002 | Needed for moderation but not launch-critical; manual DB intervention is a temporary fallback. |
| US-012 | Admin dashboard (metrics) | Could-have | 3 | US-011 | Valuable for the Business Owner but no user-facing impact; deferred post-MVP. |
| US-014 | 1,000 concurrent users load test | Could-have | 5 | US-006, US-015 | Performance hardening is important but premature before core features are stable. |
| US-015 | Docker containerisation + CI/CD pipeline | Could-have | 5 | None | Improves developer workflow but not user-visible; manual deployment is viable for early sprints. |

---

## 3. Sprint Planning — Sprint 1

### 3.1 Sprint Goal

> **"Deliver a working authentication and wallet foundation so that a user can register, log in, view their balance, and send money to another user — forming the complete core loop of SwiftPay's MVP."**

This sprint targets the highest-priority Must-have stories. Completing this sprint means a real user can create an account, authenticate, and execute a P2P transfer end-to-end — which is the minimum viable demonstration of SwiftPay's core value.

**Sprint Duration:** 2 weeks (14 days)
**Sprint Capacity:** ~80 developer hours (solo developer, ~8hrs/day, 10 working days)

---

### 3.2 Sprint Backlog — Selected Stories

| Story ID | Summary | Story Points | Rationale for Inclusion |
|---|---|---|---|
| US-001 | Register account | 3 | Foundation — nothing else works without user accounts |
| US-002 | Login / Authenticate | 2 | Required for all protected endpoints |
| US-004 | Auto-provision wallet | 2 | Wallet is the core data object |
| US-005 | View wallet balance | 2 | First user-visible feature post-login |
| US-006 | Send money (P2P transfer) | 8 | Core value proposition; must be proven in Sprint 1 |
| US-013 | Password hashing + HTTPS | 2 | Security baseline before any real data flows |

**Total Story Points: 19** (within a typical solo-developer sprint capacity of 20–25 points)

---

### 3.3 Sprint Task Breakdown

| Task ID | Story ID | Task Description | Assigned To | Estimated Hours | Status |
|---|---|---|---|---|---|
| T-001 | US-001 | Design and implement `POST /auth/register` API endpoint with input validation | Dev | 4 | To Do |
| T-002 | US-001 | Set up PostgreSQL schema: `users` and `wallets` tables with migrations | Dev | 3 | To Do |
| T-003 | US-001 | Build Registration screen UI in React Native (form, validation, error states) | Dev | 5 | To Do |
| T-004 | US-001 | Write unit tests for registration service (duplicate email, weak password cases) | Dev | 3 | To Do |
| T-005 | US-002 | Implement `POST /auth/login` endpoint with bcrypt comparison and JWT issuance | Dev | 4 | To Do |
| T-006 | US-002 | Build Login screen UI in React Native with error handling | Dev | 4 | To Do |
| T-007 | US-002 | Implement JWT middleware for protecting authenticated routes | Dev | 3 | To Do |
| T-008 | US-004 | Add wallet auto-provisioning logic to registration service (triggered post-user creation) | Dev | 2 | To Do |
| T-009 | US-005 | Implement `GET /wallet/balance` endpoint with JWT guard | Dev | 2 | To Do |
| T-010 | US-005 | Build Home Dashboard screen displaying wallet balance and user name | Dev | 4 | To Do |
| T-011 | US-006 | Design `transactions` table schema (amount, sender_id, recipient_id, status, timestamps) | Dev | 2 | To Do |
| T-012 | US-006 | Implement `POST /transactions/transfer` endpoint with atomic DB transaction logic | Dev | 8 | To Do |
| T-013 | US-006 | Integrate Payment Gateway SDK for fund settlement | Dev | 6 | To Do |
| T-014 | US-006 | Implement rollback logic on gateway timeout or failure | Dev | 4 | To Do |
| T-015 | US-006 | Build Send Money screen UI (phone input, amount, confirm button, success/error states) | Dev | 5 | To Do |
| T-016 | US-006 | Integrate Firebase FCM — send notifications to sender and recipient on transfer | Dev | 4 | To Do |
| T-017 | US-013 | Enforce bcrypt cost factor 12 on all password storage paths | Dev | 1 | To Do |
| T-018 | US-013 | Configure TLS certificate and HTTPS redirect on the backend server | Dev | 2 | To Do |
| T-019 | US-013 | Write security test: verify no plaintext passwords in DB; verify HTTPS redirect | Dev | 2 | To Do |

**Total Estimated Hours: 72** (within 80-hour sprint capacity — leaves buffer for code review and bug fixes)

---

### 3.4 Definition of Done

A user story is considered **Done** when:
- [ ] All acceptance criteria pass
- [ ] Unit tests written and passing (≥ 70% coverage on new code)
- [ ] API endpoint documented in `openapi.yaml`
- [ ] Code reviewed and merged to `main` branch
- [ ] Feature tested manually on the Android emulator

---

## 4. Traceability Summary

| Story ID | Assignment 4 FR/NFR | Assignment 5 UC | Sprint 1 |
|---|---|---|---|
| US-001 | FR-01 | UC-01 | ✅ Included |
| US-002 | FR-02 | UC-02 | ✅ Included |
| US-003 | FR-03 | UC-03 | ❌ Sprint 2 |
| US-004 | FR-04 | UC-01 | ✅ Included |
| US-005 | FR-05 | UC-04 | ✅ Included |
| US-006 | FR-07, FR-08 | UC-05 | ✅ Included |
| US-007 | FR-09 | UC-05 | ✅ Included (via T-016) |
| US-008 | FR-06 | UC-06 | ❌ Sprint 2 |
| US-009 | FR-10, FR-11 | UC-07 | ❌ Sprint 3 |
| US-010 | FR-12, FR-13 | UC-08 | ❌ Sprint 2 |
| US-011 | FR-15 | UC-10 | ❌ Sprint 2 |
| US-012 | FR-14 | UC-11 | ❌ Sprint 3 |
| US-013 | NFR-09, NFR-10 | — | ✅ Included |
| US-014 | NFR-07 | — | ❌ Sprint 3 |
| US-015 | NFR-03, NFR-04 | — | ❌ Sprint 2 |

---

## 5. Reflection — Challenges in Agile Planning as a Solo Developer (~500 words)

Agile methodology is designed for teams. It assumes a Product Owner who negotiates scope, a Scrum Master who facilitates ceremonies, and a development team who estimates collectively. Working through this assignment as a sole developer meant playing all three roles simultaneously — and the tension between those roles was the most revealing part of the exercise.

**The Prioritisation Paradox**

The hardest single task was MoSCoW prioritisation. When you are the only person on the project, every story feels important. There is no external stakeholder to tell you that bill payments matter more than the admin dashboard — the business logic is entirely self-referential. I found myself instinctively marking everything as "Must-have," which of course defeats the purpose of prioritisation entirely.

The discipline that broke through this was asking: *"If I could only ship one feature this sprint, which one would prove SwiftPay is real?"* The answer — unambiguously — was the P2P transfer (US-006). Everything else either enables it (registration, authentication, wallet) or builds on it (notifications, history, admin). That single question restructured the entire backlog. Stories that felt urgent (like the admin dashboard) became "Could-have" once I recognised they have zero user-facing impact at MVP stage.

**Estimation Without a Team**

Story point estimation through Planning Poker works because disagreement between team members surfaces hidden complexity. Alone, there is no disagreement — and therefore no mechanism to catch underestimation. I initially estimated US-006 (Send Money) at 5 points. When I broke it into tasks (T-011 through T-016), the task list totalled 29 hours — clearly an 8-point story, not a 5-point one. The task breakdown saved me from committing to an impossible sprint.

This taught me that for solo developers, **task-level hour estimation is more reliable than story points alone**. Story points are a relative measure calibrated by team velocity over time — a metric that does not exist yet for a project with one person and no sprint history.

**Balancing Technical Debt Against Delivery**

One of the more uncomfortable decisions was deciding when to include technical stories (US-013: security baseline, US-015: Docker/CI) alongside feature stories. The pressure to show visible progress — a working register screen, a working transfer flow — made technical infrastructure feel like a distraction. But skipping security (NFR-09, NFR-10) even for a single sprint would mean building all of Sprint 1 on an insecure foundation that would need to be retrofitted later — which costs more time than doing it now.

The resolution was to keep security stories in Sprint 1 but give them minimal task estimates (US-013 = 3 hours total). They are not glamorous but they are fast to implement correctly from the start.

**What Agile Taught Me About My Own Requirements**

The most unexpected benefit of this process was discovering gaps in my own SRD. Writing US-006 forced me to ask: *what is the minimum transfer amount? Is there a daily limit? What happens if the recipient has a suspended account?* None of these were specified in FR-07. Agile planning, more than any other process so far, revealed that requirements always leave something out — and that discovery is best made before writing code, not during it.

---

*SwiftPay — AGILE_PLANNING.md | Software Engineering Assignment 6*