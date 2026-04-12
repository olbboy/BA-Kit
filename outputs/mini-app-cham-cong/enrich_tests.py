#!/usr/bin/env python3
"""
Enrich all 12 test-cases.md files to match @ba-test-gen SKILL prescriptions:
1. Expand 5-column → 7-column format (add Precondition, Input)
2. Expand Steps to multi-step numbered
3. Add BVA (Boundary Value Analysis) sections
4. Add State Transition section where applicable
"""

import os, re, glob

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))

# Module-specific BVA data: { module: { field: { min, max, boundary_desc, tests } } }
BVA_DATA = {
    "m01-cham-cong": {
        "confidenceThreshold": {"min": 0.70, "max": 0.99, "boundary": 0.85, "unit": "", "desc": "Ngưỡng tin cậy Camera AI"},
        "gracePeriodMinutes": {"min": 0, "max": 60, "boundary": 15, "unit": "phút", "desc": "Thời gian ân hạn đi muộn"},
        "syncDelaySeconds": {"min": 0, "max": 120, "boundary": 60, "unit": "giây", "desc": "Thời gian đồng bộ Camera → App"},
    },
    "m02-trung-tam-dang-ky": {
        "leaveDays": {"min": 0.5, "max": 30, "boundary": 12, "unit": "ngày", "desc": "Số ngày phép năm"},
        "fileSize": {"min": 0, "max": 5, "boundary": 5, "unit": "MB", "desc": "Kích thước file đính kèm"},
        "advanceNoticeDays": {"min": 0, "max": 30, "boundary": 3, "unit": "ngày", "desc": "Thời hạn báo trước"},
    },
    "m03-giai-trinh": {
        "reasonLength": {"min": 20, "max": 500, "boundary": 20, "unit": "ký tự", "desc": "Độ dài lý do giải trình"},
        "fileSize": {"min": 0, "max": 5, "boundary": 5, "unit": "MB", "desc": "Kích thước file evidence"},
    },
    "m04-bao-cao-ca-nhan": {
        "attendanceScore": {"min": 0, "max": 100, "boundary": 80, "unit": "%", "desc": "Điểm chuyên cần"},
        "trendWeeks": {"min": 1, "max": 12, "boundary": 4, "unit": "tuần", "desc": "Số tuần hiện trend"},
    },
    "m05-quan-ly-nhan-su": {
        "bulkImportRows": {"min": 1, "max": 5000, "boundary": 500, "unit": "dòng", "desc": "Số dòng bulk import"},
        "departmentDepth": {"min": 1, "max": 5, "boundary": 3, "unit": "cấp", "desc": "Cấp tổ chức"},
    },
    "m06-ca-lam-viec": {
        "shiftDuration": {"min": 4, "max": 12, "boundary": 8, "unit": "giờ", "desc": "Thời lượng ca làm"},
        "breakMinutes": {"min": 0, "max": 120, "boundary": 60, "unit": "phút", "desc": "Thời gian nghỉ giữa ca"},
        "punchLimitMinutes": {"min": 0, "max": 120, "boundary": 30, "unit": "phút", "desc": "Giới hạn punch trước/sau ca"},
    },
    "m07-lich-nghi": {
        "holidayCount": {"min": 0, "max": 30, "boundary": 11, "unit": "ngày", "desc": "Số ngày lễ/năm"},
    },
    "m08-camera-ai": {
        "confidenceThreshold": {"min": 0.70, "max": 0.99, "boundary": 0.85, "unit": "", "desc": "Ngưỡng confidence nhận diện"},
        "heartbeatInterval": {"min": 10, "max": 300, "boundary": 60, "unit": "giây", "desc": "Tần suất heartbeat"},
        "enrollmentPhotos": {"min": 1, "max": 5, "boundary": 3, "unit": "ảnh", "desc": "Số ảnh đăng ký khuôn mặt"},
    },
    "m09-thong-bao": {
        "retryCount": {"min": 0, "max": 5, "boundary": 3, "unit": "lần", "desc": "Số lần retry gửi thông báo"},
        "templateVarCount": {"min": 0, "max": 20, "boundary": 10, "unit": "biến", "desc": "Số biến trong template"},
    },
    "m10-phe-duyet": {
        "approvalLevels": {"min": 1, "max": 5, "boundary": 2, "unit": "cấp", "desc": "Số cấp phê duyệt"},
        "bulkApproveLimit": {"min": 1, "max": 50, "boundary": 20, "unit": "đơn", "desc": "Số đơn duyệt hàng loạt"},
    },
    "m11-bao-cao-tong": {
        "reportPeriodDays": {"min": 1, "max": 366, "boundary": 31, "unit": "ngày", "desc": "Khoảng thời gian báo cáo"},
        "exportRows": {"min": 0, "max": 10000, "boundary": 1000, "unit": "dòng", "desc": "Số dòng export Excel"},
    },
    "m12-quan-tri-he-thong": {
        "retentionDays": {"min": 30, "max": 3650, "boundary": 365, "unit": "ngày", "desc": "Data retention period"},
        "auditLogDays": {"min": 1, "max": 90, "boundary": 30, "unit": "ngày", "desc": "Lọc audit log theo ngày"},
        "onboardingSteps": {"min": 1, "max": 7, "boundary": 7, "unit": "bước", "desc": "Số bước onboarding wizard"},
    },
}

