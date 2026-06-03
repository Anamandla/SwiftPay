# ROADMAP.md — SwiftPay Future Development

This roadmap outlines planned features and improvements beyond the current MVP.
Items are grouped by priority. Contributors are welcome to pick up any item — see CONTRIBUTING.md.

---

## Phase 1 — MVP Hardening (Next Sprint)

| Feature | Label | Description |
|---|---|---|
| Replace SHA-256 with bcrypt | `security`, `good-first-issue` | `UserBuilder` and `UserService` must use bcrypt (cost 12) for password hashing — NFR-09 |
| Redis OTP storage | `feature-request`, `api` | Replace datetime-based OTP TTL with real Redis key expiry for production correctness |
| JWT token issuance | `feature-request`, `api` | `POST /api/auth/login` should return a real signed JWT, not just user_id |
| Refresh token endpoint | `feature-request`, `api` | `POST /api/auth/refresh` to rotate access tokens |
| Pagination for transaction history | `feature-request`, `api` | `GET /api/users/{id}/transactions?page=1&limit=20` |

---

## Phase 2 — Storage & Infrastructure

| Feature | Label | Description |
|---|---|---|
| PostgreSQL repository implementation | `feature-request` | Implement `DatabaseUserRepository`, `DatabaseTransactionRepository` using psycopg2 |
| Docker Compose setup | `good-first-issue` | Add `docker-compose.yml` with SwiftPay API + PostgreSQL + Redis containers |
| Database migrations | `feature-request` | Add Alembic migration scripts for users, wallets, transactions tables |
| JSON filesystem repository | `good-first-issue` | Complete the `FileSystemUserRepositoryStub` — useful for local offline dev |

---

## Phase 3 — Features

| Feature | Label | Description |
|---|---|---|
| Bill payment endpoint | `feature-request` | `POST /api/transactions/bill` — pay registered service providers |
| Push notifications (FCM) | `feature-request` | Integrate Firebase Cloud Messaging for transfer alerts |
| Email notifications (SendGrid) | `feature-request` | Send OTP and transaction confirmation emails |
| Admin dashboard endpoint | `feature-request` | `GET /api/admin/stats` — total users, volume, active sessions |
| Transaction dispute/refund flow | `feature-request` | `POST /api/transactions/{id}/dispute` and `/refund` endpoints |

---

## Phase 4 — Quality & Observability

| Feature | Label | Description |
|---|---|---|
| pytest migration | `good-first-issue` | Migrate `run_all_tests.py` to proper pytest test files with fixtures |
| Test coverage reporting | `good-first-issue` | Add `pytest-cov` to CI and enforce ≥70% line coverage |
| Structured logging | `feature-request` | Replace `print()` statements with Python `logging` module |
| Rate limiting | `security` | Add per-IP rate limiting to auth endpoints (prevent brute force) |
| OpenAPI UI (Swagger) | `good-first-issue` | Integrate `flask` + `flasgger` or `FastAPI` for interactive Swagger UI |

---

## How to Contribute to the Roadmap

Open an issue with the label `roadmap` if you have a feature idea not listed here.
If you want to work on a roadmap item, comment on the relevant issue or create one if none exists.

---

*SwiftPay — ROADMAP.md*
