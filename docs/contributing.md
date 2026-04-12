# Contributing to BA-Kit

BA-Kit v3.1.0: 33 agents, 831 knowledge entries, 23 domains, 14 templates, 48 prompts.

---

## How to Add a New Agent

1. Tạo thư mục: `.agent/skills/ba-{name}/`
2. Tạo file: `.agent/skills/ba-{name}/SKILL.md`
3. Tuân theo cấu trúc bắt buộc:

```markdown
## AGENCY
[Mô tả role, scope, và khi nào agent được gọi]

## MEMORY
[Files agent cần đọc — CONTINUITY.md, data CSVs, v.v.]

## System Instructions
[Prompt chính — PHẢI có System 2 Reflection loop]

## Handoffs
[Agents nào nên được gọi sau agent này và trong tình huống nào]
```

**Bắt buộc trong System Instructions:**
- Vòng lặp: `Analysis → Draft → Reflect → Output`
- Không được bỏ Reflective Loop — đây là yêu cầu của v3.x
- Handoff protocol: agent PHẢI suggest agent tiếp theo khi xong việc

**Kiểm tra sau khi tạo:**
```
@ba-{tên-mới} "Run a self-test on task [X]"
```

---

## How to Add Knowledge

1. Xác định domain phù hợp trong `.agent/data/` (23 domains hiện có)
2. Thêm entries vào file CSV tương ứng: `.agent/data/{domain}.csv`
3. Nếu cần domain mới: tạo file `.agent/data/{domain-mới}.csv`

**Format CSV:**
```
id,domain,topic,content,source,tags
KE-{DOMAIN}-{NUMBER},{domain},{topic},{nội dung ngắn gọn},{nguồn},{tags}
```

**Kiểm tra sau khi thêm:**
```bash
python3 .agent/scripts/ba_search.py "{keyword trong entry mới}"
```

---

## How to Add Templates

1. Đặt file vào `.agent/templates/{tên-template}.md`
2. Dùng Markdown chuẩn, có placeholders rõ ràng: `[TÊN DỰ ÁN]`, `[NGÀY]`, v.v.
3. Cập nhật danh sách trong `docs/quick-start.md` nếu template quan trọng

**14 templates hiện có:** agile-artifacts, api-contract, brd, communication-plan, continuity, data-dictionary, frd, prd, rtm, srs, test-case, test-suite, use-case, user-story-spec

---

## Code Style — SKILL.md Conventions

| Rule | Chi tiết |
|------|---------|
| System 2 Reflection | Bắt buộc — `Analysis → Draft → Reflect → Output` |
| Handoff protocol | Mỗi agent PHẢI suggest agent tiếp theo |
| No hallucination | Dùng Python cho math, Grep cho file search |
| CONTINUITY.md | Agent phải đọc file này nếu tồn tại |
| Scope | Một agent = một domain, không overlap |

---

## Pull Requests

```bash
# Branch từ main
git checkout -b feat/ba-{tên-agent}-skill

# Conventional commits
git commit -m "feat: add @ba-{name} agent for {purpose}"
git commit -m "feat: add {N} knowledge entries to {domain} domain"
git commit -m "fix: correct handoff routing in @ba-{name}"

# Mở PR
gh pr create --title "feat: add @ba-{name}" --body "..."
```

**PR checklist:**
- [ ] SKILL.md có đủ AGENCY / MEMORY / System Instructions / Handoffs
- [ ] System 2 Reflection loop có trong System Instructions
- [ ] Agent đã được self-test thủ công
- [ ] Không có thông tin nhạy cảm (API keys, credentials)
- [ ] CHANGELOG cập nhật nếu thêm agent mới

---

*Code Less. Think More.*