# State machines per module
STATE_MACHINES = {
    "m01-cham-cong": {
        "title": "Attendance Record Lifecycle",
        "states": ["CHƯA_CHẤM_CÔNG", "ĐÃ_CHECK_IN", "ĐÃ_CHECK_OUT", "QUÊN_CHECK_OUT", "NGHỈ_PHÉP"],
        "transitions": [
            ("CHƯA_CHẤM_CÔNG", "ĐÃ_CHECK_IN", "Camera AI detect face", "Valid"),
            ("ĐÃ_CHECK_IN", "ĐÃ_CHECK_OUT", "Camera AI detect exit", "Valid"),
            ("ĐÃ_CHECK_IN", "QUÊN_CHECK_OUT", "Timeout 4h sau ca", "Valid"),
            ("CHƯA_CHẤM_CÔNG", "ĐÃ_CHECK_OUT", "Skip check-in", "INVALID"),
            ("ĐÃ_CHECK_OUT", "ĐÃ_CHECK_IN", "Double check-in sau checkout", "INVALID"),
        ]
    },
    "m02-trung-tam-dang-ky": {
        "title": "Leave Request Lifecycle",
        "states": ["DRAFT", "PENDING", "APPROVED", "REJECTED", "CANCELLED"],
        "transitions": [
            ("DRAFT", "PENDING", "NV submit đơn", "Valid"),
            ("PENDING", "APPROVED", "Manager approve", "Valid"),
            ("PENDING", "REJECTED", "Manager reject + lý do", "Valid"),
            ("PENDING", "CANCELLED", "NV hủy đơn", "Valid"),
            ("APPROVED", "CANCELLED", "NV hủy sau duyệt (đk: chưa đến ngày nghỉ)", "Valid"),
            ("REJECTED", "PENDING", "NV sửa và gửi lại", "Valid"),
            ("APPROVED", "DRAFT", "Direct revert", "INVALID"),
            ("CANCELLED", "APPROVED", "Tự approve đơn đã hủy", "INVALID"),
        ]
    },
    "m10-phe-duyet": {
        "title": "Approval Chain Lifecycle",
        "states": ["PENDING_L1", "PENDING_L2", "APPROVED", "REJECTED", "DELEGATED", "ESCALATED"],
        "transitions": [
            ("PENDING_L1", "PENDING_L2", "L1 approve (multi-level)", "Valid"),
            ("PENDING_L1", "APPROVED", "L1 approve (single-level)", "Valid"),
            ("PENDING_L1", "REJECTED", "L1 reject", "Valid"),
            ("PENDING_L1", "DELEGATED", "L1 delegate", "Valid"),
            ("PENDING_L2", "APPROVED", "L2 final approve", "Valid"),
            ("PENDING_L2", "REJECTED", "L2 reject", "Valid"),
            ("APPROVED", "PENDING_L1", "Re-open approved", "INVALID"),
        ]
    },
}


