# EAMS Mini App Chấm Công

Enterprise Attendance Management System — first project delivered by BA-Kit.

## Overview

| Field | Value |
|-------|-------|
| Client | Internal (Antigravity demo) |
| Domain | HR / Attendance Management |
| Scale | 5,000+ employees, multi-site, multi-tenant |
| Compliance | Luật Lao động VN 2019, NĐ 13/2023 |
| Integration | C-Vision Face Recognition (Camera AI) |

## Artifacts Produced

| Type | Count | Location |
|------|-------|----------|
| BRDs | 4 (by persona) | outputs/mini-app-cham-cong/overview/ |
| User Stories | 46 | outputs/mini-app-cham-cong/phase-01~05/ |
| API Specs | 12 | Per module api-spec.md |
| DB Schemas | 12 | Per module db-schema.md |
| Edge Cases | 168+ | Per US EDGE CASES section |
| Phase Plans | 6 | Per phase plan.md |
| Comprehensive Doc | 1 (887 lines, 17 sections) | eams-v2-comprehensive.md |

## Architecture

12 modules organized into 5 implementation phases:

- **Phase 01** (Sprint 8): m05 Nhân sự → m06 Ca → m07 Nghỉ → m09 Thông báo
- **Phase 02** (Sprint 8): m08 Camera AI
- **Phase 03** (Sprint 8): m01 Chấm công
- **Phase 04** (Sprint 9): m04 Đăng ký → m03 Giải trình → m10 Phê duyệt
- **Phase 05** (Sprint 10): m05-rpt Báo cáo CN → m11 Báo cáo tổng
- **Cross-cutting**: m12 Quản trị hệ thống

## Key Decisions

- [4-BRD Persona Strategy](../decisions/4-brd-persona-strategy.md)
- [Phase-Based Directory](../decisions/phase-based-directory.md)
- OT holiday rate: always 3.0x (Luật LĐ VN trumps weekend 2.0x)
- Grace period: 15 min default, configurable per shift
- Payroll lock: auto-lock after export, re-export creates new version
- Data retention: Face ID photos 90 days, attendance records 5 years

## Open Questions

5 items pending PO decision — see outputs/mini-app-cham-cong/README.md "Open Questions" section.
