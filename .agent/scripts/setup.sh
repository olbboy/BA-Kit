#!/usr/bin/env bash
# setup.sh — install BA-Kit skills into a target agent host.
#
# Usage:
#   ./setup.sh                  # auto-detect host
#   ./setup.sh antigravity      # Antigravity IDE (Google DeepMind)
#   ./setup.sh claude-code      # Claude Code CLI (Anthropic)
#   ./setup.sh cowork           # Claude CoWork Desktop (Anthropic)
#   ./setup.sh --list           # show detected hosts and target paths
#
# Mirrors gstack ./setup --host pattern. Idempotent: re-running updates
# in place, never touches user configs.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SKILLS_SRC="${REPO_ROOT}/.agent/skills"

# ---------------------------------------------------------------------------
# Host target resolution
# ---------------------------------------------------------------------------

target_for_host() {
    local host="$1"
    case "$host" in
        antigravity) echo "${HOME}/.gemini/antigravity/skills" ;;
        claude-code) echo "${HOME}/.claude/skills" ;;
        cowork)      echo "${HOME}/Library/Application Support/Claude/skills" ;;
        *) return 1 ;;
    esac
}

host_exists() {
    local host="$1"
    case "$host" in
        antigravity) [[ -d "${HOME}/.gemini/antigravity" ]] ;;
        claude-code) [[ -d "${HOME}/.claude" ]] ;;
        cowork)      [[ -d "${HOME}/Library/Application Support/Claude" ]] ;;
        *) return 1 ;;
    esac
}

detect_host() {
    for candidate in antigravity claude-code cowork; do
        if host_exists "$candidate"; then
            echo "$candidate"
            return 0
        fi
    done
    return 1
}

# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------

list_hosts() {
    echo "Detected BA-Kit host candidates:"
    for candidate in antigravity claude-code cowork; do
        if host_exists "$candidate"; then
            local target
            target=$(target_for_host "$candidate")
            echo "  ✓ ${candidate} → ${target}"
        else
            echo "  ✗ ${candidate} (not installed)"
        fi
    done
}

install_to() {
    local host="$1"
    local target
    target=$(target_for_host "$host") || {
        echo "Unknown host: $host" >&2
        return 2
    }

    if [[ ! -d "$SKILLS_SRC" ]]; then
        echo "Skills source not found: $SKILLS_SRC" >&2
        return 2
    fi

    echo "→ Installing BA-Kit skills to: $target"
    mkdir -p "$target"

    # Copy each skill dir; -R preserves structure and is portable.
    # Use rsync-like behavior if available for cleaner output.
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete-during \
            --exclude='.git' \
            "${SKILLS_SRC}/" "${target}/"
    else
        cp -R "${SKILLS_SRC}/." "${target}/"
    fi

    # Report
    local count
    count=$(find "$target" -name SKILL.md -type f | wc -l | tr -d ' ')
    echo "✓ Installed ${count} skills to ${target} (${host})"
    echo
    echo "Next steps:"
    case "$host" in
        antigravity)
            echo "  Restart Antigravity and type @ba-master to verify." ;;
        claude-code)
            echo "  Run 'claude --help' and check skills under @ba-*." ;;
        cowork)
            echo "  Restart Claude CoWork and verify skill palette." ;;
    esac
}

# ---------------------------------------------------------------------------
# CLI parsing
# ---------------------------------------------------------------------------

main() {
    local host="${1:-}"

    if [[ "$host" == "--list" || "$host" == "-l" ]]; then
        list_hosts
        exit 0
    fi

    if [[ "$host" == "--help" || "$host" == "-h" ]]; then
        sed -n '2,12p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
        exit 0
    fi

    if [[ -z "$host" ]]; then
        echo "No host specified. Auto-detecting..."
        host=$(detect_host) || {
            echo "Could not auto-detect. Use: $0 <antigravity|claude-code|cowork>" >&2
            exit 1
        }
        echo "Detected: $host"
    fi

    install_to "$host"
}

main "$@"
