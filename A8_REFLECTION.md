# A8_REFLECTION.md — Lessons Learned in State and Activity Modeling
## SwiftPay Mobile Payment App

> **Assignment 8 | Reflection**

---

## 1. Choosing the Right Granularity

The hardest decision in both state and activity modeling was choosing how much detail to include. Too little and the diagram fails to communicate anything a reader couldn't infer from the requirements document. Too much and the diagram becomes a wall of boxes that nobody reads.

For state diagrams, the Transaction object illustrated this tension most sharply. An early draft had twelve states including sub-states like `DebitPending`, `GatewayCallInitiated`, and `WebhookAwaited`. While technically accurate, the diagram was unreadable and offered no insight beyond what the code itself would show. The final version collapses these into `Processing` and `PendingGateway` — two states that meaningfully differ from a business perspective (one is internal, one involves an external dependency) without drowning in implementation detail.

For activity diagrams, the opposite temptation arose: over-simplifying to avoid complexity. The P2P Transfer workflow is genuinely complex — it involves two wallets, an external gateway, a rollback path, and two notification branches. Collapsing the rollback into a single "Error" box would misrepresent how critical atomicity is to the system. The decision was to keep the full rollback path visible, because it directly maps to FR-08 and is the most important safety property SwiftPay has.

The rule that emerged: **a state or action deserves its own box if it has a distinct stakeholder consequence.** A state that only a developer cares about belongs in code comments, not in a diagram.

---

## 2. Aligning Diagrams with Agile User Stories

State and activity diagrams operate at a different level of abstraction than user stories. A user story says: *"As a sender, I want to transfer money so that I can pay people quickly."* A state diagram says: *"A Transaction object transitions from Initiated → Validating → Processing → PendingGateway → Completed."* These two artifacts describe the same behaviour from completely different angles — one from the user's perspective, one from the system's internal perspective.

The challenge was ensuring they stayed consistent. US-006 specifies that a transfer must complete in ≤ 5 seconds and roll back on gateway failure. The Transaction state diagram makes the rollback path (`PendingGateway → RolledBack`) explicit as a named state — which is not obvious from the user story alone. This is where state modeling added genuine value: it revealed that "rollback" is not just an error handler, it is a first-class system state with its own postconditions (sender balance unchanged, transaction logged as FAILED, user notified).

Sprint tasks also benefited from the activity diagrams. T-012 (POST /transactions/transfer) and T-014 (rollback logic) were planned as separate tasks in Assignment 6. The P2P Transfer activity diagram makes clear why they are separate: they represent genuinely distinct workflow branches that require different testing strategies and cannot be safely merged into a single implementation task.

---

## 3. State Diagrams vs. Activity Diagrams — A Direct Comparison

Both diagram types model dynamic system behaviour, but they answer fundamentally different questions:

| Dimension | State Transition Diagram | Activity Diagram |
|---|---|---|
| **Focus** | What states can an object be in? | What steps does a process follow? |
| **Subject** | A single object (Transaction, User, OTP) | A workflow involving multiple actors |
| **Time axis** | Lifecycle (birth → death of an object) | Sequential / parallel flow of actions |
| **Best reveals** | Valid/invalid state combinations; guard conditions | Decision points; parallel actions; actor responsibilities |
| **Risk it surfaces** | Missing states (e.g. forgetting the RolledBack state) | Missing decision branches (e.g. forgetting the gateway timeout path) |

In practice, the two diagram types were complementary rather than redundant. The Transaction state diagram revealed that `Disputed` and `Refunded` are distinct post-completion states — something neither the SRD nor the use cases made explicit. The P2P Transfer activity diagram revealed that notification to the sender and notification to the recipient can and should happen in parallel — something the state diagram could not express because it models a single object, not a multi-actor workflow.

The most valuable insight from producing both types was that **state diagrams catch missing object lifecycle states, while activity diagrams catch missing process branches**. Using only one type would have left gaps that the other would have caught.

---

*SwiftPay — A8_REFLECTION.md | Software Engineering Assignment 8*
