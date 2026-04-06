# Contributing to BA-Kit

Thank you for your interest in improving BA-Kit.

BA-Kit runs on **3 agentic AI platforms** (Antigravity IDE, Claude Code, Claude CoWork). All platforms share the same skill files, so contributing works the same way regardless of which platform you use.

---

## 🏗️ Architecture Overview

*   **Logic**: The "Logic" is not in Python files; it is in the **Prompts** within `.agent/skills/`.
*   **Knowledge**: The "Textbook" is in `docs/knowledge_base/` (Markdown).
*   **Tools**: The "Hands" are standard command-line tools (`grep`, `python`, `curl`).

## ⚠️ Important Rules

### 1. Modifying Skills (`.agent/skills/`)
If you edit an agent's system prompt (the `SKILL.md` file):
*   **Do not break the XML**: The `<system_instructions>` tags are crucial.
*   **Do not remove System 2**: The "Reflective Loop" (Analysis -> Draft -> Reflection -> Output) is mandatory for v2.4 compatibility.
*   **Test**: You must verify the agent by summoning it in a new conversation:
    > "Hi @ba-modified-agent, run a self-test on task X."

### 2. Adding Knowledge
*   Place new guides in `docs/knowledge_base/`.
*   Update `AGENT.MD` or `USAGE-GUIDE.md` if the knowledge is critical.

### 3. Adding Templates
*   Place new artifacts in `templates/`.
*   Use standard Markdown or verifiable formats.

## 🐛 Reporting Bugs
*   If an Agent hallucinations, report the **Prompt ID** or the specific interaction.
*   If a Tool fails, ensure you have the required CLI installed (e.g., `graphviz` for diagrams).

## 🚀 Pull Request Process
1.  Fork the repo.
2.  Create a branch (`feature/new-agent-capability`).
3.  Commit changes.
4.  Open a PR describing *why* the Agent behavior needs changing.

---

*Code Less. Think More.*
