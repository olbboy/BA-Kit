# Quick Start — BA-Kit v3.1.0

Bắt đầu trong 5 phút. 33 agents, 831 knowledge entries, 14 templates.

---

## Prerequisites

Chỉ cần một trong 3 platforms bên dưới. Không cần cài thêm gì khác.

---

## Installation

### Clone repo

```bash
git clone https://github.com/olbboy/BA-Kit.git
cd BA-Kit
```

### Deploy theo platform

| Platform | Command | Ghi chú |
|----------|---------|---------|
| **Antigravity IDE** | `cp -r .agent/skills/* ~/.gemini/antigravity/skills/` | Full experience, MCP support |
| **Claude Code** | Clone repo vào project, skills tự nhận diện | CLI-native, git workflows |
| **Claude CoWork** | Upload từng `SKILL.md` làm project knowledge | Dễ dùng nhất cho BA truyền thống |

### Copy templates & data (khuyến nghị)

```bash
cp -r .agent/templates/ <your-project>/.agent/templates/
cp -r .agent/data/      <your-project>/.agent/data/
```

### Kiểm tra cài đặt

Gõ `@` trong chat — phải thấy autocomplete list bắt đầu bằng `@ba-master`, `@ba-writing`, v.v.

---

## First Use — 3 ví dụ nhanh

**Bắt đầu dự án mới:**
```
@ba-master "New project: [tên dự án]. Where do I start?"
```

**Viết User Story:**
```
@ba-writing "Write User Story for [tính năng] — Gherkin format, 3 ACs minimum"
```

**Review spec:**
```
@ba-validation "Review this spec: [paste nội dung]"
```

---

## Knowledge Search

Tìm kiếm trong 831 entries × 23 domains:

```bash
# Tìm theo keyword
python3 .agent/scripts/ba_search.py "MoSCoW prioritization"

# Tìm trong domain cụ thể
python3 .agent/scripts/ba_search.py "user story" --domain writing

# Xem tất cả domains
python3 .agent/scripts/ba_search.py --list-domains
```

---

## What's Next

| Tài liệu | Nội dung |
|----------|---------|
| `docs/usage-guide.md` | Cách squad 33 agents hoạt động, workflow chains |
| `docs/agent-cheat-sheet.md` | Toàn bộ 33 agents + power combos |
| `docs/prompt-library.md` | 48 copy-paste prompts theo tình huống |
| `docs/junior-start.md` | Lộ trình 4 tuần cho BA mới |

---

## FAQ

**Q: Không thấy agent trong autocomplete?**
Kiểm tra `SKILL.md` có đúng đường dẫn `.agent/skills/<tên-agent>/SKILL.md` không.

**Q: Dùng platform nào tốt nhất?**
Technical BA → Antigravity IDE. BA truyền thống → Claude CoWork. DevOps BA → Claude Code.

**Q: Templates ở đâu?**
`.agent/templates/` — 14 files: BRD, SRS, FRD, PRD, User Story Spec, RTM, Use Case, v.v.

**Q: Knowledge base có gì?**
831 entries, 23 domains (writing, validation, elicitation, nfr, process, v.v.). Search bằng `ba_search.py`.

**Q: Bắt đầu không biết gọi agent nào?**
Luôn gọi `@ba-master` — nó sẽ dispatch đến đúng specialist.

---

*Antigravity • Claude Code • Claude CoWork — Code Less. Think More.*
