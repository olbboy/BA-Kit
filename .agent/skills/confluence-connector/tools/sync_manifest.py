#!/usr/bin/env python3
"""
Sync updated docs from local → Confluence using manifest page IDs.
Maps local files to Confluence pages via the confluence_manifest.json.
Uses DC-safe XHTML conversion (json→javascript, gherkin→text, mermaid→mermaid-macro).
"""
import os, sys, re, json, time, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
# Fallback: try project root .env (tools → connector → skills → .agent → root)
_project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
load_dotenv(str(_project_root / '.env'))

BASE_URL = os.environ.get('CONFLUENCE_BASE_URL', '').rstrip('/')
PAT = os.environ.get('CONFLUENCE_PAT', '')
API = f"{BASE_URL}/rest/api/content"
HEADERS = {'Authorization': f'Bearer {PAT}', 'Content-Type': 'application/json'}

SRC = _project_root / 'outputs' / 'mini-app-cham-cong'
if not SRC.exists():
    # Fallback: try from workspace root
    SRC = Path(os.environ.get('WORKSPACE_ROOT', os.getcwd())) / 'outputs' / 'mini-app-cham-cong'
MANIFEST = SRC / 'confluence_manifest.json'

# ── Confluence DC Language Mapping ──
DC_LANG_MAP = {'json': 'javascript', 'gherkin': 'text', 'typescript': 'javascript', 'go': 'text', 'rust': 'text'}
DC_TITLE_MAP = {'json': 'JSON', 'gherkin': 'Gherkin Scenarios', 'typescript': 'TypeScript', 'go': 'Go', 'rust': 'Rust'}

