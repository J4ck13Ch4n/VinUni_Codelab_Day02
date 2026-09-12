"""
Vinhomes Complaint Routing — Frontend đơn giản để đưa cho người dùng thử.

1 file, thuần stdlib (http.server) — không thêm dependency. Tái dùng
prompt_prototype.run_pipeline() (SYSTEM_PROMPT + evaluate_prompt() +
validate_boundaries() có sẵn), chỉ thêm lớp web mỏng lên trên.

Chạy:  python3 app.py       (cần venv có google-genai nếu LLM_BACKEND=gemini)
Mở:    http://localhost:8000   (đổi cổng qua biến PORT)

HITL: mọi kết quả AI chỉ là NHÁP. Nút "Duyệt & gửi" mô phỏng hành động của
Ban quản lý — không gọi hệ thống thật nào (repo chưa có ticket system thật).
"""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import prompt_prototype  # cùng thư mục — tự load .env, SYSTEM_PROMPT, run_pipeline()

PORT = int(os.getenv("PORT", "8000"))

INDEX_HTML = """<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vinhomes — Trợ lý Phân loại &amp; Điều hướng Phản ánh</title>
<style>
  :root{
    --bg:#f4f5f7; --card:#ffffff; --text:#1c2430; --muted:#6b7684;
    --border:#e3e6ea; --brand:#0f6b4d; --brand-dark:#0a4d38;
    --warn-bg:#fdecea; --warn-border:#e0796f; --warn-text:#9c2c1f;
    --ok-bg:#eaf6ef; --ok-border:#7fc9a4; --ok-text:#0f6b4d;
  }
  *{box-sizing:border-box}
  body{
    margin:0; background:var(--bg); color:var(--text);
    font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
    padding:24px 16px 64px;
  }
  .wrap{max-width:720px; margin:0 auto}
  header{margin-bottom:20px}
  header h1{font-size:20px; margin:0 0 2px}
  header p{margin:0; color:var(--muted); font-size:13px}
  .card{
    background:var(--card); border:1px solid var(--border); border-radius:12px;
    padding:18px; margin-bottom:16px;
  }
  textarea{
    width:100%; min-height:90px; resize:vertical; padding:10px 12px;
    border:1px solid var(--border); border-radius:8px; font:inherit; color:inherit;
  }
  textarea:focus{outline:2px solid var(--brand); outline-offset:-1px}
  .row{display:flex; gap:8px; align-items:center; margin-top:10px; flex-wrap:wrap}
  button{
    font:inherit; border:none; border-radius:8px; padding:9px 16px; cursor:pointer;
    background:var(--brand); color:#fff; font-weight:600;
  }
  button:hover{background:var(--brand-dark)}
  button:disabled{background:#a9b0b8; cursor:default}
  button.secondary{background:#fff; color:var(--text); border:1px solid var(--border)}
  button.secondary:hover{background:#f0f1f3}
  button.danger{background:#fff; color:var(--warn-text); border:1px solid var(--warn-border)}
  button.danger:hover{background:var(--warn-bg)}
  .hint{color:var(--muted); font-size:12px; margin-top:6px}
  .badge{
    display:inline-block; font-size:12px; font-weight:700; padding:2px 8px;
    border-radius:999px; letter-spacing:.02em;
  }
  .badge.ok{background:var(--ok-bg); color:var(--ok-text); border:1px solid var(--ok-border)}
  .badge.warn{background:var(--warn-bg); color:var(--warn-text); border:1px solid var(--warn-border)}
  .result{border-left:4px solid var(--ok-border); padding-left:12px}
  .result.escalate{border-left-color:var(--warn-border)}
  .result h3{margin:0 0 6px; font-size:16px}
  .result .meta{color:var(--muted); font-size:13px; margin:4px 0}
  .result .note{margin:8px 0 0; font-size:14px}
  .queue-item{
    border:1px solid var(--border); border-radius:10px; padding:12px; margin-bottom:8px;
  }
  .queue-item .top{display:flex; justify-content:space-between; gap:8px; align-items:baseline}
  .queue-item .input{color:var(--muted); font-size:13px; margin:6px 0 0}
  .queue-item .status{font-size:12px; font-weight:700}
  .status.pending{color:#a9760a}
  .status.approved{color:var(--ok-text)}
  .status.escalated{color:var(--warn-text)}
  .status.rejected{color:var(--muted)}
  footer{color:var(--muted); font-size:12px; text-align:center; margin-top:24px}
  #err{color:var(--warn-text); font-size:13px; margin-top:8px; display:none}
  #backend-tag{color:var(--muted); font-size:12px}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>Vinhomes — Trợ lý Phân loại &amp; Điều hướng Phản ánh</h1>
    <p>Vin Smart Future · Mọi kết quả AI chỉ là bản NHÁP — luôn cần Ban quản lý duyệt trước khi gửi.
       <span id="backend-tag"></span></p>
  </header>

  <div class="card">
    <textarea id="input" placeholder="Nhập nội dung phản ánh của cư dân... (ví dụ: Nhà tôi mất nước từ sáng nay)"></textarea>
    <div class="row">
      <button id="submit-btn" onclick="classify()">Phân loại</button>
      <span class="hint" id="status-text"></span>
    </div>
    <div id="err"></div>
  </div>

  <div class="card" id="result-card" style="display:none">
    <div class="result" id="result-inner"></div>
  </div>

  <h2 style="font-size:15px; color:var(--muted); margin:24px 0 8px">Hàng chờ (phiên demo — không lưu lại sau khi tắt trang)</h2>
  <div id="queue"></div>

  <footer>Bản demo local — không gửi tin thật, không lưu dữ liệu sau khi đóng tab.</footer>
</div>

<script>
const CATEGORY_LABELS = {
  mat_nuoc: "Mất nước", hong_den: "Hỏng đèn", on_ao: "Ồn ào", ve_sinh: "Vệ sinh",
  an_ninh: "An ninh", phi_quan_ly: "Phí quản lý", tranh_chap: "Tranh chấp", khac: "Khác",
};
let queue = []; // {id, input, result, status}
let nextId = 1;

async function loadInfo() {
  try {
    const res = await fetch("/api/info");
    const info = await res.json();
    document.getElementById("backend-tag").textContent =
      `· Backend: ${info.backend} (${info.model})`;
  } catch (e) { /* im lặng nếu lỗi, không chặn demo */ }
}

async function classify() {
  const input = document.getElementById("input").value.trim();
  const errEl = document.getElementById("err");
  errEl.style.display = "none";
  if (!input) { errEl.textContent = "Nhập nội dung phản ánh trước đã."; errEl.style.display = "block"; return; }

  const btn = document.getElementById("submit-btn");
  const statusText = document.getElementById("status-text");
  btn.disabled = true; statusText.textContent = "Đang gọi model...";

  try {
    const res = await fetch("/api/classify", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({text: input}),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Lỗi không rõ");

    const item = {id: nextId++, input, result: data, status: data.escalate ? "escalated" : "pending"};
    queue.unshift(item);
    renderResult(item);
    renderQueue();
    document.getElementById("input").value = "";
  } catch (e) {
    errEl.textContent = "Lỗi: " + e.message;
    errEl.style.display = "block";
  } finally {
    btn.disabled = false; statusText.textContent = "";
  }
}

function renderResult(item) {
  const card = document.getElementById("result-card");
  const inner = document.getElementById("result-inner");
  const r = item.result;
  const label = CATEGORY_LABELS[r.category] || r.category;
  card.style.display = "block";
  card.dataset.currentId = item.id;
  inner.className = "result" + (r.escalate ? " escalate" : "");
  inner.innerHTML = `
    <h3>${label} <span class="badge ${r.escalate ? "warn" : "ok"}">${r.escalate ? "CẦN DUYỆT NGAY" : "Có thể tự điều hướng"}</span></h3>
    <div class="meta">Độ tin cậy: ${(r.confidence * 100).toFixed(0)}% ${r.route_target ? "· Đề xuất chuyển: " + r.route_target : ""}</div>
    <p class="note">${escapeHtml(r.draft_note || "")}</p>
    <div class="row" id="actions-${item.id}"></div>
  `;
  renderActions(item, document.getElementById(`actions-${item.id}`));
}

function renderActions(item, el) {
  el.innerHTML = "";
  if (item.status === "approved" || item.status === "rejected") {
    const span = document.createElement("span");
    span.className = "hint";
    span.textContent = item.status === "approved" ? "Đã duyệt & gửi." : "Đã từ chối, chuyển xử lý thủ công.";
    el.appendChild(span);
    return;
  }
  if (item.result.escalate) {
    const span = document.createElement("span");
    span.className = "hint";
    span.textContent = "Đã vào hàng chờ ưu tiên cho Ban quản lý — AI không tự gửi.";
    el.appendChild(span);
    return;
  }
  const approveBtn = document.createElement("button");
  approveBtn.textContent = "Duyệt & gửi";
  approveBtn.onclick = () => setStatus(item.id, "approved");
  const rejectBtn = document.createElement("button");
  rejectBtn.className = "danger";
  rejectBtn.textContent = "Từ chối";
  rejectBtn.onclick = () => setStatus(item.id, "rejected");
  el.appendChild(approveBtn);
  el.appendChild(rejectBtn);
}

function setStatus(id, status) {
  const item = queue.find(q => q.id === id);
  if (!item) return;
  item.status = status;
  renderQueue();
  const card = document.getElementById("result-card");
  if (card.style.display !== "none" && card.dataset.currentId == id) renderResult(item);
}

function renderQueue() {
  const el = document.getElementById("queue");
  if (queue.length === 0) { el.innerHTML = '<p class="hint">Chưa có ticket nào trong phiên này.</p>'; return; }
  el.innerHTML = queue.map(item => {
    const label = CATEGORY_LABELS[item.result.category] || item.result.category;
    return `
      <div class="queue-item">
        <div class="top">
          <strong>${label}</strong>
          <span class="status ${item.status}">${statusLabel(item.status)}</span>
        </div>
        <p class="input">"${escapeHtml(item.input)}"</p>
      </div>`;
  }).join("");
}

function statusLabel(s) {
  return {pending: "Chờ duyệt", approved: "Đã gửi", escalated: "Ưu tiên cho BQL", rejected: "Đã từ chối"}[s] || s;
}

function escapeHtml(s) {
  const div = document.createElement("div");
  div.textContent = s;
  return div.innerHTML;
}

loadInfo();
renderQueue();
</script>
</body>
</html>
"""


def _resolve_model_label() -> str:
    if prompt_prototype.LLM_BACKEND == "gemini":
        return prompt_prototype.GEMINI_MODEL
    return (os.getenv("LAB_MINI_MODEL") or os.getenv("LAB_MODEL")
            or prompt_prototype.ROUTER_DEFAULT_MODEL)


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path in ("/", "/index.html"):
            body = INDEX_HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/api/info":
            self._send_json(200, {"backend": prompt_prototype.LLM_BACKEND, "model": _resolve_model_label()})
        else:
            self.send_error(404)

    def do_POST(self) -> None:
        if self.path != "/api/classify":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length) or b"{}")
            text = (data.get("text") or "").strip()
            if not text:
                self._send_json(400, {"error": "Thiếu nội dung phản ánh."})
                return
            result = prompt_prototype.run_pipeline(text)
            self._send_json(200, result)
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def log_message(self, fmt: str, *args) -> None:
        pass  # im lặng access log cho gọn terminal khi demo


if __name__ == "__main__":
    print(f"Vinhomes Complaint Routing — mở http://localhost:{PORT}")
    print(f"   Backend: {prompt_prototype.LLM_BACKEND} ({_resolve_model_label()})")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
