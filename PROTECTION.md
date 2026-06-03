# PROTECTION.md — Branch Protection Rules
## SwiftPay Mobile Payment App

> **Assignment 13 | Branch Protection Setup**

---

## Rules Applied to `main` Branch

| Rule | Setting | Why |
|---|---|---|
| Require pull request reviews | ✅ Minimum 1 reviewer | Prevents unreviewed code from reaching production. Every change is seen by at least one other person before merging. |
| Require status checks to pass | ✅ `test` job must pass | The CI pipeline runs all 41 tests on every PR. A failing test blocks the merge — no broken code reaches `main`. |
| Require branches to be up to date | ✅ Enabled | Forces PRs to rebase on the latest `main` before merging, preventing integration failures from stale branches. |
| Restrict direct pushes | ✅ No direct push to main | All changes must go through a PR. This creates an audit trail for every change and prevents accidental force-pushes. |
| Require linear history | ✅ Enabled | Squash/rebase merges keep `git log` readable — no merge commit clutter. |

---

## Why These Rules Matter

**1. Quality Gate — Tests Must Pass**
The CI workflow (`ci.yml`) runs all 41 tests across repository, service, and API layers. If any test fails, the PR is blocked. This enforces the principle that `main` always represents a deployable, working state of SwiftPay.

**2. Code Review — No Solo Merges**
Financial systems carry real consequences for bugs. A second pair of eyes on every PR catches logic errors (e.g. an off-by-one in a balance calculation) before they reach users' wallets. This directly supports FR-08 (atomicity) and NFR-09 (security).

**3. No Direct Pushes — Full Audit Trail**
Every change to `main` is traceable to a PR, a reviewer, and a set of CI results. This satisfies the Compliance Officer's requirement (from Assignment 4) for audit traceability of system changes.

**4. Up-to-Date Branches — No Integration Surprises**
Requiring branches to be current before merging means two PRs cannot simultaneously pass CI in isolation and then break `main` when both land. This is especially important for the wallet balance logic where concurrent changes could introduce race conditions.

---

## How to Set Up Branch Protection on GitHub

1. Go to your SwiftPay repository → **Settings** → **Branches**
2. Under "Branch protection rules" click **"Add rule"**
3. Branch name pattern: `main`
4. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require approvals (set to 1)
   - ✅ Require status checks to pass before merging
   - ✅ Search for and select: `test` (your CI job name)
   - ✅ Require branches to be up to date before merging
   - ✅ Do not allow bypassing the above settings
5. Click **Save changes**

---

*SwiftPay — PROTECTION.md | Software Engineering Assignment 13*
