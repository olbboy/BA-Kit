#!/usr/bin/env python3
"""
Download Confluence page tree recursively and convert to Markdown.
Creates a folder structure mirroring the Confluence page hierarchy:
  - Pages WITH children → become folders with README.md for their content
  - Pages WITHOUT children (leaf) → become .md files in their parent folder
"""

import os
import sys
import re
import json
import html
from html.parser import HTMLParser

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '.agent', 'skills', 'confluence-connector', 'scripts'))
from confluence_client import ConfluenceClient


class XHTMLToMarkdownConverter(HTMLParser):
    """Convert Confluence XHTML storage format to Markdown."""

    def __init__(self):
        super().__init__()
        self.output = []
        self.current_text = ""
        self.tag_stack = []
        self.list_stack = []
        self.ol_counters = []
        self.in_code_block = False
        self.code_language = ""
        self.code_content = ""
        self.in_table = False
        self.table_rows = []
        self.current_row = []
        self.current_cell = ""
        self.is_header_row = False
        self.in_link = False
        self.link_href = ""
        self.link_text = ""
        self.in_macro = False
        self.macro_name = ""
        self.macro_body = ""
        self.macro_params = {}
        self.heading_level = 0
        self.ignore_content = False

    def _flush_text(self):
        if self.current_text:
            self.output.append(self.current_text)
            self.current_text = ""

    def _get_list_indent(self):
        depth = len(self.list_stack) - 1
        return "    " * max(0, depth)

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        tag_lower = tag.lower()

        if tag_lower == 'ac:structured-macro':
            self.in_macro = True
            self.macro_name = attrs_dict.get('ac:name', '')
            self.macro_body = ""
            self.macro_params = {}
            return

        if self.in_macro:
            if tag_lower == 'ac:parameter':
                self._current_param_name = attrs_dict.get('ac:name', '')
                self._current_param_value = ""
                return
            if tag_lower in ('ac:plain-text-body', 'ac:rich-text-body'):
                self.macro_body = ""
                return

        if tag_lower in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self._flush_text()
            self.heading_level = int(tag_lower[1])
            self.output.append('\n' + '#' * self.heading_level + ' ')
        elif tag_lower == 'p':
            self._flush_text()
            if not self.in_table:
                self.output.append('\n')
        elif tag_lower == 'br':
            if self.in_table:
                self.current_cell += " "
            else:
                self.output.append('  \n')
        elif tag_lower in ('strong', 'b'):
            self.output.append('**')
        elif tag_lower in ('em', 'i'):
            self.output.append('*')
        elif tag_lower == 'u':
            self.output.append('<u>')
        elif tag_lower in ('s', 'del'):
            self.output.append('~~')
        elif tag_lower == 'code':
            if not self.in_code_block:
                self.output.append('`')
        elif tag_lower == 'pre':
            self._flush_text()
            self.in_code_block = True
            self.code_content = ""
            self.output.append('\n```\n')
        elif tag_lower == 'ul':
            self._flush_text()
            self.list_stack.append('ul')
            if len(self.list_stack) == 1:
                self.output.append('\n')
        elif tag_lower == 'ol':
            self._flush_text()
            self.list_stack.append('ol')
            self.ol_counters.append(0)
            if len(self.list_stack) == 1:
                self.output.append('\n')
        elif tag_lower == 'li':
            self._flush_text()
            indent = self._get_list_indent()
            if self.list_stack and self.list_stack[-1] == 'ol':
                if self.ol_counters:
                    self.ol_counters[-1] += 1
                    self.output.append(f'{indent}{self.ol_counters[-1]}. ')
                else:
                    self.output.append(f'{indent}1. ')
            else:
                self.output.append(f'{indent}- ')
        elif tag_lower == 'a':
            self.in_link = True
            self.link_href = attrs_dict.get('href', '')
            self.link_text = ""
        elif tag_lower == 'ac:link':
            self.in_link = True
            self.link_href = ""
            self.link_text = ""
        elif tag_lower == 'ri:page' and self.in_link:
            self.link_href = attrs_dict.get('ri:content-title', '')
        elif tag_lower in ('ac:link-body', 'ac:plain-text-link-body'):
            pass
        elif tag_lower == 'table':
            self._flush_text()
            self.in_table = True
            self.table_rows = []
            self.output.append('\n')
        elif tag_lower == 'tr':
            self.current_row = []
            self.is_header_row = False
        elif tag_lower == 'th':
            self.current_cell = ""
            self.is_header_row = True
        elif tag_lower == 'td':
            self.current_cell = ""
        elif tag_lower in ('img', 'ac:image'):
            src = attrs_dict.get('src', attrs_dict.get('ac:src', ''))
            alt = attrs_dict.get('alt', attrs_dict.get('ac:alt', 'image'))
            if src:
                self.output.append(f'![{alt}]({src})')
        elif tag_lower == 'ri:attachment':
            filename = attrs_dict.get('ri:filename', '')
            if filename:
                self.output.append(f'![{filename}](attachments/{filename})')
        elif tag_lower == 'blockquote':
            self._flush_text()
            self.output.append('\n> ')
        elif tag_lower == 'hr':
            self._flush_text()
            self.output.append('\n---\n')
        elif tag_lower in ('ac:task-list', 'ac:task', 'ac:task-status', 'ac:task-body'):
            if tag_lower == 'ac:task-list':
                self._flush_text()
                self.output.append('\n')

        self.tag_stack.append(tag_lower)

    def handle_endtag(self, tag):
        tag_lower = tag.lower()

        if tag_lower == 'ac:structured-macro':
            self.in_macro = False
            self._handle_macro_end()
            if self.tag_stack and self.tag_stack[-1] == tag_lower:
                self.tag_stack.pop()
            return

        if self.in_macro:
            if tag_lower == 'ac:parameter':
                self.macro_params[getattr(self, '_current_param_name', '')] = getattr(self, '_current_param_value', '')
                return
            if tag_lower in ('ac:plain-text-body', 'ac:rich-text-body'):
                return

        if tag_lower in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self._flush_text()
            self.output.append('\n')
            self.heading_level = 0
        elif tag_lower == 'p':
            self._flush_text()
            if not self.in_table:
                self.output.append('\n')
        elif tag_lower in ('strong', 'b'):
            self.output.append('**')
        elif tag_lower in ('em', 'i'):
            self.output.append('*')
        elif tag_lower == 'u':
            self.output.append('</u>')
        elif tag_lower in ('s', 'del'):
            self.output.append('~~')
        elif tag_lower == 'code':
            if not self.in_code_block:
                self.output.append('`')
        elif tag_lower == 'pre':
            self.in_code_block = False
            self.output.append('\n```\n')
        elif tag_lower == 'ul':
            if self.list_stack and self.list_stack[-1] == 'ul':
                self.list_stack.pop()
            if not self.list_stack:
                self.output.append('\n')
        elif tag_lower == 'ol':
            if self.list_stack and self.list_stack[-1] == 'ol':
                self.list_stack.pop()
                if self.ol_counters:
                    self.ol_counters.pop()
            if not self.list_stack:
                self.output.append('\n')
        elif tag_lower == 'li':
            self._flush_text()
            self.output.append('\n')
        elif tag_lower == 'a':
            if self.in_link and self.link_href:
                self.output.append(f'[{self.link_text}]({self.link_href})')
            elif self.in_link:
                self.output.append(self.link_text)
            self.in_link = False
            self.link_text = ""
            self.link_href = ""
        elif tag_lower == 'ac:link':
            if self.link_href:
                display = self.link_text or self.link_href
                self.output.append(f'[{display}]({self.link_href})')
            self.in_link = False
            self.link_text = ""
            self.link_href = ""
        elif tag_lower in ('ac:link-body', 'ac:plain-text-link-body'):
            pass
        elif tag_lower == 'table':
            self._flush_table()
            self.in_table = False
        elif tag_lower == 'tr':
            self.table_rows.append((self.is_header_row, list(self.current_row)))
        elif tag_lower in ('th', 'td'):
            self.current_row.append(self.current_cell.strip())
            self.current_cell = ""
        elif tag_lower == 'blockquote':
            self._flush_text()
            self.output.append('\n')
        elif tag_lower == 'ac:task':
            self._flush_text()
            self.output.append('\n')

        if self.tag_stack and self.tag_stack[-1] == tag_lower:
            self.tag_stack.pop()

    def handle_data(self, data):
        if self.in_macro:
            if hasattr(self, '_current_param_name') and self.tag_stack and self.tag_stack[-1] == 'ac:parameter':
                self._current_param_value = data
                return
            self.macro_body += data
            return
        if self.in_link:
            self.link_text += data
            return
        if self.in_table:
            self.current_cell += data
            return
        if self.in_code_block:
            self.code_content += data
            self.output.append(data)
            return
        self.output.append(data)

    def handle_entityref(self, name):
        char = html.unescape(f'&{name};')
        if self.in_link:
            self.link_text += char
        elif self.in_table:
            self.current_cell += char
        else:
            self.output.append(char)

    def handle_charref(self, name):
        char = html.unescape(f'&#{name};')
        if self.in_link:
            self.link_text += char
        elif self.in_table:
            self.current_cell += char
        else:
            self.output.append(char)

    def _handle_macro_end(self):
        name = self.macro_name
        if name in ('code', 'noformat'):
            lang = self.macro_params.get('language', '')
            self.output.append(f'\n```{lang}\n{self.macro_body.strip()}\n```\n')
        elif name in ('info', 'note', 'warning', 'tip'):
            icon_map = {'info': 'ℹ️', 'note': '📝', 'warning': '⚠️', 'tip': '💡'}
            title = self.macro_params.get('title', name.capitalize())
            icon = icon_map.get(name, '')
            self.output.append(f'\n> {icon} **{title}**: {self.macro_body.strip()}\n')
        elif name == 'panel':
            title = self.macro_params.get('title', '')
            if title:
                self.output.append(f'\n> **{title}**\n> {self.macro_body.strip()}\n')
            else:
                self.output.append(f'\n> {self.macro_body.strip()}\n')
        elif name in ('expand', 'excerpt'):
            title = self.macro_params.get('title', 'Details')
            self.output.append(f'\n<details>\n<summary>{title}</summary>\n\n{self.macro_body.strip()}\n\n</details>\n')
        elif name == 'toc':
            self.output.append('\n[TOC]\n')
        elif name == 'status':
            title = self.macro_params.get('title', '')
            self.output.append(f' `{title}` ')
        elif name == 'jira':
            key = self.macro_params.get('key', '')
            self.output.append(f'[{key}]')
        elif name == 'children':
            self.output.append('\n*[Child pages]*\n')
        elif name in ('include', 'excerpt-include'):
            page = self.macro_params.get('', '')
            self.output.append(f'\n*[Include: {page}]*\n')
        else:
            if self.macro_body.strip():
                self.output.append(f'\n{self.macro_body.strip()}\n')

    def _flush_table(self):
        if not self.table_rows:
            return
        max_cols = max(len(row[1]) for row in self.table_rows) if self.table_rows else 0
        if max_cols == 0:
            return
        for i, (is_header, cells) in enumerate(self.table_rows):
            while len(cells) < max_cols:
                cells.append('')
        lines = []
        header_written = False
        for is_header, cells in self.table_rows:
            clean_cells = [c.replace('|', '\\|').replace('\n', ' ') for c in cells]
            line = '| ' + ' | '.join(clean_cells) + ' |'
            lines.append(line)
            if is_header and not header_written:
                separator = '| ' + ' | '.join(['---'] * max_cols) + ' |'
                lines.append(separator)
                header_written = True
        if not header_written and lines:
            separator = '| ' + ' | '.join(['---'] * max_cols) + ' |'
            lines.insert(1, separator)
        self.output.append('\n' + '\n'.join(lines) + '\n')

    def get_markdown(self):
        text = ''.join(self.output)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()


