# CONTRIBUTION_PLAN.md — Cross-Project Contribution Strategy
## SwiftPay | Assignment 15

---

## Overview

This document outlines my plan for contributing to peers' repositories as part of Assignment 15.
The strategy prioritises small, well-tested contributions that can pass CI quickly and add genuine value.

---

## Projects Selected for Contribution

| # | Repository | Owner | Why Selected | Issues Identified |
|---|---|---|---|---|
| 1 | *TailorFit* | *znxos* | Clear CONTRIBUTING.md, `good-first-issue` labels, active CI | *issue 38 max length job description* |
| 2 | *(peer repo name)* | *(username)* | Good domain model, missing test coverage for edge cases | *(e.g. Issue #8: Write tests for wallet debit with zero amount)* |
| 3 | *(peer repo name)* | *(username)* | Needs README improvements and setup instructions | *(e.g. Issue #5: Improve Getting Started section)* |

---

## Contribution Strategy

### Phase 1 — Documentation Fixes (Days 1–2)
Start with documentation contributions. These:
- Have low risk of breaking CI
- Are immediately useful to the project
- Help me understand the codebase before writing code
- Get merged quickly, building trust with the maintainer

Target tasks: README improvements, missing docstrings, clarifying CONTRIBUTING.md instructions.

### Phase 2 — Test Coverage (Days 3–4)
Add tests for untested edge cases. These:
- Require reading the actual source code closely
- Provide real value (catching bugs)
- Are easy for maintainers to review (test output is binary — pass or fail)

Target tasks: Missing unit tests for service layer edge cases, missing API error response tests.

### Phase 3 — Bug Fixes / Small Features (Days 5–7)
Tackle a `good-first-issue` bug or small feature. These:
- Are the highest-impact contributions
- Require following the project's coding standards closely
- Must include tests to be accepted

Target tasks: Input validation gaps, missing HTTP status codes, edge case handling.

---

## Process for Each PR

1. **Comment first** on the issue: *"I'd like to work on this — starting now."*
2. Fork the repository and create a branch: `git checkout -b fix/issue-number-description`
3. Make the change, write tests, verify CI passes locally
4. Submit PR with:
   - Descriptive title linking the issue
   - Explanation of what changed and why
   - Screenshots if UI-related
5. Respond to review comments within 24 hours
6. Once merged, update MERGED_PRS.md

---

## Principles

- **Small PRs only** — one issue per PR, max ~100 lines changed
- **No unsolicited refactors** — only change what the issue asks for
- **Match the project style** — copy the naming/formatting conventions already in use
- **Tests required** — never submit a code change without a test

---

*SwiftPay — CONTRIBUTION_PLAN.md | Software Engineering Assignment 15*
