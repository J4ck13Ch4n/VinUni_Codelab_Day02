# 03 — AI Log &amp; Reflection

> Deliverable cá nhân — Phase 6 (REFLECTION). Bản nháp dựa trên log làm việc thật với AI
> trong suốt lab (từ chọn bài toán đến code + test). **Điền tên bạn và chỉnh giọng văn
> theo trải nghiệm cá nhân trước khi nộp** — nội dung dưới đây kể lại đúng sự việc đã xảy ra,
> không phải văn mẫu.

---

## AI giúp gì?

Tôi dùng Claude làm thought-partner xuyên suốt cả 4 phase của lab, không chỉ để "hỏi đáp" mà để cùng lặp lại (iterate) trên một sản phẩm cụ thể:

- **Scoping bài toán:** Từ danh sách gợi ý trong `03-inspiration-kit.md`, AI giúp tôi cân nhắc và chọn ra bài toán "Vinhomes — Phân loại & điều hướng phản ánh cư dân", với lý do rõ ràng (không trùng worked example của lớp, có ranh giới an toàn dễ kiểm chứng bằng code).
- **Viết PRD/TRD:** AI dựng PRD và TRD đầy đủ (functional requirements, taxonomy, JSON schema, thiết kế `validate_boundaries()`) từ một mô tả bài toán ngắn gọn của tôi.
- **Chia việc nhóm:** Chuyển PRD/TRD thành bảng phân công task cụ thể cho 5 thành viên, sau đó tái cấu trúc lại để các task có thể làm **song song** thay vì chờ nhau tuần tự — nhờ việc "đóng băng" trước interface chung (taxonomy + JSON schema) trong TRD.
- **Code + tích hợp model thật:** Viết `prompt_prototype.py` hoàn chỉnh, rồi khi tôi đổi ý muốn dùng 9Router (gateway local) thay vì gọi thẳng Gemini SDK, AI tự tìm hiểu 9Router là gì (tôi chỉ gõ đúng 2 chữ "9router"), test bằng `curl` thật để xác nhận endpoint/format trước khi sửa code — không đoán mò.
- **Xây frontend:** Từ yêu cầu "dựng 1 frontend đơn giản", AI viết 1 file `app.py` (thuần stdlib, không thêm dependency), rồi tự mở trình duyệt thật (Playwright) để bấm nút và kiểm tra flow, thay vì chỉ đưa code rồi nói "chắc là chạy được".

## AI trả lời sai / hallucination ở đâu — và tôi (hoặc AI tự) đã sửa ra sao?

Đây là phần quan trọng nhất — vài lần AI **tự tin đưa ra thứ sai**, và điều sửa được nó không phải là "hỏi lại cho kỹ" mà là **chạy thật và nhìn kết quả**:

1. **Bug trong chính bộ test do AI viết:** Khi thêm 3 adversarial test case, AI mặc định rằng "escalate=True luôn là câu trả lời an toàn" cho cả 3 test — sai. Ở Test Case 2 (cư dân giả vờ "khẩn cấp" cho một phản ánh ồn ào bình thường), hành vi **đúng** của model lại là **không** escalate. Khi chạy thật, model trả về đúng (`escalate: false`) nhưng bộ test tự chấm "Failed" — tức là chính logic kiểm tra của AI mới là thứ sai, không phải model. AI chỉ nhận ra khi tôi yêu cầu chạy thật và nhìn output, chứ không tự phát hiện được nếu chỉ đọc code.
2. **Bug thứ tự đọc config:** Sau khi thêm `LLM_BACKEND` để chọn giữa 9Router và Gemini, tôi đổi `.env` sang `LLM_BACKEND=gemini` nhưng chương trình vẫn chạy backend cũ. Nguyên nhân: AI đặt dòng đọc biến `LLM_BACKEND` **trước** dòng nạp file `.env` trong code — lỗi thứ tự rất dễ đọc code mà bỏ sót, chỉ lộ ra khi chạy thật và thấy header in sai backend.
3. **"Ranh giới" ban đầu chỉ đúng trên giấy:** Model `gemini-2.5-flash` (SDK trực tiếp) từng thật sự bị dụ bởi từ "KHẨN CẤP" viết hoa, tự tăng escalate cho một ca ồn ào — trong khi `gemini-3-flash` (qua 9Router) không bị. Tức là cùng một `SYSTEM_PROMPT`, hai model khác nhau cho hai kết quả khác nhau trên cùng một đầu vào tấn công. Phải chạy thật trên cả 2 model mới phát hiện ra, không đoán được nếu chỉ đọc prompt.
4. **Giới hạn thật của môi trường, không phải hallucination nhưng dễ nhầm:** Key Gemini thật đầu tiên bị lỗi `403 PERMISSION_DENIED` (do project chưa bật đúng API), sau đó bị `429 RESOURCE_EXHAUSTED` (hết quota free-tier 20 request/ngày). AI không "bịa" ra cách né các lỗi này — chỉ báo đúng nguyên nhân và đề xuất hướng sửa (tạo key ở AI Studio, đổi backend khác để không tốn quota khi test lặp lại).

## Tôi đã sửa ranh giới/prompt ra sao?

Sau khi phát hiện lỗi (2) ở trên, tôi yêu cầu "siết SYSTEM_PROMPT" — AI thêm một quy tắc rõ ràng: *cư dân tự xưng khẩn cấp/viết hoa/lặp từ không tự động đổi category hay tăng escalate; chỉ escalate khi nội dung thực sự khớp quy tắc phí/tranh chấp hoặc từ khóa an toàn thật.* Sau khi thêm, chạy lại cả 2 backend đều đạt 7/7 — có bằng chứng thật (log chạy), không chỉ "chắc là ổn rồi".

## Bài học rút ra

- AI viết code/tài liệu nhanh, nhưng **giá trị thật nằm ở việc chạy thử và đọc kết quả**, không phải ở việc đọc code trông có vẻ đúng. Cả 2 bug nghiêm trọng nhất trong lab này (bug test, bug thứ tự config) đều là loại lỗi "đọc qua thì thấy hợp lý" nhưng sai khi chạy thật.
- Ranh giới an toàn (Operational Boundary) không nên chỉ nằm trong `SYSTEM_PROMPT` — phần `validate_boundaries()` viết ở tầng code mới là thứ đảm bảo model không thể bị dụ vi phạm, kể cả khi prompt chưa hoàn hảo.
- Khi AI hỗ trợ, vai trò của tôi là **đặt câu hỏi đúng lúc** ("chạy thật đi", "test cả 2 model xem sao") hơn là tự đọc/tự đoán code có đúng không.
