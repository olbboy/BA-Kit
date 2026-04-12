#!/usr/bin/env python3
"""
Confluence DC XHTML Converter — Markdown → XHTML with built-in rendering rules.

USAGE:
    from confluence_xhtml import md_to_xhtml, validate_rendered_pages

    # Convert markdown to Confluence-safe XHTML
    xhtml = md_to_xhtml(markdown_content)

    # Validate pages after upload
    broken = validate_rendered_pages(client, page_ids)

RULES EMBEDDED:
    - Code language mapping (json→javascript, gherkin→text, etc.)
    - Mermaid → mermaid-macro plugin (Stratus Add-ons)
    - HTML macro blocked
    - Post-upload validation via body.view

Reference: confluence-dc-rendering-rules.md
"""

import re
import json
import urllib.request
import ssl
import os

# ==============================================================================
# RULE: Confluence DC Code Macro Language Whitelist
# ==============================================================================

SAFE_LANGUAGES = frozenset({
    'text', 'javascript', 'java', 'python', 'sql', 'xml', 'html', 'css',
    'bash', 'ruby', 'groovy', 'csharp', 'c++', 'diff', 'php', 'scala',
    'perl', 'yaml', 'powershell', 'none', 'actionscript3', 'applescript',
    'coldfusion', 'delphi', 'erlang', 'javafx', 'vb', 'sh',
})

LANGUAGE_MAP = {
    'json': 'javascript',
    'gherkin': 'text',
    'typescript': 'javascript',
    'ts': 'javascript',
    'go': 'text',
    'rust': 'text',
    'kotlin': 'text',
    'swift': 'text',
    'toml': 'text',
    'hcl': 'text',
    'mermaid': None,  # Special: use mermaid-macro plugin
}

# ==============================================================================
# RULE: Mermaid plugin macro name (Stratus Add-ons)
# ==============================================================================

MERMAID_MACRO_NAME = 'mermaid-macro'  # NOT 'mermaid', NOT 'mermaid-cloud'


# ==============================================================================
# Core: XML Helpers
# ==============================================================================