def xhtml_to_markdown(xhtml_content):
    if not xhtml_content:
        return ""
    wrapped = f"<div>{xhtml_content}</div>"
    converter = XHTMLToMarkdownConverter()
    try:
        converter.feed(wrapped)
    except Exception as e:
        print(f"  Warning: HTML parse error: {e}", file=sys.stderr)
        return re.sub(r'<[^>]+>', '', xhtml_content)
    return converter.get_markdown()


def sanitize_dirname(title):
    """Convert a page title to a safe directory/file name (kebab-case)."""
    name = re.sub(r'[<>:"/\\|?*]', '', title)
    name = re.sub(r'\s+', '-', name.strip())
    name = re.sub(r'-+', '-', name)
    name = name.strip('-')
    if len(name) > 100:
        name = name[:100]
    return name


# ── Tree Node ──

class PageNode:
    """Represents a page in the Confluence tree."""
    def __init__(self, page_id, title, body="", labels=None, version=0):
        self.id = page_id
        self.title = title
        self.body = body
        self.labels = labels or []
        self.version = version
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    @property
    def has_children(self):
        return len(self.children) > 0


def fetch_page_tree(client, page_id, depth=0):
    """Recursively fetch the full page tree from Confluence, building a tree of PageNode objects."""
    # Fetch this page's full content
    full_page = client.get_page(page_id, expand=["body.storage", "version", "space", "metadata.labels"])

    title = full_page.get("title", f"Untitled-{page_id}")
    body = full_page.get("body", {}).get("storage", {}).get("value", "")
    labels = [l["name"] for l in full_page.get("metadata", {}).get("labels", {}).get("results", [])]
    version = full_page.get("version", {}).get("number", 0)

    node = PageNode(page_id, title, body, labels, version)
    indent = "  " * depth
    print(f"{indent}📄 {title} (ID: {page_id})")

    # Fetch children with pagination
    start = 0
    page_size = 25
    while True:
        result = client.get_children(page_id, child_type="page", limit=page_size, start=start)
        children = result.get("results", [])
        if not children:
            break
        for child in children:
            child_node = fetch_page_tree(client, child["id"], depth + 1)
            node.add_child(child_node)
        if len(children) < page_size:
            break
        start += page_size

    return node


