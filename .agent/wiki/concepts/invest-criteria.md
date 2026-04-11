# INVEST Criteria

Quality gate for User Stories. A story must pass all 6 criteria.

## The Criteria

| Letter | Criterion | Question | Fail Example |
|--------|-----------|----------|-------------|
| **I** | Independent | Can this US be built without others? | "Login" depends on "Create Account" |
| **N** | Negotiable | Can scope be discussed? | Fixed technical spec with no flexibility |
| **V** | Valuable | Does it deliver user/business value? | "Refactor database" (no user value) |
| **E** | Estimable | Can dev estimate effort? | "Integrate with all systems" (too vague) |
| **S** | Small | Fits in one sprint? | Epic disguised as story |
| **T** | Testable | Can we write acceptance criteria? | "System should be fast" (unmeasurable) |

## ba-validation Scoring

`@ba-validation` scores each criterion ✅/❌ then gives overall INVEST pass/fail. A story with any ❌ is CONDITIONAL — must fix before sprint.

## Common Anti-Patterns

- **"As a user, I want the system to work"** → fails V, E, S, T
- **"As a dev, I want to refactor"** → fails V (no user value)
- **"As a user, I want everything"** → fails S, E

## Sources

- ebook-techniques.md (Wiegers INVEST)
- data/writing.csv
- ba-writing skill (drafting mode)
- ba-validation skill (INVEST check)
