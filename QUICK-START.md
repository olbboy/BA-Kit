# ⚡ Quick Start: BA-Kit (Antigravity Edition)

Start using the World-Class Business Analysis Squad in **2 minutes**.

## 1. Installation

The BA-Kit creates a "Squad" of agents inside your Antigravity environment.

### Step A: Locate your Brain
Find where your Antigravity Agent stores its workflows.
*   Standard (Mac/Linux): `~/.gemini/antigravity/skills/`
*   *Note: If unsure, ask your Agent "Where are my skills stored?"*

### Step B: Deploy the Squad
Copy the 19 Agent Definitions into that folder.

```bash
# Clone the repository (if you haven't)
git clone https://github.com/olbboy/ba-kit.git

# Logic Copy
cp -r ba-kit/.agent/skills/* ~/.gemini/antigravity/skills/
```

## 2. Verification

Restart your Antigravity session.
Type `@` in the chat box. You should see the auto-complete list:
*   `@ba-master`
*   `@ba-writing`
*   `@ba-validation`
*   ... (and 12 others)

## 3. Your First Interaction

### Scenario: The "Vague Idea"
You have an idea but no requirements.
**Type:**
> `Hi @ba-elicitation I want to build a Tinder for Cats app.`

**Result:**
The **Journalist Agent** will activate, adopt the persona, and start the "Funnel Questioning" technique to extract your requirements.

### Scenario: The "Quality Check"
You have a requirement but aren't sure if it's good.
**Type:**
> `@ba-validation Review this user story: "User can upload photos."`

**Result:**
The **QA Lead Agent** will activate, use System 2 Reflection, and tell you: *"Ambiguous. What format? Max size? How many photos? Mobile or Web?"*

## 4. Power User Tips

*   **Flash Mode**: Switch agents instantly. `@ba-writing` -> `@ba-nfr` -> `@ba-solution`.
*   **The Manager**: If you are lost, just type `@ba-master help me`. The Dispatcher will tell you which agent you need.
*   **Tools**: The agents will automatically use `python` (for math) and `grep` (for search). You don't need to do anything.

## 5. Troubleshooting

**Q: The agent isn't appearing?**
A: Ensure the `SKILL.md` files are in the `skills/<agent_name>/` directory.

**Q: The agent is hallucinating math?**
A: Tell it: *"Use the run_command tool with python to verify that."* (Though v2.4 agents do this automatically).
