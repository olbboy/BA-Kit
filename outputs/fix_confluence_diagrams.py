#!/usr/bin/env python3
"""
Fix diagram pages on Confluence.
Converts mermaid code blocks to rendered PNG images using mermaid-cli,
uploads them as attachments, and updates page content.
"""

import os
import sys
import json
import re
import time
import requests
import subprocess
import tempfile
from pathlib import Path
from dotenv import load_dotenv

# Load env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

BASE_URL = os.environ.get('CONFLUENCE_BASE_URL', '').rstrip('/')
PAT = os.environ.get('CONFLUENCE_PAT', '')

API = f"{BASE_URL}/rest/api/content"
HEADERS = {
    'Authorization': f'Bearer {PAT}',
    'Content-Type': 'application/json',
}
HEADERS_UPLOAD = {
    'Authorization': f'Bearer {PAT}',
    'X-Atlassian-Token': 'nocheck',
}

# Manifest from previous push
MANIFEST_PATH = Path(__file__).parent / 'mini-app-cham-cong' / 'confluence_manifest.json'
SRC_DIR = Path(__file__).parent / 'mini-app-cham-cong'


def load_manifest():
    """Load the page manifest from the push step."""
    with open(MANIFEST_PATH, 'r') as f:
        return json.load(f)


def get_page_content(page_id: str) -> dict:
    """Get current page content and version."""
    url = f"{API}/{page_id}?expand=body.storage,version"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()
    print(f"  ❌ Failed to get page {page_id}: {resp.status_code}")
    return None


def update_page_content(page_id: str, title: str, body_xhtml: str, version: int) -> bool:
    """Update a page's content."""
    payload = {
        "type": "page",
        "title": title,
        "version": {"number": version + 1},
        "body": {
            "storage": {
                "value": body_xhtml,
                "representation": "storage"
            }
        }
    }
    resp = requests.put(f"{API}/{page_id}", headers=HEADERS, json=payload)
    if resp.status_code == 200:
        return True
    print(f"  ❌ Failed to update page {page_id}: {resp.status_code}: {resp.text[:200]}")
    return False


def upload_attachment(page_id: str, filepath: str, filename: str) -> str:
    """Upload a file as attachment to a page. Returns the download URL."""
    url = f"{API}/{page_id}/child/attachment"
    with open(filepath, 'rb') as f:
        files = {'file': (filename, f, 'image/png')}
        resp = requests.post(url, headers=HEADERS_UPLOAD, files=files)
    
    if resp.status_code in (200, 201):
        results = resp.json().get('results', [])
        if results:
            dl = results[0].get('_links', {}).get('download', '')
            print(f"    📎 Attached: {filename}")
            return dl
    
    # Try updating existing attachment
    resp2 = requests.get(f"{url}?filename={filename}", headers=HEADERS)
    if resp2.status_code == 200:
        existing = resp2.json().get('results', [])
        if existing:
            att_id = existing[0]['id']
            url_update = f"{API}/{page_id}/child/attachment/{att_id}/data"
            with open(filepath, 'rb') as f:
                files = {'file': (filename, f, 'image/png')}
                resp3 = requests.post(url_update, headers=HEADERS_UPLOAD, files=files)
            if resp3.status_code in (200, 201):
                dl = resp3.json().get('_links', {}).get('download', '')
                print(f"    📎 Updated: {filename}")
                return dl
    
    print(f"    ❌ Failed to attach {filename}: {resp.status_code}: {resp.text[:200]}")
    return None