def escape_xml(text: str) -> str:
    """Escape XML special characters."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def _inline_format(text: str) -> str:
    """Convert inline markdown (bold, italic, code, links) to HTML."""
    t = escape_xml(text)

    # Preserve inline code
    codes = []
    def _save_code(m):
        codes.append(m.group(1))
        return f'\x00CODE{len(codes)-1}\x00'
    t = re.sub(r'`([^`]+)`', _save_code, t)

    # Bold, italic
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)

    # Restore code
    for i, c in enumerate(codes):
        t = t.replace(f'\x00CODE{i}\x00', f'<code>{c}</code>')

    # Links
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
               lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', t)
    return t


# ==============================================================================
# Core: Macro Builders
# ==============================================================================

def code_macro(language: str, content: str) -> str:
    """
    Build a Confluence code macro with safe language mapping.

    Applies LANGUAGE_MAP to convert unsafe languages (json, gherkin, etc.)
    to Confluence DC-compatible equivalents.
    """
    mapped = LANGUAGE_MAP.get(language, language)

    # Mermaid → use dedicated plugin
    if mapped is None:
        return mermaid_macro(content)

    # Fallback: if still not in safe list, use 'text'
    if mapped.lower() not in SAFE_LANGUAGES:
        mapped = 'text'

    # Add title param when language was remapped
    title_param = ''
    if language != mapped:
        title_param = (
            f'<ac:parameter ac:name="title">{language.upper()}</ac:parameter>'
        )

    return (
        f'<ac:structured-macro ac:name="code">'
        f'<ac:parameter ac:name="language">{mapped}</ac:parameter>'
        f'{title_param}'
        f'<ac:parameter ac:name="linenumbers">false</ac:parameter>'
        f'<ac:plain-text-body><![CDATA[{content}]]></ac:plain-text-body>'
        f'</ac:structured-macro>'
    )


def mermaid_macro(code: str) -> str:
    """
    Build a Stratus Mermaid plugin macro.

    Uses ac:name="mermaid-macro" (NOT "mermaid" or "mermaid-cloud").
    """
    return (
        f'<ac:structured-macro ac:name="{MERMAID_MACRO_NAME}">'
        f'<ac:plain-text-body><![CDATA[{code}]]></ac:plain-text-body>'
        f'</ac:structured-macro>'
    )


# ==============================================================================
# Core: Markdown → XHTML Converter
# ==============================================================================

def md_to_xhtml(md: str) -> str:
    """
    Convert Markdown content to Confluence DC-safe XHTML storage format.

    Handles: headings, tables, lists, code blocks (with language mapping),
    mermaid diagrams, horizontal rules, blockquotes, inline formatting.
    """
    lines = md.split('\n')
    parts = []
    in_code = False
    code_lang = ''
    code_lines = []
    is_mermaid = False
    in_table = False
    table_rows = []
    in_list = False
    list_items = []

    def flush_table():
        nonlocal table_rows, in_table
        if not table_rows:
            return ''
        html = '<table><tbody>'
        for i, row in enumerate(table_rows):
            cols = [c.strip() for c in row.split('|')[1:-1]]
            # Skip separator row
            if i == 1 and all(set(c.strip()) <= set('-:|') for c in cols):
                continue
            tag = 'th' if i == 0 else 'td'
            html += '<tr>' + ''.join(
                f'<{tag}>{_inline_format(c)}</{tag}>' for c in cols
            ) + '</tr>'
        html += '</tbody></table>'
        table_rows = []
        in_table = False
        return html

    def flush_list():
        nonlocal list_items, in_list
        if not list_items:
            return ''
        html = '<ul>' + ''.join(
            f'<li>{_inline_format(item)}</li>' for item in list_items
        ) + '</ul>'
        list_items = []
        in_list = False
        return html

    for line in lines:
        # Code fence
        if line.startswith('```'):
            if in_code:
                content = '\n'.join(code_lines)
                if is_mermaid:
                    parts.append(mermaid_macro(content))
                else:
                    parts.append(code_macro(code_lang, content))
                code_lines = []
                in_code = False
                is_mermaid = False
            else:
                if in_table:
                    parts.append(flush_table())
                if in_list:
                    parts.append(flush_list())
                in_code = True
                code_lang = line[3:].strip() or 'text'
                is_mermaid = (code_lang == 'mermaid')
            continue

        if in_code:
            code_lines.append(line)
            continue

        # Table row
        if '|' in line and line.strip().startswith('|'):
            if in_list:
                parts.append(flush_list())
            in_table = True
            table_rows.append(line)
            continue
        elif in_table:
            parts.append(flush_table())

        # List item
        m_list = re.match(r'^(\s*)([-*]|\d+\.)\s+(.+)', line)
        if m_list:
            if in_table:
                parts.append(flush_table())
            in_list = True
            list_items.append(m_list.group(3))
            continue
        elif in_list:
            parts.append(flush_list())

        # Heading
        m_heading = re.match(r'^(#{1,6})\s+(.+)', line)
        if m_heading:
            level = len(m_heading.group(1))
            text = _inline_format(m_heading.group(2))
            parts.append(f'<h{level}>{text}</h{level}>')
            continue

        # Horizontal rule
        if re.match(r'^---+\s*$', line):
            parts.append('<hr/>')
            continue

        # Blockquote
        if line.startswith('> '):
            parts.append(
                f'<blockquote><p>{_inline_format(line[2:])}</p></blockquote>'
            )
            continue

        # Empty line
        if not line.strip():
            continue

        # Paragraph
        parts.append(f'<p>{_inline_format(line)}</p>')

    # Flush remaining
    if in_table:
        parts.append(flush_table())
    if in_list:
        parts.append(flush_list())

    return '\n'.join(parts)


# ==============================================================================
# Validation: Post-Upload Rendering Check
# ==============================================================================

def validate_rendered_pages(client, page_ids: list) -> list:
    """
    Validate pages render correctly on Confluence DC.

    Checks body.view (NOT body.storage) for rendering errors.
    Returns list of dicts with broken page details.

    Args:
        client: ConfluenceClient instance
        page_ids: List of page ID strings

    Returns:
        List of {'id': str, 'title': str, 'errors': int} for broken pages
    """
    base_url = os.environ.get('CONFLUENCE_BASE_URL', '')
    pat = os.environ.get('CONFLUENCE_PAT', '')
    ctx = ssl.create_default_context()

    broken = []
    for pid in page_ids:
        url = f'{base_url}/rest/api/content/{pid}?expand=body.view'
        headers = {
            'Authorization': f'Bearer {pat}',
            'Accept': 'application/json'
        }
        req = urllib.request.Request(url, headers=headers)
        try:
            resp = urllib.request.urlopen(req, context=ctx, timeout=30)
            data = json.loads(resp.read().decode('utf-8'))
            view = data.get('body', {}).get('view', {}).get('value', '')
            title = data.get('title', '')

            error_count = (
                view.count('Error rendering macro') +
                view.count('Unknown macro')
            )
            if error_count > 0:
                broken.append({
                    'id': pid,
                    'title': title,
                    'errors': error_count,
                })
        except Exception as e:
            broken.append({
                'id': pid,
                'title': f'(request failed)',
                'errors': -1,
                'error': str(e),
            })

    return broken


# ==============================================================================
# CLI: Quick test
# ==============================================================================

if __name__ == '__main__':
    # Self-test: verify language mapping
    print("=== Language Mapping Test ===")
    test_cases = [
        ('json', 'javascript'),
        ('gherkin', 'text'),
        ('typescript', 'javascript'),
        ('python', 'python'),
        ('sql', 'sql'),
        ('go', 'text'),
    ]
    for src, expected in test_cases:
        mapped = LANGUAGE_MAP.get(src, src)
        if mapped is None:
            mapped = 'mermaid-macro'
        status = '✅' if mapped == expected else '❌'
        print(f'  {status} {src} → {mapped} (expected: {expected})')

    # Self-test: mermaid macro
    print("\n=== Mermaid Macro Test ===")
    result = mermaid_macro('graph LR; A-->B')
    assert MERMAID_MACRO_NAME in result
    assert 'graph LR' in result
    print(f'  ✅ Uses macro: {MERMAID_MACRO_NAME}')

    # Self-test: code macro
    print("\n=== Code Macro Test ===")
    result = code_macro('json', '{"a": 1}')
    assert 'language">javascript' in result
    assert 'title">JSON' in result
    assert 'json' not in result.split('language">')[1].split('<')[0]
    print(f'  ✅ json → javascript with title=JSON')

    # Self-test: md_to_xhtml
    print("\n=== MD → XHTML Test ===")
    md = '# Hello\n\n```json\n{"key": "value"}\n```\n\n```mermaid\ngraph LR; A-->B\n```'
    xhtml = md_to_xhtml(md)
    assert 'language">javascript' in xhtml
    assert 'mermaid-macro' in xhtml
    assert 'language">json' not in xhtml
    print(f'  ✅ json block → javascript macro')
    print(f'  ✅ mermaid block → mermaid-macro plugin')

    print("\n✅ All self-tests passed!")
