# 03 — AI Log & Reflection

**Lab 02: AI Product Scoping — Vin Smart Future**
**Bài toán:** Đề 6 — Vinhomes, phân loại và điều hướng phản ánh cư dân
**Công cụ AI đã dùng:** Claude (Anthropic) làm thought-partner, Gemini 2.5 Flash làm model của prototype

> *Ghi chú: đây là bản nhật ký cá nhân. Mỗi thành viên nên viết lại theo trải nghiệm của chính mình, vì đây là gate chấm điểm cá nhân.*

---

## 1. Tôi đã dùng AI vào việc gì

| Giai đoạn | Việc giao cho AI | Kết quả |
|---|---|---|
| Phase 1 — SCAN | Brainstorm pain point vận hành của khối Vinhomes | Có được 6 ý tưởng, nhưng chỉ 3 ý là bài toán thật, phần còn lại quá chung chung |
| Phase 2 — Quick Cards | Phản biện thẻ bài toán dưới vai CFO khó tính | Đây là phần AI hữu ích nhất, xem mục 3 |
| Phase 3 — Deep-Dive | Nháp cấu trúc bảng Problem Statement 6 trường | Khung tốt, nhưng nội dung phải viết lại gần hết |
| Phase 3 — Taxonomy | Gợi ý danh sách danh mục vé và tên bộ phận tiếp nhận | Dùng được sau khi cắt bớt, AI đề xuất 14 danh mục, nhóm rút còn 8 |
| Phase 4 — Code | Nháp cấu trúc `SYSTEM_PROMPT` và cách gọi SDK Gemini | Phần gọi SDK chính xác, phần ranh giới an toàn thì thiếu, xem mục 2 |

---

## 2. AI sai ở đâu

Đây là phần tôi học được nhiều nhất. Ghi lại ba lỗi rõ ràng nhất, theo thứ tự mức độ nguy hiểm.

### 2.1. AI viết ranh giới an toàn chỉ trong prompt rồi khẳng định như vậy là đủ

Khi tôi hỏi cách bảo đảm AI không tự ý hứa miễn phí quản lý cho cư dân, câu trả lời đầu tiên là một đoạn `SYSTEM_PROMPT` viết rất chặt, kèm câu đại ý "với chỉ thị này model sẽ không vi phạm".

Đó là câu trả lời **sai về bản chất**. Một chỉ thị trong prompt chỉ là lời khuyên đối với model. Prompt injection, cách diễn đạt lạ, hay chỉ đơn giản là đổi phiên bản model đều có thể làm nó bị bỏ qua. Nếu tin theo, sản phẩm sẽ có một ranh giới chỉ tồn tại trên giấy.

Cách tôi phát hiện: đọc kỹ mục §7 của TRD nội bộ của nhóm, trong đó viết rằng `validate_boundaries()` là "dòng quan trọng nhất của toàn prototype" vì nó biến ranh giới từ *aspirational* thành *real*. Tôi quay lại hỏi AI với câu hỏi khác hẳn: *"giả sử prompt injection đã thành công và model trả về `escalate: false` cho một vé phí quản lý, chuyện gì xảy ra tiếp theo?"*. Lúc đó AI mới thừa nhận rằng cần một lớp kiểm tra ở tầng code.

**Sửa thế nào:** thiết kế lại pipeline, thêm hàm `validate_boundaries()` chạy sau khi parse JSON, **tính lại** cờ `escalate` từ đầu thay vì đọc giá trị model trả về. Rồi viết ba adversarial test mà input giả lập là output của một model **đã bị bẻ khoá hoàn toàn**, để kiểm tra riêng lớp guard này.

**Bài học:** ranh giới viết trong prompt là lời khuyên, ranh giới viết trong code mới là ràng buộc. Câu này tôi sẽ mang theo sang các lab sau.

### 2.2. AI bịa số liệu vận hành như thể là dữ liệu có thật

Khi tôi xin số liệu cho ô Business Impact, AI đưa ra ngay "khoảng 200 vé mỗi ngày trên một cụm", "15% vé bị route nhầm", "11 phút mỗi vé", trình bày trôi chảy như thể trích từ báo cáo vận hành của Vinhomes.

Không có nguồn nào cả. Đây là hallucination dạng nguy hiểm nhất vì nó **nghe hợp lý**, và nếu bê thẳng vào báo cáo thì cả bài scoping sẽ đứng trên nền cát. Chính PRD nội bộ của nhóm cũng đã tự ghi chú rằng các con số trong đó là *illustrative*, nhưng khi tôi hỏi lại thì AI không tự nhắc điều đó.

