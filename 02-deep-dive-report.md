# 🏗️ Phase 3 — DEEP-DIVE (Nhóm, 85 min)
## 3.1. Current-State Workflow Mapping (25 min)
Quy trình xử lý phản ánh cư dân hiện tại của nhân viên Ban quản lý Vinhomes:

┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Bước 1       │     │ Bước 2       │     │ Bước 3       │     │ Bước 4       │
│ Nhận phản    │     │ Đọc nội dung │     │ Phân loại    │     │ Chuyển ticket│
│ ánh từ App   │ ──→ │ phản ánh     │ ──→ │ vấn đề và    │ ──→ │ đến bộ phận  │
│ Vinhomes     │     │              │     │ xác định bộ  │     │ phụ trách     │
│              │     │              │     │ phận xử lý   │     │              │
│ Ai: BQL      │     │ Ai: BQL      │     │ Ai: BQL      │     │ Ai: BQL      │
│ Thời gian:   │     │ Thời gian:   │     │ Thời gian:   │     │ Thời gian:   │
│ 0.5 phút     │     │ 1 phút       │     │ 1.5 phút     │     │ 0.5 phút     │
│              │     │              │     │              │     │              │
│ In: Phản ánh │     │ In: Nội dung │     │ In: Nội dung │     │ In: Ticket + │
│ Out: Ticket  │     │ Out: Vấn đề  │     │ Out: Category│     │ bộ phận      │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘

Handoff:
App Vinhomes → Ban quản lý
Ban quản lý → Bộ phận xử lý

Bottleneck:
Bước 2 và Bước 3

Tổng thời gian xử lý thủ công: 3.5 phút/ticket.

## 3.2. Problem Statement (6-field) & Metrics (15 min)
Điền đầy đủ 6 trường thông tin của bài toán:

| **Field** | **Nội dung** |
|---|---|
| **1. Actor / Operator** | Nhân viên Ban quản lý (BQL) Vinhomes phụ trách tiếp nhận và phân loại phản ánh cư dân. |
| **2. Current Workflow** | Cư dân gửi phản ánh qua App Vinhomes. Nhân viên BQL đọc nội dung, xác định vấn đề, phân loại phản ánh và chuyển ticket đến đúng bộ phận phụ trách. Quy trình gồm 4 bước, thực hiện thủ công và mất khoảng 3.5 phút/ticket. |
| **3. Bottleneck** | Bước 2 & 3: Đọc và hiểu nội dung phản ánh, sau đó xác định loại vấn đề và bộ phận xử lý phù hợp. Đặc biệt mất thời gian với phản ánh dài, diễn đạt không rõ hoặc chứa nhiều vấn đề. |
| **4. Business Impact** | Với khoảng 10.000 phản ánh/tháng, thời gian phân loại thủ công tương đương khoảng 583 giờ làm việc/tháng. Việc phân loại sai hoặc chuyển nhầm bộ phận làm tăng thời gian xử lý và có thể ảnh hưởng SLA phản hồi cư dân. |
| **5. Success Metric** | 1. Giảm thời gian phân loại và chuyển ticket từ 3.5 phút xuống dưới 30 giây/ticket.<br>2. Đạt ít nhất 90% ticket được phân loại và chuyển đúng bộ phận ngay lần đầu.<br>3. Ít hơn 5% ticket cần nhân viên phân loại lại. |
| **6. Operational Boundary** | AI được phép đọc nội dung phản ánh, xác định loại vấn đề, mức độ ưu tiên và đề xuất bộ phận xử lý. **CẤM:** AI không được tự ý đóng ticket, từ chối phản ánh hoặc đưa ra cam kết với cư dân. Các ticket có mức độ nghiêm trọng cao hoặc AI không đủ độ tin cậy phải chuyển cho nhân viên BQL duyệt trước. |

## 3.3. Future-State Flow & AI Fit (25 min)
- **AI Fit:** Chọn **LLM Feature**. Quy trình phân loại phản ánh có cấu trúc cố định, AI chủ yếu xử lý việc hiểu ngôn ngữ tự nhiên và đề xuất category/bộ phận. Không cần Agent tự trị vì việc tự động chuyển các phản ánh quan trọng có thể gây sai routing và ảnh hưởng SLA.

- **Quy trình tương lai (Future-State):**

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Bước 1       │     │ Bước 2       │     │ Bước 3       │     │ Bước 4       │
│ Nhận phản    │     │ 🔵 AI đọc &  │     │ 🔵 AI phân   │     │ 🟢 Nhân viên  │
│ ánh từ App   │ ──→ │ hiểu nội dung│ ──→ │ loại vấn đề  │ ──→ │ review &      │
│ Vinhomes     │     │              │     │ + đề xuất    │     │ duyệt routing │
│              │     │              │     │ bộ phận       │     │               │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                       │
                                                                       ▼
                                                               ┌──────────────┐
                                                               │ Chuyển ticket│
                                                               │ đến bộ phận  │
                                                               │ phụ trách     │
                                                               └──────────────┘

↩️ Fallback:
Nếu AI không đủ tự tin, phản ánh không rõ ràng hoặc
phát hiện nhiều vấn đề → chuyển sang nhân viên BQL
phân loại thủ công như quy trình hiện tại.

# 🏁 Phase 5 — EVALUATE (Nhóm, 20 min)

### AI Readiness Checklist:

1. [x] Chúng tôi có thể sử dụng dữ liệu phản ánh mẫu và lịch sử ticket để xây dựng tập test và đánh giá độ chính xác phân loại.
2. [x] Rủi ro khi AI sai nằm trong tầm kiểm soát nhờ Human-in-the-loop và cơ chế fallback về quy trình phân loại thủ công.
3. [x] Quy trình hiện tại không thay đổi đáng kể đối với nhân viên BQL; AI chủ yếu đóng vai trò đề xuất category và bộ phận xử lý để nhân viên review.

### Quyết định cuối cùng của nhóm:

[x] **GO (Bắt đầu xây dựng Prototype):** Bắt đầu phát triển với scope hẹp.

[ ] **NOT YET (Cần tích lũy thêm dữ liệu/xác lập baseline):** Trì hoãn để chuẩn bị thêm.

[ ] **NO-GO (Không khả thi / Rule-based tốt hơn):** Hủy bỏ dự án AI này.

### Justification:

> **GO.** Bài toán có dữ liệu đầu vào tương đối rõ ràng (nội dung phản ánh và lịch sử phân loại ticket), workflow cố định và KPI có thể đo trực tiếp bằng thời gian xử lý, độ chính xác phân loại và tỷ lệ phải phân loại lại. AI có nhómgiá trị ở việc hiểu các phản ánh được diễn đạt tự nhiên, không theo một format cố định, sau đó đề xuất category và bộ phận xử lý.