# Decision: 2-Tier Knowledge Architecture

**Date:** 2026-04-11
**Status:** Accepted
**Decider:** BA Team

## Context

BA-Kit had 786 expert-curated CSV entries across 23 domains. High quality but static — zero growth after creation. New project insights (EAMS decisions, edge case patterns, client preferences) were lost between sessions. Andrej Karpathy's LLM Wiki pattern proposed a persistent, compounding wiki maintained by LLMs.

## Decision

Adopt 2-tier knowledge architecture:

```
Tier 1: .agent/data/*.csv    — CURATED, FROZEN, HIGH-TRUST
         786 entries. Human-verified. Source: 7 ebooks + expert knowledge.
         LLM reads but NEVER modifies.

Tier 2: .agent/wiki/         — LIVING, COMPOUNDS, LLM-MAINTAINED
         Concepts, projects, decisions. Grows with each project.
         LLM creates, updates, cross-links pages.
```

## Operations (Karpathy Pattern)

- **Ingest**: Process new source → create/update wiki pages
- **Query**: Search both tiers → synthesize answer
- **Lint**: Health check wiki — contradictions, stale, orphans

## Alternatives Rejected

- **Replace CSV with wiki only**: Loses 786 curated entries. Hallucination risk.
- **Keep CSV only**: No growth. Knowledge frozen at v1.0.
- **RAG over raw docs**: Rediscovers knowledge from scratch every query. No compounding.

## Consequences

- Knowledge grows ~50-80 entries/month (wiki tier)
- CSV quality preserved (never auto-modified)
- Query accuracy improves: project-specific + general knowledge
- Maintenance: near-zero (LLM maintains wiki)

## Sources
- Karpathy LLM Wiki (2026): https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- plans/reports/skill-assessment-260411-1507-ba-kit-agent-skills.md