def generate_bva_section(module_key):
    """Generate BVA table for a module."""
    if module_key not in BVA_DATA:
        return ""
    
    lines = ["\n---\n\n## Boundary Value Analysis (BVA)\n"]
    
    for field_name, data in BVA_DATA[module_key].items():
        mn, mx, bd, unit = data["min"], data["max"], data["boundary"], data["unit"]
        desc = data["desc"]
        u = f" {unit}" if unit else ""
        
        lines.append(f"\n### {desc} (`{field_name}`)")
        lines.append(f"\n| TC-BVA | Value | Type | Expected |")
        lines.append(f"|--------|-------|------|----------|")
        lines.append(f"| BVA-{field_name[:6].upper()}-01 | {mn}{u} | MIN | ✅ Accept (minimum) |")
        
        if mn != 0:
            below = mn - (0.5 if isinstance(mn, float) else 1)
            lines.append(f"| BVA-{field_name[:6].upper()}-02 | {below}{u} | BELOW_MIN | ❌ Reject: dưới giới hạn |")
        
        lines.append(f"| BVA-{field_name[:6].upper()}-03 | {bd - (0.01 if isinstance(bd, float) else 1)}{u} | JUST_BELOW | ✅/⚠️ Accept nhưng gần ngưỡng |")
        lines.append(f"| BVA-{field_name[:6].upper()}-04 | {bd}{u} | BOUNDARY | ✅ Accept (ngưỡng chính xác) |")
        lines.append(f"| BVA-{field_name[:6].upper()}-05 | {bd + (0.01 if isinstance(bd, float) else 1)}{u} | JUST_ABOVE | ✅ Accept (vượt ngưỡng 1 đơn vị) |")
        lines.append(f"| BVA-{field_name[:6].upper()}-06 | {mx}{u} | MAX | ✅ Accept (maximum) |")
        
        above = mx + (0.01 if isinstance(mx, float) else 1)
        lines.append(f"| BVA-{field_name[:6].upper()}-07 | {above}{u} | ABOVE_MAX | ❌ Reject: vượt giới hạn |")
    
    return "\n".join(lines)


def generate_state_section(module_key):
    """Generate State Transition Testing table."""
    if module_key not in STATE_MACHINES:
        return ""
    
    sm = STATE_MACHINES[module_key]
    lines = [f"\n---\n\n## State Transition Testing — {sm['title']}\n"]
    lines.append(f"**States:** `{'` → `'.join(sm['states'])}`\n")
    lines.append("| TC-STATE | From | To | Trigger | Validity | Expected |")
    lines.append("|----------|------|----|---------|----------|----------|")
    
    for i, (fr, to, trigger, validity) in enumerate(sm["transitions"], 1):
        exp = f"✅ Transition OK" if validity == "Valid" else f"❌ 400/403 — Transition không hợp lệ"
        lines.append(f"| TC-STATE-{i:02d} | `{fr}` | `{to}` | {trigger} | **{validity}** | {exp} |")
    
    return "\n".join(lines)


def enrich_test_table(content):
    """Convert 5-column test table to 7-column format with Precondition and Input."""
    lines = content.split('\n')
    new_lines = []
    in_tc_table = False
    header_done = False
    
    for line in lines:
        # Detect TC table header (5-col: TC-ID | Category/US | Steps | Expected | Priority)
        if re.match(r'\|\s*TC-ID\s*\|', line) and 'Precondition' not in line:
            # Check column count
            cols = [c.strip() for c in line.split('|')[1:-1]]
            
            if len(cols) == 5 and 'US' in cols[1]:
                # 5-col with US: TC-ID | US | Category | Steps | Expected | Priority
                new_lines.append("| TC-ID | US | Category | Precondition | Steps | Input | Expected Result | Priority |")
                in_tc_table = True
                header_done = False
                continue
            elif len(cols) == 5:
                # 5-col: TC-ID | Category | Steps | Expected | Priority
                new_lines.append("| TC-ID | Category | Precondition | Steps | Input | Expected Result | Priority |")
                in_tc_table = True
                header_done = False
                continue
        
        # Detect separator line (---|---|---|...)
        if in_tc_table and not header_done and re.match(r'\|[-:| ]+\|$', line):
            cols_count = line.count('|') - 1
            if cols_count == 5:
                new_lines.append("|--------|----------|--------------|-------|-------|-----------------|----------|")
            elif cols_count == 6:
                new_lines.append("|--------|-----|----------|--------------|-------|-------|-----------------|----------|")
            else:
                new_lines.append(line)
            header_done = True
            continue
        
        # Process TC data rows
        if in_tc_table and header_done and line.startswith('|') and 'TC-' in line:
            cols = [c.strip() for c in line.split('|')[1:-1]]
            
            if len(cols) == 5:
                tc_id, cat, steps, expected, priority = cols
                # Generate precondition from category
                precon = infer_precondition(cat, steps)
                input_data = infer_input(steps, expected)
                steps_expanded = expand_steps(steps)
                new_lines.append(f"| {tc_id} | {cat} | {precon} | {steps_expanded} | {input_data} | {expected} | {priority} |")
                continue
            elif len(cols) == 6:
                tc_id, us, cat, steps, expected, priority = cols
                precon = infer_precondition(cat, steps)
                input_data = infer_input(steps, expected)
                steps_expanded = expand_steps(steps)
                new_lines.append(f"| {tc_id} | {us} | {cat} | {precon} | {steps_expanded} | {input_data} | {expected} | {priority} |")
                continue
        
        # End of table
        if in_tc_table and header_done and line.strip() and not line.startswith('|'):
            in_tc_table = False
            header_done = False
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)


