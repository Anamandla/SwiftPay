# REFLECTION_A5.md — Challenges in Translating Requirements to Use Cases and Tests
## SwiftPay Mobile Payment App

> **Assignment 5 | Reflection (~500 words)**

---

## Reflection

Translating stakeholder requirements and functional specifications into use case models and test cases revealed a layer of complexity that was not immediately obvious when the requirements were first written. While the SRD produced in Assignment 4 felt comprehensive at the time, modelling actual user interactions forced a much deeper interrogation of assumptions, edge cases, and system boundaries.

**The Gap Between "What" and "How"**

The most significant challenge was the conceptual shift from requirements — which describe *what* the system shall do — to use cases, which describe *how* actors interact with the system step by step. A requirement like "FR-07: The system shall allow a user to transfer funds to another registered user" appears straightforward on paper. But when modelling UC-05 (Send Money), it immediately raised questions that the requirement left unanswered: What happens if the recipient's phone is registered but their account is suspended? Should the sender receive a specific message about the recipient's status, or would that expose private account information? What is the maximum and minimum transfer amount? Is there a daily limit?

These questions do not have obvious answers from a purely technical standpoint — they require business decisions. Modelling the use case made these gaps visible in a way that simply writing requirements did not.

**Modelling «include» Relationships Without Over-Engineering**

Deciding which behaviours deserved their own «include» relationship in the use case diagram was surprisingly difficult. For example, `Validate Wallet Balance` appears as an included use case shared by UC-05 (Send Money) and UC-07 (Pay Bill). This is accurate — both use cases must check the balance before proceeding. However, it was tempting to decompose even further: should `Send Push Notification` be its own actor interaction? Should `Write Audit Log` be modelled explicitly?

The principle I settled on was only to model «include» relationships where the sub-behaviour is genuinely reusable across multiple use cases and meaningful to a stakeholder. Audit logging, while important for the Compliance Officer, is an internal system concern and does not represent a distinct actor interaction. This distinction — between user-visible behaviour and internal system mechanics — required careful thought.

**The Challenge of Testing Non-Functional Requirements**

Writing test cases for functional requirements was relatively mechanical: define inputs, expected outputs, and edge cases. Non-functional requirements presented a much harder challenge. How do you write a repeatable, verifiable test for "the system shall support 1,000 concurrent users"? The test is only meaningful if the infrastructure, dataset size, and network conditions are carefully controlled. TC-NFR-01 addresses this by specifying a k6 load testing script, a staging environment, and a 5-minute test window — but in practice, reproducing this test consistently requires DevOps expertise beyond the scope of a single developer.

Security testing introduced similar challenges. TC-NFR-04 (verifying bcrypt hashing) requires direct database access, which is straightforward in development but restricted in production. Writing tests that are both meaningful and practically executable required acknowledging the environment gap between development and deployment.

**What This Process Taught Me**

Overall, building use cases and test cases from existing requirements was a humbling exercise. It revealed that requirements written in the abstract often paper over real design decisions. The process of asking "who does this, how, and what can go wrong?" transformed vague specifications into concrete, testable contracts — which is ultimately the point of requirements engineering.

---

*SwiftPay — REFLECTION_A5.md | Software Engineering Assignment 5*