# ── File → Manifest Title Mapping ──
# Built by matching local filenames to manifest page titles
FILE_TO_TITLE = {
    # Root docs
    'overview/README.md': 'Tổng quan dự án',
    'eams-v2-comprehensive.md': 'EAMS v2.1 — Tài liệu nghiệp vụ toàn diện',
    'overview/BRD-01-Nhân-viên.md': 'BRD-01: Nhân viên',
    'overview/BRD-02-Quản-lý.md': 'BRD-02: Quản lý',
    'overview/BRD-03-HR-Admin.md': 'BRD-03: HR Admin',
    'overview/BRD-04-IT-và-System-Admin.md': 'BRD-04: IT & System Admin',
    'overview/modules-overview.md': 'Tổng quan Modules',
    'overview/Demo-Plan-Sprint-8.md': 'Demo Plan Sprint 8',
    'RTM.md': 'RTM — Ma trận truy vết yêu cầu',
    'AUDIT-REPORT.md': 'AUDIT-REPORT — Sức khỏe dự án',
    # M01
    'modules/m01-cham-cong/README.md': 'M01. Chấm công & Nhật ký',
    'modules/m01-cham-cong/us-atten-01-hub-cham-cong.md': 'US-ATTEN-01: Hub chấm công',
    'modules/m01-cham-cong/us-atten-02-thong-ke-hieu-suat-thang.md': 'US-ATTEN-02: Thống kê hiệu suất tháng',
    'modules/m01-cham-cong/us-atten-03-xem-chi-tiet-nhat-ky-cham-cong.md': 'US-ATTEN-03: Xem chi tiết nhật ký chấm công',
    'modules/m01-cham-cong/us-atten-04-trung-tam-canh-bao-va-thong-bao.md': 'US-ATTEN-04: Trung tâm cảnh báo và thông báo',
    'modules/m01-cham-cong/us-atten-05-nhap-cham-cong-thu-cong.md': 'US-ATTEN-05: Nhập chấm công thủ công (Manual Entry)',
    'modules/m01-cham-cong/api-spec.md': 'API Specification — M01. Chấm công & Nhật ký',
    'modules/m01-cham-cong/db-schema.md': 'Database Schema — M01. Chấm công & Nhật ký',
    'modules/m01-cham-cong/test-cases.md': 'Test Suite — M01. Chấm công & Nhật ký',
    # M02
    'modules/m02-trung-tam-dang-ky/README.md': 'M02. Trung tâm Đăng ký',
    'modules/m02-trung-tam-dang-ky/us-reg-01-dang-ky-nghe-phep.md': 'US-REG-01: Đăng ký nghỉ phép',
    'modules/m02-trung-tam-dang-ky/us-reg-02-dang-ky-doi-ca.md': 'US-REG-02: Đăng ký đổi ca',
    'modules/m02-trung-tam-dang-ky/us-reg-03-dang-ky-tang-ca.md': 'US-REG-03: Đăng ký tăng ca (OT)',
    'modules/m02-trung-tam-dang-ky/us-reg-04-theo-doi-don-tu-va-han-muc.md': 'US-REG-04: Theo dõi đơn từ và hạn mức',
    'modules/m02-trung-tam-dang-ky/us-reg-05-cau-hinh-chinh-sach-phep-nam.md': 'US-REG-05: Cấu hình chính sách phép năm (Leave Policy Admin)',
    'modules/m02-trung-tam-dang-ky/us-reg-06-dang-ky-cong-tac-va-wfh.md': 'US-REG-06: Đăng ký công tác & WFH (Business Travel / Work From Home)',
    'modules/m02-trung-tam-dang-ky/api-spec.md': 'API Specification — M02. Trung tâm Đăng ký',
    'modules/m02-trung-tam-dang-ky/db-schema.md': 'Database Schema — M02. Trung tâm Đăng ký',
    'modules/m02-trung-tam-dang-ky/test-cases.md': 'Test Suite — M02. Trung tâm Đăng ký',
    # M03
    'modules/m03-giai-trinh/README.md': 'M03. Giải trình công',
    'modules/m03-giai-trinh/us-expl-01-danh-sach-loi-can-giai-trinh.md': 'US-EXPL-01: Danh sách lỗi cần giải trình',
    'modules/m03-giai-trinh/us-expl-02-yeu-cau-sua-cham-cong.md': 'US-EXPL-02: Yêu cầu sửa chấm công (Attendance Correction)',
    'modules/m03-giai-trinh/api-spec.md': 'API Specification — M03. Giải trình công',
    'modules/m03-giai-trinh/db-schema.md': 'Database Schema — M03. Giải trình công',
    'modules/m03-giai-trinh/test-cases.md': 'Test Suite — M03. Giải trình công',
    # M04
    'modules/m04-bao-cao-ca-nhan/README.md': 'M04. Báo cáo cá nhân',
    'modules/m04-bao-cao-ca-nhan/us-rptprs-01-dashboard-hieu-suat-ca-nhan.md': 'US-RPTPRS-01: Dashboard hiệu suất cá nhân',
    'modules/m04-bao-cao-ca-nhan/us-rptprs-02-bang-kpi-va-highlights.md': 'US-RPTPRS-02: Bảng KPI và Highlights',
    'modules/m04-bao-cao-ca-nhan/api-spec.md': 'API Specification — M04. Báo cáo cá nhân',
    'modules/m04-bao-cao-ca-nhan/db-schema.md': 'Database Schema — M04. Báo cáo cá nhân',
    'modules/m04-bao-cao-ca-nhan/test-cases.md': 'Test Suite — M04. Báo cáo cá nhân',
    # M05
    'modules/m05-quan-ly-nhan-su/README.md': 'M05. Quản lý Nhân sự',
    'modules/m05-quan-ly-nhan-su/us-emp-01-so-do-co-cau-to-chuc.md': 'US-EMP-01: Sơ đồ cơ cấu tổ chức',
    'modules/m05-quan-ly-nhan-su/us-emp-02-quan-ly-phong-ban.md': 'US-EMP-02: Quản lý phòng ban (CRUD)',
    'modules/m05-quan-ly-nhan-su/us-emp-03-danh-sach-nhan-su.md': 'US-EMP-03: Danh sách nhân sự và tìm kiếm',
    'modules/m05-quan-ly-nhan-su/us-emp-04-bulk-import-nhan-vien.md': 'US-EMP-04: Bulk Import nhân viên',
    'modules/m05-quan-ly-nhan-su/us-emp-05-dashboard-hien-dien.md': 'US-EMP-05: Dashboard hiện diện real-time',
    'modules/m05-quan-ly-nhan-su/us-emp-06-danh-muc-cap-bac.md': 'US-EMP-06: Danh mục cấp bậc',
    'modules/m05-quan-ly-nhan-su/api-spec.md': 'API Specification — M05. Quản lý Nhân sự',
    'modules/m05-quan-ly-nhan-su/db-schema.md': 'Database Schema — M05. Quản lý Nhân sự',
    'modules/m05-quan-ly-nhan-su/test-cases.md': 'Test Suite — M05. Quản lý Nhân sự',
    # M06
    'modules/m06-ca-lam-viec/README.md': 'M06. Ca làm việc & Phân ca',
    'modules/m06-ca-lam-viec/us-shift-01-danh-sach-ca-lam-viec.md': 'US-SHIFT-01: Danh sách ca làm việc',
    'modules/m06-ca-lam-viec/us-shift-02-cau-hinh-gio-va-ngay-lam-viec.md': 'US-SHIFT-02: Cấu hình giờ và ngày làm việc',
    'modules/m06-ca-lam-viec/us-shift-03-gioi-han-thoi-gian-cham-cong-punch-limit.md': 'US-SHIFT-03: Giới hạn thời gian chấm công (punch limit)',
    'modules/m06-ca-lam-viec/us-shift-04-cau-hinh-gio-nghi.md': 'US-SHIFT-04: Cấu hình giờ nghỉ',
    'modules/m06-ca-lam-viec/us-shift-05-import-nhan-vien-vao-ca.md': 'US-SHIFT-05: Import nhân viên vào ca',
    'modules/m06-ca-lam-viec/us-shift-06-phan-ca-theo-pattern.md': 'US-SHIFT-06: Phân ca theo Pattern (Ca xoay/luân phiên)',
    'modules/m06-ca-lam-viec/us-shift-07-xem-lich-phan-ca-team.md': 'US-SHIFT-07: Xem lịch phân ca team (Manager View)',
    'modules/m06-ca-lam-viec/api-spec.md': 'API Specification — M06. Ca làm việc & Phân ca',
    'modules/m06-ca-lam-viec/db-schema.md': 'Database Schema — M06. Ca làm việc & Phân ca',
    'modules/m06-ca-lam-viec/test-cases.md': 'Test Suite — M06. Ca làm việc & Phân ca',
    # M07
    'modules/m07-lich-nghi/README.md': 'M07. Lịch nghỉ & Ngày lễ',
    'modules/m07-lich-nghi/us-hol-01-quan-ly-danh-sach-ngay-nghi.md': 'US-HOL-01: Quản lý danh sách ngày nghỉ',
    'modules/m07-lich-nghi/us-hol-02-cau-hinh-policy-nghi-va-rule-nghi.md': 'US-HOL-02: Cấu hình policy nghỉ và rule nghỉ',
    'modules/m07-lich-nghi/us-hol-03-logic-sync-batch-job.md': 'US-HOL-03: Logic sync & batch job',
    'modules/m07-lich-nghi/us-hol-04-api-hien-thi.md': 'US-HOL-04: API hiển thị',
    'modules/m07-lich-nghi/api-spec.md': 'API Specification — M07. Lịch nghỉ & Ngày lễ',
    'modules/m07-lich-nghi/db-schema.md': 'Database Schema — M07. Lịch nghỉ & Ngày lễ',
    'modules/m07-lich-nghi/test-cases.md': 'Test Suite — M07. Lịch nghỉ & Ngày lễ',
    # M08
    'modules/m08-camera-ai/README.md': 'M08. Camera AI (C-Vision)',
    'modules/m08-camera-ai/us-cam-01-quan-ly-danh-sach-thiet-bi.md': 'US-CAM-01: Quản lý danh sách thiết bị Camera',
    'modules/m08-camera-ai/us-cam-02-mapping-nhan-vien.md': 'US-CAM-02: Mapping nhân viên - Camera',
    'modules/m08-camera-ai/us-cam-03-health-check-va-monitoring.md': 'US-CAM-03: Health check và Monitoring',
    'modules/m08-camera-ai/us-cam-04-dang-ky-khuon-mat-nhan-vien.md': 'US-CAM-04: Đăng ký khuôn mặt nhân viên (Face ID Enrollment)',
    'modules/m08-camera-ai/api-spec.md': 'API Specification — M08. Camera AI (C-Vision)',
    'modules/m08-camera-ai/db-schema.md': 'Database Schema — M08. Camera AI (C-Vision)',
    'modules/m08-camera-ai/test-cases.md': 'Test Suite — M08. Camera AI (C-Vision)',
    # M09
    'modules/m09-thong-bao/README.md': 'M09. Cấu hình Thông báo',
    'modules/m09-thong-bao/us-notif-01-cau-hinh-kenh-thong-bao.md': 'US-NOTIF-01: Cấu hình kênh thông báo',
    'modules/m09-thong-bao/us-notif-02-cau-hinh-su-kien-kich-hoat.md': 'US-NOTIF-02: Cấu hình sự kiện kích hoạt',
    'modules/m09-thong-bao/us-notif-03-quan-ly-policy-thong-bao.md': 'US-NOTIF-03: Quản lý policy thông báo',
    'modules/m09-thong-bao/us-notif-04-quan-ly-template-email.md': 'US-NOTIF-04: Quản lý Template Email thông báo',
    'modules/m09-thong-bao/api-spec.md': 'API Specification — M09. Cấu hình Thông báo',
    'modules/m09-thong-bao/db-schema.md': 'Database Schema — M09. Cấu hình Thông báo',
    'modules/m09-thong-bao/test-cases.md': 'Test Suite — M09. Cấu hình Thông báo',
    # M10
    'modules/m10-phe-duyet/README.md': 'M10. Trung tâm Phê duyệt',
    'modules/m10-phe-duyet/us-appr-01-inbox-phe-duyet.md': 'US-APPR-01: Inbox phê duyệt',
    'modules/m10-phe-duyet/us-appr-02-cau-hinh-chuoi-phe-duyet.md': 'US-APPR-02: Cấu hình chuỗi phê duyệt',
    'modules/m10-phe-duyet/us-appr-03-phe-duyet-hang-loat.md': 'US-APPR-03: Phê duyệt hàng loạt',
    'modules/m10-phe-duyet/api-spec.md': 'API Specification — M10. Trung tâm Phê duyệt',
    'modules/m10-phe-duyet/db-schema.md': 'Database Schema — M10. Trung tâm Phê duyệt',
    'modules/m10-phe-duyet/test-cases.md': 'Test Suite — M10. Trung tâm Phê duyệt',
    # M11
    'modules/m11-bao-cao-tong/README.md': 'M11. Báo cáo tổng & Xuất dữ liệu',
    'modules/m11-bao-cao-tong/us-rpt-01-dashboard-quan-ly.md': 'US-RPT-01: Dashboard quản lý',
    'modules/m11-bao-cao-tong/us-rpt-02-xuat-bao-cao-va-payroll.md': 'US-RPT-02: Xuất báo cáo và Payroll',
    'modules/m11-bao-cao-tong/us-rpt-03-bao-cao-tuan-thu.md': 'US-RPT-03: Báo cáo tuân thủ',
    'modules/m11-bao-cao-tong/us-rpt-04-khoa-ky-luong.md': 'US-RPT-04: Khóa kỳ lương (Payroll Lock)',
    'modules/m11-bao-cao-tong/api-spec.md': 'API Specification — M11. Báo cáo tổng & Xuất dữ liệu',
    'modules/m11-bao-cao-tong/db-schema.md': 'Database Schema — M11. Báo cáo tổng & Xuất dữ liệu',
    'modules/m11-bao-cao-tong/test-cases.md': 'Test Suite — M11. Báo cáo tổng & Xuất dữ liệu',
    # M12
    'modules/m12-quan-tri-he-thong/README.md': 'M12. Quản trị hệ thống',
    'modules/m12-quan-tri-he-thong/us-sys-01-quan-ly-chi-nhanh.md': 'US-SYS-01: Quản lý chi nhánh (Site Management)',
    'modules/m12-quan-tri-he-thong/us-sys-02-audit-log-viewer.md': 'US-SYS-02: Audit Log Viewer',
    'modules/m12-quan-tri-he-thong/us-sys-03-employee-offboarding.md': 'US-SYS-03: Employee Offboarding Workflow',
    'modules/m12-quan-tri-he-thong/us-sys-04-chot-cong-thang.md': 'US-SYS-04: Chốt công tháng (Period Closing)',
    'modules/m12-quan-tri-he-thong/us-sys-05-employee-onboarding.md': 'US-SYS-05: Employee Onboarding Wizard',
    'modules/m12-quan-tri-he-thong/us-sys-06-cau-hinh-data-retention-policy.md': 'US-SYS-06: Cấu hình Data Retention Policy',
    'modules/m12-quan-tri-he-thong/api-spec.md': 'API Specification — M12. Quản trị hệ thống',
    'modules/m12-quan-tri-he-thong/db-schema.md': 'Database Schema — M12. Quản trị hệ thống',
    'modules/m12-quan-tri-he-thong/test-cases.md': 'Test Suite — M12. Quản trị hệ thống',
}


