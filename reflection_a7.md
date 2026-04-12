# reflection.md — Lessons Learned in Kanban Implementation
## SwiftPay Mobile Payment App

> **Assignment 7 | Reflection**

---

## Reflection: Challenges in Template Selection, Customisation, and Tool Comparison

### Choosing a Template Is a Design Decision

The first challenge in this assignment was recognising that selecting a GitHub project template is not a trivial administrative step — it is a design decision that shapes how the entire project is managed for the remainder of the semester. The four templates (Basic Kanban, Automated Kanban, Bug Triage, Team Planning) look superficially similar: they all have columns, they all accept Issues as cards. But their underlying assumptions about workflow are meaningfully different.

Bug Triage assumes your primary work is reacting to defects. Team Planning assumes you have a backlog to groom across multiple teams. Basic Kanban assumes you want simplicity above all else. Automated Kanban assumes you want the board to reflect reality without manual effort. Only by reading what each template actually automates — and comparing that against SwiftPay's specific situation (solo developer, Sprint 1, active feature development, 19 defined tasks) — did the right choice become clear.

The temptation was to choose Basic Kanban because it seemed the easiest to understand. But "easiest to understand" and "most useful for the project" are not the same thing. Automated Kanban requires a small amount of upfront learning (understanding GitHub's automation rules, linking Issues to PRs) but pays back that investment every day by keeping the board accurate without manual maintenance.

### Customisation: More Columns Is Not Always Better

Once Automated Kanban was selected, the next challenge was deciding how many custom columns to add. The assignment required 2+, but there is a real risk in over-engineering a Kanban board: too many columns creates friction. If a task has to pass through seven stages before it can be marked Done, developers start skipping columns — and a board with stale, inaccurate cards is worse than no board at all.

The four columns added — Backlog, In Review, Testing, and Blocked — were each justified by a genuine gap in the default template. "In Review" and "Testing" exist because, in practice, code that is written is not the same as code that is reviewed, and code that is reviewed is not the same as code that is tested and accepted. Without these columns, the "In Progress" → "Done" jump hides an entire phase of work that takes real time and can genuinely block delivery. "Blocked" exists because invisible blockers are a project management failure — if a task is stalled, that stall needs to be surfaced and addressed, not left silently rotting in "In Progress."

### GitHub Projects vs. Trello vs. Jira

Working with GitHub Projects prompted comparison with other tools. **Trello** is simpler and more visually flexible — its card system is more customisable and its Power-Ups ecosystem is extensive. However, Trello exists outside the codebase. A Trello card for "implement the transfer API" has no connection to the actual PR that implements it unless you manually paste links. GitHub Projects, by contrast, is integrated into the repository: Issues, PRs, milestones, and labels all live in the same place. For a developer-managed project, that integration is worth more than Trello's aesthetic flexibility.

**Jira** is the industry standard for large teams and is far more powerful than GitHub Projects — it supports custom workflows, velocity charts, burndown reports, sprint retrospectives, and deep integration with CI/CD pipelines. However, Jira's power comes with significant complexity. Setting up a Jira project correctly for a solo developer would take longer than the sprint itself. GitHub Projects is the pragmatic choice at this scale: enough structure to stay organised, not so much overhead that the tooling becomes the project.

### The Deeper Lesson

The real lesson from this assignment was not about GitHub's features — it was about the relationship between process and behaviour. A Kanban board is only as useful as the discipline applied to maintaining it. Automation helps (issues auto-moving on open/close), but the "In Review" and "Testing" columns require a developer to consciously move cards. That manual step is not a bug — it is a forcing function. Moving a card to "Testing" requires you to stop and ask: *have I actually tested this against the acceptance criteria?* The board, when used properly, makes that question unavoidable.

---

*SwiftPay — reflection.md | Software Engineering Assignment 7*
