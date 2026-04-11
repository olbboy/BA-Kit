# Decision: Phase-Based Directory Structure

**Date:** 2026-04-11
**Status:** Accepted
**Decider:** BA Team

## Context

EAMS documentation used Confluence-style module numbering (2.11.1 through 2.11.12). Module 05 (HR) must be implemented before Module 01 (Attendance), but numbering implied opposite order. Developers didn't know which module to start with.

## Decision

Restructure into 5 phases matching UAT Scenarios sprint mapping:

```
phase-01-thiet-lap/  (Sprint 8: m05, m06, m07, m09)
phase-02-dinh-danh/  (Sprint 8: m08)
phase-03-van-hanh/   (Sprint 8: m01)
phase-04-xu-ly/      (Sprint 9: m04, m03, m10)
phase-05-ket-thuc/   (Sprint 10: m05-rpt, m11)
cross-cutting/       (Ongoing: m12)
```

Each phase folder contains: plan.md (roadmap + dependency DAG) + module folders (BRD + US + API spec + DB schema).

## Consequences

- Dev opens phase folder → knows exactly what to build and in what order
- BA/PO reviews by phase → sprint-aligned
- Added 30 new files (6 plans + 12 API specs + 12 DB schemas)
- All old 2.11.x paths broken → migrated with git mv (history preserved)
