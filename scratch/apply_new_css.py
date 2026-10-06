import sys
import urllib.request
import json

sys.stdout.reconfigure(encoding='utf-8')

new_css = """
.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Hiragino Sans", "Hiragino Kaku Gothic ProN", Meiryo, sans-serif;
    font-size: 18px;
    line-height: 1.6;
    text-align: center;
    color: #1e293b;
    background-color: #ffffff;
    max-width: 680px;
    margin: 0 auto;
    padding: 12px;
}

/* Light Theme (White Background) Contrast Fixes */
.card span[style*="#fef08a"],
.card span[style*="#fde047"],
.card [style*="color: #fef08a"],
.card [style*="color: #fde047"],
.card [style*="color:#fef08a"],
.card [style*="color:#fde047"] {
    color: #854d0e !important; /* 고대비 앰버 브라운 - 흰색 배경에서 선명 */
    background: #fef08a !important; /* 밝은 노란색 하이라이트 */
    font-weight: 800 !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
    border-bottom: 2px solid #ca8a04 !important;
}

/* Section label headings (접속, 핵심 의미, 예문 1, 예문 2, 구별 포인트, 시험 신호) */
.card div[style*="font-size:13px"],
.card div[style*="font-size: 13px"] {
    color: #0284c7 !important; /* 선명한 스카이블루/네이비 */
    background: #f0f9ff !important;
    display: inline-block !important;
    padding: 3px 12px !important;
    border-radius: 99px !important;
    border: 1px solid #bae6fd !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    margin-top: 16px !important;
    margin-bottom: 4px !important;
}

/* Top Meaning Title (~라면, ~인 경우라면) */
.card div[style*="font-size:20px"],
.card div[style*="font-size: 20px"] {
    color: #0f172a !important; /* 깊은 네이비 블랙 */
    font-size: 22px !important;
    font-weight: 800 !important;
    margin-bottom: 16px !important;
}

/* Japanese Grammar Main Prompt in Front */
.card div[style*="font-size:30px"],
.card div[style*="font-size: 30px"] {
    color: #0f172a !important;
    font-size: 32px !important;
    font-weight: 800 !important;
}

/* Gray subtext (번역문, 가이드 문구) */
.card span[style*="#6b7280"],
.card div[style*="#6b7280"],
.card [style*="color:#6b7280"] {
    color: #475569 !important; /* 더 짙고 또렷한 슬레이트 */
}

/* Dark Mode / Night Mode Support */
.nightMode .card,
.night_mode .card {
    background-color: #0f172a !important;
    color: #f8fafc !important;
}

.nightMode span[style*="#fef08a"],
.nightMode span[style*="#fde047"],
.nightMode [style*="color: #fef08a"],
.nightMode [style*="color: #fde047"],
.night_mode span[style*="#fef08a"],
.night_mode span[style*="#fde047"] {
    color: #fef08a !important;
    background: rgba(250, 204, 21, 0.25) !important;
    border-bottom: 2px solid #facc15 !important;
}

.nightMode div[style*="font-size:13px"],
.night_mode div[style*="font-size:13px"] {
    color: #38bdf8 !important;
    background: rgba(56, 189, 248, 0.12) !important;
    border-color: rgba(56, 189, 248, 0.3) !important;
}

.nightMode div[style*="font-size:20px"],
.night_mode div[style*="font-size:20px"],
.nightMode div[style*="font-size:30px"],
.night_mode div[style*="font-size:30px"] {
    color: #f1f5f9 !important;
}

.nightMode span[style*="#6b7280"],
.night_mode span[style*="#6b7280"] {
    color: #94a3b8 !important;
}
""".strip()

req_body = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "update_model_styling",
        "arguments": {
            "model_name": "Basic",
            "css": new_css
        }
    }
}

data = json.dumps(req_body, ensure_ascii=False).encode('utf-8')
req = urllib.request.Request(
    "http://127.0.0.1:3141/",
    data=data,
    headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
    method="POST"
)

with urllib.request.urlopen(req, timeout=10) as resp:
    body = resp.read().decode('utf-8')

for line in body.splitlines():
    if line.startswith("data: "):
        res = json.loads(line[6:])
        print("Result:", res)
