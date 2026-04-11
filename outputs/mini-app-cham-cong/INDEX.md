# Mini App Chấm Công — EAMS

*Updated: 2026-04-11 | 12 modules · 5 phases · 53 US · 12 API specs · 12 DB schemas · 12 test suites · 1 RTM*

## Cấu trúc dự án

- [README — Tổng quan dự án](./README.md)
- [EAMS v2.0 — Tài liệu nghiệp vụ toàn diện](./eams-v2-comprehensive.md)
- [📊 AUDIT-REPORT — Báo cáo sức khỏe dự án](./AUDIT-REPORT.md)
- [🔗 RTM — Ma trận truy vết yêu cầu (482 TCs)](./RTM.md)

### Tổng quan

- [Tổng quan 12 modules](./overview/modules-overview.md)
- [BRD-01 Nhân viên](./overview/BRD-01-Nhân-viên.md) — 6 chức năng ESS (EMPLOYEE)
- [BRD-02 Quản lý](./overview/BRD-02-Quản-lý.md) — 7 chức năng (MANAGER, DEPT_HEAD)
- [BRD-03 HR Admin](./overview/BRD-03-HR-Admin.md) — 13 chức năng quản trị (SITE_HR, GLOBAL_HR)
- [BRD-04 IT & System Admin](./overview/BRD-04-IT-và-System-Admin.md) — 10 chức năng kỹ thuật (IT_ADMIN, SYS_ADMIN)
- [Demo Plan Sprint 8](./overview/Demo-Plan-Sprint-8.md)
- [UAT Scenarios](./overview/UAT-SCENARIOS.md)

---

### Phase 01: Thiết lập hệ thống — Sprint 8

- [Plan](./phase-01-thiet-lap/plan.md) — Roadmap + Dependency DAG
- **m05 Quản lý Nhân sự** — [BRD](./phase-01-thiet-lap/m05-quan-ly-nhan-su/README.md) · [API](./phase-01-thiet-lap/m05-quan-ly-nhan-su/api-spec.md) · [DB](./phase-01-thiet-lap/m05-quan-ly-nhan-su/db-schema.md)
  - [US-EMP-01](./phase-01-thiet-lap/m05-quan-ly-nhan-su/US-EMP-01-Sơ-đồ-cơ-cấu-tổ-chức.md) · [US-EMP-02](./phase-01-thiet-lap/m05-quan-ly-nhan-su/US-EMP-02-Quản-lý-phòng-ban.md) · [US-EMP-03](./phase-01-thiet-lap/m05-quan-ly-nhan-su/US-EMP-03-Danh-sách-nhân-sự.md) · [US-EMP-04](./phase-01-thiet-lap/m05-quan-ly-nhan-su/US-EMP-04-Bulk-import-nhân-viên.md) · [US-EMP-05](./phase-01-thiet-lap/m05-quan-ly-nhan-su/US-EMP-05-Dashboard-hiện-diện.md) · [US-EMP-06](./phase-01-thiet-lap/m05-quan-ly-nhan-su/US-EMP-06-Danh-mục-cấp-bậc.md)
- **m06 Ca làm việc** — [BRD](./phase-01-thiet-lap/m06-ca-lam-viec/README.md) · [API](./phase-01-thiet-lap/m06-ca-lam-viec/api-spec.md) · [DB](./phase-01-thiet-lap/m06-ca-lam-viec/db-schema.md)
  - [US-SHIFT-01](./phase-01-thiet-lap/m06-ca-lam-viec/US-SHIFT-01-Danh-sách-ca-làm-việc.md) · [US-SHIFT-02](./phase-01-thiet-lap/m06-ca-lam-viec/US-SHIFT-02-Cấu-hình-giờ-và-ngày-làm-việc.md) · [US-SHIFT-03](./phase-01-thiet-lap/m06-ca-lam-viec/US-SHIFT-03-Giới-hạn-thời-gian-chấm-công-(punch-limit).md) · [US-SHIFT-04](./phase-01-thiet-lap/m06-ca-lam-viec/US-SHIFT-04-Cấu-hình-giờ-nghỉ.md) · [US-SHIFT-05](./phase-01-thiet-lap/m06-ca-lam-viec/US-SHIFT-05-Import-nhân-viên-vào-ca.md) · [US-SHIFT-06](./phase-01-thiet-lap/m06-ca-lam-viec/US-SHIFT-06-Phân-ca-theo-pattern.md) · [US-SHIFT-07](./phase-01-thiet-lap/m06-ca-lam-viec/US-SHIFT-07-Xem-lịch-phân-ca-team.md)
