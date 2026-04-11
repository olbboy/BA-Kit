# Decision: 4-BRD Persona Strategy

**Date:** 2026-04-11
**Status:** Accepted
**Decider:** BA Team

## Context

EAMS had 2 BRDs: HR Admin (8 features) + Nhân viên (6 features). As system grew to 12 modules with 6 distinct user roles, 2 BRDs could not represent all personas adequately. Manager workflow (approval, team dashboard) was buried inside HR Admin BRD.

## Decision

Split into 4 BRDs by persona grouping:

| BRD | Persona | Features |
|-----|---------|----------|
| BRD-01 | EMPLOYEE | 6 ESS functions |
| BRD-02 | MANAGER, DEPT_HEAD | 7 approval + monitoring |
| BRD-03 | SITE_HR, GLOBAL_HR | 13 admin functions |
| BRD-04 | IT_ADMIN, SYS_ADMIN | 10 technical functions |

## Alternatives Rejected

- **6 BRDs (1 per role)**: Over-engineered, duplicate content between Manager/DEPT_HEAD
- **Keep 2 BRDs**: Insufficient — Manager persona invisible
- **BRD per module**: 12 BRDs = fragmented, hard to review holistically

## Consequences

- Each persona has dedicated review document for UAT
- Training materials can be role-specific
- Maintenance cost: 4 files instead of 2 (acceptable)