# ── XHTML Converter (DC-safe) ──
def _esc(t):
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    t = re.sub(r'[\U0001F300-\U0001F9FF\U00002600-\U000027BF\U0001FA00-\U0001FAFF\u2B50\u2705\u26A0\u2753\u274C\u2714\u2611\u2B06\u2191]', '', t)
    return t

def _inline(t):
    t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)
    t = re.sub(r'\*\*\*\*', '', t)
    t = re.sub(r'\*\*(.+?)\*\*', lambda m: f'<strong>{_esc(m.group(1))}</strong>', t)
    t = re.sub(r'(?<!<)\*(.+?)\*(?!>)', lambda m: f'<em>{_esc(m.group(1))}</em>', t)
    t = re.sub(r'`(.+?)`', lambda m: f'<code>{_esc(m.group(1))}</code>', t)
    parts = re.split(r'(</?(?:strong|em|code)[^>]*>)', t)
    return ''.join(_esc(s) if not re.match(r'</?(?:strong|em|code)', s) else s for s in parts).strip()

def _table(rows):
    if not rows: return ''
    h = '<table><colgroup>'
    for _ in rows[0]: h += '<col />'
    h += '</colgroup><tbody>'
    for i, row in enumerate(rows):
        h += '<tr>'
        tag = 'th' if i == 0 else 'td'
        for cell in row: h += f'<{tag}>{_inline(cell)}</{tag}>'
        h += '</tr>'
    h += '</tbody></table>'
    return h