def render_mermaid_to_png(mermaid_code: str, output_path: str) -> bool:
    """Render mermaid code to PNG using mermaid-cli (mmdc)."""
    # Write mermaid source to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, dir=SRC_DIR) as f:
        f.write(mermaid_code)
        mmd_path = f.name
    
    try:
        # Try mmdc (mermaid CLI)
        result = subprocess.run(
            ['npx', '-y', '@mermaid-js/mermaid-cli', 'mmdc',
             '-i', mmd_path, '-o', output_path,
             '-b', 'white', '-w', '1200'],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0 and os.path.exists(output_path):
            return True
        print(f"    ⚠️  mmdc failed: {result.stderr[:200]}")
    except FileNotFoundError:
        print("    ⚠️  mmdc not found, using Kroki API fallback")
    except subprocess.TimeoutExpired:
        print("    ⚠️  mmdc timed out, using Kroki API fallback")
    finally:
        os.unlink(mmd_path)
    
    # Fallback: Use Kroki.io public API
    import base64, zlib
    try:
        encoded = base64.urlsafe_b64encode(
            zlib.compress(mermaid_code.encode('utf-8'), 9)
        ).decode('ascii')
        kroki_url = f"https://kroki.io/mermaid/png/{encoded}"
        resp = requests.get(kroki_url, timeout=30)
        if resp.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(resp.content)
            return True
        print(f"    ⚠️  Kroki failed: {resp.status_code}")
    except Exception as e:
        print(f"    ⚠️  Kroki error: {e}")
    
    return False


def extract_mermaid_blocks(md_content: str) -> list:
    """Extract all mermaid code blocks from markdown."""
    blocks = []
    pattern = re.compile(r'```mermaid\s*\n(.*?)```', re.DOTALL)
    for i, match in enumerate(pattern.finditer(md_content)):
        blocks.append({
            'index': i,
            'code': match.group(1).strip(),
            'full_match': match.group(0),
            'start': match.start(),
            'end': match.end()
        })
    return blocks


def find_page_id_by_title(manifest: dict, title_fragment: str) -> str:
    """Find page ID from manifest by partial title match."""
    for p in manifest.get('pages', []):
        if title_fragment.lower() in p['title'].lower():
            return p['id']
    return None


def process_page_diagrams(page_id: str, title: str, md_filepath: Path):
    """Process mermaid diagrams for a single page."""
    print(f"\n📄 Processing: {title} (ID: {page_id})")
    
    # Read local markdown
    with open(md_filepath, 'r') as f:
        md_content = f.read()
    
    blocks = extract_mermaid_blocks(md_content)
    if not blocks:
        print("   No mermaid diagrams found")
        return
    
    print(f"   Found {len(blocks)} mermaid diagram(s)")
    
    # Get current page from Confluence
    page = get_page_content(page_id)
    if not page:
        return
    
    current_body = page['body']['storage']['value']
    current_version = page['version']['number']
    new_body = current_body
    
    for block in blocks:
        diagram_name = f"diagram_{page_id}_{block['index']}.png"
        png_path = os.path.join(tempfile.gettempdir(), diagram_name)
        
        print(f"   Rendering diagram {block['index']+1}...")
        if render_mermaid_to_png(block['code'], png_path):
            # Upload as attachment
            dl_url = upload_attachment(page_id, png_path, diagram_name)
            if dl_url:
                # Replace mermaid code block in Confluence XHTML with image reference
                # Find the code block in XHTML (it was converted as a code macro)
                code_pattern = re.compile(
                    r'<ac:structured-macro ac:name="code">'
                    r'<ac:parameter ac:name="language">mermaid</ac:parameter>'
                    r'<ac:plain-text-body><!\[CDATA\[.*?\]\]></ac:plain-text-body>'
                    r'</ac:structured-macro>',
                    re.DOTALL
                )
                
                image_xhtml = (
                    f'<p><ac:image ac:align="center" ac:width="800">'
                    f'<ri:attachment ri:filename="{diagram_name}" />'
                    f'</ac:image></p>'
                )
                
                # Replace first occurrence
                new_body = code_pattern.sub(image_xhtml, new_body, count=1)
            
            # Cleanup temp file
            if os.path.exists(png_path):
                os.unlink(png_path)
        else:
            print(f"   ⚠️  Could not render diagram {block['index']+1}")
    
    # Update page if body changed
    if new_body != current_body:
        print(f"   Updating page content...")
        if update_page_content(page_id, title, new_body, current_version):
            print(f"   ✅ Page updated with {len(blocks)} diagram image(s)")
        else:
            print(f"   ❌ Failed to update page")
    else:
        print(f"   ℹ️  No mermaid code blocks found in XHTML (might already be fixed)")


def main():
    print("=" * 60)
    print("Fix Diagrams on Confluence Pages")
    print("=" * 60)
    
    manifest = load_manifest()
    
    # Map of local files with diagrams → their Confluence page IDs
    diagram_pages = [
        {
            'md_file': SRC_DIR / '2.11-Mini-app' / 'README.md',
            'title_match': '2.11 Mini app',
        },
        {
            'md_file': SRC_DIR / '2.11-Mini-app' / '2.11.3.-Giải-trình-công' / 'README.md',
            'title_match': '2.11.3',
        },
        {
            'md_file': SRC_DIR / '2.11-Mini-app' / '2.11.7.-Cấu-hình-lịch-nghỉ' / 'README.md',
            'title_match': '2.11.7',
        },
    ]
    
    for dp in diagram_pages:
        page_id = find_page_id_by_title(manifest, dp['title_match'])
        if page_id:
            page = get_page_content(page_id)
            if page:
                process_page_diagrams(page_id, page['title'], dp['md_file'])
                time.sleep(0.5)
        else:
            print(f"  ⚠️  Page not found in manifest for: {dp['title_match']}")
    
    print("\n" + "=" * 60)
    print("Done!")


if __name__ == '__main__':
    main()
