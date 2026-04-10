#!/usr/bin/env python3
"""
Push Mini App Chấm Công (New) documentation tree to Confluence.
Creates a new root page as sibling of the original "Mini App Chấm công" (ID: 196775636),
then recursively creates child pages mirroring the local folder structure.
"""

import os
import sys
import json
import re
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

BASE_URL = os.environ.get('CONFLUENCE_BASE_URL', '').rstrip('/')
PAT = os.environ.get('CONFLUENCE_PAT', '')
SPACE_KEY = 'CVH'
PARENT_PAGE_ID = '183973889'  # "02. Requirement" — same parent as original page

API = f"{BASE_URL}/rest/api/content"
HEADERS = {
    'Authorization': f'Bearer {PAT}',
    'Content-Type': 'application/json',
}

# Source directory
SRC_DIR = Path(__file__).parent / 'mini-app-cham-cong'

# Track created pages
created_pages = []


def md_to_xhtml(md_content: str) -> str:
    """Convert markdown to Confluence XHTML storage format."""
    lines = md_content.split('\n')
    xhtml_parts = []
    in_table = False
    in_code = False
    code_lang = ''
    code_lines = []
    in_list = False
    table_rows = []

    for line in lines:
        # Code blocks
        if line.startswith('```'):
            if in_code:
                code_content = '\n'.join(code_lines)
                xhtml_parts.append(
                    f'<ac:structured-macro ac:name="code">'
                    f'<ac:parameter ac:name="language">{code_lang}</ac:parameter>'
                    f'<ac:plain-text-body><![CDATA[{code_content}]]></ac:plain-text-body>'
                    f'</ac:structured-macro>'
                )
                in_code = False
                code_lines = []
            else:
                in_code = True
                code_lang = line[3:].strip() or 'text'
            continue

        if in_code:
            code_lines.append(line)
            continue

        # Table
        if '|' in line and line.strip().startswith('|'):
            cells = [c.strip() for c in line.strip().split('|')[1:-1]]
            if all(set(c) <= {'-', ':', ' '} for c in cells):
                continue  # separator row
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            continue
        elif in_table:
            # Flush table
            xhtml_parts.append(_render_table(table_rows))
            in_table = False
            table_rows = []

        # Headers
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            text = _clean_inline(m.group(2))
            xhtml_parts.append(f'<h{level}>{text}</h{level}>')
            continue

        # Horizontal rule
        if line.strip() in ('---', '***', '___'):
            xhtml_parts.append('<hr />')
            continue

        # Unordered list
        m = re.match(r'^(\s*)[-*]\s+(.*)', line)
        if m:
            text = _clean_inline(m.group(2))
            if not in_list:
                xhtml_parts.append('<ul>')
                in_list = True
            xhtml_parts.append(f'<li>{text}</li>')
            continue
        elif in_list:
            xhtml_parts.append('</ul>')
            in_list = False

        # Ordered list
        m = re.match(r'^(\s*)\d+\.\s+(.*)', line)
        if m:
            text = _clean_inline(m.group(2))
            xhtml_parts.append(f'<li>{text}</li>')
            continue

        # Empty line
        if not line.strip():
            if in_list:
                xhtml_parts.append('</ul>')
                in_list = False
            continue

        # Regular paragraph
        text = _clean_inline(line)
        if text:
            xhtml_parts.append(f'<p>{text}</p>')

    # Flush remaining
    if in_table:
        xhtml_parts.append(_render_table(table_rows))
    if in_list:
        xhtml_parts.append('</ul>')
    if in_code:
        code_content = '\n'.join(code_lines)
        xhtml_parts.append(
            f'<ac:structured-macro ac:name="code">'
            f'<ac:parameter ac:name="language">{code_lang}</ac:parameter>'
            f'<ac:plain-text-body><![CDATA[{code_content}]]></ac:plain-text-body>'
            f'</ac:structured-macro>'
        )

    return '\n'.join(xhtml_parts)


def _render_table(rows):
    if not rows:
        return ''
    html = '<table><colgroup>'
    for _ in rows[0]:
        html += '<col />'
    html += '</colgroup><tbody>'
    for i, row in enumerate(rows):
        html += '<tr>'
        tag = 'th' if i == 0 else 'td'
        for cell in row:
            html += f'<{tag}>{_clean_inline(cell)}</{tag}>'
        html += '</tr>'
    html += '</tbody></table>'
    return html