def md_to_xhtml(md):
    lines = md.split('\n')
    out = []
    in_tbl = in_code = in_list = False
    c_lang = ''; c_orig = ''; c_lines = []; lt = None; trows = []
    
    def _flush_code():
        content = '\n'.join(c_lines)
        if c_orig == 'mermaid':
            return f'<ac:structured-macro ac:name="mermaid-macro"><ac:plain-text-body><![CDATA[{content}]]></ac:plain-text-body></ac:structured-macro>'
        title = f'<ac:parameter ac:name="title">{DC_TITLE_MAP[c_orig]}</ac:parameter>' if c_orig in DC_TITLE_MAP else ''
        return f'<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">{c_lang}</ac:parameter>{title}<ac:plain-text-body><![CDATA[{content}]]></ac:plain-text-body></ac:structured-macro>'
    
    for line in lines:
        if line.startswith('```'):
            if in_code:
                out.append(_flush_code())
                in_code = False; c_lines = []
            else:
                if in_list: out.append(f'</{lt}>'); in_list = False
                in_code = True
                c_orig = line[3:].strip() or 'text'
                c_lang = DC_LANG_MAP.get(c_orig, c_orig)
            continue
        if in_code: c_lines.append(line); continue
        if '|' in line and line.strip().startswith('|'):
            if in_list: out.append(f'</{lt}>'); in_list = False
            cells = [c.strip() for c in line.strip().split('|')[1:-1]]
            if all(set(c) <= {'-',':',' '} for c in cells): continue
            if not in_tbl: in_tbl = True; trows = []
            trows.append(cells); continue
        elif in_tbl: out.append(_table(trows)); in_tbl = False; trows = []
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            if in_list: out.append(f'</{lt}>'); in_list = False
            out.append(f'<h{len(m.group(1))}>{_inline(m.group(2))}</h{len(m.group(1))}>'); continue
        if line.strip() in ('---','***','___'):
            if in_list: out.append(f'</{lt}>'); in_list = False
            out.append('<hr />'); continue
        # Blockquote
        bq = re.match(r'^>\s*(.*)', line)
        if bq:
            if in_list: out.append(f'</{lt}>'); in_list = False
            out.append(f'<blockquote><p>{_inline(bq.group(1))}</p></blockquote>'); continue
        ul = re.match(r'^(\s*)[-*]\s+(.*)', line)
        if ul:
            if not in_list or lt != 'ul':
                if in_list: out.append(f'</{lt}>')
                out.append('<ul>'); in_list = True; lt = 'ul'
            out.append(f'<li>{_inline(ul.group(2))}</li>'); continue
        ol = re.match(r'^(\s*)\d+\.\s+(.*)', line)
        if ol:
            if not in_list or lt != 'ol':
                if in_list: out.append(f'</{lt}>')
                out.append('<ol>'); in_list = True; lt = 'ol'
            out.append(f'<li>{_inline(ol.group(2))}</li>'); continue
        if not line.strip():
            if in_list: out.append(f'</{lt}>'); in_list = False
            continue
        if in_list: out.append(f'</{lt}>'); in_list = False
        t = _inline(line)
        if t: out.append(f'<p>{t}</p>')
    if in_tbl: out.append(_table(trows))
    if in_list: out.append(f'</{lt}>')
    if in_code: out.append(_flush_code())
    return '\n'.join(out)


