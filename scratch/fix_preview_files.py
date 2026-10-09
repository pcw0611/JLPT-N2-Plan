import json, sys

sys.stdout.reconfigure(encoding='utf-8')

new_dialogue_block = """<div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #0284c7; border-radius:4px 8px 8px 4px; padding:12px 14px; margin-bottom:12px;">
    <div style="font-size:12px; font-weight:700; color:#0369a1; margin-bottom:8px;">📜 청해 대본 및 발화별 분석 (Verbatim Script)</div>
    <div style="background:#ffffff; padding:10px 12px; border-radius:6px; border:1px solid #e2e8f0; font-size:14px; line-height:1.65; color:#1e293b;">
      <div style="margin-bottom:6px;"><b style="color:#475569;">男：</b>中村さん、青葉市の市民文化祭のことだけど、ステージ演奏の出演者募集に応募しようっていう話、２人でギター弾いて歌おうって言ってたやつね。事前選考のための演奏動画の作成が締め切りに間に合わないって諦めたよね。それ、僕の勘違いだったよ。ごめん。応募申請書と動画を同時に提出しなきゃいけないと思ってたんだけど、動画は申請書の締め切り後、１週間以内の提出だったんだ。</div>
<div style="margin-bottom:6px;"><b style="color:#2563eb;">女：</b>え、そうだったの？私もホームページ見たのに気がつかなかった。ごめんね。</div>
<div style="margin-bottom:6px;"><b style="color:#475569;">男：</b>うん。間に合いそうだから申し込もうよ。パソコンで申請書作ってくれたって言ってたけど、削除しちゃった？</div>
<div style="margin-bottom:6px;"><b style="color:#2563eb;">女：</b>残してあるよ。</div>
<div style="margin-bottom:6px;"><b style="color:#475569;">男：</b>じゃあ、それ使えるね。締め切り明日だから提出任せるね。</div>
<div style="margin-bottom:6px;"><b style="color:#2563eb;">女：</b>了解。動画作成もすぐに取りかかんなきゃ。応募する以上は絶対出たいからね。</div>
<div><b style="color:#0369a1;">問い：</b>女の学生はこの後まず何をしますか。</div>
    </div>
  </div>"""

for path in ['scratch/final_updated_cards.json', 'scratch/updated_cards_preview.json']:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for item in data:
        back = item.get('back', '')
        if '青葉市' in back:
            # find the listening script box
            start_tag = '<div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #0284c7;'
            end_tag = '</div>\n  </div>'
            s_pos = back.find(start_tag)
            if s_pos != -1:
                # find end
                # Look for the next section: <!-- User Mistake & Trap Analysis Box -->
                next_box = '<!-- User Mistake & Trap Analysis Box -->'
                e_pos = back.find(next_box, s_pos)
                if e_pos != -1:
                    # replace between s_pos and e_pos
                    item['back'] = back[:s_pos] + new_dialogue_block + "\n\n  " + back[e_pos:]
                    print(f"Updated {path}!")
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("All preview files updated.")
