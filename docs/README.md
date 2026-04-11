# BA-Kit Documentation

## Tài liệu hướng dẫn

| Tài liệu | Mô tả | Đối tượng |
|-----------|-------|-----------|
| [AI Foundation for BA](./ai-foundation-for-ba.md) | Nền tảng AI cho Business Analysis | BA mới bắt đầu với AI |
| [AI Tools Guide](./ai-tools-guide.md) | Hướng dẫn sử dụng AI tools trong BA workflow | BA muốn tích hợp AI |
| [Antigravity Protocol](./antigravity-protocol.md) | Protocol giao tiếp giữa 25 agents | Developers |
| [Architecture Decisions](./architecture-decisions.md) | ADRs — quyết định kiến trúc | Tech Lead |
| [Design Prototype Guide](./design-prototype-guide.md) | Tạo prototype UI/UX cho BA | BA + Designer |
| [Junior Start](./junior-start.md) | Onboarding cho Junior BA | Junior BA |

## Cấu trúc BA-Kit

```
ba-kit-antigravity/
├── .agent/
│   ├── skills/         25 BA agents (.../SKILL.md)
│   ├── scripts/        Python utilities (search, coverage, docx)
│   ├── data/           23 CSV knowledge base files (809 entries)
│   └── templates/      13 BA document templates
├── docs/               Tài liệu hướng dẫn (folder này)
├── ebooks/             7 BA reference ebooks
└── outputs/            Project outputs (e.g., EAMS)
```

## Agent Activation

```
@ba-master       → Dispatcher (route requests)
@ba-elicitation  → Interview stakeholders
@ba-writing      → Write US/BRD/SRS
@ba-validation   → Validate quality (INVEST)
@ba-test-gen     → Generate test cases from AC
@ba-traceability → Build/audit RTM
@ba-quality-gate → Score artifacts (PASS/FAIL)
@ba-consistency  → Cross-artifact alignment
@ba-auditor      → Full project health report
```

## Knowledge Search

```bash
python3 .agent/scripts/ba_search.py "topic" --domain elicitation
python3 .agent/scripts/ba_search.py "query" --multi-domain
python3 .agent/scripts/coverage_checker.py outputs/project-name/
```
