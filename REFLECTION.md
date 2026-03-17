# REFLECTION.md — Balancing Stakeholder Needs
## SwiftPay Mobile Payment App

> **Assignment 4 | Reflection**
> A candid discussion of the challenges encountered when eliciting and balancing competing stakeholder requirements for SwiftPay.

---

## 1. Overview

Requirements engineering is rarely straightforward. While it might seem that defining what a system "should do" is simply a matter of asking users what they want, the reality involves navigating competing priorities, hidden assumptions, and trade-offs between groups who often want fundamentally different things. This reflection documents the most significant challenges encountered during the stakeholder and requirements analysis for SwiftPay.

---

## 2. Challenge 1: Speed vs. Security

**The Tension:**
End users (both senders and recipients) expressed a clear priority: transfers must be instant. Any delay in seeing money move feels like a system failure to a user accustomed to apps like Zelle or PayPal. On the other hand, the Compliance Officer's primary concern is fraud prevention — which typically requires transaction screening, pattern analysis, and sometimes holds on suspicious activity.

**Why It Was Difficult:**
These two goals are structurally in conflict. Proper fraud screening takes time. If every transfer is blocked pending a compliance check, the user experience degrades severely. But if transfers are instant with no screening, the platform becomes a vector for financial crime.

**How It Was Resolved:**
The resolution adopted for SwiftPay is an **asynchronous fraud screening model**: transfers are approved and funds move immediately for low-risk transactions (small amounts, known recipients, established users), while a background process flags and reviews suspicious patterns post-transfer. High-risk transactions (large amounts, new accounts, unusual geography) are placed in a short review hold of up to 60 seconds before release. This approach appears in NFR-11 and the Compliance Officer's success metrics.

---

## 3. Challenge 2: Feature Velocity vs. System Stability

**The Tension:**
The Business Owner and Product Manager want rapid feature delivery — new payment categories, loyalty rewards, and integrations keep users engaged and drive growth. The IT/DevOps Engineer, however, prioritises stability. Every new feature is a potential source of bugs, deployment failures, and regression issues in a system handling real money.

**Why It Was Difficult:**
In a financial application, instability is not just inconvenient — it is damaging. A bug that causes a double-debit or a missed credit erodes user trust immediately and may trigger regulatory scrutiny. Yet a product that moves slowly loses users to competitors.

**How It Was Resolved:**
The requirements were structured around a **phased delivery model** using Agile principles. The SRD distinguishes "Must Have" from "Should Have" requirements using MoSCoW prioritisation. Non-critical features (bill payments, transaction filters) are marked "Should Have" and deferred to later sprints. NFR-03 (Docker containerisation) and NFR-06 (70% test coverage) directly address stability concerns, ensuring that the infrastructure for safe, fast deployments is built first.

---

## 4. Challenge 3: Data Access vs. User Privacy

**The Tension:**
Customer Support agents need access to detailed user transaction history to resolve complaints effectively. If a user reports a failed transfer, the support agent needs to see timestamps, amounts, gateway responses, and wallet states. However, the Compliance Officer's concern — aligned with POPIA (South Africa's data protection law) — is that broad internal access to financial data creates exposure risk.

**Why It Was Difficult:**
There is no clean technical line between "enough data to help a user" and "too much data to be safe." Every additional field exposed to support agents increases privacy risk. But every restriction makes support less effective, which increases user frustration and churn.

**How It Was Resolved:**
FR-15 and NFR-09 together address this through **Role-Based Access Control (RBAC)**. Support agents are granted a read-only role scoped to transaction records and masked personal data (e.g., phone numbers partially hidden). Full user PII is accessible only to Compliance Officers through a separately audited interface. All access events are logged to satisfy NFR-11's audit trail requirement.

---

## 5. Challenge 4: Affordability vs. Sustainability

**The Tension:**
End users want free transfers — especially in a South African context where many users are cost-sensitive and alternatives like EFT are free (just slow). The Business Owner, however, needs revenue to sustain the platform. Payment gateway fees, server costs, and engineering salaries require a monetisation model.

**Why It Was Difficult:**
Introducing fees risks driving users away, particularly in the early growth phase. But a completely free model is financially unsustainable. Finding a fee structure that feels fair to users while generating enough revenue was genuinely difficult to specify as a requirement without making assumptions about business strategy.

**How It Was Resolved:**
The requirements were kept flexible here. FR-07 (P2P transfers) does not hardcode a fee, instead specifying that the business logic layer handles fee calculation. A tiered model (free below R500/month, small fee above) is documented in the Stakeholder Trade-offs table as a recommended approach, but left as a configurable business rule rather than a hardcoded system constraint. This gives the Product Manager flexibility to experiment without requiring a code change.

---

## 6. Key Lessons Learned

- **Stakeholders don't always know what they want** until you show them a conflict. The tension between instant transfers and fraud screening only became clear when both stakeholders were considered side by side.
- **Non-functional requirements are where the hardest trade-offs live.** Functional requirements were relatively easy to agree on. It was the quality attributes — how fast, how secure, how available — where real negotiation was required.
- **Measurable criteria are essential.** Vague requirements like "the system should be secure" create false agreement. Forcing each requirement to have a specific, testable acceptance criterion exposed many hidden assumptions and disagreements early.
- **Agile flexibility is valuable.** Framing requirements as a living document rather than a fixed contract reduced the pressure to resolve every trade-off upfront, allowing some tensions to be deferred to later sprints when more information is available.

---

*SwiftPay — REFLECTION.md | Software Engineering Assignment 4*
