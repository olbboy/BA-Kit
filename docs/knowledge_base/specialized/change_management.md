# Change Management — Specialized BA Knowledge

> Quản lý thay đổi: đảm bảo con người ADOPT giải pháp, không chỉ triển khai công nghệ.

## Tại sao Change Management quan trọng với BA?

Hệ thống hoạt động hoàn hảo nhưng không ai dùng = dự án thất bại. BA không chỉ thu thập requirements mà còn đảm bảo solution được adopted.

## ADKAR Model (Prosci)

Framework đánh giá và quản lý thay đổi ở cấp CÁ NHÂN:

| Element | Câu hỏi | Nếu thiếu |
|---------|---------|-----------|
| **Awareness** | Họ có BIẾT tại sao cần thay đổi? | Confusion, resistance |
| **Desire** | Họ có MUỐN thay đổi? | Passive resistance |
| **Knowledge** | Họ có BIẾT CÁCH dùng hệ thống mới? | Frustration, errors |
| **Ability** | Họ CÓ THỂ thực hiện trong thực tế? | Skill gap, workarounds |
| **Reinforcement** | Họ có TIẾP TỤC dùng sau go-live? | Revert to old ways |

**Quy tắc**: Luôn giải quyết element ĐẦU TIÊN bị điểm thấp (barrier point) trước khi chuyển sang element sau.

## Change Impact Assessment

Đánh giá trên 3 trục:

| Trục | Câu hỏi đánh giá |
|------|------------------|
| **People** | Ai bị ảnh hưởng? Công việc hàng ngày thay đổi thế nào? Bao nhiêu người? |
| **Process** | Quy trình nào thay đổi? Mới hoàn toàn hay sửa đổi? Quy trình nào bị retired? |
| **Technology** | Tool nào thay đổi? Skill mới cần học? Learning curve dài bao lâu? |

## Training Needs Analysis

1. **Xác định skill gap**: So sánh As-Is skill vs To-Be requirement
2. **Phân nhóm**: Mỗi user group có gap khác nhau
3. **Chọn format**: Phù hợp thực tế (shift workers → hands-on tại site, managers → online)
4. **Schedule**: Tính đến constraint thực tế (ca làm việc, địa điểm)
5. **Support plan**: Buddy system, hotline, FAQ sau go-live

## Go-Live Planning

### Cutover Strategy Options
| Strategy | Mô tả | Risk | Khi nào dùng |
|----------|-------|------|-------------|
| **Big Bang** | Chuyển toàn bộ cùng lúc | High | Hệ thống đơn giản, ít user |
| **Phased** | Triển khai từng module/site | Medium | Nhiều module, multi-site |
| **Parallel Run** | Chạy song song cũ + mới | Low | Mission-critical, compliance |
| **Pilot** | Thử với 1 nhóm nhỏ trước | Low | User không quen tech, cần validate |

### Go/No-Go Criteria
- [ ] UAT signed off
- [ ] Data migration validated
- [ ] Training completed ≥ 80% users
- [ ] Rollback plan tested
- [ ] Support team ready
- [ ] Communication sent to all users

## Benefits Realization

Sau go-live, theo dõi:
- **Adoption rate**: % users thực sự dùng hệ thống mới
- **Support tickets**: Volume và trend (nên giảm sau 2 tuần)
- **Process efficiency**: So sánh KPI trước/sau (thời gian xử lý, error rate)
- **User satisfaction**: Survey NPS sau 1 tháng
- **ROI thực tế**: So sánh với dự kiến từ @ba-solution

## Resistance Management

| Loại resistance | Dấu hiệu | Cách xử lý |
|----------------|-----------|-----------|
| **Awareness** | "Tại sao phải đổi?" | Town hall, communication rõ ràng |
| **Skill** | "Tôi không biết dùng" | Training, buddy system |
| **Political** | "Hệ thống này làm tôi mất quyền" | Stakeholder management 1-on-1 |
| **Habit** | "Cách cũ tốt hơn" | Quick wins, gamification |

## Post-Implementation Review (PIR)

Thực hiện 1-3 tháng sau go-live:
1. Benefits có đạt như kế hoạch?
2. Lessons learned — cái gì worked, cái gì không?
3. Outstanding issues cần xử lý?
4. Recommendations cho phase tiếp theo?

## Agents liên quan
- **@ba-change**: Agent chính cho kỹ năng này
- **@ba-identity**: Stakeholder mapping cho change impact
- **@ba-communication**: Crafting change announcements
- **@ba-facilitation**: Workshop readiness/training
- **@ba-metrics**: KPI tracking cho adoption
- **@ba-solution**: ROI comparison (planned vs actual)

## Sources
- Prosci — ADKAR Model
- Kotter — 8 Steps of Change
- BABOK v3 — Solution Evaluation Knowledge Area
