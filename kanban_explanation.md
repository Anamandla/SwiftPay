# kanban_explanation.md — Kanban Board Definition & Implementation
## SwiftPay Mobile Payment App

> **Assignment 7 | Kanban Board Explanation**

---

## 1. What is a Kanban Board?

A **Kanban board** is a visual project management tool that represents the stages of a workflow as columns, and individual units of work (tasks, user stories, bugs) as cards that move through those columns from left to right as progress is made.

The word *Kanban* comes from Japanese (看板) and means "signboard" or "visual card." The concept originated in Toyota's manufacturing system in the 1940s as a way to control inventory flow and reduce waste. It was later adapted for software development by David Anderson in the 2000s and has since become one of the most widely used frameworks in Agile teams worldwide.

At its core, a Kanban board answers three questions at a glance:
- **What needs to be done?** (Backlog / To Do)
- **What is being worked on right now?** (In Progress)
- **What has been completed?** (Done)

---

## 2. SwiftPay's Custom Kanban Board

### 2.1 Board Structure

SwiftPay's Kanban board is built on GitHub Projects using the **Automated Kanban** template, customised with four additional columns to reflect the real lifecycle of a development task:

```
┌──────────┐   ┌─────────┐   ┌─────────────┐   ┌───────────┐   ┌─────────┐   ┌─────────┐   ┌──────┐
│ BACKLOG  │ → │  TO DO  │ → │ IN PROGRESS │ → │ IN REVIEW │ → │ TESTING │ → │ BLOCKED │   │ DONE │
│          │   │ WIP: 6  │   │   WIP: 3    │   │  WIP: 3   │   │  WIP: 3 │   │         │   │      │
│ US-001   │   │ T-001   │   │             │   │           │   │         │   │         │   │      │
│ US-002   │   │ T-002   │   │             │   │           │   │         │   │         │   │      │
│ US-003   │   │ T-003   │   │             │   │           │   │         │   │         │   │      │
│ ...      │   │ ...     │   │             │   │           │   │         │   │         │   │      │
└──────────┘   └─────────┘   └─────────────┘   └───────────┘   └─────────┘   └─────────┘   └──────┘
```

### 2.2 Column Definitions

| Column | Symbol | Description | Automation | WIP Limit |
|---|---|---|---|---|
| **Backlog** | 📋 | All user stories (US-001 to US-015) and future sprint tasks reside here. Items are pulled into To Do during sprint planning. | Manual | None |
| **To Do** | 📌 | Tasks committed to Sprint 1 that have not yet been started. Cards here are ready to be picked up immediately. | Auto-populated when Issue is added to sprint milestone | 6 |
| **In Progress** | 🔨 | Tasks actively being coded. A WIP limit of 3 prevents context-switching and keeps focus high. | Auto-moves here when a linked Issue is opened | 3 |
| **In Review** | 👀 | Code is written and a Pull Request has been raised. The task is awaiting code review before merge. This column was added because code review is a distinct, time-consuming step that deserves its own visibility. | Auto-moves when PR is opened | 3 |
| **Testing** | 🧪 | PR has been merged to `main`. The task is being validated against its acceptance criteria (manual testing on emulator, automated test run). This column was added to make QA visible — without it, testing gets collapsed into "Done" prematurely. | Manual | 3 |
| **Blocked** | 🚫 | Tasks that cannot progress due to an external dependency, unclear requirement, or technical blocker. This column was added to make impediments visible immediately rather than leaving them silently stalled in "In Progress." | Manual | None |
| **Done** | ✅ | Tasks that have passed testing and satisfy the Definition of Done (acceptance criteria met, tests passing, documented, merged). | Auto-moves when linked Issue is closed or PR is merged | None |

---

## 3. How the Board Visualises Workflow

