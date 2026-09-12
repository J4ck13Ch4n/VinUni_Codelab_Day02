"""Local demo UI. Run: python starter-code/app.py, then http://127.0.0.1:8000."""
import json
import secrets
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from vinhomes_service import BUILDINGS, ROUTES, normalize, evaluate_prompt, validate_boundaries

TICKETS = {}
LOCK = Lock()
TOKEN = secrets.token_urlsafe(24)
TEAMS = dict.fromkeys(ROUTES.values()) | {'ban_quan_ly': None}


def classify_demo(text, building):
    category = 'khac'
    words = {'mat_nuoc': ['mat nuoc', 'khong co nuoc', 'ro nuoc', 'ro ri nuoc',
                          'nuoc yeu', 'ap luc nuoc thap', 'tac cong', 'nghet cong', 'tran nuoc'],
             'hong_den': ['hong den', 'den hong', 'mat dien', 'khong sang', 'nhap nhay',
                          'den chap chon', 'den nhap nhay', 'den bi hong'],
             'on_ao': ['on ao', 'karaoke', 'tieng on', 'am thanh lon', 'tieng khoan'],
             've_sinh': ['rac', 'mui hoi', 've sinh', 'san ban', 'bui ban'],
             'an_ninh': ['an ninh', 'nguoi la', 'chan loi thoat hiem', 'do xe sai',
                         'cong ra vao', 'camera', 'mat cap']}
    content = normalize(text)
    for name, keywords in words.items():
        if any(re.search(r'\b' + re.escape(word) + r'\b', content) for word in keywords):
            category = name
            break
    result = validate_boundaries({'category': category, 'confidence': 0.9, 'emergency': False}, text, building)
    result['confidence'] = None  # Keyword demo has no calibrated model confidence.
    return result


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def reply(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path != '/':
            return self.reply({'error': 'Không tìm thấy'}, 404)
        body = Path(__file__).with_name('ui.html').read_text(encoding='utf-8').replace('__TOKEN__', TOKEN).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.headers.get('X-Demo-Token') != TOKEN:
            return self.reply({'error': 'Phiên không hợp lệ. Tải lại trang.'}, 403)
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 50000:
                raise ValueError('Dữ liệu quá dài hoặc trống.')
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError('Dữ liệu không hợp lệ.')
            if self.path == '/classify':
                text, building, mode = data.get('text'), data.get('building'), data.get('mode')
                if not isinstance(text, str) or not text.strip() or len(text) > 10000:
                    raise ValueError('Nhập phản ánh từ 1 đến 10.000 ký tự.')
                if building not in BUILDINGS or mode not in ('demo', 'gemini'):
                    raise ValueError('Chọn tòa và chế độ hợp lệ.')
                result = classify_demo(text, building) if mode == 'demo' else json.loads(evaluate_prompt(text, building))
                ticket = {'id': secrets.token_hex(4).upper(), 'text': text, 'building': building,
                          'mode': mode, 'result': result, 'status': 'pending', 'approval': None}
                with LOCK:
                    if len(TICKETS) >= 200:
                        raise ValueError('Demo đã đủ 200 vé. Khởi động lại để tạo phiên mới.')
                    TICKETS[ticket['id']] = ticket
                return self.reply(ticket)
            if self.path == '/approve':
                reviewer, team = data.get('reviewer'), data.get('team')
                if not isinstance(reviewer, str) or not reviewer.strip() or len(reviewer) > 100:
                    raise ValueError('Nhập tên nhân viên duyệt (tối đa 100 ký tự).')
                if not isinstance(team, str) or team not in TEAMS:
                    raise ValueError('Bộ phận không hợp lệ.')
                with LOCK:
                    ticket = TICKETS.get(str(data.get('id')))
                    if ticket is None:
                        raise ValueError('Không tìm thấy vé; hãy gửi lại phản ánh.')
                    if ticket['status'] != 'pending':
                        raise ValueError('Vé này đã được duyệt.')
                    if ticket['result']['escalate'] and team != 'ban_quan_ly':
                        raise ValueError('Ca cần xem xét phải chuyển ban quản lý xử lý thủ công.')
                    ticket['status'] = 'approved'
                    ticket['approval'] = {'reviewer': reviewer.strip(), 'route': ticket['building'] + '/' + team}
                return self.reply(ticket)
            return self.reply({'error': 'Không tìm thấy'}, 404)
        except (ValueError, TypeError) as exc:
            self.reply({'error': str(exc)}, 400)


if __name__ == '__main__':
    print('Demo: http://127.0.0.1:8000 — Ctrl+C to stop. Data is in memory only.')
    ThreadingHTTPServer(('127.0.0.1', 8000), Handler).serve_forever()

