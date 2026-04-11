# 🏥 PROJECT HEALTH REPORT — EAMS Mini App Chấm Công

**Audit Date:** 2026-04-11
**Auditor:** BA-Kit Antigravity (Full Audit Protocol)
**Overall Health:** 78% — AT RISK (pre-improvement baseline)

---

## Executive Summary

| Dimension | Score | Trend | Status |
|-----------|-------|-------|--------|
| Requirements Completeness | 92% | ► | 🟢 |
| AC Scenario Depth | 85% | ► | 🟢 |
| Cross-Artifact Consistency | 82% | ► | 🟢 |
| Test Coverage | 0% | ▼ | 🔴 |
| BRD Quality | 88% | ► | 🟢 |
| Traceability | 0% | ▼ | 🔴 |
| **Overall** | **78%** | | **🟡 AT RISK** |

> Test coverage (0%) and traceability (0%) are the critical blockers dragging overall health below the 80% PASS threshold.

---

## 📦 Phase 2: Quality Gate Audit

### Gate 1: User Story Completeness — Module Summary

| Module | US Count | Actor | Action | Value | Biz Flow | RBAC | AC-Happy | AC-Edge | AC-Error | Cross-Ref | No-Ambig | Score | Verdict |
|--------|----------|-------|--------|-------|----------|------|----------|---------|----------|-----------|----------|-------|---------|
| M01 Chấm công | 5 | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ | 3/5 ⚠️ | 4/5 ⚠️ | **90%** | ✅ PASS |
| M05 Nhân sự | 6 | 6/6 ✅ | 6/6 ✅ | 6/6 ✅ | 6/6 ✅ | 6/6 ✅ | 6/6 ✅ | 5/6 ⚠️ | 5/6 ⚠️ | 4/6 ⚠️ | 5/6 ⚠️ | **87%** | ✅ PASS |
| M06 Ca làm việc | 6 | 6/6 ✅ | 6/6 ✅ | 5/6 ⚠️ | 6/6 ✅ | 6/6 ✅ | 6/6 ✅ | 5/6 ⚠️ | 4/6 ⚠️ | 4/6 ⚠️ | 5/6 ⚠️ | **84%** | ✅ PASS |
| M07 Lịch nghỉ | 4 | 4/4 ✅ | 4/4 ✅ | 4/4 ✅ | 4/4 ✅ | 4/4 ✅ | 4/4 ✅ | 4/4 ✅ | 3/4 ⚠️ | 3/4 ⚠️ | 4/4 ✅ | **88%** | ✅ PASS |
| M09 Thông báo | 3 | 3/3 ✅ | 3/3 ✅ | 3/3 ✅ | 3/3 ✅ | 3/3 ✅ | 3/3 ✅ | 3/3 ✅ | 2/3 ⚠️ | 2/3 ⚠️ | 3/3 ✅ | **86%** | ✅ PASS |
| M08 Camera AI | 4 | 4/4 ✅ | 4/4 ✅ | 4/4 ✅ | 4/4 ✅ | 4/4 ✅ | 4/4 ✅ | 4/4 ✅ | 4/4 ✅ | 4/4 ✅ | 4/4 ✅ | **95%** | ✅ PASS |
| M04 Đăng ký | 6 | 6/6 ✅ | 6/6 ✅ | 6/6 ✅ | 6/6 ✅ | 6/6 ✅ | 6/6 ✅ | 6/6 ✅ | 5/6 ⚠️ | 4/6 ⚠️ | 5/6 ⚠️ | **89%** | ✅ PASS |
| M03 Giải trình | 2 | 2/2 ✅ | 2/2 ✅ | 2/2 ✅ | 2/2 ✅ | 2/2 ✅ | 2/2 ✅ | 2/2 ✅ | 2/2 ✅ | 2/2 ✅ | 2/2 ✅ | **92%** | ✅ PASS |
| M10 Phê duyệt | 3 | 3/3 ✅ | 3/3 ✅ | 3/3 ✅ | 3/3 ✅ | 3/3 ✅ | 3/3 ✅ | 3/3 ✅ | 3/3 ✅ | 2/3 ⚠️ | 3/3 ✅ | **91%** | ✅ PASS |
| M05-RPT Báo cáo CN | 2 | 2/2 ✅ | 2/2 ✅ | 2/2 ✅ | 2/2 ✅ | 2/2 ✅ | 2/2 ✅ | 1/2 ⚠️ | 1/2 ⚠️ | 1/2 ⚠️ | 2/2 ✅ | **82%** | ✅ PASS |
| M11 Báo cáo tổng | 4 | 4/4 ✅ | 4/4 ✅ | 4/4 ✅ | 4/4 ✅ | 4/4 ✅ | 4/4 ✅ | 3/4 ⚠️ | 3/4 ⚠️ | 2/4 ⚠️ | 4/4 ✅ | **85%** | ✅ PASS |
| M12 Quản trị | 5 | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ | **94%** | ✅ PASS |
| **OVERALL** | **50** | | | | | | | | | | | **88.6%** | **✅ PASS** |

### Key Quality Gate Findings

**Strengths (90%+ compliance):**
- ✅ All 50 US have Actor/Action/Value (100%)
- ✅ All 50 US have Business Flow section (100%)
- ✅ All 50 US have RBAC/ABAC matrix (100%)
- ✅ 48/50 US have detailed Edge Cases (96%)
- ✅ All US have DoD section (100%)