The board provides an instant snapshot of the project's state. Each Sprint 1 task (T-001 to T-019) is a card on the board, linked to its parent GitHub Issue (user story). The card shows:
- **Title** (e.g., "T-012: Implement POST /transactions/transfer endpoint")
- **Assignee** (@mention of the developer)
- **Labels** (e.g., `must-have`, `sprint-1`, `feature`, `security`, `api`)
- **Linked Issue** (e.g., #US-006 — Send Money)
- **Milestone** (Sprint 1 — 2 weeks)

By scanning the board left to right, anyone can immediately see where work is concentrated, whether any column is approaching its WIP limit, and whether any tasks are blocked.

---

## 4. Work-in-Progress (WIP) Limits

WIP limits are one of the most important Kanban principles. They cap the number of tasks allowed in a column simultaneously, which:

- **Prevents multitasking.** A WIP limit of 3 on "In Progress" means you cannot start a fourth task without finishing one first. This forces prioritisation and reduces the cognitive cost of context-switching.
- **Exposes bottlenecks.** If "In Review" consistently hits its WIP limit of 3, it signals that the review step is slower than the development step — a bottleneck that needs to be addressed (in a team: more reviewers; solo: dedicated review time blocks).
- **Keeps flow smooth.** Kanban's goal is continuous, smooth flow rather than big-batch delivery. WIP limits enforce pull-based work: you pull a new task only when capacity exists.

For SwiftPay, the WIP limits per column are:

| Column | WIP Limit | Rationale |
|---|---|---|
| To Do | 6 | Enough tasks visible for the sprint without overwhelming the view |
| In Progress | 3 | Hard focus limit — no more than 3 active workstreams simultaneously |
| In Review | 3 | Reviews should be quick; a full column signals a review backlog |
| Testing | 3 | Testing should follow closely behind review; a full column signals QA debt |

---

## 5. How the Board Supports Agile Principles

| Agile Principle | How SwiftPay's Kanban Board Supports It |
|---|---|
| **Working software over comprehensive documentation** | The board tracks code tasks (T-001 to T-019), not document tasks. "Done" requires merged, tested code — not just written specs. |
| **Responding to change over following a plan** | Columns can be reordered, cards re-prioritised, and new tasks added at any sprint boundary without breaking the board structure. |
| **Continuous delivery of valuable software** | The Backlog → Done pipeline is designed for continuous flow. Small tasks (2–8 hrs) complete frequently, producing a steady stream of merged features. |
| **Simplicity — the art of maximising the work not done** | The "Blocked" column surfaces impediments early, preventing wasted effort on tasks that cannot actually be completed yet. |
| **Self-organising teams** | GitHub's @mention assignment and comment threads on each card give every task its own communication space, reducing the need for external coordination tools. |

---

## 6. GitHub Issues Setup — Labels and Milestones

### Labels used in SwiftPay's board:

| Label | Colour | Purpose |
|---|---|---|
| `must-have` | 🔴 Red | MoSCoW Must-have stories |
| `should-have` | 🟠 Orange | MoSCoW Should-have stories |
| `could-have` | 🟡 Yellow | MoSCoW Could-have stories |
| `sprint-1` | 🔵 Blue | Included in Sprint 1 |
| `feature` | 🟢 Green | New capability or user-facing feature |
| `security` | 🟣 Purple | Security-related task (NFR) |
| `api` | ⚫ Dark | Backend API endpoint task |
| `ui` | 🩵 Light blue | Mobile frontend UI task |
| `blocked` | ⬛ Grey | Task currently blocked |

### Milestone: Sprint 1
- **Title:** Sprint 1 — MVP Core Loop
- **Due date:** 2 weeks from project start
- **Description:** Deliver working registration, authentication, wallet, and P2P transfer
- **Linked issues:** US-001, US-002, US-004, US-005, US-006, US-013 (and their tasks T-001 to T-019)

---

## 7. How to Set Up the Board on GitHub (Step-by-Step)

1. Navigate to your SwiftPay GitHub repository.
2. Click the **"Projects"** tab → **"New project"**.
3. Select **"Automated Kanban"** template → click **"Create project"**.
4. Rename the project to **"SwiftPay — Sprint 1 Board"**.
5. Add custom columns: click **"+ Add column"** and add **Backlog**, **In Review**, **Testing**, and **Blocked** (drag to correct positions).
6. Create GitHub Issues for each user story (US-001 to US-015) with appropriate labels and milestone.
7. For each Sprint 1 task (T-001 to T-019), create a sub-issue or note card linked to the parent story issue.
8. Drag Sprint 1 issues into the **To Do** column; remaining stories go into **Backlog**.
9. As you work, open issues to trigger auto-move to **In Progress**; close or merge PRs to auto-move to **Done**.

---

*SwiftPay — kanban_explanation.md | Software Engineering Assignment 7*