- **m07 Lịch nghỉ** — [BRD](./phase-01-thiet-lap/m07-lich-nghi/README.md) · [API](./phase-01-thiet-lap/m07-lich-nghi/api-spec.md) · [DB](./phase-01-thiet-lap/m07-lich-nghi/db-schema.md)
  - [US-HOL-01](./phase-01-thiet-lap/m07-lich-nghi/US-HOL-01-Quản-lý-danh-sách-ngày-nghỉ.md) · [US-HOL-02](./phase-01-thiet-lap/m07-lich-nghi/US-HOL-02-Cấu-hình-policy-nghỉ-và-rule-nghỉ.md) · [US-HOL-03](./phase-01-thiet-lap/m07-lich-nghi/US-HOL-03-Logic-sync-&-batch-job.md) · [US-HOL-04](./phase-01-thiet-lap/m07-lich-nghi/US-HOL-04-API-hiển-thị.md)
- **m09 Thông báo** — [BRD](./phase-01-thiet-lap/m09-thong-bao/README.md) · [API](./phase-01-thiet-lap/m09-thong-bao/api-spec.md) · [DB](./phase-01-thiet-lap/m09-thong-bao/db-schema.md)
  - [US-NOTIF-01](./phase-01-thiet-lap/m09-thong-bao/US-NOTIF-01-Cấu-hình-kênh-thông-báo.md) · [US-NOTIF-02](./phase-01-thiet-lap/m09-thong-bao/US-NOTIF-02-Cấu-hình-sự-kiện-kích-hoạt.md) · [US-NOTIF-03](./phase-01-thiet-lap/m09-thong-bao/US-NOTIF-03-Quản-lý-policy-thông-báo.md) · [US-NOTIF-04](./phase-01-thiet-lap/m09-thong-bao/US-NOTIF-04-Quản-lý-template-email.md)

### Phase 02: Định danh Camera AI — Sprint 8

- [Plan](./phase-02-dinh-danh/plan.md)
- **m08 Camera AI** — [BRD](./phase-02-dinh-danh/m08-camera-ai/README.md) · [API](./phase-02-dinh-danh/m08-camera-ai/api-spec.md) · [DB](./phase-02-dinh-danh/m08-camera-ai/db-schema.md)
  - [US-CAM-01](./phase-02-dinh-danh/m08-camera-ai/US-CAM-01-Quản-lý-danh-sách-thiết-bị.md) · [US-CAM-02](./phase-02-dinh-danh/m08-camera-ai/US-CAM-02-Mapping-nhân-viên.md) · [US-CAM-03](./phase-02-dinh-danh/m08-camera-ai/US-CAM-03-Health-check-và-monitoring.md) · [US-CAM-04](./phase-02-dinh-danh/m08-camera-ai/US-CAM-04-Đăng-ký-khuôn-mặt-nhân-viên.md)

### Phase 03: Vận hành chấm công — Sprint 8

- [Plan](./phase-03-van-hanh/plan.md)
- **m01 Chấm công** — [BRD](./phase-03-van-hanh/m01-cham-cong/README.md) · [API](./phase-03-van-hanh/m01-cham-cong/api-spec.md) · [DB](./phase-03-van-hanh/m01-cham-cong/db-schema.md)
  - [US-ATTEN-01](./phase-03-van-hanh/m01-cham-cong/US-ATTEN-01-Hub-chấm-công.md) · [US-ATTEN-02](./phase-03-van-hanh/m01-cham-cong/US-ATTEN-02-Thống-kê-hiệu-suất-tháng.md) · [US-ATTEN-03](./phase-03-van-hanh/m01-cham-cong/US-ATTEN-03-Xem-chi-tiết-nhật-ký-chấm-công.md) · [US-ATTEN-04](./phase-03-van-hanh/m01-cham-cong/US-ATTEN-04-Trung-tâm-cảnh-báo-và-thông-báo.md) · [US-ATTEN-05](./phase-03-van-hanh/m01-cham-cong/US-ATTEN-05-Nhập-chấm-công-thủ-công.md)

### Phase 04: Xử lý đơn từ — Sprint 9

- [Plan](./phase-04-xu-ly/plan.md)
- **m04 Trung tâm Đăng ký** — [BRD](./phase-04-xu-ly/m04-trung-tam-dang-ky/README.md) · [API](./phase-04-xu-ly/m04-trung-tam-dang-ky/api-spec.md) · [DB](./phase-04-xu-ly/m04-trung-tam-dang-ky/db-schema.md)
  - [US-REG-01](./phase-04-xu-ly/m04-trung-tam-dang-ky/US-REG-01-Đăng-ký-nghỉ-phép.md) · [US-REG-02](./phase-04-xu-ly/m04-trung-tam-dang-ky/US-REG-02-Đăng-ký-đổi-ca.md) · [US-REG-03](./phase-04-xu-ly/m04-trung-tam-dang-ky/US-REG-03-Đăng-ký-tăng-ca.md) · [US-REG-04](./phase-04-xu-ly/m04-trung-tam-dang-ky/US-REG-04-Theo-dõi-đơn-từ-và-hạn-mức.md) · [US-REG-05](./phase-04-xu-ly/m04-trung-tam-dang-ky/US-REG-05-Cấu-hình-chính-sách-phép-năm.md) · [US-REG-06](./phase-04-xu-ly/m04-trung-tam-dang-ky/US-REG-06-Đăng-ký-công-tác-và-WFH.md)
