# Traceability Chain

The full requirements traceability path in BA-Kit projects.

## The Chain

```
Business Goal → KPI → Stakeholder Need → Use Case
    → BRD Feature → User Story → Acceptance Criteria
        → Test Case → API Endpoint → DB Table
```

Every artifact links to predecessor (backward) AND successor (forward). Break in chain = gap = risk.

## Coverage Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Backward Coverage | (US with BRD source) / Total US × 100 | 100% |
| Forward Coverage | (US with Test Cases) / Total US × 100 | 100% |
| Orphan Rate | (US without source) / Total US × 100 | 0% |
| Gold-Plating Rate | (Code without US) / Total code modules × 100 | 0% |

## Tools

- `ba-traceability` skill — build RTM, impact analysis, health check
- `coverage_checker.py` — automated scan
- RTM template — `.agent/templates/rtm-template.md`

## EAMS Project Example

46 US traced to 4 BRDs across 12 modules. Coverage: 100% backward (US→BRD), 0% forward (no TCs yet).

## Sources

- data/traceability.csv (35 entries)
- ebook-requirements-memory-jogger.md Ch.6
- IEEE 29148
