import sys

sys.stdout.reconfigure(encoding='utf-8')

# Target in anki_error_notes_listening_25.tsv:
# Replace the old lines with exact verbatim lines
with open('anki_error_notes_listening_25.tsv', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace in anki_error_notes_listening_25.tsv
old_pattern = """<div style="margin-bottom:6px;"><b style="color:#475569;">男：</b>中村さん、青葉市の市民文化祭のことだけど、ステージ演奏の出演者募集に応募しようっていう話、２人でギター弾いて歌おうって言ってたやつね。事前選考のための演奏動画の作成が締め切りに間に合わないって諦めたよね。それ、僕の勘違いだったよ。ごめん。</div><br><div style="margin-bottom:6px;"><b style="color:#2563eb;">女：</b>え？</div><br><div style="margin-bottom:6px;"><b style="color:#475569;">男：</b>応募申請書と動画を同時に提出しなきゃいけないと思ってたんだけど、動画は申請書の締め切り後、１週間以内の提出だったんだ。</div><br><div style="margin-bottom:6px;"><b style="color:#2563eb;">女：</b>え、そうだったの？私もホームページ見たのに気がつかなかった、ごめんね。</div><br><div style="margin-bottom:6px;"><b style="color:#475569;">男：</b>うん、間に合いそうだから申し込もうよ。パソコンで申請書作ってくれたって言ってたけど、削除しちゃった？</div><br><div style="margin-bottom:6px;"><b style="color:#2563eb;">女：</b>残してあるよ。</div><br><div style="margin-bottom:6px;"><b style="color:#475569;">男：</b>じゃあそれ使えるね。締め切り明日だから、提出任せるね。</div><br><div><b style="color:#2563eb;">女：</b>了解。動画作成もすぐに取りかかんなきゃ。応募する以上は絶対出たいからね。</div>"""

new_pattern = """<div style="margin-bottom:6px;"><b style="color:#475569;">男：</b>中村さん、青葉市の市民文化祭のことだけど、ステージ演奏の出演者募集に応募しようっていう話、２人でギター弾いて歌おうって言ってたやつね。事前選考のための演奏動画の作成が締め切りに間に合わないって諦めたよね。それ、僕の勘違いだったよ。ごめん。応募申請書と動画を同時に提出しなきゃいけないと思ってたんだけど、動画は申請書の締め切り後、１週間以内の提出だったんだ。</div><br><div style="margin-bottom:6px;"><b style="color:#2563eb;">女：</b>え、そうだったの？私もホームページ見たのに気がつかなかった。ごめんね。</div><br><div style="margin-bottom:6px;"><b style="color:#475569;">男：</b>うん。間に合いそうだから申し込もうよ。パソコンで申請書作ってくれたって言ってたけど、削除しちゃった？</div><br><div style="margin-bottom:6px;"><b style="color:#2563eb;">女：</b>残してあるよ。</div><br><div style="margin-bottom:6px;"><b style="color:#475569;">男：</b>じゃあ、それ使えるね。締め切り明日だから提出任せるね。</div><br><div style="margin-bottom:6px;"><b style="color:#2563eb;">女：</b>了解。動画作成もすぐに取りかかんなきゃ。応募する以上は絶対出たいからね。</div><br><div><b style="color:#0369a1;">問い：</b>女の学生はこの後まず何をしますか。</div>"""

if old_pattern in text:
    text = text.replace(old_pattern, new_pattern)
    with open('anki_error_notes_listening_25.tsv', 'w', encoding='utf-8') as f:
        f.write(text)
    print("[OK] Replaced in anki_error_notes_listening_25.tsv")
else:
    print("[WARN] old_pattern not found directly, checking partial replacement...")
    # Find start and end in line 10
    lines = text.split('\n')
    for idx, line in enumerate(lines):
        if '青葉市' in line:
            start_tag = '<div style="margin-bottom:6px;"><b style="color:#475569;">男：</b>中村さん、青葉市'
            end_tag = '絶対出たいからね。</div>'
            s_pos = line.find(start_tag)
            e_pos = line.find(end_tag)
            if s_pos != -1 and e_pos != -1:
                e_pos += len(end_tag)
                line = line[:s_pos] + new_pattern + line[e_pos:]
                lines[idx] = line
                print(f"[OK] Replaced in line {idx+1}")
    text = '\n'.join(lines)
    with open('anki_error_notes_listening_25.tsv', 'w', encoding='utf-8') as f:
        f.write(text)

# Also update scratch/anki_error_notes_listening_25.tsv if present
try:
    with open('scratch/anki_error_notes_listening_25.tsv', 'r', encoding='utf-8') as f:
        s_text = f.read()
    s_lines = s_text.split('\n')
    for idx, line in enumerate(s_lines):
        if '青葉市' in line:
            start_tag = '男：</b>中村さん、青葉市'
            end_tag = '絶対出たいからね。</div>'
            s_pos = line.find('男：</b>中村さん、青葉市')
            e_pos = line.find('絶対出たいからね。</div>')
            if s_pos != -1 and e_pos != -1:
                # find opening <div before s_pos
                div_pos = line.rfind('<div', 0, s_pos)
                e_pos += len(end_tag)
                line = line[:div_pos] + new_pattern + line[e_pos:]
                s_lines[idx] = line
                print(f"[OK] Replaced in scratch/anki_error_notes_listening_25.tsv line {idx+1}")
    with open('scratch/anki_error_notes_listening_25.tsv', 'w', encoding='utf-8') as f:
        f.write('\n'.join(s_lines))
except Exception as e:
    print(f"Error updating scratch TSV: {e}")