- **m03 Giải trình** — [BRD](./phase-04-xu-ly/m03-giai-trinh/README.md) · [API](./phase-04-xu-ly/m03-giai-trinh/api-spec.md) · [DB](./phase-04-xu-ly/m03-giai-trinh/db-schema.md)
  - [US-EXPL-01](./phase-04-xu-ly/m03-giai-trinh/US-EXPL-01-Danh-sách-lỗi-cần-giải-trình.md) · [US-EXPL-02](./phase-04-xu-ly/m03-giai-trinh/US-EXPL-02-Yêu-cầu-sửa-chấm-công.md)
- **m10 Phê duyệt** — [BRD](./phase-04-xu-ly/m10-phe-duyet/README.md) · [API](./phase-04-xu-ly/m10-phe-duyet/api-spec.md) · [DB](./phase-04-xu-ly/m10-phe-duyet/db-schema.md)
  - [US-APPR-01](./phase-04-xu-ly/m10-phe-duyet/US-APPR-01-Inbox-phê-duyệt.md) · [US-APPR-02](./phase-04-xu-ly/m10-phe-duyet/US-APPR-02-Cấu-hình-chuỗi-phê-duyệt.md) · [US-APPR-03](./phase-04-xu-ly/m10-phe-duyet/US-APPR-03-Phê-duyệt-hàng-loạt.md)

### Phase 05: Báo cáo & Hoàn thiện — Sprint 10

- [Plan](./phase-05-ket-thuc/plan.md)
- **m05 Báo cáo cá nhân** — [BRD](./phase-05-ket-thuc/m05-bao-cao-ca-nhan/README.md) · [API](./phase-05-ket-thuc/m05-bao-cao-ca-nhan/api-spec.md) · [DB](./phase-05-ket-thuc/m05-bao-cao-ca-nhan/db-schema.md)
  - [US-RPTPRS-01](./phase-05-ket-thuc/m05-bao-cao-ca-nhan/US-RPTPRS-01-Dashboard-hiệu-suất-cá-nhân.md) · [US-RPTPRS-02](./phase-05-ket-thuc/m05-bao-cao-ca-nhan/US-RPTPRS-02-Bảng-KPI-và-highlights.md)
- **m11 Báo cáo tổng** — [BRD](./phase-05-ket-thuc/m11-bao-cao-tong/README.md) · [API](./phase-05-ket-thuc/m11-bao-cao-tong/api-spec.md) · [DB](./phase-05-ket-thuc/m11-bao-cao-tong/db-schema.md)
  - [US-RPT-01](./phase-05-ket-thuc/m11-bao-cao-tong/US-RPT-01-Dashboard-quản-lý.md) · [US-RPT-02](./phase-05-ket-thuc/m11-bao-cao-tong/US-RPT-02-Xuất-báo-cáo-và-payroll.md) · [US-RPT-03](./phase-05-ket-thuc/m11-bao-cao-tong/US-RPT-03-Báo-cáo-tuân-thủ.md) · [US-RPT-04](./phase-05-ket-thuc/m11-bao-cao-tong/US-RPT-04-Khóa-kỳ-lương.md)

### Cross-cutting — Sprint 8-10

- [Plan](./cross-cutting/plan.md)
- **m12 Quản trị hệ thống** — [BRD](./cross-cutting/m12-quan-tri-he-thong/README.md) · [API](./cross-cutting/m12-quan-tri-he-thong/api-spec.md) · [DB](./cross-cutting/m12-quan-tri-he-thong/db-schema.md)
  - [US-SYS-01](./cross-cutting/m12-quan-tri-he-thong/US-SYS-01-Quản-lý-chi-nhánh.md) · [US-SYS-02](./cross-cutting/m12-quan-tri-he-thong/US-SYS-02-Audit-log-viewer.md) · [US-SYS-03](./cross-cutting/m12-quan-tri-he-thong/US-SYS-03-Employee-offboarding.md) · [US-SYS-04](./cross-cutting/m12-quan-tri-he-thong/US-SYS-04-Chốt-công-tháng.md) · [US-SYS-05](./cross-cutting/m12-quan-tri-he-thong/US-SYS-05-Employee-onboarding.md) · [US-SYS-06](./cross-cutting/m12-quan-tri-he-thong/US-SYS-06-Cấu-hình-data-retention-policy.md)

