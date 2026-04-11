---
name: ba-kit-search
description: "BM25+ knowledge search across 831 BA entries in 23 domains. Use before drafting requirements, reviewing specs, or analyzing."
user-invocable: true
argument-hint: "<search query> [--domain <domain>]"
---

# BA-Kit Knowledge Search Engine

Search the indexed BA knowledge base using BM25+ ranking.

## Usage

```bash
# Search specific domain
python3 .claude/skills/ba-kit-search/scripts/ba_search.py "acceptance criteria gherkin" --domain writing

# Auto-detect domain
python3 .claude/skills/ba-kit-search/scripts/ba_search.py "stakeholder power interest"

# Search all domains
python3 .claude/skills/ba-kit-search/scripts/ba_search.py "GDPR compliance" --multi-domain

# Statistics
python3 .claude/skills/ba-kit-search/scripts/ba_search.py --stats

# List domains
python3 .claude/skills/ba-kit-search/scripts/ba_search.py --list-domains
```

## 23 Domains

writing, elicitation, validation, nfr, process, prioritization, traceability, conflict, solution, systems, agile, identity, workshop, innovation, metrics, modeling, ux-research, business-rules, integration, compliance, communication, testing, data-analytics
