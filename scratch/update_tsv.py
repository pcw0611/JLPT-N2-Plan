import sys, re

sys.stdout.reconfigure(encoding='utf-8')

for path in ['anki_error_notes_listening_25.tsv', 'scratch/anki_error_notes_listening_25.tsv']:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Old fake script part in TSV
    old_fragment = "え、どういうこと？"
    if old_fragment in content:
        # replace dialogue in Q76
        # Let's inspect where it is
        print(f"Found old fragment in {path}")
        # Let's replace the whole dialogue chunk in Q76
        # Let's see the old dialogue in TSV
        # In TSV, newlines in fields are <br>
        # Let's check how it's formatted
        lines = content.split('\n')
        for i, l in enumerate(lines):
            if '青葉市' in l:
                print(f"Line {i+1} has 青葉市")
                # Replace the dialogue
                # From: 男：中村さん、青葉市の市民文化祭のことだけど...
                # To: authentic dialogue
                # Let's find and replace
                old_part = "男：</b>中村さん、青葉市の市民文化祭のことだけど、ステージ演奏の出演者募集に応募しようっていう話、２人でギター弾いて歌おうって言ってたやつね。事前選考のための演奏動画の作成が締め切りに間に合わないって諦めたよね。それ、僕の勘違いだったよ。ごめん。</div> <div style=\"margin-bottom:6px;\"><b style=\"color:#2563eb;\">女：</b>え、どういうこと？</div> <div style=\"margin-bottom:6px;\"><b style=\"color:#475569;\">男：</b>応募の申請書を出すのが明日までで、動画は申請書を出したあと１週間以内に出せばいいって書いてあったんだ。申請書は先週もう作ってあるんだ。</div> <div style=\"margin-bottom:6px;\"><b style=\"color:#2563eb;\">女：</b>本当？動画はあと１週間あるんだ。</div> <div style=\"margin-bottom:6px;\"><b style=\"color:#475569;\">男：</b>うん。それで、今日中に申請書出せるかな？パソコンに残してあるよ。締め切り明日だから提出任せるね。</div> <div><b style=\"color:#2563eb;\">女：</b>了解。じゃあ、今すぐ申請書確認して提出するね。動画の準備はそれからだね。</div>"
                
                new_part = "男：</b>中村さん、青葉市の市民文化祭のことだけど、ステージ演奏の出演者募集に応募しようっていう話、２人でギター弾いて歌おうって言ってたやつね。事前選考のための演奏動画の作成が締め切りに間に合わないって諦めたよね。それ、僕の勘違いだったよ。ごめん。応募申請書と動画を同時に提出しなきゃいけないと思ってたんだけど、動画は申請書の締め切り後、１週間以内の提出だったんだ。</div> <div style=\"margin-bottom:6px;\"><b style=\"color:#2563eb;\">女：</b>え、そうだったの？私もホームページ見たのに気がつかなかった。ごめんね。</div> <div style=\"margin-bottom:6px;\"><b style=\"color:#475569;\">男：</b>うん。間に合いそうだから申し込もうよ。パソコンで申請書作ってくれたって言ってたけど、削除しちゃった？</div> <div style=\"margin-bottom:6px;\"><b style=\"color:#2563eb;\">女：</b>残してあるよ。</div> <div style=\"margin-bottom:6px;\"><b style=\"color:#475569;\">男：</b>じゃあ、それ使えるね。締め切り明日だから提出任せるね。</div> <div style=\"margin-bottom:6px;\"><b style=\"color:#2563eb;\">女：</b>了解。動画作成もすぐに取りかかんなきゃ。応募する以上は絶対出たいからね。</div> <div><b style=\"color:#0369a1;\">問い：</b>女の学生はこの後まず何をしますか。</div>"

                if old_part in l:
                    lines[i] = l.replace(old_part, new_part)
                    print(f"Successfully replaced in line {i+1}")
                else:
                    print("old_part exact match not found, inspecting line...")
                    # Let's inspect snippet
                    pos = l.find('青葉市')
                    print("Snippet around 青葉市:", repr(l[pos:pos+400]))

        new_content = '\n'.join(lines)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Saved {path}")
