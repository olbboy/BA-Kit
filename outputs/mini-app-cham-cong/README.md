# Mini App Chấm Công — EAMS (Enterprise Attendance Management System)

**Phiên bản:** 2.0 | **Cập nhật:** 2026-03-17 | **Trạng thái:** Production Ready

---

## 📖 Giới thiệu

EAMS là hệ thống quản lý chấm công doanh nghiệp quy mô lớn, tích hợp C-Vision Face Recognition. Hệ thống phục vụ 5,000+ nhân viên đồng thời trên nhiều chi nhánh, tuân thủ Luật Lao động Việt Nam & Nghị định 13/2023/NĐ-CP.

## 📂 Cấu trúc tài liệu

Dự án có **2 lớp tài liệu** bổ trợ nhau:

### Lớp 1: Kiến trúc nghiệp vụ toàn diện
| Tài liệu | Mô tả | Đối tượng |
|-----------|-------|-----------|
| [EAMS v2.0 — Tài liệu nghiệp vụ toàn diện](./eams-v2-comprehensive.md) | Kiến trúc hệ thống, công thức tính giờ, luồng phê duyệt, tích hợp C-Vision, tuân thủ pháp luật VN, ma trận quyền hạn | Dev Team, Architect, Tech Lead |

### Lớp 2: BRD & User Stories (Confluence Specs)
| Section | Mô tả | Số US | Sprint |
|---------|-------|-------|--------|
| [2.11 Mini App — BRD Tổng](./overview/modules-overview.md) | Overview 11 modules, mục tiêu, danh sách tính năng | — | — |
| [2.11.1. Chấm công & Nhật ký](./phase-03-van-hanh/m01-cham-cong/) | Dashboard, tiến độ, nhật ký, cảnh báo vi phạm | 4 | Sprint 8 |
| [2.11.2. Cấu hình ca làm việc](./phase-01-thiet-lap/m06-ca-lam-viec/) | Danh sách ca, giờ/ngày, punch limit, nghỉ, import NV | 5 | Sprint 8 |
| [2.11.3. Giải trình công](./phase-04-xu-ly/m03-giai-trinh/) | Danh sách lỗi, form giải trình, minh chứng, deadline chốt công | 1 | Sprint 9 |
| [2.11.7. Cấu hình lịch nghỉ](./phase-01-thiet-lap/m07-lich-nghi/) | Ngày nghỉ, policy/rules, batch sync, API hiển thị | 4 | Sprint 8 |
| [Tài liệu dự án](./overview/) | BRD HR Admin, BRD Nhân viên, Demo Plan Sprint 8, UAT Scenarios | — | — |

### Cây trang đầy đủ
→ Xem [INDEX.md](./INDEX.md) để duyệt toàn bộ cây trang Confluence.

---

## 📋 Module Registry

| # | Module | EAMS v2.0 | Confluence | Status |
|---|--------|-----------|------------|--------|
| 01 | Chấm công & Nhật ký | §3 | [2.11.1](./phase-03-van-hanh/m01-cham-cong/) (4 US) | ✅ Đầy đủ |
| 02 | Trung tâm Đăng ký (Nghỉ/Đổi ca/OT) | §5, §6 | [2.11.4](./phase-04-xu-ly/m04-trung-tam-dang-ky/) (4 US) | ✅ Đầy đủ |
| 03 | Giải trình công | §3.3 | [2.11.3](./phase-04-xu-ly/m03-giai-trinh/) (1 US) | ✅ Đầy đủ |
| 04 | Báo cáo cá nhân | §9.1 | [2.11.5](./phase-05-ket-thuc/m05-bao-cao-ca-nhan/) (2 US) | ✅ Đầy đủ |
| 05 | Quản lý NV & CCTC | §2 | [2.11.6](./phase-01-thiet-lap/m05-quan-ly-nhan-su/) (6 US) | ✅ Đầy đủ |
| 06 | Ca làm việc & Phân ca | §4 | [2.11.2](./phase-01-thiet-lap/m06-ca-lam-viec/) (5 US) | ✅ Đầy đủ |
| 07 | Cấu hình Lịch & Ngày nghỉ | §10.2 | [2.11.7](./phase-01-thiet-lap/m07-lich-nghi/) (4 US) | ✅ Đầy đủ |
| 08 | Cấu hình Camera AI | §8 | [2.11.8](./phase-02-dinh-danh/m08-camera-ai/) (3 US) | ✅ Đầy đủ |
| 09 | Cấu hình Thông báo | — | [2.11.9](./phase-01-thiet-lap/m09-thong-bao/) (3 US) | ✅ Đầy đủ |
| 10 | Trung tâm Phê duyệt | §7 | [2.11.10](./phase-04-xu-ly/m10-phe-duyet/) (3 US) | ✅ Đầy đủ |
| 11 | Báo cáo tổng & Xuất | §9.2-9.3 | [2.11.11](./phase-05-ket-thuc/m11-bao-cao-tong/) (3 US) | ✅ Đầy đủ |