**Sửa thế nào:** giữ các con số làm giả định làm việc, nhưng gắn nhãn rõ ràng là ước tính chưa kiểm chứng, và bổ sung hẳn một bảng "cách validate" vào mục 3.1 của báo cáo, nêu cụ thể lấy số từ trường dữ liệu nào và tính bằng công thức gì. Tôi cũng thêm chi tiết dùng **trung vị** thay vì trung bình cho thời gian triage, để tránh lệch do vé bị bỏ quên trong hàng đợi.

**Bài học:** với AI, số liệu là thứ phải nghi ngờ trước tiên. Một bản scoping trung thực về việc mình chưa biết gì thì đáng tin hơn một bản đầy số đẹp.

### 2.3. AI đề xuất kiến trúc phức tạp hơn mức cần thiết

Câu hỏi mở đầu của tôi là "nên dùng kiến trúc AI nào cho bài toán này", và câu trả lời đầu tiên là một **multi-agent system**: một agent phân loại, một agent tra cứu bộ phận, một agent soạn phản hồi, một agent điều phối.

Nghe rất ấn tượng và hoàn toàn sai cho bài toán này. Quy trình nghiệp vụ ở đây cố định và chỉ có một bước cần suy luận. Tệ hơn, bản chất của agent là được trao quyền hành động, mà đóng vé và nhắn cư dân lại đúng là những quyền Operational Boundary đang cấm. Chọn agent là tự tay mở lại các cửa vừa đóng.

**Sửa thế nào:** tôi đổi câu hỏi thành *"hãy lập luận vì sao KHÔNG nên dùng agent cho bài này"*. Lần này AI đưa ra đúng các lý do trên. Tôi đưa cả ba phương án vào bảng so sánh Rule với LLM với Agent trong báo cáo, kèm lý do loại từng phương án, thay vì chỉ nêu phương án được chọn.

**Bài học:** cách đặt câu hỏi quyết định chất lượng câu trả lời. Hỏi "nên dùng gì" thì AI có xu hướng đề xuất thứ phức tạp. Hỏi "vì sao không nên dùng X" thì nhận được phản biện thật.

---

## 3. Prompt tôi đã sửa như thế nào

### Lần 1 — quá chung chung

> *"Gợi ý cho tôi vài bài toán AI cho Vinhomes."*

Nhận về toàn ý tưởng sáo rỗng kiểu "chatbot chăm sóc khách hàng", "dự đoán nhu cầu bảo trì". Không có bài nào gắn với một quy trình cụ thể có người thật đang làm thủ công.

### Lần 2 — thêm vai, thêm ràng buộc, thêm yêu cầu về bằng chứng

> *"Tôi là AI Engineer tại Vin Smart Future. Hãy liệt kê 5 quy trình nghiệp vụ THỦ CÔNG mà nhân viên ban quản lý toà nhà Vinhomes đang làm hằng ngày. Với mỗi quy trình, nêu rõ ai làm, mất bao lâu mỗi lượt, và bước nào là bottleneck. Nếu con số nào là ước đoán của bạn, hãy ghi rõ là ước đoán."*

Khác biệt rõ rệt. Câu cuối là câu tôi thêm sau khi dính lỗi 2.2, và nó khiến AI tự gắn nhãn phần nào là phỏng đoán thay vì trình bày tất cả như sự thật.

### Lần 3 — ép AI đóng vai đối thủ

Dùng gợi ý trong `01-worksheet.md`, tôi dán thẻ bài toán và yêu cầu AI đóng vai CFO khó tính chỉ ra ba điểm yếu và lập luận vì sao rule-based tốt hơn.

Phản biện đắt giá nhất nhận được: *"Nếu đã có taxonomy cố định 8 danh mục thì vì sao không dùng một classifier nhỏ được huấn luyện trên log vé, vừa rẻ hơn vừa kiểm soát được, thay vì gọi LLM cho từng vé?"*

Đây là câu hỏi đúng và tôi không bác bỏ được hoàn toàn. Câu trả lời trung thực là: huấn luyện classifier cần tập vé đã gắn nhãn mà nhóm **chưa có quyền truy cập**. Chính vì vậy mục AI Readiness Checklist câu 1 được trả lời là "một phần" chứ không phải "có", và việc trích xuất 2.000 vé đã gắn nhãn được đưa thành điều kiện tiên quyết của pilot. Nếu sau này dữ liệu đó cho thấy classifier nhỏ đủ tốt, nhóm nên chuyển sang classifier thay vì cố giữ LLM.

### Lần 4 — sửa SYSTEM_PROMPT sau khi đọc TRD

> Từ: *"viết system prompt phân loại khiếu nại cư dân"*
> Thành: *"viết system prompt, liệt kê các luật cứng theo đúng thứ tự, mỗi luật nêu rõ hành vi bị cấm VÀ giá trị JSON bắt buộc phải trả khi gặp tình huống đó. Cuối cùng mô tả schema JSON output."*

