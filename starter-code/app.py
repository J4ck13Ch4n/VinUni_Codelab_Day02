from flask import Flask, request, render_template_string
from prompt_prototype import evaluate_prompt, _parse_model_output

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Vinhomes Complaint Routing — Demo</title>
  <style>
    body { font-family: sans-serif; max-width: 700px; margin: 40px auto; }
    textarea { width: 100%; height: 100px; }
    button { padding: 8px 16px; margin-top: 8px; }
    .result-box {
      background: #f4f4f4; padding: 16px; border-radius: 8px; margin-top: 16px;
    }
    .badge {
      display: inline-block; padding: 2px 10px; border-radius: 12px;
      font-size: 13px; font-weight: bold; color: white; margin-right: 6px;
    }
    .escalate-true { background: #d9534f; }
    .escalate-false { background: #5cb85c; }
    .note { font-size: 16px; margin-top: 10px; line-height: 1.5; }
    .meta { color: #666; font-size: 13px; margin-top: 8px; }
  </style>
</head>
<body>
  <h2>🚀 Vinhomes Resident Complaint Routing — Demo</h2>
  <form method="POST">
    <label>Nội dung phản ánh của cư dân:</label><br>
    <textarea name="complaint">{{ complaint or '' }}</textarea><br>
    <button type="submit">Gửi</button>
  </form>

  {% if result %}
    <div class="result-box">
      <span class="badge {{ 'escalate-true' if result.escalate else 'escalate-false' }}">
        {{ 'CẦN DUYỆT (ESCALATE)' if result.escalate else 'TỰ ĐỘNG ĐIỀU PHỐI' }}
      </span>
      <span class="badge" style="background:#337ab7;">{{ result.category }}</span>

      <div class="note">📝 {{ result.draft_note }}</div>

      <div class="meta">
        Route target: <b>{{ result.route_target or '(chờ nhân viên BQL duyệt)' }}</b><br>
        Độ tin cậy: {{ (result.confidence * 100) | round(1) }}%
      </div>
    </div>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    complaint = None
    if request.method == "POST":
        complaint = request.form.get("complaint", "")
        raw_output = evaluate_prompt(complaint)
        result = _parse_model_output(raw_output, complaint)
    return render_template_string(HTML_PAGE, result=result, complaint=complaint)

if __name__ == "__main__":
    app.run(debug=True, port=5000)