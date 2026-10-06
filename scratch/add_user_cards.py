import sys
import urllib.request
import json

sys.stdout.reconfigure(encoding='utf-8')

ENDPOINT = "http://127.0.0.1:3141/"
DECK_NAME = "JLPT N2::오답노트 (선정 어휘·문형)"

def mcp_call(name, args=None):
    req_body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": name,
            "arguments": args or {}
        }
    }
    data = json.dumps(req_body, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read().decode('utf-8')
    for line in body.splitlines():
        if line.startswith("data: "):
            return json.loads(line[6:]).get('result')
    return None

# 1. Create deck
print("[1] Creating deck:", DECK_NAME)
res_deck = mcp_call('create_deck', {'deck_name': DECK_NAME})
print("    Result:", res_deck)

# Card 1: 回答
front_1 = """
<div style="color:#64748b;font-size:13px;font-weight:700;letter-spacing:0.05em">JLPT N2 핵심 어휘 · 오답노트 선정</div>
<div style="font-size:36px;font-weight:800;color:#0f172a;margin:10px 0 12px">回答</div>
<div style="color:#64748b;font-size:14px">독음 · 뜻 · 구별 포인트를 떠올려 보세요.</div>
""".strip()

back_1 = """
<div style="font-size:24px;font-weight:800;color:#0f172a;margin-bottom:14px">회답, 답변, 응답</div>

<div style="color:#0284c7;font-size:12px;font-weight:700;background:#f0f9ff;display:inline-block;padding:2px 10px;border-radius:99px;border:1px solid #bae6fd;margin-top:14px">독음 & 품사</div>
<div style="line-height:1.6;margin-top:4px;font-size:17px;font-weight:600;color:#1e293b"><ruby>回答<rt>かいとう</rt></ruby> (명사, ス동사)</div>

<div style="color:#0284c7;font-size:12px;font-weight:700;background:#f0f9ff;display:inline-block;padding:2px 10px;border-radius:99px;border:1px solid #bae6fd;margin-top:14px">핵심 의미 & 연어</div>
<div style="line-height:1.6;margin-top:4px;color:#1e293b">질문·요구·의뢰나 설문조사 등에 답함.<br>
• <ruby>質問<rt>しつもん</rt></ruby>に<b><ruby>回答<rt>かいとう</rt></ruby>する</b> (질문에 답변하다)<br>
• アンケートに<b><ruby>回答<rt>かいとう</rt></ruby>する</b> (설문에 응답하다)<br>
• <b><ruby>回答<rt>かいとう</rt></ruby>を<ruby>得<rt>え</rt></ruby>る</b> (답변을 얻다) / <b><ruby>控<rt>ひか</rt></ruby>える</b> (답변을 보류하다)</div>

<div style="color:#0284c7;font-size:12px;font-weight:700;background:#f0f9ff;display:inline-block;padding:2px 10px;border-radius:99px;border:1px solid #bae6fd;margin-top:14px">구별 포인트 (시험 빈출 함정)</div>
<div style="line-height:1.6;margin-top:4px;color:#1e293b">
• <b><ruby>回答<rt>かいとう</rt></ruby></b>: 질문·의뢰에 대한 <b>답변·회신</b> (비즈니스/설문/공식 대응)<br>
• <b><ruby>解答<rt>かいとう</rt></ruby></b>: 문제나 시험의 <b>정답·해답·풀이</b> (<ruby>問題<rt>もんだい</rt></ruby>の<ruby>解答<rt>かいとう</rt></ruby>) ➔ <b>한자 표기 문제 필수 구별!</b><br>
• <b><ruby>返事<rt>へんじ</rt></ruby></b>: 부름에 대답하기, 일상적인 연락/답장
</div>

<div style="color:#0284c7;font-size:12px;font-weight:700;background:#f0f9ff;display:inline-block;padding:2px 10px;border-radius:99px;border:1px solid #bae6fd;margin-top:14px">예문 1</div>
<div style="line-height:1.6;margin-top:4px;color:#1e293b">
<ruby>質問<rt>しつもん</rt></ruby>に<ruby>対<rt>たい</rt></ruby>する<span style="background:#fef08a;color:#854d0e;font-weight:700;padding:2px 6px;border-radius:4px;border-bottom:2px solid #ca8a04;"><ruby>回答<rt>かいとう</rt></ruby></span>は、メールにてお<ruby>知<rt>し</rt></ruby>らせいたします。<br>
<span style="color:#475569;font-size:14px">질문에 대한 답변은 이메일로 알려드리겠습니다.</span>
</div>

<div style="color:#0284c7;font-size:12px;font-weight:700;background:#f0f9ff;display:inline-block;padding:2px 10px;border-radius:99px;border:1px solid #bae6fd;margin-top:14px">예문 2</div>
<div style="line-height:1.6;margin-top:4px;color:#1e293b">
アンケートに<span style="background:#fef08a;color:#854d0e;font-weight:700;padding:2px 6px;border-radius:4px;border-bottom:2px solid #ca8a04;"><ruby>回答<rt>かいとう</rt></ruby>して</span>いただいた<ruby>方<rt>かた</rt></ruby>に、ギフトカードをプレゼントします。<br>
<span style="color:#475569;font-size:14px">설문조사에 응답해 주신 분께 기프트 카드를 선물합니다.</span>
</div>

<div style="color:#0284c7;font-size:12px;font-weight:700;background:#f0f9ff;display:inline-block;padding:2px 10px;border-radius:99px;border:1px solid #bae6fd;margin-top:14px">시험 신호</div>
<div style="line-height:1.6;margin-top:4px;color:#1e293b">
문자·어휘 문제2(한자 표기)에서 <b>『回答』 vs 『解答』</b>를 묻는 문제가 단골 출제되며, 청해 비즈니스 대화에서 정중표현 <b>『ご回答』</b>로 빈출됩니다.
</div>
""".strip()

# Card 2: 〜を除いて
front_2 = """
<div style="color:#64748b;font-size:13px;font-weight:700;letter-spacing:0.05em">JLPT N2 핵심 문형 · 오답노트 선정</div>
<div style="font-size:36px;font-weight:800;color:#0f172a;margin:10px 0 12px">〜を除いて</div>
<div style="color:#64748b;font-size:14px">접속 · 의미 · 구별 포인트를 떠올려 보세요.</div>
""".strip()

back_2 = """
<div style="font-size:24px;font-weight:800;color:#0f172a;margin-bottom:14px">~을 제외하고, ~을 빼고</div>

<div style="color:#0284c7;font-size:12px;font-weight:700;background:#f0f9ff;display:inline-block;padding:2px 10px;border-radius:99px;border:1px solid #bae6fd;margin-top:14px">접속 형태</div>
<div style="line-height:1.6;margin-top:4px;font-size:17px;font-weight:600;color:#1e293b"><b>名詞(N) ＋ を除いて</b> / <b>を除いては</b> / <b>を除けば</b></div>

<div style="color:#0284c7;font-size:12px;font-weight:700;background:#f0f9ff;display:inline-block;padding:2px 10px;border-radius:99px;border:1px solid #bae6fd;margin-top:14px">핵심 의미 & 1초 플래그</div>
<div style="line-height:1.6;margin-top:4px;color:#1e293b">
전체 범위 중에서 <b>특정 대상을 제외함</b>을 명시하는 격식체 표현.<br>
🚨 <b>1초 플래그:</b> <b>『~빼고 전부 다! (예외 지정)』</b>
</div>

<div style="color:#0284c7;font-size:12px;font-weight:700;background:#f0f9ff;display:inline-block;padding:2px 10px;border-radius:99px;border:1px solid #bae6fd;margin-top:14px">구별 포인트 (유사 문형 대조)</div>
<div style="line-height:1.6;margin-top:4px;color:#1e293b">
• <b>〜を<ruby>除<rt>のぞ</rt></ruby>いて</b>: 전체 집합에서 특정 하나를 <b>'제외'</b>하는 격식 표현 (단독 예외)<br>
• <b>〜<ruby>抜<rt>ぬ</rt></ruby>きで / 〜<ruby>抜<rt>ぬ</rt></ruby>きにして</b>: 당연히 있어야 할 요소를 <b>'생략하고 / 없이'</b> (<ruby>冗談抜<rt>じょうだんぬ</rt></ruby>きで 농담 빼고)<br>
• <b>〜をはじめ（として）</b>: 대표적인 것을 <b>'첫머리로 꼽아 포함'</b>할 때 (~을 비롯하여) [정반대 방향!]
</div>

<div style="color:#0284c7;font-size:12px;font-weight:700;background:#f0f9ff;display:inline-block;padding:2px 10px;border-radius:99px;border:1px solid #bae6fd;margin-top:14px">예문 1</div>
<div style="line-height:1.6;margin-top:4px;color:#1e293b">
<ruby>日曜日<rt>にちようび</rt></ruby>を<span style="background:#fef08a;color:#854d0e;font-weight:700;padding:2px 6px;border-radius:4px;border-bottom:2px solid #ca8a04;"><ruby>除<rt>のぞ</rt></ruby>いて</span>、<ruby>毎日<rt>まいにち</rt></ruby><ruby>図書館<rt>としょかん</rt></ruby>へ<ruby>通<rt>かよ</rt></ruby>っています。<br>
<span style="color:#475569;font-size:14px">일요일을 제외하고 매일 도서관에 다니고 있습니다.</span>
</div>

<div style="color:#0284c7;font-size:12px;font-weight:700;background:#f0f9ff;display:inline-block;padding:2px 10px;border-radius:99px;border:1px solid #bae6fd;margin-top:14px">예문 2</div>
<div style="line-height:1.6;margin-top:4px;color:#1e293b">
<ruby>田中<rt>たなか</rt></ruby>さんを<span style="background:#fef08a;color:#854d0e;font-weight:700;padding:2px 6px;border-radius:4px;border-bottom:2px solid #ca8a04;"><ruby>除<rt>のぞ</rt></ruby>いては</span>、全員がその<ruby>提案<rt>ていあん</rt></ruby>に<ruby>賛成<rt>さんせい</rt></ruby>した。<br>
<span style="color:#475569;font-size:14px">다나카 씨를 제외하고는 전원이 그 제안에 찬성했다.</span>
</div>

<div style="color:#0284c7;font-size:12px;font-weight:700;background:#f0f9ff;display:inline-block;padding:2px 10px;border-radius:99px;border:1px solid #bae6fd;margin-top:14px">시험 신호</div>
<div style="line-height:1.6;margin-top:4px;color:#1e293b">
N2 독해 및 문법 문제7(문법형식 판단)에서 <b>『Aを除いてすべてBだ』</b> (A를 제외하고 전부 B이다) 구문으로 강력한 한정 조건을 제시할 때 빈출됩니다.
</div>
""".strip()

# 2. Add cards
print("[2] Adding card: 回答")
res_c1 = mcp_call('add_note', {
    'deck_name': DECK_NAME,
    'model_name': 'Basic',
    'fields': {
        'Front': front_1,
        'Back': back_1
    },
    'tags': ['JLPT_N2', '오답노트_선정어휘', '어휘', '回答'],
    'allow_duplicate': True
})
print("    Result:", res_c1)

print("[3] Adding card: 〜を除いて")
res_c2 = mcp_call('add_note', {
    'deck_name': DECK_NAME,
    'model_name': 'Basic',
    'fields': {
        'Front': front_2,
        'Back': back_2
    },
    'tags': ['JLPT_N2', '오답노트_선전문형', '문법', 'を除いて'],
    'allow_duplicate': True
})
print("    Result:", res_c2)

# 3. Trigger Sync
print("[4] Triggering Anki sync...")
res_sync = mcp_call('sync')
print("    Sync Result:", res_sync)
