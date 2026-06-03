# REFLECTION_A15.md — Cross-Project Contribution Lessons
## SwiftPay | Assignment 15

---

## Reflection: Contributing to Peers' Repositories

### What I Learned from Contributing to Another Codebase

Contributing to a peer's repository is a fundamentally different experience from writing your own code. When working on SwiftPay, every architectural decision made sense because I made it. Walking into someone else's codebase means encountering a different set of decisions — some that I agreed with, some that surprised me, and some that I would have done differently. That friction is valuable. It forces you to read code more carefully, ask questions before assuming, and write changes that fit into an existing style rather than imposing your own.

The most important skill this process developed was **reading code before writing it**. Before making any change to a peer's repository, I spent time understanding the existing patterns: how errors were handled, what naming conventions were used, whether tests were written before or after implementation. Matching these conventions — even when they differed from my own preferences — is what makes a PR acceptable to a maintainer. A technically correct change that violates the project's style is harder to review and less likely to be merged.

### Challenges Encountered

**Finding the right scope** was consistently the hardest part. Issues labelled `good-first-issue` sometimes turned out to require understanding several interconnected components. Before commenting "I'll work on this," I learned to trace the issue through the codebase — find the relevant files, understand what they depend on, and estimate the real scope — rather than assuming the label meant the work was trivial.

**CI failures on first submission** were a common experience. A change that passed my local test runner would sometimes fail the peer's CI pipeline due to a different Python version, a missing import, or a test fixture that my change accidentally broke. This taught me to always run the full test suite before pushing, and to read the CI configuration carefully to understand what environment it uses.

**Review response time** required patience. Maintainers have their own workload. Waiting 24–48 hours for a review comment, then addressing it promptly, is part of the collaborative rhythm. The temptation to close and reopen a PR to get attention should be resisted — a polite comment after 48 hours is the appropriate escalation.

### Lessons for Open-Source Work

The experience reinforced several principles that apply directly to real-world open-source contribution:

1. **Communicate before coding.** Commenting on an issue before starting prevents wasted work and duplicate effort. It also signals to the maintainer that you're engaged and thoughtful.

2. **Small PRs get merged. Large PRs get stuck in review.** A 20-line PR that fixes one clear thing is reviewed in minutes. A 200-line PR that touches multiple files requires the reviewer to hold a lot of context in their head — it sits in the review queue longer and is more likely to generate requests for changes.

3. **Tests are the difference between a contribution and a risk.** A code change without a test asks the maintainer to trust that nothing broke. A code change with a test that reproduces the bug or verifies the feature gives the maintainer confidence to merge.

---

*SwiftPay — REFLECTION_A15.md | Software Engineering Assignment 15*
