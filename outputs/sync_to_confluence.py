#!/usr/bin/env python3
"""
Sync all locally-fixed pages to Confluence.
Re-reads each local markdown file, converts to XHTML,
and updates the corresponding Confluence page.
"""

import os
import sys
import json
import re
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

BASE_URL = os.environ.get('CONFLUENCE_BASE_URL', '').rstrip('/')
PAT = os.environ.get('CONFLUENCE_PAT', '')
API = f"{BASE_URL}/rest/api/content"
HEADERS = {
    'Authorization': f'Bearer {PAT}',
    'Content-Type': 'application/json',
}

SRC_DIR = Path(__file__).parent / 'mini-app-cham-cong'


# ────────────────────────────────────────────────────────────
# Markdown → XHTML converter (improved from push script)
# ────────────────────────────────────────────────────────────

def _escape_xml(text):
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = re.sub(r'[\U0001F300-\U0001F9FF\U00002600-\U000027BF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF'
                  r'\u2B50\u2705\u26A0\u2753\u274C\u2714\U0001F534\U0001F7E0\U0001F7E1'
                  r'\U0001F4CB\U0001F4D0\U0001F4C8\U0001F4C2\U0001F4D8\U0001F4D6\U0001F4C4'
                  r'\U0001F527\U0001F6A8\u2B55\U0001F7E2\U0001F4DD\u2B06\u2191'
                  r'\U0001F4E3\U0001F4E6\U0001F4E5\U0001F4E4\U0001F4E2\U0001F4E1'
                  r'\U0001F464\U0001F454\U0001F3E2\U00002699\U0001F528]', '', text)
    return text


def _clean_inline(text):
    def process_formatting(s):
        s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
        s = re.sub(r'\*\*\*\*', '', s)
        s = re.sub(r'\*\*(.+?)\*\*', lambda m: f'<strong>{_escape_xml(m.group(1))}</strong>', s)
        s = re.sub(r'(?<!<)\*(.+?)\*(?!>)', lambda m: f'<em>{_escape_xml(m.group(1))}</em>', s)
        s = re.sub(r'`(.+?)`', lambda m: f'<code>{_escape_xml(m.group(1))}</code>', s)
        return s

    result = process_formatting(text)
    final = []
    tag_pattern = re.compile(r'(</?(?:strong|em|code)[^>]*>)')
    for seg in tag_pattern.split(result):
        if tag_pattern.match(seg):
            final.append(seg)
        else:
            final.append(_escape_xml(seg))
    return ''.join(final).strip()


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


