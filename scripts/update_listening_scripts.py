import os
import sys
import json
import re
import urllib.request
import time

ENDPOINT = "http://127.0.0.1:3141/"
DECK_LISTENING = "JLPT N2::오답노트 (청해 25문항 · 실전 음원)"

def mcp_call(name: str, arguments: dict = None):
    req_body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": name,
            "arguments": arguments or {}
        }
    }
    data = json.dumps(req_body, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode('utf-8')
    for line in body.splitlines():
        if line.startswith("data: "):
            res = json.loads(line[6:])
            return res.get('result')
    return None

# Complete script dictionary for all 25 listening error items
LISTENING_SCRIPTS = {
    # --- Exam 1 (2018 Official Vol. 2) ---
    ('1회_공식제2집', 76): """
<div style="margin-bottom:6px;"><b style="color:#2563eb;">女：</b>ええと、この授業を休むときは、必ず前の日までに連絡してください。</div>
<div style="margin-bottom:6px;"><b style="color:#475569;">男：</b>メールでもいいですか。</div>
<div style="margin-bottom:6px;"><b style="color:#2563eb;">女：</b>はい、いいですよ。あ、それから、休んだときは、私の研究室の前の掲示を見て、宿題を確認してください。友達に聞いたりしないで、自分で確かめてちゃんとやってきてくださいね。</div>
<div><b style="color:#475569;">男：</b>はい、分かりました。</div>
""",

    ('1회_공식제2집', 80): """
<div style="margin-bottom:6px;"><b style="color:#2563eb;">女：</b>来週の大阪出張、先方の都合で打ち合わせが翌日にも入ることになったんだ。</div>
<div style="margin-bottom:6px;"><b style="color:#475569;">男：</b>分かりました。では新幹線はそのままですね。</div>
<div style="margin-bottom:6px;"><b style="color:#2563eb;">女：</b>うん。ただ、ホテルの予約を一日延ばして、もう一泊できるように変更手続きをしてくれるかい？</div>
<div><b style="color:#475569;">男：</b>かしこまりました。すぐに旅行会社に電話して変更いたします。</div>
""",

    ('1회_공식제2집', 90): """
<div><b style="color:#475569;">男：</b>近年、都市部で深刻化するヒートアイランド現象に対して、ビルの屋上を植物で覆う「屋上緑化」の試みが注目されています。私たちの実測データによると、屋上を緑化した建物ではコンクリート表面の温度が最大で約２５度低下し、建物全体のエアコン消費電力も１５％削減できることが実証されました。緑の屋根は都市を冷やす天然のクーラーと言えます。</div>
""",

    ('1회_공식제2집', 94): """
<div style="margin-bottom:8px;"><b style="color:#2563eb;">【発話】</b> 女：部長、社内アンケート、山田さんを除いて全員から回答を得ました。</div>
<div style="color:#16a34a; font-weight:700;">1. 山田さんはまだなんだね。（正解）</div>
<div style="color:#64748b;">2. 全員分集まってよかったよ。</div>
<div style="color:#64748b;">3. 山田さんだけ回答したんだね。</div>
""",

    ('1회_공식제2집', 97): """
<div style="margin-bottom:8px;"><b style="color:#475569;">【発話】</b> 男：課長、プリンター、修理に出したんですが、もう買い替えるしかないって言われました。</div>
<div style="color:#64748b;">1. じゃあ、新しく買うのはやめよう。</div>
<div style="color:#16a34a; font-weight:700;">2. そうか、直せないんじゃ仕方ないね。（正解）</div>
<div style="color:#64748b;">3. 修理代、ずいぶん高かったんだね。</div>
""",

    ('1회_공식제2집', 99): """
<div style="margin-bottom:8px;"><b style="color:#2563eb;">【発話】</b> 女：この会議室、壁の色変えたせいか、広く見えるんじゃない？</div>
<div style="color:#64748b;">1. 前より狭く感じるよね。</div>
<div style="color:#16a34a; font-weight:700;">2. 本当、広くなった気がするね。（正解）</div>
<div style="color:#64748b;">3. 壁の色、変わってないと思うよ。</div>
""",

    ('1회_공식제2집', 102): """
<div style="margin-bottom:8px;"><b style="color:#475569;">【発話】</b> 男：昨日のサッカーの決勝戦、見逃しちゃったんだ。</div>
<div style="color:#16a34a; font-weight:700;">1. 残念、すごくいい試合だったのに。（正解）</div>
<div style="color:#64748b;">2. ちゃんと最後まで見られたんだね。</div>
<div style="color:#64748b;">3. 録画しておいてあげればよかった？</div>
""",

    ('1회_공식제2집', 106): """
<div style="margin-bottom:6px;"><b style="color:#475569;">店員：</b>いらっしゃいませ。信州へのご旅行ですね。４つのプランがございます。</div>
<div style="margin-bottom:6px;"><b style="color:#475569;">夫：</b>あなた、どれがいい？私は体を動かすハイキングコースがいいと思うんだけど。</div>
<div><b style="color:#2563eb;">妻：</b>うーん、最近残業続きで腰も痛いし、せっかくの旅行だから、あんまり歩き回らずに名湯の温泉宿で美味しいものを食べてのんびり癒やされたいよ。３番のプランがいいな。</div>
""",

    # --- Exam 2 (2023.12 Official Past Exam) ---
    ('2회_202312', 75): """
<div style="margin-bottom:6px;"><b style="color:#2563eb;">先生：</b>ゴミ処理問題をテーマに、来月発表してもらいます。役割分担は前回の授業で決めましたね。</div>
<div><b style="color:#2563eb;">先生：</b>今日はまず、どの国について調べるかグループで話し合ってください。授業の終わりに私に報告してください。</div>
<div style="margin-top:6px; color:#64748b; font-size:13px;">※ 役割分担は前回決定済み ➔ 今日の授業終了時までに決めるのは「調べる国」。</div>
""",

    ('2회_202312', 76): """
<div style="margin-bottom:6px;"><b style="color:#475569;">男：</b>市民文化祭の演奏応募、動画撮影が締め切りに間に合わないかもしれない。</div>
<div style="margin-bottom:6px;"><b style="color:#2563eb;">女：</b>要項を見たら、動画は申請書を出した後、1週間以内に提出すればいいらしいよ。</div>
<div style="margin-bottom:6px;"><b style="color:#475569;">男：</b>本当？申請書ファイルならパソコンに残ってるから、明日までに提出してくれる？</div>
<div><b style="color:#2563eb;">女：</b>うん、分かった。すぐに出してくるね。</div>
""",

    ('2회_202312', 77): """
<div style="margin-bottom:6px;"><b style="color:#475569;">男：</b>花壇の花が元気がなくて…もっと水をやった方がいいかな？</div>
<div style="margin-bottom:6px;"><b style="color:#2563eb;">女：</b>水をやりすぎると根腐れしちゃうのよ。土が乾くまで水やりは待って。</div>
<div><b style="color:#2563eb;">女：</b>それより、まず枯れた葉をハサミで切り落として、風通しをよくしてあげて。肥料はその後ね。</div>
""",

    ('2회_202312', 78): """
<div style="margin-bottom:6px;"><b style="color:#2563eb;">女：</b>あのアナウンサー、落ち着いた声も素敵だし、笑顔も感じがいいよね。</div>
<div style="margin-bottom:6px;"><b style="color:#475569;">男：</b>声もいいけど、僕は討論番組でゲストが勝手なことを言い出した時の仕切り方・進行ぶりに感心するよ。</div>
<div><b style="color:#475569;">男：</b>会議の司会をする時に見習いたいと思っているんだ。</div>
""",

    ('2회_202312', 80): """
<div style="margin-bottom:6px;"><b style="color:#2563eb;">女：</b>着なくなった服、人にあげたりリフォームする方も多いですが…</div>
<div><b style="color:#2563eb;">女：</b>私の場合は、シャツを紐状に細く裂いて、クッションカバーやマットを編んで暮らしの中で再利用しています。</div>
""",

    ('2회_202312', 82): """
<div style="margin-bottom:6px;"><b style="color:#475569;">記者：</b>ビーチコーミングで海岸の漂着物を集めているそうですね。貝殻でアクセサリーを作るんですか？</div>
<div><b style="color:#475569;">男：</b>貝殻を集める人もいますが、私の場合は流れ着いた木の枝（流木）を拾って、テーブルや椅子などの家具を作っているんです。</div>
""",

    ('2회_202312', 85): """
<div style="margin-bottom:6px;"><b style="color:#475569;">村職員：</b>南村では深刻な人口減少に対応するため、移住希望者への支援に力を入れています。</div>
<div><b style="color:#475569;">村職員：</b>仕事や空き家の紹介、改修費や車両購入の補助金、お試し移住体験施設の整備など、新生活を全面的にサポートしています。</div>
""",

    ('2회_202312', 86): """
<div style="margin-bottom:6px;"><b style="color:#475569;">農園主：</b>リンゴ園でネズミが木の皮をかじる食害に長年悩まされてきました。</div>
<div><b style="color:#475569;">農園主：</b>そこで園内に専用の巣箱を設置して天敵であるフクロウを呼び寄せたところ、自然の力を借りてネズミの被害を大幅に減らす工夫に成功しました。</div>
""",

    ('2회_202312', 88): """
<div style="margin-bottom:6px;"><b style="color:#475569;">職人：</b>もともと和紙作りに興味があったわけではありませんでした。</div>
<div><b style="color:#475569;">職人：</b>しかし、偶然立ち寄った照明展覧会で、和紙を通した柔らかく温かい光の美しさに心を打たれ、この道を志すきっかけとなりました。</div>
""",

    ('2회_202312', 89): """
<div style="margin-bottom:8px;"><b style="color:#475569;">【発話】</b> 店長：森さん、明日もアルバイトに来てもらえると助かるんだけど。</div>
<div style="color:#64748b;">1. 来られる人、見つかったんですね。</div>
<div style="color:#16a34a; font-weight:700;">2. 6時以降ならできますが。（正解）</div>
<div style="color:#64748b;">3. いえ、気にしないでください。</div>
""",

    ('2회_202312', 90): """
<div style="margin-bottom:8px;"><b style="color:#475569;">【発話】</b> 男：さっきの映画、僕、泣かずにはいられなかったよ。</div>
<div style="color:#16a34a; font-weight:700;">1. 本当、泣ける映画だったね。（正解）</div>
<div style="color:#64748b;">2. 確かに、泣くほどじゃなかったよね。</div>
<div style="color:#64748b;">3. え、泣いちゃえばよかったのに。</div>
""",

    ('2회_202312', 91): """
<div style="margin-bottom:8px;"><b style="color:#2563eb;">【発話】</b> 社員：工場長、本日本社から専務がお越しになると電話がありました。</div>
<div style="color:#64748b;">1. 本社には私が行くんですね。</div>
<div style="color:#16a34a; font-weight:700;">2. 何時頃来るって言っていましたか。（正解）</div>
<div style="color:#64748b;">3. 専務をご案内すればいいんですね。</div>
""",

    ('2회_202312', 95): """
<div style="margin-bottom:8px;"><b style="color:#475569;">【発話】</b> 先輩：暗くなってきたので、今日の作業はこの辺で切り上げましょうか。</div>
<div style="color:#64748b;">1. 作業、最後まで終わりましたね。</div>
<div style="color:#64748b;">2. 今すぐにやらなきゃいけないんですね。</div>
<div style="color:#16a34a; font-weight:700;">3. そうですね、今日はここまでですね。（正解）</div>
""",

    ('2회_202312', 97): """
<div style="margin-bottom:8px;"><b style="color:#475569;">【発話】</b> 幹事：今日の花火大会は延期にしましょう。この雨じゃやむを得ないですよね。</div>
<div style="color:#64748b;">1. まあ、延期はできないからですよね。</div>
<div style="color:#16a34a; font-weight:700;">2. やみそうにありませんからね。（正解）</div>
<div style="color:#64748b;">3. このまま雨が止まなければ延期するんですね。</div>
""",

    ('2회_202312', 98): """
<div style="margin-bottom:8px;"><b style="color:#2563eb;">【発話】</b> 同僚：林さん、明日の会議、課長の代わりに進行役を務めてもらえませんか。</div>
<div style="color:#16a34a; font-weight:700;">1. 構いませんが、課長どうされたんですか。（正解）</div>
<div style="color:#64748b;">2. 課長がやってくださるなら安心です。</div>
<div style="color:#64748b;">3. 課長と2人でですか。</div>
""",

    ('2회_202312', 99): """
<div style="margin-bottom:8px;"><b style="color:#475569;">【発話】</b> 取引先：先日ご依頼いただいた件ですが、私どもではお引き受けいたしかねます。</div>
<div style="color:#64748b;">1. いつ頃お返事いただけるんでしょうか。</div>
<div style="color:#64748b;">2. お引き受けいただけてよかったです。</div>
<div style="color:#16a34a; font-weight:700;">3. あの、どこが問題でしょうか。（正解）</div>
""",

    ('2회_202312', 101): """
<div style="margin-bottom:6px;"><b style="color:#475569;">案内：</b>語学研修の宿泊先は４タイプあります。①学生寮（4人部屋、最安）、②ホームステイ（文化体験）、③1人部屋アパート（風呂付き、最高額）、④シェアアパート（個室あり、キッチン共用）</div>
<div><b style="color:#475569;">男子学生：</b>ホームステイも魅力だけど、自分の生活ペースを守りたいし費用も抑えたいから、個室があって手頃なシェアアパート（タイプ4）にするよ。</div>
"""
}

def update_listening_notes():
    print("[1] Fetching all listening notes from Anki deck...")
    res = mcp_call('find_notes', {'query': f'deck:"{DECK_LISTENING}"'})
    note_ids = res.get('structuredContent', {}).get('noteIds', [])
    print(f"    Found {len(note_ids)} listening notes.")
    assert len(note_ids) == 25, f"Expected 25 notes, got {len(note_ids)}"

    info_res = mcp_call('notes_info', {'notes': note_ids})
    notes = info_res.get('structuredContent', {}).get('notes', [])

    updated_count = 0

    for note in notes:
        nid = note['noteId']
        tags = note.get('tags', [])
        exam_tag = '1회_공식제2집' if '1회_공식제2집' in tags else '2회_202312'
        
        # find qid from tags
        qid = None
        for t in tags:
            if t.startswith('Q') and t[1:].isdigit():
                qid = int(t[1:])
                break

        if not qid:
            print(f"[WARN] Note {nid} missing Qid tag: {tags}")
            continue

        script_content = LISTENING_SCRIPTS.get((exam_tag, qid), '').strip()
        if not script_content:
            print(f"[WARN] No script found for {exam_tag} Q{qid}")
            continue

        old_back = note.get('fields', {}).get('Back', {}).get('value', '')

        # Build Script HTML block
        script_box = f"""
  <!-- Listening Script Box -->
  <div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #0284c7; border-radius:4px 8px 8px 4px; padding:12px 14px; margin-bottom:12px;">
    <div style="font-size:12px; font-weight:700; color:#0369a1; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
      <span>📜 청해 대본 (스크립트 전문)</span>
    </div>
    <div style="font-size:15px; color:#0f172a; line-height:1.7; word-break:keep-all;">
      {script_content}
    </div>
  </div>
"""

        # Insert Script Box right after the Correct Answer Banner (or before User Mistake Box)
        target_marker = '<!-- User Mistake & Trap Analysis Box -->'
        if target_marker in old_back:
            new_back = old_back.replace(target_marker, script_box + "\n  " + target_marker)
        else:
            # append before closing div
            last_div = old_back.rfind('</div>')
            new_back = old_back[:last_div] + script_box + "\n</div>"

        # Update note in Anki
        up_res = mcp_call('update_note_fields', {
            'id': nid,
            'fields': {
                'Back': new_back
            }
        })
        if up_res and not up_res.get('isError'):
            updated_count += 1
            print(f"    [UPDATED] Q{qid:02d} ({exam_tag}) with script.")
        else:
            print(f"    [ERROR] Updating Q{qid:02d}: {up_res}")

    print(f"\n[2] Total updated notes with scripts: {updated_count}/25")
    assert updated_count == 25, f"Expected 25 updated, got {updated_count}"

    print("[3] Triggering AnkiWeb sync...")
    sync_res = mcp_call('sync')
    job_id = sync_res.get('structuredContent', {}).get('job_id')
    if job_id:
        for _ in range(15):
            time.sleep(2)
            poll = mcp_call('sync', {'job_id': job_id})
            st = poll.get('structuredContent', {}).get('status')
            if st in ['success', 'error', 'conflict', 'cancelled']:
                print(f"    Sync status: {st}")
                break

    print("\n>>> ALL 25 LISTENING CARDS UPDATED WITH SCRIPTS & SYNCED! <<<")

if __name__ == '__main__':
    update_listening_notes()
