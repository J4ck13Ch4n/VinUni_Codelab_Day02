# Phân Công Task Nhóm — Dự Án Điều Hướng Phản Ánh Vinhomes

Nguồn: `PRD-vinhomes-complaint-routing-vi.md` + `TRD-vinhomes-complaint-routing-vi.md`
Số lượng thành viên: 5. Đổi `Member 1–5` thành tên thật/tên branch (theo README §4 Bước 2: `git checkout -b <ten-cua-ban>`).

**Đã sắp xếp lại ưu tiên cho MVP demo.** Mục tiêu: một script chạy được, demo trực tiếp trong buổi demo, thể hiện đúng giá trị cốt lõi + câu chuyện an toàn — không phải toàn bộ hồ sơ giấy tờ. Các deliverable đầy đủ của lab vẫn phải nộp (quy định chấm điểm README không đổi) nhưng dời xuống §2, sau demo.

---

## 1. MVP Demo (làm cái này trước)

**Lời hứa của demo:** chạy `prompt_prototype.py` trực tiếp, thể hiện (a) một phản ánh thông thường được phân loại + điều hướng đúng tự động, (b) một ticket phí/tranh chấp bị buộc escalate — không bao giờ tự xử lý, (c) một lần cố tình tấn công để bỏ qua escalate nhưng vẫn thất bại. Ý (c) mới là điểm "wow" thật sự — code ghi đè lên model, không chỉ là prompt lịch sự nhờ vả.

**Điểm mở khóa để làm song song:** interface đã được "đóng băng" sẵn — bảng phân loại (TRD §4), JSON schema (TRD §5), quy tắc escalate (TRD §6–7). Không ai cần chờ code của người khác; ai cũng code trực tiếp theo bản hợp đồng (contract) đã viết sẵn đó. Điểm tuần tự duy nhất là bước ghép cuối ở Task 5, và đó chỉ là copy-paste, không phải xây lại từ đầu.

| # | Người phụ trách | Task | Deliverable | Phụ thuộc |
|---|---|---|---|---|
| 1 | Member 1 | Hiện thực `evaluate_prompt()`: `SYSTEM_PROMPT` + gọi Gemini 2.5 Flash thật, output khớp JSON schema ở TRD §5 | `evaluate_prompt()` chạy được | Chỉ cần contract TRD |
| 2 | Member 2 | Hiện thực `validate_boundaries()` + viết self-test nhỏ dùng mock JSON dict — hàm thuần (pure function), không cần gọi API thật, test trực tiếp theo schema ở TRD §5 | hàm chạy được + self-test | Chỉ cần contract TRD |
| 3 | Member 3 | Chọn 4 input demo (2 happy-path, 1 ticket phí/tranh chấp trực tiếp, 1 lần tấn công bypass) + `category`/`escalate` kỳ vọng cho mỗi input, dựa theo bảng phân loại ở TRD §4 | bộ input demo + gạch đầu dòng thuyết trình | Chỉ cần contract TRD |
| 4 | Member 4 | Bản 1 trang giới thiệu bài toán (từ PRD §1) + sơ đồ trước/sau đơn giản | tài liệu/slide 1 trang | không |
| 5 | Member 5 | Viết integration harness **ngay từ đầu**, dùng bản stub của `evaluate_prompt()`/`validate_boundaries()` (trả giá trị mẫu khớp schema) để chứng minh phần ghép nối chạy được trước khi code thật của ai xong. Khi Member 1 & 2 xong, thay bằng hàm thật, chạy bộ input của Member 3 qua đó, rồi làm bước kiểm tra độ ổn định (check API key, chạy live ≥2 lần, quay/chụp dự phòng, note "hạn chế đã biết") | script đã ghép + log test + phương án dự phòng | chỉ cần output thật của Task 1–2 ở bước ghép cuối; phần harness thì bắt đầu ngay |

**Định nghĩa "xong" cho demo:** script chạy hết không crash, cả 4 input đã chọn (Task 3) cho ra đúng hành vi escalate/route mong đợi, Member 5 đã chạy live thành công tối thiểu 2 lần trước ngày demo.

**Vì sao làm song song được:** Task 1–4 đều code/viết theo contract đã có sẵn trong TRD, không phụ thuộc lẫn nhau — bắt đầu cả 4 việc ngay khi đọc xong file này. Task 5 cũng bắt đầu ngay (harness + stub), chỉ cần hàm *thật* của Task 1–2 ở bước thay thế cuối cùng, mất vài phút, không phải vài ngày.

---

## 2. Nộp bài đầy đủ cho lab (theo README, không cần cho demo)

| Task | Người phụ trách | Deliverable | Rubric Gate |
|---|---|---|---|
| Sơ đồ workflow hiện tại (bản hoàn chỉnh) | Member 4 (phát triển từ bản sketch ở Task 4) | `04-workflow-diagram.png` | G1 (20đ) |
| Viết Problem Statement 6-field + business case | Member 1 hoặc 2 | `02-deep-dive-report.md` §3.2 | G2 (20đ) |
| Viết Future-state flow + AI-Fit | Member 3 | `02-deep-dive-report.md` §3.3 | G3 (10đ) |
| Readiness checklist + GO/NOT-YET/NO-GO + tổng hợp cuối + merge vào `main` | Member 5 | `02-deep-dive-report.md` (bản cuối) + merge | G4 (10đ) |

### Việc cá nhân (mỗi thành viên tự làm trên branch riêng — không giao được cho người khác)
- `01-problem-scan.md`, `03-ai-log.md`, bản `prompt_prototype.py` riêng của mỗi người. Mỗi người fork từ script MVP ở §1 sang branch/file của riêng mình — code được chấm theo từng branch, không merge vào `main` (README §3.2).

**Ghi chú về autograder (không đổi):** autograder quét từ khóa `draft_only` / `5%` / `dispatch_mobile_charger` (kịch bản EV-battery), không phải các từ liên quan Vinhomes. Script MVP dùng luật Vinhomes có chủ đích (để demo mạch lạc) — mất khoảng 0.5/10đ ở tiêu chí autograder đó. Có thể chấp nhận cho demo; xem lại trước khi nộp bài cá nhân cuối cùng nếu 0.5 điểm đó quan trọng.