---

## 📖 Glossary — Ánh xạ thuật ngữ

Mapping giữa thuật ngữ Confluence (UI Specs) và EAMS v2.0 (Architecture):

| Confluence Term | EAMS v2.0 Term | Ghi chú |
|-----------------|---------------|---------|
| HR | `SITE_HR_ADMIN` hoặc `GLOBAL_HR_ADMIN` | EAMS phân biệt HR chi nhánh vs. HR tổng |
| Quản lý | `MANAGER` hoặc `DEPT_HEAD` | EAMS phân biệt quản lý trực tiếp vs. trưởng phòng |
| Admin | `SYSTEM_ADMIN` | EAMS có thêm `SUPER_ADMIN` (toàn quyền) |
| Nhân viên | `EMPLOYEE` | Tương đương |
| Ban Giám đốc / Ban Lãnh đạo | `SITE_MANAGER` | Quản lý cấp chi nhánh |
| Ca làm việc | `Shift` (type: FIXED / FLEXIBLE / ROTATING / SPLIT / FREE) | Confluence chỉ mô tả FIXED + Night |
| Punch Limit | `earlyCheckInMinutes` / `lateCheckOutMinutes` | Tên khác nhau, logic tương đương |
| Giải trình công | `AttendanceCorrection` (type: ADD / MODIFY / DELETE) | EAMS có 3 loại, Confluence gộp chung |
| Nghỉ phép | `LeaveRequest` (8 loại: ANNUAL, SICK, MATERNITY, ...) | Confluence chỉ nêu phép/ko lương |
| Ngày chốt công | Không có thuật ngữ tương ứng | Chỉ có ở Confluence (business rule quan trọng) |
| Grace Period | `gracePeriodMinutes` (mặc định: 15 phút) | ⚠️ Confluence không đề cập — cần bổ sung |
| Đi muộn | `LATE` (lateMins = CheckIn - ShiftStart - GracePeriod) | EAMS trừ grace period, Confluence không |
| Real-time | Webhook → BullMQ Queue → Processor | Latency: < 60s (SLA ở Confluence 2.11.1) |

---

## 👥 Stakeholders

| Vai trò | Tên | Trách nhiệm |
|---------|-----|-------------|
| Document Owner | ndthuy1 / BA Team | Viết và duy trì BRD + User Stories |
| Product Owner | — | Phê duyệt scope và ưu tiên |
| Dev Lead | — | Thực thi theo EAMS v2.0 + User Stories |
| QA Lead | — | Kiểm thử theo Acceptance Criteria + UAT |

---

## Open Questions (Cần PO/Stakeholder quyết định)

| # | Câu hỏi | Module | Impact |
|---|---------|--------|--------|
| OQ-1 | **Grace Period và Ca Đêm:** Grace period tính tại thời điểm bắt đầu ca (20:00) hay bắt đầu ngày mới (00:00)? | 01, 02 | Tính trễ sai cho NV ca đêm |
| OQ-2 | **Multi-tenant holiday:** Mỗi tenant có lịch nghỉ riêng hay dùng chung lịch quốc gia? | 07 | Ảnh hưởng thiết kế DB + UI |
| OQ-3 | **OT ca đêm surcharge:** OT từ 22:00-06:00 có tính thêm hệ số ca đêm (night shift premium) ngoài hệ số OT không? | 04, 11 | Tính lương sai |
| OQ-4 | **WFH tracking:** NV đăng ký WFH nhưng không có mốc chấm công. Coi như "Có mặt" hay "WFH — không kiểm chứng"? | 06, 07 | Ảnh hưởng báo cáo chuyên cần |
| OQ-5 | **Payroll template:** MISA, SAP, Oracle HCM yêu cầu format khác nhau. Cần configurable template hay cố định 13 cột? | 11 | Scope phát triển export |
