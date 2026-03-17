# STAKEHOLDERS.md — SwiftPay Mobile Payment App

> **Assignment 4 | Stakeholder Analysis**
> This document identifies all key stakeholders for SwiftPay, detailing their roles, concerns, pain points, and measurable success metrics.

---

## Stakeholder Analysis Table

| # | Stakeholder | Role | Key Concerns | Pain Points | Success Metrics |
|---|---|---|---|---|---|
| 1 | **End User (Sender)** | Primary app user who initiates payments and transfers | Fast, reliable money transfers; low or no fees; simple UI | Bank transfers are slow (1–3 days); high transaction fees; complex banking apps | 95% of transfers complete in under 5 seconds; user satisfaction score ≥ 4.5/5 |
| 2 | **End User (Recipient)** | Receives money via the SwiftPay platform | Instant notification of received funds; easy withdrawal | Delayed notifications; uncertainty about when funds arrive | Push notification delivered within 3 seconds of transfer; zero missed credit alerts |
| 3 | **System Administrator** | Monitors platform health, manages users, detects fraud | Real-time visibility into transactions; ability to suspend bad actors; audit logs | No centralised dashboard; manual fraud detection; reactive rather than proactive | Fraud detection flags suspicious transactions within 60 seconds; admin dashboard loads in < 2s |
| 4 | **Payment Gateway Provider** (e.g. Peach Payments) | External partner that processes and settles real fund movement | Reliable API integration; proper error handling; retry logic | Poorly integrated clients cause duplicate transactions and settlement failures | Zero duplicate transactions; 99.9% successful API handshake rate |
| 5 | **IT / DevOps Engineer** | Deploys, maintains, and monitors backend infrastructure | System uptime; scalable architecture; easy CI/CD deployment; observable logs | Downtime during deployments; no monitoring alerts; difficult rollbacks | 99.5% uptime; deployment time under 10 minutes; automated rollback on failure |
| 6 | **Compliance / Security Officer** | Ensures system meets financial regulations and data protection laws | Data encryption; audit trails; KYC-readiness; POPIA/GDPR alignment | No built-in compliance reporting; user data stored in plaintext historically | 100% of sensitive data encrypted at rest and in transit; full audit log retained for 12 months |
| 7 | **Business Owner / Product Manager** | Oversees product direction and financial sustainability | User growth; transaction volume; feature adoption; revenue from fees | Lack of analytics; unclear user drop-off points; slow feature delivery | 20% month-on-month user growth; transaction volume dashboard updated daily |
| 8 | **Customer Support Agent** | Handles user complaints, failed transactions, and account issues | Access to user transaction history; ability to reverse failed payments; fast resolution tools | No support dashboard; must query DB manually; slow resolution times | Average ticket resolution time ≤ 4 hours; support portal loads in < 2 seconds |

---

## Stakeholder Relationship Map

```
End Users (Sender / Recipient)
        │
        ▼
  [SwiftPay Mobile App]
        │
        ▼
  [Backend API Server] ◄──── System Administrator
        │                          │
        ├──► Payment Gateway        └──► Compliance Officer
        ├──► Firebase FCM
        ├──► Email Service          IT/DevOps Engineer
        └──► PostgreSQL DB  ◄────────────┘
                                Business Owner / PM
                                Customer Support Agent
```

---

## Key Stakeholder Trade-offs

| Tension | Stakeholder A | Stakeholder B | Resolution Approach |
|---|---|---|---|
| Speed vs. Security | End User (wants instant transfer) | Compliance Officer (wants fraud checks) | Async fraud screening — approve fast, flag for review post-transfer |
| Feature velocity vs. Stability | Business Owner (wants new features fast) | IT Engineer (wants stable deployments) | Feature flags and staged rollouts |
| Data access vs. Privacy | Customer Support (needs transaction history) | Compliance Officer (limits data exposure) | Role-based access control (RBAC) with audit trail |
| Low fees vs. Revenue | End User (wants free transfers) | Business Owner (needs revenue) | Free tier up to R500/month; fee above threshold |

---

*SwiftPay — STAKEHOLDERS.md | Software Engineering Assignment 4*