# ── Confluence API ──
def get_page(page_id):
    resp = requests.get(f"{API}/{page_id}?expand=version", headers=HEADERS)
    return resp.json() if resp.status_code == 200 else None

def update_page(page_id, title, body, version):
    payload = {
        "type": "page", "title": title,
        "version": {"number": version + 1},
        "body": {"storage": {"value": body, "representation": "storage"}}
    }
    resp = requests.put(f"{API}/{page_id}", headers=HEADERS, json=payload)
    return resp.status_code == 200, resp.text[:200] if resp.status_code != 200 else ''

def validate_page(page_id):
    """Check body.view for rendering errors."""
    resp = requests.get(f"{API}/{page_id}?expand=body.view", headers=HEADERS)
    if resp.status_code == 200:
        view = resp.json()['body']['view']['value']
        if 'Error rendering' in view or 'Unknown macro' in view:
            return False, 'Rendering error detected'
        return True, 'OK'
    return False, f'HTTP {resp.status_code}'


def main():
    # Load manifest
    manifest = json.load(open(MANIFEST))
    title_to_id = {p['title']: p['id'] for p in manifest['pages']}
    
    print("=" * 70)
    print("Confluence Sync — Local → DC (with DC-safe XHTML conversion)")
    print(f"Source: {SRC}")
    print(f"Target: {BASE_URL}/display/CVH/Attendance")
    print(f"Files to sync: {len(FILE_TO_TITLE)}")
    print("=" * 70)
    
    if not BASE_URL or not PAT:
        print("ERROR: Set CONFLUENCE_BASE_URL and CONFLUENCE_PAT in .env")
        sys.exit(1)
    
    # Validate mapping
    unmapped = []
    for fp, title in FILE_TO_TITLE.items():
        if title not in title_to_id:
            unmapped.append((fp, title))
    
    if unmapped:
        print(f"\n⚠️  {len(unmapped)} titles not found in manifest:")
        for fp, title in unmapped:
            print(f"  ❌ {fp}: \"{title}\"")
        print("Fix FILE_TO_TITLE mapping or update manifest.")
        sys.exit(1)
    
    print(f"\n✅ All {len(FILE_TO_TITLE)} file→title→page_id mappings validated.")
    
    # Check --dry-run mode
    dry_run = '--dry-run' in sys.argv
    if dry_run:
        print("\n🔍 DRY RUN MODE — no changes will be made.\n")
    
    updated = skipped = failed = 0
    
    for rel_path, title in FILE_TO_TITLE.items():
        filepath = SRC / rel_path
        page_id = title_to_id[title]
        
        if not filepath.exists():
            print(f"  ⚠️  File not found: {rel_path}")
            skipped += 1
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            md = f.read()
        
        body = md_to_xhtml(md)
        
        if dry_run:
            # Just report what would happen
            has_json = '```json' in md
            has_gherkin = '```gherkin' in md
            has_mermaid = '```mermaid' in md
            flags = []
            if has_json: flags.append('JSON')
            if has_gherkin: flags.append('Gherkin')
            if has_mermaid: flags.append('Mermaid')
            flag_str = f' [{",".join(flags)}]' if flags else ''
            
            # Verify mapping worked
            if has_json and 'language">json' in body:
                print(f"  ❌ {rel_path}: JSON NOT MAPPED!")
                failed += 1
            elif has_gherkin and 'language">gherkin' in body:
                print(f"  ❌ {rel_path}: Gherkin NOT MAPPED!")
                failed += 1
            elif has_mermaid and 'language">mermaid' in body:
                print(f"  ❌ {rel_path}: Mermaid NOT using macro!")
                failed += 1
            else:
                print(f"  ✅ {rel_path} → {page_id}{flag_str}")
                updated += 1
            continue
        
        # Real push
        page = get_page(page_id)
        if not page:
            print(f"  ❌ Cannot get page {page_id}: {title}")
            failed += 1; continue
        
        ver = page['version']['number']
        ok, err = update_page(page_id, title, body, ver)
        if ok:
            print(f"  ✅ {title} (v{ver+1})")
            updated += 1
        else:
            print(f"  ❌ {title}: {err}")
            failed += 1
        
        time.sleep(0.3)
    
    print(f"\n{'=' * 70}")
    mode = "DRY RUN" if dry_run else "DONE"
    print(f"{mode}! Updated: {updated} | Skipped: {skipped} | Failed: {failed}")
    print("=" * 70)
    
    if not dry_run and failed == 0:
        print("\n🔍 Post-upload validation (sampling 5 pages)...")
        sample_ids = [title_to_id[t] for _, t in list(FILE_TO_TITLE.items())[:5]]
        for pid in sample_ids:
            ok, msg = validate_page(pid)
            print(f"  {'✅' if ok else '❌'} Page {pid}: {msg}")


if __name__ == '__main__':
    main()