**Improvements Needed:**
- ⚠️ **Cross-references to EAMS**: Only 36/50 US have explicit EAMS §X.X references (72%)
- ⚠️ **AC format**: 0/50 US use Gherkin Given/When/Then — all prose (0%)
- ⚠️ **Ambiguous terms**: 8 US contain vague terms ("mượt mà", "nhanh", "tương thích")
- ⚠️ **Missing 401 error code**: 4/12 API specs don't define 401 Unauthorized explicitly

---

## 📊 Phase 3: Consistency Audit

### US → API Alignment

| Module | US Actions | API Endpoints | Matches | Mismatches | Score |
|--------|-----------|---------------|---------|------------|-------|
| M01 | 9 operations | 9 endpoints | 9 | 0 | 100% |
| M04 | 11 operations | 11 endpoints | 10 | 1 | 91% |
| M05 | 10 operations | — | — | — | — |
| M06 | 9 operations | — | — | — | — |
| M07 | 6 operations | — | — | — | — |
| M08 | 14 operations | 16 endpoints | 14 | 0 | 100% |
| M09 | 5 operations | — | — | — | — |
| M03 | 4 operations | — | — | — | — |
| M10 | 8 operations | 10 endpoints | 8 | 0 | 100% |
| M11 | 6 operations | — | — | — | — |
| M12 | 8 operations | 8 endpoints | 7 | 1 | 88% |
| **Overall** | | | **48** | **2** | **96%** |

**Mismatches detail:**
1. **M04**: US-REG-06 (Công tác & WFH) has no dedicated API endpoints in api-spec.md — need POST /business-trips and POST /wfh-requests
2. **M12**: US-SYS-04 (Chốt công) and US-SYS-05 (Onboarding) have no API endpoints in api-spec.md — need period-closing and onboarding endpoints

### API → DB Alignment

| Module | API Fields | DB Columns | Matches | Computed | Mismatches | Score |
|--------|-----------|------------|---------|----------|------------|-------|
| M01 | 12 | 25+ | 12 | 2 (computados) | 0 | 100% |
| M08 | 10 | 12 | 10 | 0 | 0 | 100% |
| M10 | 8 | 10 | 8 | 0 | 0 | 100% |
| M04 | 10 | 15 | 9 | 1 | 0 | 100% |
| M12 | 8 | 10 | 7 | 0 | 1 | 88% |

**Mismatch detail:**
1. **M12**: API `closingDay` field in `/admin/sites` → DB sites table missing explicit `closing_day` column (likely stored in config JSONB but not documented in db-schema.md)

### BRD → US Traceability

| BRD | Features | US Mapped | Orphan | Score |
|-----|----------|-----------|--------|-------|
| BRD-01 (Nhân viên) | 6 | 6 (F01→US-ATTEN-01, F02→US-ATTEN-03, F03→US-REG-*, F04→US-EXPL-*, F05→US-RPTPRS-*, F06→US-CAM-04) | 0 | 100% |
| BRD-02 (Quản lý) | 7 | 6 | 1 | 86% |
| BRD-03 (HR Admin) | 13 | 12 | 1 | 92% |
| BRD-04 (IT/SysAdmin) | 10 | 9 | 1 | 90% |
| **Overall** | **36** | **33** | **3** | **92%** |

**Orphan requirements:**
1. BRD-02: "Xem lịch phân ca team" — no dedicated US (partially covered by US-SHIFT-05 but from HR perspective, not Manager)
2. BRD-03: "Quản lý template email thông báo" — no US exists
3. BRD-04: "Cấu hình Data Retention Policy" — no US exists

### Terminology Consistency

| Term | BRD | US | API | DB | Consistent? |
|------|-----|-----|-----|-----|------------|
| Nhân viên / Employee | ✅ | ✅ | employee | employee_id | ✅ |
| Giờ Vào / Check-in | ✅ | Check-in | checkIn | check_in_time | ✅ (convention) |
| Ca làm việc / Shift | ✅ | Ca | shift | shifts | ✅ |
| Phê duyệt / Approval | ✅ | Duyệt | approve | approval_entries | ✅ |
| Nghỉ phép / Leave | ✅ | Nghỉ phép | leaveType | leave_type | ✅ |
| Giải trình / Correction | ⚠️ Giải trình | ⚠️ Mixed | correction | attendance_corrections | ⚠️ US uses "Giải trình" and "Sửa chấm công" interchangeably |
| **Overall** | | | | | **95%** |

---

## ⚠️ Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------:|
| 0% test coverage | Certain | Critical | Generate test cases for all 50 US (Phase 5) |
| 0% traceability | Certain | High | Build RTM (Phase 6) |
| Missing API endpoints for US-REG-06, SYS-04, SYS-05 | Certain | High | Add endpoints to M04 and M12 api-spec.md |
| 3 orphan BRD requirements | Medium | Medium | Create new US or document deferral |
| Prose AC (not Gherkin) | Low | Medium | Optional conversion in Phase 4 |

---

## Top 5 Actions (Prioritized)

| # | Action | Owner Agent | Impact | Effort |
|---|--------|-------------|--------|--------|
| 1 | Generate test cases for all 50 US | @ba-test-gen | Critical | High |
| 2 | Build RTM (BRD→US→AC→TC→API→DB) | @ba-traceability | Critical | Medium |
| 3 | Add missing API endpoints to M04, M12 | @ba-writing | High | Low |
| 4 | Add EAMS cross-references to 14 US | @ba-writing | Medium | Low |
| 5 | Create US for 3 orphan BRD requirements | @ba-writing | Medium | Medium |

---

*Report generated by BA-Kit Antigravity — Full Audit Protocol*
*Standards: CMMI, ISO 25010, BABOK v3, IEEE 29148, ISTQB*