def md_to_xhtml(md_content):
    lines = md_content.split('\n')
    xhtml_parts = []
    in_table = False
    in_code = False
    code_lang = ''
    code_lines = []
    in_list = False
    list_type = None  # 'ul' or 'ol'
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
                if in_list:
                    xhtml_parts.append(f'</{list_type}>')
                    in_list = False
                in_code = True
                code_lang = line[3:].strip() or 'text'
            continue

        if in_code:
            code_lines.append(line)
            continue

        # Table
        if '|' in line and line.strip().startswith('|'):
            if in_list:
                xhtml_parts.append(f'</{list_type}>')
                in_list = False
            cells = [c.strip() for c in line.strip().split('|')[1:-1]]
            if all(set(c) <= {'-', ':', ' '} for c in cells):
                continue
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            continue
        elif in_table:
            xhtml_parts.append(_render_table(table_rows))
            in_table = False
            table_rows = []

        # Headers
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            if in_list:
                xhtml_parts.append(f'</{list_type}>')
                in_list = False
            level = len(m.group(1))
            text = _clean_inline(m.group(2))
            xhtml_parts.append(f'<h{level}>{text}</h{level}>')
            continue

        # Horizontal rule
        if line.strip() in ('---', '***', '___'):
            if in_list:
                xhtml_parts.append(f'</{list_type}>')
                in_list = False
            xhtml_parts.append('<hr />')
            continue

        # Unordered list
        m_ul = re.match(r'^(\s*)[-*]\s+(.*)', line)
        if m_ul:
            text = _clean_inline(m_ul.group(2))
            if not in_list or list_type != 'ul':
                if in_list:
                    xhtml_parts.append(f'</{list_type}>')
                xhtml_parts.append('<ul>')
                in_list = True
                list_type = 'ul'
            xhtml_parts.append(f'<li>{text}</li>')
            continue

        # Ordered list
        m_ol = re.match(r'^(\s*)\d+\.\s+(.*)', line)
        if m_ol:
            text = _clean_inline(m_ol.group(2))
            if not in_list or list_type != 'ol':
                if in_list:
                    xhtml_parts.append(f'</{list_type}>')
                xhtml_parts.append('<ol>')
                in_list = True
                list_type = 'ol'
            xhtml_parts.append(f'<li>{text}</li>')
            continue

        # Empty line
        if not line.strip():
            if in_list:
                xhtml_parts.append(f'</{list_type}>')
                in_list = False
            continue

        # Regular paragraph
        if in_list:
            xhtml_parts.append(f'</{list_type}>')
            in_list = False
        text = _clean_inline(line)
        if text:
            xhtml_parts.append(f'<p>{text}</p>')

    # Flush
    if in_table:
        xhtml_parts.append(_render_table(table_rows))
    if in_list:
        xhtml_parts.append(f'</{list_type}>')
    if in_code:
        code_content = '\n'.join(code_lines)
        xhtml_parts.append(
            f'<ac:structured-macro ac:name="code">'
            f'<ac:parameter ac:name="language">{code_lang}</ac:parameter>'
            f'<ac:plain-text-body><![CDATA[{code_content}]]></ac:plain-text-body>'
            f'</ac:structured-macro>'
        )

    return '\n'.join(xhtml_parts)


# ────────────────────────────────────────────────────────────
# Confluence API
# ────────────────────────────────────────────────────────────

def get_page(page_id):
    resp = requests.get(f"{API}/{page_id}?expand=body.storage,version", headers=HEADERS)
    return resp.json() if resp.status_code == 200 else None


def update_page(page_id, title, body, version):
    payload = {
        "type": "page",
        "title": title,
        "version": {"number": version + 1},
        "body": {"storage": {"value": body, "representation": "storage"}}
    }
    resp = requests.put(f"{API}/{page_id}", headers=HEADERS, json=payload)
    if resp.status_code == 200:
        return True
    print(f"    ❌ Update failed: {resp.status_code}: {resp.text[:200]}")
    return False


# ────────────────────────────────────────────────────────────
# File → Page ID mapping (manually built from manifest)
# ────────────────────────────────────────────────────────────

