#!/usr/bin/env python3
"""
BA-Kit Coverage Checker — Automated RTM Scanner
Scans project artifacts to detect gaps in the BRD → US → AC → TC → API → DB pipeline.

Usage:
    python3 .agent/scripts/coverage_checker.py outputs/mini-app-cham-cong/
    python3 .agent/scripts/coverage_checker.py outputs/mini-app-cham-cong/ --verbose
    python3 .agent/scripts/coverage_checker.py outputs/mini-app-cham-cong/ --json
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict


def extract_title(filepath):
    """Extract H1 title from markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith('# '):
                return line.strip()[2:].strip()
    return filepath.stem


def count_acceptance_criteria(filepath):
    """Count AC sections in a US file. Returns (total_ac, has_happy, has_edge, has_error)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().lower()

    # Count AC blocks — match patterns like:
    #   #### **AC1. Title**        (bold heading, e.g. m04-m12)
    #   #### **3.1. Title**        (numbered sub-section, e.g. m01)
    #   #### AC-01: Title          (dashed ID)
    #   ### Scenario 1: Happy Path (Gherkin)
    #   Given ... When ... Then    (GWT blocks)
    ac_heading_pattern = re.compile(
        r'#{2,4}\s+\*{0,2}\s*(?:ac[-\s]?\d|scenario|trường hợp)',
        re.IGNORECASE
    )
    # Also match #### **3.1. Title** sub-section format (numbered AC decomposition)
    ac_subsection_pattern = re.compile(r'####\s+\*{0,2}\s*\d+\.\d+\.')
    ac_sections = len(ac_heading_pattern.findall(content)) + len(ac_subsection_pattern.findall(content))
    gwt_blocks = len(re.findall(r'given\s', content))
    if ac_sections == 0:
        ac_sections = max(1, gwt_blocks)

    # Detect coverage types — expanded patterns for Vietnamese BA output
    has_happy = bool(re.search(
        r'(happy.?path|thành công|đúng giờ|hợp lệ|valid|success|hiển thị|'
        r'danh sách|mặc định|cho phép|hỗ trợ|render|trả về)',
        content
    ))
    has_edge = bool(re.search(
        r'(edge.?case|boundary|biên|giới hạn|maximum|minimum|tối đa|tối thiểu|'
        r'100%|0%|grace|đặc biệt|ca đêm|cross-|vượt|quá hạn|hết hạn)',
        content
    ))
    has_error = bool(re.search(
        r'(error|lỗi|fail|thất bại|invalid|không hợp lệ|từ chối|reject|'
        r'exception|ngoại lệ|chặn|cảnh báo|warning|offline|timeout)',
        content
    ))
    has_security = bool(re.search(
        r'(rbac|abac|role|quyền|access|unauthorized|403|bảo mật|phân quyền)',
        content
    ))

    return {
        'total_ac': ac_sections,
        'gwt_blocks': gwt_blocks,
        'has_happy': has_happy,
        'has_edge': has_edge,
        'has_error': has_error,
        'has_security': has_security,
    }


def scan_ambiguous_terms(filepath):
    """Scan for forbidden ambiguous terms."""
    FORBIDDEN = [
        'adequate', 'appropriate', 'as quickly as possible', 'easy', 'efficient',
        'fast', 'flexible', 'good', 'intuitive', 'lightweight', 'maximize',
        'minimize', 'normal', 'optimal', 'quick', 'reasonable', 'robust',
        'seamless', 'simple', 'sufficient', 'timely', 'transparent',
        'user-friendly', 'user friendly', 'tbd', 'nhanh', 'dễ dàng',
        'hiệu quả', 'tối ưu', 'linh hoạt'
    ]
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().lower()

    found = []
    for term in FORBIDDEN:
        if term in content:
            found.append(term)
    return found


def scan_project(project_dir):
    """Scan entire project and generate coverage report."""
    project_dir = Path(project_dir)
    report = {
        'modules': defaultdict(lambda: {
            'user_stories': [],
            'has_api_spec': False,
            'has_db_schema': False,
            'has_readme': False,
        }),
        'brds': [],
        'root_files': [],
        'test_cases': [],
        'summary': {},
    }

    # Scan all markdown files
    for md in sorted(project_dir.rglob('*.md')):
        rel = md.relative_to(project_dir)
        parts = list(rel.parts)

        # Root files
        if len(parts) == 1:
            report['root_files'].append(str(rel))
            continue

        # Determine module from directory structure
        # Phase-based: phase-01/m05-xxx/US-xxx.md
        # Or direct: 2.11-Mini-app/2.11.1-xxx/US-xxx.md
        module_key = None
        if len(parts) >= 2:
            # Find the module directory
            for i, part in enumerate(parts):
                if part.startswith('m') and '-' in part and i > 0:
                    module_key = part
                    break
                if re.match(r'2\.11\.\d+', part):
                    module_key = part
                    break

        if not module_key:
            if 'overview' in str(rel) or 'BRD' in md.name:
                report['brds'].append({
                    'path': str(rel),
                    'title': extract_title(md),
                })
            elif 'cross-cutting' in str(rel):
                module_key = 'cross-cutting'
            else:
                report['root_files'].append(str(rel))
                continue

        if module_key:
            mod = report['modules'][module_key]
            if md.name == 'README.md':
                mod['has_readme'] = True
                mod['title'] = extract_title(md)
            elif md.name == 'api-spec.md':
                mod['has_api_spec'] = True
            elif md.name == 'db-schema.md':
                mod['has_db_schema'] = True
            elif md.name.startswith('US-') or re.match(r'US-\w+-\d+', md.stem):
                ac_info = count_acceptance_criteria(md)
                ambiguous = scan_ambiguous_terms(md)
                us_info = {
                    'id': md.stem,
                    'title': extract_title(md),
                    'path': str(rel),
                    'ac': ac_info,
                    'ambiguous_terms': ambiguous,
                }
                mod['user_stories'].append(us_info)
            elif md.name.startswith('TC-'):
                report['test_cases'].append(str(rel))

    return report


def calculate_scores(report):
    """Calculate quality scores from scan results."""
    scores = {
        'modules': {},
        'overall': {},
    }

    total_us = 0
    total_us_with_3ac = 0
    total_us_with_happy = 0
    total_us_with_edge = 0
    total_us_with_error = 0
    total_us_with_security = 0
    total_modules_with_api = 0
    total_modules_with_db = 0
    total_modules = 0
    total_ambiguous = 0

    for mod_key, mod in report['modules'].items():
        total_modules += 1
        us_list = mod['user_stories']
        n_us = len(us_list)

        if mod['has_api_spec']:
            total_modules_with_api += 1
        if mod['has_db_schema']:
            total_modules_with_db += 1

        mod_score = {
            'us_count': n_us,
            'has_api': mod['has_api_spec'],
            'has_db': mod['has_db_schema'],
            'avg_ac': 0,
            'pct_happy': 0,
            'pct_edge': 0,
            'pct_error': 0,
            'pct_security': 0,
            'ambiguous_count': 0,
        }

        if n_us > 0:
            total_ac = sum(us['ac']['total_ac'] for us in us_list)
            mod_score['avg_ac'] = round(total_ac / n_us, 1)
            mod_score['pct_happy'] = round(sum(1 for us in us_list if us['ac']['has_happy']) / n_us * 100)
            mod_score['pct_edge'] = round(sum(1 for us in us_list if us['ac']['has_edge']) / n_us * 100)
            mod_score['pct_error'] = round(sum(1 for us in us_list if us['ac']['has_error']) / n_us * 100)
            mod_score['pct_security'] = round(sum(1 for us in us_list if us['ac']['has_security']) / n_us * 100)
            mod_score['ambiguous_count'] = sum(len(us['ambiguous_terms']) for us in us_list)

            total_us += n_us
            total_us_with_3ac += sum(1 for us in us_list if us['ac']['total_ac'] >= 3)
            total_us_with_happy += sum(1 for us in us_list if us['ac']['has_happy'])
            total_us_with_edge += sum(1 for us in us_list if us['ac']['has_edge'])
            total_us_with_error += sum(1 for us in us_list if us['ac']['has_error'])
            total_us_with_security += sum(1 for us in us_list if us['ac']['has_security'])
            total_ambiguous += mod_score['ambiguous_count']

        scores['modules'][mod_key] = mod_score

    # Overall scores
    if total_us > 0:
        scores['overall'] = {
            'total_us': total_us,
            'total_modules': total_modules,
            'total_brds': len(report['brds']),
            'total_test_cases': len(report['test_cases']),
            'api_coverage': round(total_modules_with_api / total_modules * 100) if total_modules > 0 else 0,
            'db_coverage': round(total_modules_with_db / total_modules * 100) if total_modules > 0 else 0,
            'avg_ac_per_us': round(sum(s['avg_ac'] for s in scores['modules'].values() if s['us_count'] > 0) / max(1, sum(1 for s in scores['modules'].values() if s['us_count'] > 0)), 1),
            'us_with_3ac_pct': round(total_us_with_3ac / total_us * 100),
            'happy_path_coverage': round(total_us_with_happy / total_us * 100),
            'edge_case_coverage': round(total_us_with_edge / total_us * 100),
            'error_case_coverage': round(total_us_with_error / total_us * 100),
            'security_coverage': round(total_us_with_security / total_us * 100),
            'total_ambiguous_terms': total_ambiguous,
        }

        # Calculate overall health score
        health = (
            (scores['overall']['happy_path_coverage'] / 100 * 0.15) +
            (scores['overall']['edge_case_coverage'] / 100 * 0.20) +
            (scores['overall']['error_case_coverage'] / 100 * 0.20) +
            (scores['overall']['security_coverage'] / 100 * 0.15) +
            (scores['overall']['api_coverage'] / 100 * 0.10) +
            (scores['overall']['db_coverage'] / 100 * 0.10) +
            (min(scores['overall']['us_with_3ac_pct'], 100) / 100 * 0.10)
        ) * 100
        # Penalty for ambiguous terms
        penalty = min(total_ambiguous * 0.5, 10)
        scores['overall']['health_score'] = round(max(0, health - penalty))
        scores['overall']['health_status'] = (
            '🟢 HEALTHY' if scores['overall']['health_score'] >= 80 else
            '🟡 AT RISK' if scores['overall']['health_score'] >= 60 else
            '🔴 CRITICAL'
        )

    return scores


def print_report(report, scores, verbose=False):
    """Print the coverage report in markdown format."""
    o = scores['overall']
    print("=" * 60)
    print(f"  BA-Kit Coverage Report")
    print(f"  Health: {o.get('health_score', 0)}% — {o.get('health_status', 'N/A')}")
    print("=" * 60)

    print(f"\n## Inventory")
    print(f"  User Stories: {o.get('total_us', 0)}")
    print(f"  Modules: {o.get('total_modules', 0)}")
    print(f"  BRD Documents: {o.get('total_brds', 0)}")
    print(f"  Test Cases: {o.get('total_test_cases', 0)}")

    print(f"\n## Coverage Scores")
    print(f"  API Spec Coverage: {o.get('api_coverage', 0)}%")
    print(f"  DB Schema Coverage: {o.get('db_coverage', 0)}%")
    print(f"  Avg AC per US: {o.get('avg_ac_per_us', 0)}")
    print(f"  US with ≥3 AC: {o.get('us_with_3ac_pct', 0)}%")

    print(f"\n## Scenario Coverage")
    print(f"  Happy Path: {o.get('happy_path_coverage', 0)}%")
    print(f"  Edge Cases: {o.get('edge_case_coverage', 0)}%")
    print(f"  Error Cases: {o.get('error_case_coverage', 0)}%")
    print(f"  Security: {o.get('security_coverage', 0)}%")

    print(f"\n## Quality")
    print(f"  Ambiguous Terms Found: {o.get('total_ambiguous_terms', 0)}")

    if verbose:
        print(f"\n## Module Detail")
        for mod_key, ms in sorted(scores['modules'].items()):
            api_icon = '✅' if ms['has_api'] else '❌'
            db_icon = '✅' if ms['has_db'] else '❌'
            print(f"\n  ### {mod_key}")
            print(f"    US: {ms['us_count']} | API: {api_icon} | DB: {db_icon}")
            print(f"    Avg AC: {ms['avg_ac']} | Happy: {ms['pct_happy']}% | Edge: {ms['pct_edge']}% | Error: {ms['pct_error']}% | Sec: {ms['pct_security']}%")
            if ms['ambiguous_count'] > 0:
                print(f"    ⚠️ Ambiguous terms: {ms['ambiguous_count']}")

            # List user stories with issues
            mod = report['modules'][mod_key]
            for us in mod['user_stories']:
                issues = []
                if not us['ac']['has_happy']:
                    issues.append('no happy path')
                if not us['ac']['has_edge']:
                    issues.append('no edge case')
                if not us['ac']['has_error']:
                    issues.append('no error case')
                if us['ambiguous_terms']:
                    issues.append(f'ambiguous: {", ".join(us["ambiguous_terms"][:3])}')
                if issues:
                    print(f"      ⚠️ {us['id']}: {'; '.join(issues)}")

    print(f"\n{'=' * 60}")
    print(f"  VERDICT: {o.get('health_status', 'N/A')}")
    print(f"{'=' * 60}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 coverage_checker.py <project_dir> [--verbose] [--json]")
        sys.exit(1)

    project_dir = sys.argv[1]
    verbose = '--verbose' in sys.argv
    as_json = '--json' in sys.argv

    if not os.path.isdir(project_dir):
        print(f"Error: {project_dir} is not a directory")
        sys.exit(1)

    report = scan_project(project_dir)
    scores = calculate_scores(report)

    if as_json:
        # Convert defaultdict for JSON serialization
        report['modules'] = dict(report['modules'])
        print(json.dumps({'report': report, 'scores': scores}, indent=2, ensure_ascii=False))
    else:
        print_report(report, scores, verbose)


if __name__ == '__main__':
    main()
