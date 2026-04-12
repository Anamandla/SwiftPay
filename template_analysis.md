# template_analysis.md — GitHub Project Template Analysis & Selection
## SwiftPay Mobile Payment App

> **Assignment 7 | Template Analysis**
> Evaluates GitHub's built-in project templates and justifies the selection for SwiftPay's Agile workflow.

---

## 1. GitHub Project Templates — Comparison Table

| Feature | Basic Kanban | Automated Kanban | Bug Triage | Team Planning |
|---|---|---|---|---|
| **Default Columns** | To Do, In Progress, Done | To Do, In Progress, Done | Needs Triage, High Priority, Low Priority, Closed | To Do, In Progress, Done, Backlog |
| **Number of Columns** | 3 | 3 | 4 | 4 |
| **Automation** | None — all cards moved manually | Issues auto-move to "In Progress" when opened; auto-move to "Done" when closed or merged | Issues auto-added to "Needs Triage" when opened; auto-closed when issue is closed | Limited — some auto-close on issue close |
| **Custom Column Support** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **GitHub Issues Linking** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **PR Integration** | Manual | ✅ Auto-moves on PR open/merge | Limited | Limited |
| **Labels & Milestones** | Manual | ✅ Supported natively | ✅ Bug-focused labels built in | ✅ Milestone-based grouping |
| **WIP Limit Support** | ❌ Not built-in | ❌ Not built-in | ❌ Not built-in | ❌ Not built-in |
| **Best Suited For** | Small projects, learning Kanban basics, solo developers starting out | Agile sprint teams needing automation; projects with active PR workflows | Maintenance-phase projects managing defects and regressions | Teams planning across multiple sprints with backlog grooming |
| **Agile Methodology Fit** | ⭐⭐ (basic) | ⭐⭐⭐⭐⭐ (excellent) | ⭐⭐ (maintenance-focused) | ⭐⭐⭐ (planning-focused) |
| **Complexity** | Low | Medium | Low–Medium | Medium |

---

## 2. Template Evaluation for SwiftPay

### 2.1 Why Basic Kanban Was Ruled Out
Basic Kanban requires every card to be moved manually between columns. For a project like SwiftPay where GitHub Issues are linked to user stories and pull requests, manual movement creates unnecessary overhead and introduces the risk of the board falling out of sync with actual code activity. It is suitable for learning but not for a project that already has 19 sprint tasks and 15 user stories defined.

### 2.2 Why Bug Triage Was Ruled Out
Bug Triage is designed for maintenance and support workflows — its columns (Needs Triage, High Priority, Low Priority) are built around defect management, not feature delivery. SwiftPay is in active development (Sprint 1), not in a maintenance phase. This template would require significant restructuring to serve an Agile sprint workflow, making it the wrong starting point.

### 2.3 Why Team Planning Was Not Selected
Team Planning adds a Backlog column and milestone grouping, which is useful. However, its automation is limited compared to Automated Kanban, and its milestone-based focus is better suited to multi-team projects planning across many sprints. For a solo developer in Sprint 1, the overhead of milestone management outweighs the benefit.

---

## 3. Selected Template: Automated Kanban ✅

### Justification

**Automated Kanban** is the optimal template for SwiftPay for the following reasons:

**1. Automation reduces overhead for a solo developer.**
SwiftPay is a solo project. Every minute spent manually moving cards between columns is a minute not spent writing code. Automated Kanban's built-in rules — issues move to "In Progress" when opened, move to "Done" when closed or a PR is merged — keep the board accurate without manual intervention. This directly addresses one of the most common failure modes of Kanban boards: boards that become stale because developers forget to update them.

**2. PR-linked automation aligns with the Definition of Done.**
The Sprint 1 Definition of Done (defined in AGILE_PLANNING.md) requires code to be reviewed and merged to `main`. Automated Kanban automatically moves a card to "Done" when its linked PR is merged — which means the board state and the code state are always synchronised.

**3. It maps directly to Sprint 1's task lifecycle.**
The 19 tasks defined in Sprint 1 (T-001 to T-019) naturally flow through: `Backlog → To Do → In Progress → In Review → Testing → Done`. Automated Kanban provides the base structure, which is then customised with "In Review" and "Testing" columns (see kanban_explanation.md).

**4. Native Issues and Labels support traceability.**
SwiftPay's user stories (US-001 to US-015) are entered as GitHub Issues with labels (`must-have`, `sprint-1`, `feature`, `security`). Automated Kanban links these Issues to board cards natively, maintaining traceability back to Assignment 4 (SRD.md) and Assignment 5 (USE_CASES.md).

**5. It supports Agile's iterative principles.**
Automated Kanban does not enforce a rigid structure. Columns can be added, renamed, and reordered as the project evolves across sprints — aligning with Agile's core principle of responding to change over following a fixed plan.

---

## 4. Customisation Plan

Starting from the Automated Kanban base (To Do → In Progress → Done), the following customisations are applied for SwiftPay:

| Column | Type | Purpose | WIP Limit |
|---|---|---|---|
| 📋 Backlog | Custom (added) | Holds all user stories and tasks not yet scheduled for the current sprint | None |
| 📌 To Do | Default | Sprint-committed tasks ready to be started | 6 tasks |
| 🔨 In Progress | Default | Tasks actively being worked on | 3 tasks |
| 👀 In Review | Custom (added) | Code complete; awaiting self-review or peer review before merge | 3 tasks |
| 🧪 Testing | Custom (added) | Merged code being validated against acceptance criteria | 3 tasks |
| 🚫 Blocked | Custom (added) | Tasks stalled due to a dependency, missing information, or external issue | No limit |
| ✅ Done | Default | Tasks meeting the Definition of Done | None |

This 7-column structure reflects the actual lifecycle of a SwiftPay task from idea to verified completion.

---

*SwiftPay — template_analysis.md | Software Engineering Assignment 7*
