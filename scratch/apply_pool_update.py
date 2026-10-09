import json, sys

sys.stdout.reconfigure(encoding='utf-8')

NEW_DIALOGUE_TURNS = [
    {
        "speaker": "男",
        "ja": "中村さん、青葉市の市民文化祭のことだけど、ステージ演奏の出演者募集に応募しようっていう話、２人でギター弾いて歌おうって言ってたやつね。事前選考のための演奏動画の作成が締め切りに間に合わないって諦めたよね。それ、僕の勘違いだったよ。ごめん。応募申請書と動画を同時に提出しなきゃいけないと思ってたんだけど、動画は申請書の締め切り後、１週間以内の提出だったんだ。",
        "ko": "남: 나카무라 씨, 아오바 시 시민문화제 말인데, 무대 연주 출연자 모집에 응모하자던 이야기, 둘이서 기타 치며 노래하자던 그거. 사전 심사용 연주 영상 제작이 마감에 늦을 것 같아 포기했었잖아. 그거 내 착각이었어. 미안. 응모 신청서와 영상을 동시에 제출해야 하는 줄 알았는데, 영상은 신청서 마감 후 1주일 이내 제출이었어."
    },
    {
        "speaker": "女",
        "ja": "え、そうだったの？私もホームページ見たのに気がつかなかった。ごめんね。",
        "ko": "여: 어, 그랬던 거야? 나도 홈페이지 봤는데 알아채지 못했네. 미안해."
    },
    {
        "speaker": "男",
        "ja": "うん。間に合いそうだから申し込もうよ。パソコンで申請書作ってくれたって言ってたけど、削除しちゃった？",
        "ko": "남: 응. 시간 맞출 수 있을 것 같으니까 신청하자. 컴퓨터로 신청서 써 줬다고 했었는데, 삭제해 버렸어?"
    },
    {
        "speaker": "女",
        "ja": "残してあるよ。",
        "ko": "여: 남겨 뒀어."
    },
    {
        "speaker": "男",
        "ja": "じゃあ、それ使えるね。締め切り明日だから提出任せるね。",
        "ko": "남: 그럼 그거 쓸 수 있겠네. 마감이 내일까지니까 제출 부탁할게."
    },
    {
        "speaker": "女",
        "ja": "了解。動画作成もすぐに取りかかんなきゃ。応募する以上は絶対出たいからね。",
        "ko": "여: 알겠어. 영상 제작도 바로 시작해야겠네. 응모하는 이상은 꼭 나가고 싶으니까."
    },
    {
        "speaker": "問い",
        "ja": "女の学生はこの後まず何をしますか。",
        "ko": "질문: 여학생은 이 뒤에 가장 먼저 무엇을 합니까?"
    }
]

# Build dialogue HTML
turns_html = []
for t in NEW_DIALOGUE_TURNS:
    spk_color = '#475569' if t['speaker'] == '男' else ('#2563eb' if t['speaker'] == '女' else '#0369a1')
    turns_html.append(f"""<div style="margin-bottom:10px; padding-bottom:8px; border-bottom:1px dashed #e2e8f0;">
  <div style="font-size:14px; line-height:1.7; color:#0f172a; word-break:keep-all;"><b style='color:{spk_color};'>{t['speaker']}：</b>{t['ja']}</div>
  <div style="font-size:13px; line-height:1.6; color:#475569; margin-top:3px; word-break:keep-all;">↳ {t['ko']}</div>
</div>""")

dialogue_box = "\n".join(turns_html)