Bản sau dùng được gần như nguyên vẹn, vì mỗi luật đã gắn với một hậu quả cụ thể trong dữ liệu thay vì chỉ là lời răn đe.

---

## 4. Điều AI không tìm ra, tôi tìm ra khi chạy thật

Lỗi đáng nhớ nhất của buổi lab không đến từ việc hỏi AI mà đến từ việc **chạy code**.

Prototype phân loại vé *"Đèn hành lang tầng 12 toà S3 cháy bóng mấy hôm nay"* và đẩy nó lên hàng đợi khẩn cấp. Lý do: danh sách `SAFETY_KEYWORDS` có từ `"cháy"`, và phép kiểm tra dùng khớp chuỗi con, nên cụm *"cháy bóng"* khớp nhầm với từ khoá hoả hoạn.

Không AI nào cảnh báo tôi về chuyện này, kể cả khi tôi đưa nguyên danh sách từ khoá và hỏi có vấn đề gì không. Nó chỉ lộ ra khi có một câu tiếng Việt đời thường đi qua hệ thống.

**Sửa thế nào:** thêm danh sách cụm từ lành tính được lọc ra trước khi quét từ khoá, và ghi hẳn tỉ lệ false positive dưới 2% thành một trong bốn điều kiện thoát pilot.

**Bài học lớn nhất của buổi lab:** một bản scoping chỉ thật sự được kiểm chứng khi có code chạy trên dữ liệu giống đời thật. Trước đó nó vẫn chỉ là một giả thuyết được trình bày đẹp.

### Lỗi thứ hai, và lần này là do chính AI gây ra

Sau khi dựng thêm một bản demo chạy trên trình duyệt, tôi bật chế độ gọi model trực tiếp và thử lại đúng vé đèn hành lang. Model phân loại đúng danh mục với độ tin cậy 0.95, nhưng trả về mã bộ phận tiếp nhận là `bao_tri_dien`, một mã **không có** trong bảng định tuyến gồm năm bộ phận của hệ thống.

Điều đáng nói là guard của tôi để lọt. Nó đối chiếu trường phân loại với taxonomy, nhưng không đối chiếu trường bộ phận với bảng bộ phận, dù danh sách hợp lệ đã nằm sẵn trong code. Tôi đã khai báo một enum rồi quên dùng nó để kiểm tra.

Hậu quả tệ hơn lỗi từ khoá an toàn. Lỗi kia làm nghẽn hàng đợi ưu tiên, còn lỗi này khiến vé biến mất trong im lặng: hệ thống báo đã điều hướng, không ai nhận, và không có tín hiệu báo động nào.

**Sửa thế nào:** thêm luật thứ bảy vào guard, và biến chính payload mà model vừa sinh ra thành một bài test hồi quy. Bây giờ bộ test có bốn bài, trong đó ba bài do nhóm nghĩ ra và một bài do model tự tặng.

**Bài học:** tôi từng nghĩ hallucination chỉ xảy ra ở phần văn xuôi. Thực ra nó xảy ra ở **mọi trường** mà model sinh ra, kể cả những trường trông giống mã định danh có cấu trúc và dễ khiến người ta tin ngay. Mỗi trường mà hệ thống hạ nguồn tiêu thụ đều phải được đối chiếu với một tập giá trị hợp lệ.

---

## 5. Tổng kết

Ba điều tôi mang về:

1. **Ranh giới viết trong prompt là lời khuyên, ranh giới viết trong code mới là ràng buộc.** Cách kiểm chứng là giả định model đã bị bẻ khoá rồi hỏi hệ thống còn an toàn không. Và một enum khai báo mà không dùng để đối chiếu thì cũng chỉ là tài liệu.
2. **Số liệu do AI đưa ra phải bị nghi ngờ trước tiên.** Gắn nhãn ước tính và kèm cách validate thì trung thực hơn nhiều so với một bảng số liệu trơn tru không nguồn.
3. **Cách đặt câu hỏi quyết định chất lượng câu trả lời.** Hỏi "nên dùng gì" nhận về thứ phức tạp; hỏi "vì sao không nên dùng X" mới nhận được phản biện thật.

AI rút ngắn đáng kể thời gian đi từ trang giấy trắng đến bản nháp đầu tiên. Nhưng mọi quyết định có hậu quả thật trong bài này, gồm thu hẹp scope, tách nhóm danh mục nhạy cảm, và đặt guard ở tầng code, đều đến từ việc đọc kỹ tài liệu và chạy thử code, chứ không đến từ việc hỏi AI.