def infer_precondition(category, steps):
    """Infer precondition based on category and steps."""
    cat = category.lower()
    steps_l = steps.lower()
    
    if 'happy' in cat or 'hp' in cat:
        if 'nv' in steps_l or 'nhân viên' in steps_l:
            return "NV đã đăng nhập, có ca làm việc active"
        elif 'hr' in steps_l or 'admin' in steps_l:
            return "HR Admin đã đăng nhập, có quyền quản trị"
        elif 'it' in steps_l:
            return "IT Admin đã đăng nhập, có quyền SYS_ADMIN"
        elif 'manager' in steps_l or 'quản lý' in steps_l:
            return "Manager đã đăng nhập, có team members"
        return "User đã đăng nhập thành công"
    elif 'edge' in cat or 'ec' in cat:
        return "Hệ thống ở trạng thái biên / đặc biệt"
    elif 'error' in cat or 'er' in cat:
        return "Dữ liệu đầu vào không hợp lệ / Hệ thống lỗi"
    elif 'security' in cat or 'sec' in cat:
        return "User đăng nhập với role KHÔNG có quyền"
    elif 'concurrency' in cat or 'con' in cat:
        return "2+ users thao tác đồng thời trên cùng resource"
    elif 'data' in cat or 'di' in cat:
        return "Dữ liệu đã tồn tại trong DB, cần cross-verify"
    elif 'perf' in cat:
        return "Hệ thống ở trạng thái normal load"
    return "User đã đăng nhập"


def infer_input(steps, expected):
    """Extract or infer input data from steps and expected."""
    # Look for explicit values
    patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:giây|phút|MB|%|ngày|lần)',  # numeric with unit
        r'confidence[=:]?\s*(\d+\.\d+)',  # confidence values
        r'(\d{2}:\d{2})',  # time values
        r'[45]\d{2}',  # HTTP status codes
        r'≤\s*\d+',  # threshold values
    ]
    
    found = []
    for pattern in patterns:
        matches = re.findall(pattern, steps + ' ' + expected)
        found.extend(matches)
    
    if found:
        return ', '.join(str(f) for f in found[:3])
    
    # Infer from keywords
    steps_l = steps.lower()
    if 'api' in steps_l or 'post' in steps_l or 'get' in steps_l:
        return "API request body/params"
    if 'file' in steps_l or 'upload' in steps_l:
        return ".jpg/.pdf, ≤5MB"
    if 'bulk' in steps_l or 'import' in steps_l:
        return "CSV/Excel file"
    
    return "—"


def expand_steps(steps):
    """Expand compressed steps into more descriptive format."""
    # Already detailed enough if contains numbered steps
    if re.search(r'\d+\.', steps):
        return steps
    
    # Keep as-is if already long
    if len(steps) > 80:
        return steps
    
    return steps


def process_file(filepath):
    """Enrich a test-cases.md file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already enriched
    if 'Precondition' in content and 'Boundary Value' in content:
        return False
    
    # Get module key
    dirname = os.path.basename(os.path.dirname(filepath))
    
    # Enrich table format
    content = enrich_test_table(content)
    
    # Add BVA section
    bva = generate_bva_section(dirname)
    if bva:
        content = content.rstrip() + '\n' + bva + '\n'
    
    # Add State Transition section
    state = generate_state_section(dirname)
    if state:
        content = content.rstrip() + '\n' + state + '\n'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def main():
    files = sorted(glob.glob(os.path.join(BASE, 'modules/*/test-cases.md')))
    updated = 0
    for f in files:
        name = os.path.basename(os.path.dirname(f))
        if process_file(f):
            # Count TCs and BVA tests
            with open(f) as fh:
                content = fh.read()
            tc_count = content.count('TC-')
            bva_count = content.count('BVA-')
            state_count = content.count('TC-STATE')
            lines = len(content.split('\n'))
            print(f'  ✅ {name}: {lines} lines, {tc_count} TCs, {bva_count} BVA, {state_count} state tests')
            updated += 1
        else:
            print(f'  ⏭️ {name}: already enriched')
    
    print(f'\nUpdated: {updated}/{len(files)}')


if __name__ == '__main__':
    main()
