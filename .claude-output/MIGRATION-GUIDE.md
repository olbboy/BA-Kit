# BA-Kit Multi-Platform Deployment Guide

## Canonical Source

**`.agent/skills/`** = source of truth (26 BA skills + 2 connectors).

**`.claude-output/`** = pre-built export for Claude Code deployment.

## Platform Targets

| Platform | Skill Location | Activation | Status |
|----------|---------------|------------|--------|
| Antigravity | `.agent/skills/ba-xxx/` | `@ba-xxx` | Production |
| Claude Code | `~/.claude/skills/ba-xxx/` | `/ba-xxx` | Ready (copy .claude-output/) |
| Claude Cowork | Project `.claude/skills/` | `/ba-xxx` | Same as Claude Code |
| Codex (OpenAI) | `.codex/agents/` | Agent config | Needs adapter |

## Claude Code Deployment

```bash
# Copy skills
cp -r .claude-output/skills/* ~/.claude/skills/

# Copy CLAUDE.md (squad instructions)
cp .claude-output/CLAUDE.md .claude/CLAUDE.md

# Verify
ls ~/.claude/skills/ba-*/SKILL.md | wc -l  # expect: 26+
python3 ~/.claude/skills/ba-kit-search/scripts/ba_search.py --stats
```

## Tool Name Mapping

| Action | Antigravity | Claude Code | Codex |
|--------|------------|-------------|-------|
| Run Python | `run_command` | `Bash` tool | `shell` |
| Search files | `grep_search` | `Grep` tool | `grep` |
| Write file | `write_to_file` | `Write` tool | `write_file` |
| Read file | `read_file` | `Read` tool | `read_file` |
| Web search | `search_web` | `WebSearch` tool | N/A |
| Ask user | Direct prompt | `AskUserQuestion` | N/A |

## Self-Contained Skill Format (Claude Code)

Each skill folder must be self-contained:
```
ba-kit-search/
├── SKILL.md           ← Skill definition
├── scripts/           ← Python utilities (bundled)
│   ├── ba_core.py
│   └── ba_search.py
└── data/              ← Knowledge CSVs (bundled)
    └── *.csv (23 files)
```

## Sync Workflow

When `.agent/skills/` is updated:
1. Run export script to regenerate `.claude-output/skills/`
2. Test on Claude Code
3. Commit both canonical + export
