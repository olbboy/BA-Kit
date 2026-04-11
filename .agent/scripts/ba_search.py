#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BA-Kit Knowledge Search CLI — BM25 search for Business Analysis knowledge.
Usage:
  python3 ba-search.py "acceptance criteria gherkin"
  python3 ba-search.py "EARS pattern" --domain writing
  python3 ba-search.py "validate NFR" --multi-domain
  python3 ba-search.py "ambiguous words" --max-results 5
  python3 ba-search.py "OT holiday rate" --wiki          # Search wiki (Tier 2)
  python3 ba-search.py "traceability" --multi-domain --wiki  # Both tiers
  python3 ba-search.py --list-domains
"""

import argparse
import json
import sys
import os

# Add scripts dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ba_core import (
    AVAILABLE_DOMAINS,
    DATA_DIR,
    DOMAIN_FILES,
    MAX_RESULTS,
    search,
    search_multi,
)


def format_output(result):
    """Format results for LLM consumption (token-optimized)."""
    if "error" in result:
        return f"Error: {result['error']}"

    lines = []
    if result.get("domains"):
        lines.append(f"## BA Knowledge Search (Multi-Domain)")
        lines.append(f"**Query:** {result['query']} | **Found:** {result['count']}")
    else:
        lines.append(f"## BA Knowledge Search")
        lines.append(f"**Domain:** {result['domain']} | **Query:** {result['query']} | **Found:** {result['count']}")
    lines.append("")

    for i, entry in enumerate(result["results"], 1):
        score = entry.pop("_score", 0)
        entry_id = entry.get("entry_id", "?")
        title = entry.get("title", "Untitled")
        entry_type = entry.get("type", "?")
        domain = entry.get("domain", result.get("domain", "?"))

        lines.append(f"### [{entry_id}] {title} ({entry_type}) — score: {score}")
        lines.append(f"**Domain:** {domain} | **Agents:** {entry.get('agents', '?')}")

        content = entry.get("content", "")
        if len(content) > 500:
            content = content[:500] + "..."
        lines.append(f"\n{content}\n")

        tags = entry.get("tags", "")
        if tags:
            lines.append(f"**Tags:** {tags}")

        source = entry.get("source", "")
        if source:
            lines.append(f"**Source:** {source}")
        lines.append("")

    if result["count"] == 0:
        lines.append("No results found. Try broader keywords or a different domain.")
        lines.append(f"Available domains with data: {', '.join(d for d, f in DOMAIN_FILES.items() if (DATA_DIR / f).exists())}")

    return "\n".join(lines)


def search_wiki(query, max_results=5):
    """Search Tier 2 wiki pages using simple keyword matching."""
    wiki_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "wiki")
    if not os.path.isdir(wiki_dir):
        return {"query": query, "tier": 2, "count": 0, "results": [], "error": "Wiki directory not found"}

    results = []
    query_lower = query.lower()
    query_terms = query_lower.split()

    for root, dirs, files in os.walk(wiki_dir):
        for fname in files:
            if not fname.endswith(".md") or fname in ("index.md", "log.md"):
                continue
            filepath = os.path.join(root, fname)
            rel_path = os.path.relpath(filepath, wiki_dir)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            content_lower = content.lower()
            # Score: count matching query terms in content
            score = sum(content_lower.count(term) for term in query_terms)
            if score == 0:
                continue

            # Extract title (first # heading)
            title = fname.replace(".md", "").replace("-", " ").title()
            for line in content.split("\n"):
                if line.startswith("# "):
                    title = line[2:].strip()
                    break

            # Extract category from path
            category = os.path.dirname(rel_path) or "root"

            # Extract first paragraph as summary
            paragraphs = [p.strip() for p in content.split("\n\n") if p.strip() and not p.strip().startswith("#")]
            summary = paragraphs[0][:200] if paragraphs else ""

            results.append({
                "path": f"wiki/{rel_path}",
                "title": title,
                "category": category,
                "summary": summary,
                "_score": round(score, 2),
            })

    results.sort(key=lambda x: x["_score"], reverse=True)
    results = results[:max_results]

    return {"query": query, "tier": 2, "count": len(results), "results": results}


def format_wiki_output(result):
    """Format wiki search results for LLM consumption."""
    lines = [f"## Wiki Search (Tier 2)", f"**Query:** {result['query']} | **Found:** {result['count']}", ""]
    for i, entry in enumerate(result["results"], 1):
        lines.append(f"### [{entry['category']}] {entry['title']} — score: {entry['_score']}")
        lines.append(f"**Path:** .agent/{entry['path']}")
        lines.append(f"\n{entry['summary']}\n")
    if result["count"] == 0:
        lines.append("No wiki results found. Try CSV search: `--multi-domain` without `--wiki`")
    return "\n".join(lines)


def list_domains():
    """Show available domains and their data status."""
    lines = ["## BA Knowledge Domains", ""]
    for domain in AVAILABLE_DOMAINS:
        filepath = DATA_DIR / DOMAIN_FILES[domain]
        status = "ready" if filepath.exists() else "no data"
        lines.append(f"- **{domain}** → {DOMAIN_FILES[domain]} [{status}]")
    return "\n".join(lines)


def show_stats():
    """Show knowledge base statistics and coverage analytics."""
    import csv as csv_mod
    lines = ["## BA Knowledge Base Statistics", ""]
    total = 0
    type_counts = {}
    agent_counts = {}
    source_counts = {}
    ready_domains = []

    for domain in AVAILABLE_DOMAINS:
        filepath = DATA_DIR / DOMAIN_FILES[domain]
        if not filepath.exists():
            continue
        ready_domains.append(domain)
        with open(filepath, "r", encoding="utf-8") as f:
            rows = list(csv_mod.DictReader(f))
        total += len(rows)
        for row in rows:
            t = row.get("type", "unknown")
            type_counts[t] = type_counts.get(t, 0) + 1
            for agent in row.get("agents", "").split():
                agent_counts[agent] = agent_counts.get(agent, 0) + 1
            src = row.get("source", "")
            if src:
                source_counts[src] = source_counts.get(src, 0) + 1

    lines.append(f"**Total entries:** {total}")
    lines.append(f"**Active domains:** {len(ready_domains)}/{len(AVAILABLE_DOMAINS)}")
    lines.append("")

    lines.append("### Entries by Domain")
    for domain in ready_domains:
        filepath = DATA_DIR / DOMAIN_FILES[domain]
        with open(filepath, "r", encoding="utf-8") as f:
            count = sum(1 for _ in csv_mod.DictReader(f))
        bar = "#" * (count // 2)
        lines.append(f"  {domain:18s} {count:3d} {bar}")
    lines.append("")

    lines.append("### Entries by Type")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"  {t:18s} {c:3d}")
    lines.append("")

    lines.append("### Top 10 Agents by Coverage")
    for agent, c in sorted(agent_counts.items(), key=lambda x: -x[1])[:10]:
        lines.append(f"  {agent:22s} {c:3d} entries")
    lines.append("")

    lines.append("### Top 5 Source Files")
    for src, c in sorted(source_counts.items(), key=lambda x: -x[1])[:5]:
        lines.append(f"  {c:3d} entries ← {src}")

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BA-Kit Knowledge Search (BM25)")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--domain", "-d", choices=AVAILABLE_DOMAINS, help="Search domain")
    parser.add_argument("--max-results", "-n", type=int, default=MAX_RESULTS, help="Max results (default: 3)")
    parser.add_argument("--multi-domain", "-m", action="store_true", help="Search across all domains")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--list-domains", "-l", action="store_true", help="List available domains")
    parser.add_argument("--stats", action="store_true", help="Show knowledge base statistics")
    parser.add_argument("--wiki", "-w", action="store_true", help="Also search wiki pages (Tier 2)")

    args = parser.parse_args()

    if args.stats:
        print(show_stats())
        sys.exit(0)

    if args.list_domains:
        print(list_domains())
        sys.exit(0)

    if not args.query:
        parser.print_help()
        sys.exit(1)

    if args.multi_domain:
        result = search_multi(args.query, max_results=args.max_results)
    else:
        result = search(args.query, domain=args.domain, max_results=args.max_results)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_output(result))

    # Wiki search (Tier 2) if requested
    if args.wiki:
        wiki_result = search_wiki(args.query, max_results=args.max_results)
        if args.json:
            print(json.dumps(wiki_result, indent=2, ensure_ascii=False))
        else:
            print("\n" + format_wiki_output(wiki_result))
