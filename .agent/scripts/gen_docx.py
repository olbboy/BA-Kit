#!/usr/bin/env python3
"""
BA-Kit Enterprise Document Exporter (SKILL-21)
Converts Markdown documents to DOCX using Pandoc with customer-specific reference templates.
"""

import argparse
import subprocess
import sys
from pathlib import Path

# ANSI colors
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

REFERENCES_DIR = Path(__file__).parent.parent / "references"
DEFAULT_REFERENCE = REFERENCES_DIR / "default_reference.docx"

def check_pandoc():
    """Check if Pandoc is installed."""
    try:
        result = subprocess.run(["pandoc", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"{GREEN}✓ {version}{RESET}")
            return True
    except FileNotFoundError:
        pass
    
    print(f"{RED}✗ Pandoc not found. Install with: brew install pandoc{RESET}")
    return False

def get_reference(customer):
    """Get the reference.docx path for a customer."""
    if customer:
        customer_ref = REFERENCES_DIR / f"{customer}_reference.docx"
        if customer_ref.exists():
            return customer_ref
        print(f"{YELLOW}⚠ Reference for '{customer}' not found. Using default.{RESET}")
    
    if DEFAULT_REFERENCE.exists():
        return DEFAULT_REFERENCE
    
    return None

def export_docx(input_md, output_docx, customer=None, toc=True, numbered=True):
    """Export Markdown to DOCX using Pandoc."""
    print(f"{CYAN}📄 Export: {input_md} → {output_docx}{RESET}")
    
    if not check_pandoc():
        return False
    
    reference = get_reference(customer)
    
    cmd = ["pandoc", str(input_md), "-t", "docx"]
    
    if reference:
        cmd.extend(["--reference-doc", str(reference)])
        print(f"   Reference: {reference.name}")
    
    if toc:
        cmd.extend(["--toc", "--toc-depth=3"])
        print(f"   TOC: Enabled (depth 3)")
    
    if numbered:
        cmd.append("--number-sections")
        print(f"   Numbering: Enabled")
    
    cmd.extend(["-o", str(output_docx)])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{GREEN}✅ Export successful: {output_docx}{RESET}")
            return True
        else:
            print(f"{RED}✗ Export failed: {result.stderr}{RESET}")
            return False
    except Exception as e:
        print(f"{RED}✗ Error: {e}{RESET}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BA-Kit Document Exporter (MD → DOCX)')
    parser.add_argument('input', help='Input Markdown file')
    parser.add_argument('-o', '--output', help='Output DOCX file (default: same name as input)')
    parser.add_argument('-c', '--customer', help='Customer profile (e.g., bank_a, gov_standard)')
    parser.add_argument('--no-toc', action='store_true', help='Disable table of contents')
    parser.add_argument('--no-number', action='store_true', help='Disable section numbering')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"{RED}✗ File not found: {args.input}{RESET}")
        sys.exit(1)
    
    output_path = args.output or input_path.with_suffix('.docx')
    
    success = export_docx(
        input_path, 
        output_path, 
        customer=args.customer,
        toc=not args.no_toc,
        numbered=not args.no_number
    )
    
    sys.exit(0 if success else 1)
