# Quick Start: BA-Kit

Start using the BA-Kit agent squad in **2 minutes**.

---

## 1. Choose Your Platform

BA-Kit runs on 3 agentic AI platforms. Pick one:

| Platform | Best For | Setup |
|----------|----------|-------|
| **Antigravity IDE** | Full agent skills, MCP integration, System 2 | Copy `.agent/skills/` |
| **Claude Code** | CLI developers, CI/CD, Git-native workflows | Copy `.agent/skills/` |
| **Claude CoWork** | Non-technical BAs, document synthesis | Copy `.agent/skills/` |

All 3 platforms use the same skill files. The setup is identical.

## 2. Installation

### Step A: Clone the Repository

```bash
git clone https://github.com/olbboy/BA-Kit.git
```

### Step B: Deploy the Squad

Copy the 26 agent skill files into your platform's workspace:

**Antigravity IDE:**
```bash
cp -r BA-Kit/.agent/skills/* <your-project>/.agent/skills/
```

**Claude Code:**
```bash
cp -r BA-Kit/.agent/skills/* <your-project>/.agent/skills/
```

**Claude CoWork:**
```bash
# Drag the BA-Kit folder into your CoWork project
# Or copy .agent/skills/ to your project directory
```

### Step C: Copy Templates & Knowledge (Optional)

```bash
cp -r BA-Kit/templates/ <your-project>/templates/
cp -r BA-Kit/docs/knowledge_base/ <your-project>/docs/knowledge_base/
cp -r BA-Kit/ebooks/ <your-project>/ebooks/
```

## 3. Verification

Start a new conversation in your platform.
Type `@` in the chat box. You should see the auto-complete list:
*   `@ba-master`
*   `@ba-writing`
*   `@ba-validation`
*   `@ba-elicitation`
*   ... (and 22 others)

## 4. Your First Interaction

### Scenario: The "Vague Idea"
You have an idea but no requirements.

> `@ba-elicitation I want to build a task management app for freelancers.`

**Result:** The agent will start Funnel Questioning to extract your requirements.

### Scenario: The "Quality Check"
You have a requirement but aren't sure if it's good.

> `@ba-validation Review this user story: "User can upload photos."`

**Result:** The agent will identify ambiguities: *"What format? Max size? How many? Mobile or Web?"*

### Scenario: The "Full Pipeline"
You want to go from idea to dev-ready specs.

> `@ba-master I need to build a customer feedback portal. Guide me through the full process.`

**Result:** The orchestrator will route you through: elicitation → writing → prioritization → validation → export.

## 5. Power User Tips

*   **Flash Mode**: Switch agents instantly. `@ba-writing` → `@ba-nfr` → `@ba-solution`.
*   **The Dispatcher**: If lost, type `@ba-master help me` — it routes to the right specialist.
*   **Tools**: Agents automatically use `python` (math), `grep` (search), `search_web` (standards).
*   **Prompt Library**: See `docs/prompt-library.md` for 33 copy-paste prompts.
*   **Design**: Use Stitch MCP / Figma MCP for UI generation. See `docs/design-prototype-guide.md`.

## 6. Troubleshooting

**Q: The agent isn't appearing?**
A: Ensure `SKILL.md` files are in `.agent/skills/<agent_name>/` directories.

**Q: Which platform should I use?**
A: See `docs/ai-tools-guide.md` for the full comparison matrix.

**Q: Where are the templates?**
A: `templates/` folder — PRD, BRD, SRS, FRD, Use Case, Data Dictionary, and more.

---

*Antigravity • Claude Code • Claude CoWork — Code Less. Think More.*