def _escape_xml(text):
    """Escape XML special characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    # Remove emoji characters
    text = re.sub(r'[\U0001F300-\U0001F9FF\U00002600-\U000027BF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\u2B50\u2705\u26A0\u2753\u274C\u2714\U0001F534\U0001F7E0\U0001F7E1\U0001F4CB\U0001F4D0\U0001F4C8\U0001F4C2\U0001F4D8\U0001F4D6\U0001F4C4\U0001F527\U0001F6A8\u2B55\U0001F7E2\U0001F4DD\u2B06\u2191]', '', text)
    return text


def _clean_inline(text):
    """Convert inline markdown to XHTML, with proper XML escaping."""
    # Step 1: Extract and process inline formatting
    # We process bold, italic, code, links to placeholder tokens, escape the rest
    parts = []
    remainder = text

    # Process bold **text** → placeholder
    def process_formatting(s):
        # Links first (before bold/italic mess with them)
        s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
        # Bold
        s = re.sub(r'\*\*\*\*', '', s)  # clean stray ****
        s = re.sub(r'\*\*(.+?)\*\*', lambda m: f'<strong>{_escape_xml(m.group(1))}</strong>', s)
        # Italic (but not in already processed strong tags)
        s = re.sub(r'(?<!<)\*(.+?)\*(?!>)', lambda m: f'<em>{_escape_xml(m.group(1))}</em>', s)
        # Inline code
        s = re.sub(r'`(.+?)`', lambda m: f'<code>{_escape_xml(m.group(1))}</code>', s)
        return s

    # Extract code/bold/italic segments, escape everything else
    # Simple approach: process formatting first, then escape non-tag text
    result = process_formatting(remainder)

    # Now escape any remaining raw text that's not inside HTML tags
    final = []
    tag_pattern = re.compile(r'(</?(?:strong|em|code)[^>]*>)')
    segments = tag_pattern.split(result)
    for seg in segments:
        if tag_pattern.match(seg):
            final.append(seg)  # Keep HTML tags as-is
        else:
            final.append(_escape_xml(seg))  # Escape text content

    return ''.join(final).strip()


def create_page(title: str, body_xhtml: str, parent_id: str) -> dict:
    """Create a Confluence page."""
    payload = {
        "type": "page",
        "title": title,
        "space": {"key": SPACE_KEY},
        "ancestors": [{"id": parent_id}],
        "body": {
            "storage": {
                "value": body_xhtml,
                "representation": "storage"
            }
        }
    }
    resp = requests.post(API, headers=HEADERS, json=payload)
    if resp.status_code in (200, 201):
        data = resp.json()
        print(f"  ✅ Created: \"{title}\" (ID: {data['id']})")
        created_pages.append({'id': data['id'], 'title': title})
        return data
    else:
        print(f"  ❌ FAILED: \"{title}\" — {resp.status_code}: {resp.text[:200]}")
        return None


def read_md_file(filepath: Path) -> str:
    """Read markdown file content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def get_title_from_md(content: str, fallback: str) -> str:
    """Extract title from first # heading."""
    for line in content.split('\n'):
        m = re.match(r'^#\s+(.+)', line)
        if m:
            title = m.group(1).strip()
            # Clean markdown formatting from title
            title = re.sub(r'\*\*(.+?)\*\*', r'\1', title)
            title = re.sub(r'\*(.+?)\*', r'\1', title)
            title = re.sub(r'`(.+?)`', r'\1', title)
            return title
    return fallback


# Titles that already exist on Confluence and need suffix
EXISTING_TITLES = set()


def check_title_exists(title: str) -> bool:
    """Check if a page title already exists in the space."""
    import urllib.parse
    cql = f'space="{SPACE_KEY}" AND title="{title}"'
    url = f"{BASE_URL}/rest/api/content/search?cql={urllib.parse.quote(cql)}&limit=1"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            return resp.json().get('size', 0) > 0
    except:
        pass
    return False


def make_unique_title(title: str) -> str:
    """Add ' (v2)' suffix if title conflicts with existing page."""
    if check_title_exists(title):
        new_title = f"{title} (v2)"
        print(f"    ⚠️  Title conflict: \"{title}\" → \"{new_title}\"")
        return new_title
    return title


def push_directory(dir_path: Path, parent_id: str, prefix: str = ''):
    """Recursively push a directory to Confluence."""
    readme = dir_path / 'README.md'
    if not readme.exists():
        return

    # Read README as the parent page content
    content = read_md_file(readme)
    title = get_title_from_md(content, dir_path.name)

    # Add prefix for new pages to distinguish
    if prefix:
        title = f"{prefix} {title}" if not title.startswith(prefix) else title

    # Check for title collision
    title = make_unique_title(title)

    body = md_to_xhtml(content)
    page = create_page(title, body, parent_id)

    if not page:
        return

    page_id = page['id']
    time.sleep(0.3)  # Rate limiting

    # Push child .md files (not README)
    md_files = sorted([f for f in dir_path.glob('*.md') if f.name != 'README.md'])
    for md_file in md_files:
        child_content = read_md_file(md_file)
        child_title = get_title_from_md(child_content, md_file.stem)
        child_title = make_unique_title(child_title)
        child_body = md_to_xhtml(child_content)
        create_page(child_title, child_body, page_id)
        time.sleep(0.3)

    # Push child directories
    subdirs = sorted([d for d in dir_path.iterdir() if d.is_dir()])
    for subdir in subdirs:
        push_directory(subdir, page_id)


def main():
    print("=" * 60)
    print("Push Mini App Chấm Công (New) to Confluence — RESUME")
    print(f"Space: {SPACE_KEY}")
    print(f"Parent: 02. Requirement (ID: {PARENT_PAGE_ID})")
    print(f"Source: {SRC_DIR}")
    print("=" * 60)

    if not BASE_URL or not PAT:
        print("ERROR: Missing CONFLUENCE_BASE_URL or CONFLUENCE_PAT")
        sys.exit(1)

    # Root page already created in previous run
    root_id = '196786905'  # "Mini App Chấm công (New)"
    print(f"  ♻️  Reusing root page (ID: {root_id})")

    # EAMS doc already created (ID: 196786906) — skip

    # Push 2.11-Mini-app tree (the part that failed last time)
    mini_app_dir = SRC_DIR / '2.11-Mini-app'
    if mini_app_dir.exists():
        push_directory(mini_app_dir, root_id)

    # Summary
    print("\n" + "=" * 60)
    print(f"DONE! Created {len(created_pages)} pages on Confluence.")
    print("=" * 60)
    for p in created_pages:
        print(f"  {p['id']}: {p['title']}")

    # Save manifest
    manifest_path = SRC_DIR / 'confluence_manifest.json'
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump({
            'root_page_id': root_id,
            'pages': created_pages,
            'pushed_at': time.strftime('%Y-%m-%dT%H:%M:%S')
        }, f, indent=2, ensure_ascii=False)
    print(f"\nManifest saved: {manifest_path}")


if __name__ == '__main__':
    main()