FILE_TO_PAGE = {
    # Root
    'README.md': '196786905',
    # EAMS v2.0
    'docs_business-comprehensive-documentation.md': '196786906',
    # 2.11 Mini app
    '2.11-Mini-app/README.md': '196786907',
    # 2.11.1 Chấm công
    '2.11-Mini-app/2.11.1.-Chấm-công-và-Nhật-ký-chấm-công/README.md': '196786908',
    '2.11-Mini-app/2.11.1.-Chấm-công-và-Nhật-ký-chấm-công/US-ATTEN-01-Hub-chấm-công.md': '196786909',
    '2.11-Mini-app/2.11.1.-Chấm-công-và-Nhật-ký-chấm-công/US-ATTEN-02-Thống-kê-hiệu-suất-tháng.md': '196786910',
    '2.11-Mini-app/2.11.1.-Chấm-công-và-Nhật-ký-chấm-công/US-ATTEN-03-Xem-chi-tiết-nhật-ký-chấm-công.md': '196786911',
    '2.11-Mini-app/2.11.1.-Chấm-công-và-Nhật-ký-chấm-công/US-ATTEN-04-Trung-tâm-cảnh-báo-và-thông-báo.md': '196786912',
    # 2.11.2 Ca làm việc
    '2.11-Mini-app/2.11.2.-Cấu-hình-ca-làm-việc/README.md': '196786921',
    '2.11-Mini-app/2.11.2.-Cấu-hình-ca-làm-việc/US-SHIFT-01-Danh-sách-ca-làm-việc.md': '196786922',
    '2.11-Mini-app/2.11.2.-Cấu-hình-ca-làm-việc/US-SHIFT-02-Cấu-hình-giờ-và-ngày-làm-việc.md': '196786923',
    '2.11-Mini-app/2.11.2.-Cấu-hình-ca-làm-việc/US-SHIFT-03-Giới-hạn-thời-gian-chấm-công-(punch-limit).md': '196786924',
    '2.11-Mini-app/2.11.2.-Cấu-hình-ca-làm-việc/US-SHIFT-04-Cấu-hình-giờ-nghỉ.md': '196786925',
    '2.11-Mini-app/2.11.2.-Cấu-hình-ca-làm-việc/US-SHIFT-05-Import-nhân-viên-vào-ca.md': '196786926',
    # 2.11.3 Giải trình
    '2.11-Mini-app/2.11.3.-Giải-trình-công/README.md': '196786927',
    '2.11-Mini-app/2.11.3.-Giải-trình-công/US-EXPL-01-Danh-sách-lỗi-cần-giải-trình.md': '196786928',
    # 2.11.4 Trung tâm đăng ký
    '2.11-Mini-app/2.11.4.-Trung-tâm-đăng-ký/README.md': '196786929',
    # 2.11.5 Báo cáo cá nhân
    '2.11-Mini-app/2.11.5.-Báo-cáo-cá-nhân/README.md': '196786934',
    # 2.11.6 Quản lý nhân sự
    '2.11-Mini-app/2.11.6.-Quản-lý-nhân-sự/README.md': '196786937',
    # 2.11.7 Cấu hình lịch nghỉ
    '2.11-Mini-app/2.11.7.-Cấu-hình-lịch-nghỉ/README.md': '196786944',
    '2.11-Mini-app/2.11.7.-Cấu-hình-lịch-nghỉ/US-HOL-01-Quản-lý-danh-sách-ngày-nghỉ.md': '196786945',
    '2.11-Mini-app/2.11.7.-Cấu-hình-lịch-nghỉ/US-HOL-02-Cấu-hình-policy-nghỉ-và-rule-nghỉ.md': '196786946',
    '2.11-Mini-app/2.11.7.-Cấu-hình-lịch-nghỉ/US-HOL-03-Logic-sync-&-batch-job.md': '196786947',
    '2.11-Mini-app/2.11.7.-Cấu-hình-lịch-nghỉ/US-HOL-04-API-hiển-thị.md': '196786948',
    # 2.11.8 Camera AI
    '2.11-Mini-app/2.11.8.-Cấu-hình-Camera-AI/README.md': '196786949',
    # 2.11.9 Thông báo
    '2.11-Mini-app/2.11.9.-Cấu-hình-thông-báo/README.md': '196786953',
    # 2.11.10 Phê duyệt
    '2.11-Mini-app/2.11.10.-Trung-tâm-phê-duyệt/README.md': '196786913',
    # 2.11.11 Báo cáo tổng
    '2.11-Mini-app/2.11.11.-Báo-cáo-tổng/README.md': '196786917',
    # Tài liệu dự án
    '2.11-Mini-app/Tài-liệu-dự-án-Mini-App/README.md': '196786957',
    '2.11-Mini-app/Tài-liệu-dự-án-Mini-App/BRD-HR-(Admin).md': '196786958',
    '2.11-Mini-app/Tài-liệu-dự-án-Mini-App/BRD-Nhân-viên.md': '196786959',
    '2.11-Mini-app/Tài-liệu-dự-án-Mini-App/Demo-Plan-Sprint-8.md': '196786960',
    '2.11-Mini-app/Tài-liệu-dự-án-Mini-App/UAT-SCENARIOS.md': '196786961',
    # NEW: US-ATTEN-05
    '2.11-Mini-app/2.11.1.-Chấm-công-và-Nhật-ký-chấm-công/US-ATTEN-05-Nhập-chấm-công-thủ-công.md': '196787044',
    # NEW: US-EXPL-02
    '2.11-Mini-app/2.11.3.-Giải-trình-công/US-EXPL-02-Yêu-cầu-sửa-chấm-công.md': '196787045',
    # NEW: US-SHIFT-06
    '2.11-Mini-app/2.11.2.-Cấu-hình-ca-làm-việc/US-SHIFT-06-Phân-ca-theo-pattern.md': '196787046',
    # NEW: US-REG-05
    '2.11-Mini-app/2.11.4.-Trung-tâm-đăng-ký/US-REG-05-Cấu-hình-chính-sách-phép-năm.md': '196787047',
    # NEW: Module 12
    '2.11-Mini-app/2.11.12.-Quản-trị-hệ-thống/README.md': '196787048',
    '2.11-Mini-app/2.11.12.-Quản-trị-hệ-thống/US-SYS-01-Quản-lý-chi-nhánh.md': '196787049',
    '2.11-Mini-app/2.11.12.-Quản-trị-hệ-thống/US-SYS-02-Audit-log-viewer.md': '196787050',
    '2.11-Mini-app/2.11.12.-Quản-trị-hệ-thống/US-SYS-03-Employee-offboarding.md': '196787051',
}

