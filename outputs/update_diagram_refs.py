#!/usr/bin/env python3
"""
Direct fix: Replace broken diagram data in Confluence pages with image references.
The diagram PNGs were already uploaded as attachments.
"""

import os
import re
import time
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

BASE_URL = os.environ.get('CONFLUENCE_BASE_URL', '').rstrip('/')
PAT = os.environ.get('CONFLUENCE_PAT', '')
API = f"{BASE_URL}/rest/api/content"
HEADERS = {
    'Authorization': f'Bearer {PAT}',
    'Content-Type': 'application/json',
}


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
    print(f"  ❌ Update failed: {resp.status_code}: {resp.text[:300]}")
    return False


def fix_page_diagrams(page_id, attachment_names):
    """
    Find the USE CASE DIAGRAM / WORKFLOW sections and replace
    broken encoded data with <ac:image> references.
    """
    page = get_page(page_id)
    if not page:
        print(f"  ❌ Could not get page {page_id}")
        return

    title = page['title']
    body = page['body']['storage']['value']
    version = page['version']['number']
    print(f"\n📄 {title} (v{version})")

    original_body = body
    att_idx = 0

    # Strategy: Find diagram heading sections and replace
    # the broken content that follows.
    # Pattern: <h3>..DIAGRAM..</h3> followed by broken data (long encoded strings)
    # until the next <h3>, <h2>, <hr> or end of document

    # Find all diagram section headings
    heading_pattern = re.compile(
        r'(<h[23]>.*?(?:DIAGRAM|WORKFLOW|SƠ ĐỒ).*?</h[23]>)',
        re.IGNORECASE | re.DOTALL
    )

    matches = list(heading_pattern.finditer(body))
    if not matches:
        print("   No diagram headings found")
        return

    print(f"   Found {len(matches)} diagram heading(s)")

    # Process in reverse order to preserve positions
    for m in reversed(matches):
        if att_idx >= len(attachment_names):
            # Use from end of list backwards
            img_idx = len(attachment_names) - 1 - (len(matches) - 1 - att_idx)
            if img_idx < 0:
                img_idx = 0
        else:
            img_idx = att_idx

        heading_end = m.end()

        # Find the end of the broken content section
        # (next heading or horizontal rule or end of body)
        next_section = re.search(r'<h[123]>|<hr\s*/?>', body[heading_end:])
        if next_section:
            section_end = heading_end + next_section.start()
        else:
            section_end = len(body)

        # Check if the content between heading and next section looks broken
        # (contains long strings of alphanumeric chars — encoded data)
        between = body[heading_end:section_end]
        has_broken = bool(re.search(r'[A-Za-z0-9+/=]{50,}', between))

        if has_broken:
            filename = attachment_names[img_idx] if img_idx < len(attachment_names) else attachment_names[-1]
            image_xhtml = (
                f'\n<p><ac:image ac:align="center" ac:width="900">'
                f'<ri:attachment ri:filename="{filename}" />'
                f'</ac:image></p>\n'
            )
            body = body[:heading_end] + image_xhtml + body[section_end:]
            print(f"   ✅ Replaced broken data after \"{m.group(1)[:60]}...\" → {filename}")
        else:
            print(f"   ℹ️  Content after \"{m.group(1)[:60]}...\" looks clean, skipping")

        att_idx += 1

    if body != original_body:
        if update_page(page_id, title, body, version):
            print(f"   ✅ Page updated (v{version+1})")
        else:
            print(f"   ❌ Failed to update")
    else:
        print("   No changes needed")


def main():
    print("=" * 60)
    print("Fix broken diagrams on Confluence pages")
    print("=" * 60)

    # Page → attachment mapping
    pages = [
        ('196786907', ['diagram_196786907_0.png']),                    # 2.11 Mini app
        ('196786927', ['diagram_196786927_0.png', 'diagram_196786927_1.png']),  # 2.11.3
        ('196786944', ['diagram_196786944_0.png', 'diagram_196786944_1.png']),  # 2.11.7
    ]

    for page_id, attachments in pages:
        fix_page_diagrams(page_id, attachments)
        time.sleep(0.5)

    print("\n" + "=" * 60)
    print("Done!")


if __name__ == '__main__':
    main()
