# CONTRIBUTING.md — SwiftPay Contribution Guide

Welcome to SwiftPay! We're glad you want to contribute. This guide covers everything you need to get started.

---

## Prerequisites

- Python 3.10 or higher
- Git
- A GitHub account

---

## Setup Instructions

```bash
# 1. Fork this repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/SwiftPay.git
cd SwiftPay

# 2. Verify Python version
python3 --version  # must be 3.10+

# 3. No pip install needed — SwiftPay uses stdlib only
# Optionally install pytest for enhanced test output:
pip install pytest pytest-cov

# 4. Run all tests to verify your setup
python3 tests/run_all_tests.py
```

All **41 tests should pass** before you start making changes.

---

## How to Pick an Issue

1. Browse [open issues](../../issues)
2. Look for issues labelled:
   - `good-first-issue` — small, well-scoped tasks perfect for new contributors
   - `help-wanted` — larger tasks where input is welcome
   - `feature-request` — new capabilities (higher impact, more complex)
3. Comment on the issue: *"I'd like to work on this!"* — wait for confirmation before starting to avoid duplicate work
4. Create a branch: `git checkout -b fix-issue-42` or `git checkout -b feature/redis-otp`

---

## Coding Standards

- **Language:** Python 3.10+
- **Style:** Follow PEP 8. Function and variable names in `snake_case`, classes in `PascalCase`
- **Private fields:** Prefix with `_` (e.g. `self._balance`)
- **Type hints:** Use them on all public method signatures
- **Docstrings:** Required on all public classes and methods
- **No external dependencies** for core domain/service/repository code — stdlib only
- External dependencies for API framework (Flask/FastAPI) are acceptable; add to `requirements.txt`

---

## Testing Requirements

- Every new feature must include tests in the `/tests` directory
- Every bug fix must include a test that reproduces the bug before the fix
- Run `python3 tests/run_all_tests.py` — all tests must pass before submitting a PR
- Aim for coverage of happy path + at least 2 edge cases per function

---

## Submitting a Pull Request

1. Ensure all tests pass: `python3 tests/run_all_tests.py`
2. Write a clear PR title: `Fix: Rollback not triggered on gateway timeout` or `Feature: Add OTP expiry endpoint`
3. In the PR description:
   - Link the issue: `Closes #42`
   - Describe what changed and why
   - List any edge cases you tested
4. CI will run automatically — the PR cannot be merged if CI fails
5. A maintainer will review within 2 business days

---

## Project Structure

```
SwiftPay/
├── src/               # Domain models (User, Wallet, Transaction...)
├── repositories/      # Repository interfaces + in-memory implementations
├── services/          # Business logic (UserService, TransactionService...)
├── api/               # REST API (app.py)
├── tests/             # All tests
│   ├── services/
│   └── api/
├── .github/workflows/ # CI/CD pipeline
└── docs/              # OpenAPI specification
```

---

## Code of Conduct

Be respectful. Be constructive. If you disagree with a review comment, explain your reasoning — don't just revert it.

---

*SwiftPay — CONTRIBUTING.md*