new_explanation_html = f"""<div style="font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Hiragino Sans', sans-serif; max-width:620px; margin:0 auto; padding:6px 2px;">
  <!-- Header -->
  <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #e2e8f0; padding-bottom:8px; margin-bottom:12px;">
    <span style="font-size:12px; font-weight:700; color:#16a34a; background:#f0fdf4; padding:3px 8px; border-radius:6px;">공식 정답 및 대본 완비</span>
    <span style="font-size:12px; font-weight:600; color:#475569;">제2회 실전 모의고사 (2023.12 기출 완본) · Q76</span>
  </div>

  <!-- Correct Answer Banner -->
  <div style="background:#f0fdf4; border-left:4px solid #16a34a; padding:12px 14px; border-radius:0 8px 8px 0; margin-bottom:12px;">
    <div style="font-size:11px; font-weight:700; color:#166534; text-transform:uppercase;">공식 정답</div>
    <div style="font-size:21px; font-weight:800; color:#14532d; margin:4px 0 6px;">4番: 応募申請書を提出する</div>
    <div style="font-size:14px; color:#334155; line-height:1.55;">【청해 해설】 남학생이 마감이 내일인 신청서 제출을 부탁했고(締め切り明日だから提出任せるね), 여학생이 컴퓨터에 남아있는 기존 신청서를 제출하기로 수락(了解)했습니다. 영상 제작은 그 다음 단계이므로(動画作成もすぐに取りかかんなきゃ) 여학생이 가장 먼저 할 일은 '4번: 응모 신청서를 제출하는 것(応募申請書を提出する)'입니다.</div>
    <div style="font-size:11px; color:#64748b; margin-top:4px;">분류: 청해 → 과제이해(課題理解) → 문화제 응모 최우선 절차</div>
  </div>

  <!-- Listening Script Box (Verbatim) -->
  <div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #0284c7; border-radius:4px 8px 8px 4px; padding:12px 14px; margin-bottom:12px;">
    <div style="font-size:12px; font-weight:700; color:#0369a1; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;">
      <span>📜 청해 대본 및 한국어 완본 번역 (発話スクリプト・対訳)</span>
      <span style="font-size:11px; font-weight:600; color:#0284c7; background:#e0f2fe; padding:2px 6px; border-radius:4px;">문장별 완벽 대조</span>
    </div>
    <div style="background:#ffffff; padding:10px 12px; border-radius:6px; border:1px solid #e2e8f0;">
{dialogue_box}
    </div>
  </div>

  <!-- User Mistake & Trap Analysis Box -->
  <div style="background:#fff1f2; border:1px solid #fecdd3; border-radius:8px; padding:12px 14px; margin-bottom:12px;">
    <div style="font-size:13px; font-weight:700; color:#9f1239; margin-bottom:6px;">
      ❌ 내 선택: <span style="font-weight:800; color:#be123c;">応募申請書を新しく作成する</span>
      <span style="font-size:11px; font-weight:500; color:#881337; margin-left:6px;">(풀이 체류: 70초)</span>
    </div>
    <div style="font-size:13px; color:#9f1239; line-height:1.5;">
      <b>⚠️ 함정 분석:</b> 신청서는 새로 만드는 것이 아니라(新しく作成する), 이미 컴퓨터에 작성해 둔 파일이 남아있어 그대로 제출(提出する)하는 것입니다.
    </div>
  </div>

  <!-- Connection & Meaning Box -->
  <div style="border:1px solid #e2e8f0; border-radius:8px; padding:12px 14px; margin-bottom:12px; background:#ffffff;">
    <div style="font-size:13px; color:#1e293b; line-height:1.55;">
      <b style="color:#2563eb;">📌 청취 포인트 & 단서:</b><br>「残してあるよ」→「じゃあそれ使えるね。締め切り明日だから、提出任せるね」→「了解」。
    </div>
    <div style="margin-top:10px; padding-top:10px; border-top:1px dashed #e2e8f0; font-size:13px; line-height:1.5;">
      <b style="color:#0891b2;">🔍 유사 문형·표현 비교:</b><br>新しく作成（X, 残してあるファイルあり） ↔ 提出する（O, 明日締め切りなので最優先）。
    </div>
  </div>

  <!-- Example Box -->
  <div style="border:1px solid #e2e8f0; border-radius:8px; padding:12px 14px; margin-bottom:12px; background:#fafafa;">
    <div style="font-size:12px; font-weight:700; color:#475569; margin-bottom:4px;">📖 핵심 표현 훈련</div>
    <div style="font-size:17px; line-height:1.6; color:#0f172a;"><ruby>応募<rt>おうぼ</rt></ruby><ruby>申請書<rt>しんせいしょ</rt></ruby>を<ruby>提出<rt>ていしゅつ</rt></ruby>する。</div>
  </div>

  <!-- Exam Signal & Pre-submission Check -->
  <div style="background:#eff6ff; border-left:4px solid #2563eb; padding:10px 14px; border-radius:0 8px 8px 0; font-size:13px; color:#1e40af; line-height:1.5;">
    <b>💡 직전 체크 & 시험 신호:</b><br>「새로 만들기」와 「기존 파일 제출」의 차이를 듣고, 즉시 취해야 할 행동을 정확히 골랐는가?
  </div>
</div>"""

files = [
    'jlpt-calendar-site/public/exams/n2-mock-error-review-pool.html',
    'quiz_sites/n2-mock-error-review-pool.html'
]

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read()

    start_marker = 'const ALL_ERROR_QUESTIONS = '
    start_idx = text.find(start_marker) + len(start_marker)

    bracket_depth = 0
    in_string = False
    escape = False
    quote_char = None
    end_idx = -1

    for i in range(start_idx, len(text)):
        c = text[i]
        if in_string:
            if escape:
                escape = False
            elif c == '\\':
                escape = True
            elif c == quote_char:
                in_string = False
        else:
            if c in ('"', "'"):
                in_string = True
                quote_char = c
            elif c == '[':
                bracket_depth += 1
            elif c == ']':
                bracket_depth -= 1
                if bracket_depth == 0:
                    end_idx = i + 1
                    break

    questions = json.loads(text[start_idx:end_idx].strip())
    updated = False
    for q in questions:
        if q.get('id') == 'err-listen-10':
            q['explanation_html'] = new_explanation_html
            updated = True
            break

    if updated:
        new_json_str = json.dumps(questions, ensure_ascii=False)
        new_text = text[:start_idx] + new_json_str + text[end_idx:]
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print(f"[SUCCESS] Updated err-listen-10 in {fp}")
    else:
        print(f"[FAIL] Could not find err-listen-10 in {fp}")
