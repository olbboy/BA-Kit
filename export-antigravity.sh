#!/bin/bash
echo "# ANTIGRAVITY CONFIGURATION DUMP" > antigravity-dump.md
echo "## Generated: $(date)" >> antigravity-dump.md
echo "" >> antigravity-dump.md

# Gom tất cả .md files tìm được trong .agent/
find .agent/ -name "*.md" -type f 2>/dev/null | sort | while read f; do
  echo "---" >> antigravity-dump.md
  echo "### FILE: $f" >> antigravity-dump.md
  echo '```' >> antigravity-dump.md
  cat "$f" >> antigravity-dump.md
  echo '```' >> antigravity-dump.md
  echo "" >> antigravity-dump.md
done

echo "Done! Check antigravity-dump.md"
wc -l antigravity-dump.md