def write_tree_to_disk(node, parent_dir, depth=0):
    """
    Recursively write the page tree to disk mirroring the Confluence hierarchy.

    Rules:
      - If a node HAS children → create a folder named after the page,
        write the page's own content as README.md inside it.
      - If a node has NO children (leaf) → write it as a .md file
        in the parent directory.
    """
    indent = "  " * depth
    dir_name = sanitize_dirname(node.title)

    # Convert XHTML body to Markdown
    md_content = xhtml_to_markdown(node.body)
    full_md = f"# {node.title}\n\n"
    if node.labels:
        full_md += f"**Labels:** {', '.join(node.labels)}\n\n"
    full_md += "---\n\n"
    full_md += md_content + "\n"

    if node.has_children:
        # This page is a branch → create a folder
        folder_path = os.path.join(parent_dir, dir_name)
        os.makedirs(folder_path, exist_ok=True)

        # Write this page's content as README.md
        readme_path = os.path.join(folder_path, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(full_md)
        print(f"{indent}📁 {dir_name}/")
        print(f"{indent}   └── README.md")

        # Process children recursively
        for child in node.children:
            write_tree_to_disk(child, folder_path, depth + 1)
    else:
        # This page is a leaf → write as .md file
        file_name = dir_name + ".md"
        file_path = os.path.join(parent_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(full_md)
        print(f"{indent}📄 {file_name}")


def generate_index(node, lines=None, depth=0, rel_path="."):
    """Generate INDEX.md content with links reflecting the folder structure."""
    if lines is None:
        lines = [f"# {node.title} - Confluence Export\n\n"]
        lines.append("## Page Tree\n\n")

    indent = "  " * depth
    dir_name = sanitize_dirname(node.title)

    if node.has_children:
        if depth == 0:
            # Root node
            link_path = f"./README.md"
        else:
            link_path = f"{rel_path}/{dir_name}/README.md"
        lines.append(f"{indent}- 📁 [{node.title}]({link_path})\n")

        for child in node.children:
            child_rel = f"{rel_path}/{dir_name}" if depth > 0 else "."
            generate_index(child, lines, depth + 1, child_rel)
    else:
        file_name = dir_name + ".md"
        link_path = f"{rel_path}/{file_name}"
        lines.append(f"{indent}- 📄 [{node.title}]({link_path})\n")

    return lines


def count_nodes(node):
    """Count total pages in the tree."""
    total = 1
    for child in node.children:
        total += count_nodes(child)
    return total


def main():
    # Load env vars from .env file
    env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

    client = ConfluenceClient()

    ROOT_PAGE_ID = "196775636"
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "mini-app-cham-cong")

    # Clean previous output
    import shutil
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)

    print("=" * 60)
    print("  Confluence Page Tree → Markdown (Hierarchical)")
    print("=" * 60)
    print()

    # ── Phase 1: Build tree from Confluence ──
    print("Phase 1: Fetching page tree from Confluence...\n")
    root = fetch_page_tree(client, ROOT_PAGE_ID)
    total = count_nodes(root)
    print(f"\n✅ Fetched {total} pages total.\n")

    # ── Phase 2: Write to disk with folder hierarchy ──
    print("Phase 2: Writing to disk with folder hierarchy...\n")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Root is always a folder
    root_md = xhtml_to_markdown(root.body)
    root_full_md = f"# {root.title}\n\n"
    if root.labels:
        root_full_md += f"**Labels:** {', '.join(root.labels)}\n\n"
    root_full_md += "---\n\n"
    root_full_md += root_md + "\n"

    with open(os.path.join(OUTPUT_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(root_full_md)
    print(f"📁 mini-app-cham-cong/")
    print(f"   └── README.md")

    for child in root.children:
        write_tree_to_disk(child, OUTPUT_DIR, depth=1)

    # ── Phase 3: Generate INDEX.md ──
    print(f"\nPhase 3: Generating INDEX.md...\n")
    index_lines = generate_index(root)
    # Add total count at top
    index_lines.insert(2, f"*Exported {total} pages on {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")

    index_path = os.path.join(OUTPUT_DIR, "INDEX.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("".join(index_lines))
    print(f"📄 INDEX.md")

    print(f"\n{'=' * 60}")
    print(f"  ✅ Done! {total} pages exported to:")
    print(f"  {OUTPUT_DIR}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
