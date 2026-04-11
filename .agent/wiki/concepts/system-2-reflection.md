# System 2 Reflection

Every BA-Kit agent follows a dual-process cognitive loop before delivering output.

## Pattern

```
Input → System 1 (fast draft) → System 2 (slow critique) → Refined Output
```

System 2 manifests as a `### Reflection Mode` section in every SKILL.md:
- **Critic questions**: "Is this math right?", "Did I hallucinate links?", "Am I biased toward the CEO?"
- **Actions**: Use tools to verify (Python for math, Grep for links, WebSearch for standards)
- **Gate**: If any critic fails → fix before output. Never deliver unchecked work.

## Why It Works

LLMs are System 1 machines — fast pattern matching. System 2 reflection forces a pause that catches:
- Hallucinated file references (verify with Grep)
- Wrong calculations (verify with Python)
- Outdated standards (verify with WebSearch)
- Bias toward powerful stakeholders (check Power/Interest grid)

## Agents Using This

All 25 agents. Enforced via `_shared/system-prompt.md`.

## Sources

- ebook-fundamentals.md (BABOK Validation)
- Kahneman — Thinking, Fast and Slow (System 1 vs System 2)
- AGENT.MD cognitive architecture diagram
