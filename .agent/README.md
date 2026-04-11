# .agent/ — BA-Kit Agent System

Core engine của BA-Kit Antigravity: 25 specialized Business Analysis agents.

## Cấu trúc

```
.agent/
├── skills/                     25 BA agents + 2 connectors
│   ├── _shared/                System prompt fragment (shared identity)
│   │   └── system-prompt.md    Prepend cho tất cả agents
│   │
│   ├── ba-master/              Orchestrator — route requests tới đúng agent
│   │
│   ├── ── Core Workflow ──
│   ├── ba-elicitation/         Khai thác requirements (Funnel, 5W1H, Why Laddering)
│   ├── ba-writing/             Viết US/BRD/SRS (INVEST, Gherkin)
│   ├── ba-validation/          Validate chất lượng (INVEST check, ambiguity scan)
│   ├── ba-test-gen/            Generate test cases từ AC (Happy/Edge/Error/Security)
│   ├── ba-traceability/        RTM — build, impact analysis, health check
│   ├── ba-quality-gate/        Quality scoring pipeline (8 dimensions, PASS/FAIL)
│   ├── ba-consistency/         Cross-artifact alignment (US↔API↔DB)
│   ├── ba-auditor/             Meta-agent — full project health report
│   │
│   ├── ── Specialized ──
│   ├── ba-agile/               Story Mapping, MVP, Hypothesis-Driven
│   ├── ba-nfr/                 NFR framework (ISO 25010)
│   ├── ba-process/             BPMN modeling (As-Is/To-Be)
│   ├── ba-prioritization/      MoSCoW, RICE, WSJF ranking
│   ├── ba-metrics/             SPC, defect density, control charts
│   ├── ba-identity/            Stakeholder mapping (Power/Interest, RACI)
│   ├── ba-conflict/            Conflict resolution (Harvard Negotiation, ADR)
│   ├── ba-root-cause/          Fishbone, 5 Whys, Pareto
│   ├── ba-innovation/          A/B testing, hypothesis design
│   ├── ba-solution/            Business case, ROI analysis
│   ├── ba-strategy/            SWOT, PESTLE, Porter's, BMC
│   ├── ba-systems/             Systems thinking (Stocks/Flows/Loops)
│   ├── ba-facilitation/        Workshop design (ODEC)
│   ├── ba-export/              Enterprise DOCX export (Pandoc)
│   │
│   ├── ── Integrations ──
│   ├── ba-confluence/          Publish/import Confluence pages
│   ├── ba-jira/                Sync tickets to Jira
│   ├── confluence-connector/   Confluence REST API client + tools
│   └── jira-connector/         Jira REST API client
│
├── scripts/                    Python utilities
│   ├── ba_core.py              BM25+ search engine core
│   ├── ba_search.py            CLI: search knowledge base
│   ├── coverage_checker.py     CLI: RTM coverage scanner
│   ├── gen_docx.py             DOCX generation via Pandoc
│   └── batch_remediate.py      Batch fix/cleanup utility
│
├── data/                       Knowledge base (23 CSV files, 809 entries)
│   ├── agile.csv               15 entries — Agile practices
│   ├── elicitation.csv         70 entries — Questioning techniques
│   ├── writing.csv             50 entries — Requirements writing
│   ├── validation.csv          50 entries — Quality validation
│   ├── traceability.csv        35 entries — RTM, change control
│   ├── testing.csv             30 entries — Test design
│   └── ... (17 more domains)
│
└── templates/                  13 BA document templates
    ├── brd-template.md         Business Requirements Document
    ├── srs-template.md         Software Requirements Specification
    ├── user-story-spec-template.md  User Story Specification
    ├── test-case-template.md   Test Case (Given/When/Then)
    ├── rtm-template.md         Requirements Traceability Matrix
    └── ... (8 more templates)
```

## Cách sử dụng

### Activation (Antigravity)
```
@ba-master "Tôi cần viết BRD cho module chấm công"
→ Master routes tới @ba-writing → output BRD draft
→ Handoff: @ba-validation → quality check
→ Handoff: @ba-test-gen → generate test cases
```

### Knowledge Search
```bash
python3 .agent/scripts/ba_search.py "stakeholder interview" --domain elicitation
python3 .agent/scripts/ba_search.py "INVEST criteria" --multi-domain
```

### Coverage Check
```bash
python3 .agent/scripts/coverage_checker.py outputs/project-name/
```

## Thêm skill mới

1. Tạo folder `.agent/skills/ba-{name}/SKILL.md`
2. Frontmatter bắt buộc: `name`, `description`, `version`
3. Sections bắt buộc: AGENCY, MEMORY, System Instructions, Reflection Mode, Squad Handoffs, Knowledge Search, Knowledge Reference
4. Tạo CSV tương ứng trong `.agent/data/{domain}.csv` (nếu cần)
5. Đăng ký trong `ba-master/SKILL.md` decision matrix

## 2-Tier Knowledge (Karpathy LLM Wiki Pattern)

```
Tier 1: data/*.csv      → 809 curated entries (human-verified, frozen)
Tier 2: wiki/            → Living pages (LLM-maintained, compounds)
         ├── concepts/   BA concept pages
         ├── projects/   Project-specific context
         └── decisions/  ADRs and key decisions
```

Operations: `@ba-wiki ingest <source>` | `@ba-wiki query "<question>"` | `@ba-wiki lint`

Search both tiers: `python3 .agent/scripts/ba_search.py "query" --wiki --multi-domain`

## Cognitive Architecture

Mỗi agent tuân theo System 2 Reflection loop:

```
User Input → System 1 (Draft) → System 2 (Reflect/Challenge) → Refined Output
```

Behavioral Principles:
- **ALWAYS**: Verify math (Python), verify links (Grep), verify standards (WebSearch), Reflect
- **NEVER**: Assume user intent — ask `@ba-elicitation`. Hallucinate file contents — check with Grep/Read

## Multi-platform

Xem `.claude-output/MIGRATION-GUIDE.md` để deploy lên Claude Code, Cowork, hoặc Codex.