# Pages with diagram attachments — preserve image refs, don't overwrite with mermaid
DIAGRAM_PAGES = {'196786907', '196786927', '196786944'}


def main():
    print("=" * 60)
    print("Sync ALL local files → Confluence pages")
    print(f"Source: {SRC_DIR}")
    print(f"Pages to sync: {len(FILE_TO_PAGE)}")
    print("=" * 60)

    if not BASE_URL or not PAT:
        print("ERROR: Missing CONFLUENCE_BASE_URL or CONFLUENCE_PAT")
        sys.exit(1)

    updated = 0
    skipped = 0
    failed = 0

    for rel_path, page_id in FILE_TO_PAGE.items():
        filepath = SRC_DIR / rel_path
        if not filepath.exists():
            print(f"  ⚠️  File not found: {rel_path}")
            skipped += 1
            continue

        # Read local file
        with open(filepath, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Convert to XHTML
        body_xhtml = md_to_xhtml(md_content)

        # For diagram pages, replace mermaid code blocks with image references
        if page_id in DIAGRAM_PAGES:
            # Get current page to preserve diagram image refs
            current_page = get_page(page_id)
            if current_page:
                current_body = current_page['body']['storage']['value']
                # Extract existing image references
                img_refs = re.findall(
                    r'<p><ac:image[^>]*><ri:attachment ri:filename="[^"]*" /></ac:image></p>',
                    current_body
                )
                # Replace mermaid code blocks in new body with the image refs
                mermaid_pattern = re.compile(
                    r'<ac:structured-macro ac:name="code">\s*'
                    r'<ac:parameter ac:name="language">mermaid</ac:parameter>\s*'
                    r'<ac:plain-text-body><!\[CDATA\[.*?\]\]></ac:plain-text-body>\s*'
                    r'</ac:structured-macro>',
                    re.DOTALL
                )
                mermaid_blocks = list(mermaid_pattern.finditer(body_xhtml))
                for i, match in enumerate(reversed(mermaid_blocks)):
                    if i < len(img_refs):
                        body_xhtml = (body_xhtml[:match.start()] +
                                      img_refs[len(img_refs) - 1 - i] +
                                      body_xhtml[match.end():])

        # Get current Confluence page for version
        page = get_page(page_id)
        if not page:
            print(f"  ❌ Cannot get page {page_id} for {rel_path}")
            failed += 1
            continue

        title = page['title']
        version = page['version']['number']

        # Update
        if update_page(page_id, title, body_xhtml, version):
            print(f"  ✅ {title} (v{version+1}) ← {rel_path}")
            updated += 1
        else:
            failed += 1

        time.sleep(0.3)

    print("\n" + "=" * 60)
    print(f"DONE! Updated: {updated} | Skipped: {skipped} | Failed: {failed}")
    print("=" * 60)


if __name__ == '__main__':
    main()
