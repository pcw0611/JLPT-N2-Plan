import re, sys

sys.stdout.reconfigure(encoding='utf-8')

OLD_SCRIPT_HTML = """<div style=\\"margin-bottom:10px; padding-bottom:8px; border-bottom:1px dashed #e2e8f0;\\">
  <div style=\\"font-size:14px; line-height:1.7; color:#0f172a; word-break:keep-all;\\"><b style=\'color:#475569;\'>男：</b>中村さん、青葉市の市民文化祭のことだけど、ステージ演奏の出演者募集に応募しようっていう話、２人でギター弾いて歌おうって言ってたやつね。事前選考のための演奏動画の作成が締め切りに間に合わないって諦めたよね。それ、僕の勘違いだったよ。ごめん。</div>
  <div style=\\"font-size:13px; line-height:1.6; color:#475569; margin-top:3px; word-break:keep-all;\\">↳ 남: 나카무라 씨, 아오바 시 시민문화제 말인데, 무대 연주 출연자 모집에 응모하자던 이야기, 둘이서 기타 치며 노래하자던 그거. 사전 심사용 연주 영상 제작이 마감에 늦을 것 같아 포기했었잖아. 그거 내 착각이었어. 미안.</div>
</div>
<div style=\\"margin-bottom:10px; padding-bottom:8px; border-bottom:1px dashed #e2e8f0;\\">
  <div style=\\"font-size:14px; line-height:1.7; color:#0f172a; word-break:keep-all;\\"><b style=\'color:#2563eb;\'>女：</b>え、どういうこと？</div>
  <div style=\\"font-size:13px; line-height:1.6; color:#475569; margin-top:3px; word-break:keep-all;\\">↳ 여: 어, 무슨 소리야?</div>
</div>
<div style=\\"margin-bottom:10px; padding-bottom:8px; border-bottom:1px dashed #e2e8f0;\\">
  <div style=\\"font-size:14px; line-height:1.7; color:#0f172a; word-break:keep-all;\\"><b style=\'color:#475569;\'>男：</b>応募の申請書を出すのが明日までで、動画は申請書を出したあと１週間以内に出せばいいって書いてあったんだ。申請書は先週もう作ってあるんだ。</div>
  <div style=\\"font-size:13px; line-height:1.6; color:#475569; margin-top:3px; word-break:keep-all;\\">↳ 남: 응모 신청서를 내는 게 내일까지고, 영상은 신청서를 낸 뒤 1주일 이내에 내면 된다고 써 있었어. 신청서는 지난주에 이미 다 써 놨거든.</div>
</div>
<div style=\\"margin-bottom:10px; padding-bottom:8px; border-bottom:1px dashed #e2e8f0;\\">
  <div style=\\"font-size:14px; line-height:1.7; color:#0f172a; word-break:keep-all;\\"><b style=\'color:#2563eb;\'>女：</b>本当？動画はあと１週間あるんだ。</div>
  <div style=\\"font-size:13px; line-height:1.6; color:#475569; margin-top:3px; word-break:keep-all;\\">↳ 여: 정말? 영상은 1주일 더 여유가 있는 거네.</div>
</div>
<div style=\\"margin-bottom:10px; padding-bottom:8px; border-bottom:1px dashed #e2e8f0;\\">
  <div style=\\"font-size:14px; line-height:1.7; color:#0f172a; word-break:keep-all;\\"><b style=\'color:#475569;\'>男：</b>うん。それで、今日中に申請書出せるかな？パソコンに残してあるよ。締め切り明日だから提出任せるね。</div>
  <div style=\\"font-size:13px; line-height:1.6; color:#475569; margin-top:3px; word-break:keep-all;\\">↳ 남: 응. 그래서 그런데, 오늘 중에 신청서 낼 수 있을까? 컴퓨터에 파일 저장해 뒀어. 마감이 내일까지니까 제출을 부탁해도 될까?</div>
</div>
<div style=\\"margin-bottom:10px; padding-bottom:8px; border-bottom:1px dashed #e2e8f0;\\">
  <div style=\\"font-size:14px; line-height:1.7; color:#0f172a; word-break:keep-all;\\"><b style=\'color:#2563eb;\'>女：</b>了解。じゃあ、今すぐ申請書確認して提出するね。動画の準備はそれからだね。</div>
  <div style=\\"font-size:13px; line-height:1.6; color:#475569; margin-top:3px; word-break:keep-all;\\">↳ 여: 알겠어. 그럼 내가 지금 바로 신청서 확인하고 제출할게. 영상 준비는 그다음부터 하자.</div>
</div>"""

NEW_SCRIPT_HTML = """<div style=\\"margin-bottom:10px; padding-bottom:8px; border-bottom:1px dashed #e2e8f0;\\">
  <div style=\\"font-size:14px; line-height:1.7; color:#0f172a; word-break:keep-all;\\"><b style=\'color:#475569;\'>男：</b>中村さん、青葉市の市民文化祭のことだけど、ステージ演奏の出演者募集に応募しようっていう話、２人でギター弾いて歌おうって言ってたやつね。事前選考のための演奏動画の作成が締め切りに間に合わないって諦めたよね。それ、僕の勘違いだったよ。ごめん。応募申請書と動画を同時に提出しなきゃいけないと思ってたんだけど、動画は申請書の締め切り後、１週間以内の提出だったんだ。</div>
  <div style=\\"font-size:13px; line-height:1.6; color:#475569; margin-top:3px; word-break:keep-all;\\">↳ 남: 나카무라 씨, 아오바 시 시민문화제 말인데, 무대 연주 출연자 모집에 응모하자던 이야기, 둘이서 기타 치며 노래하자던 그거. 사전 심사용 연주 영상 제작이 마감에 늦을 것 같아 포기했었잖아. 그거 내 착각이었어. 미안. 응모 신청서와 영상을 동시에 제출해야 하는 줄 알았는데, 영상은 신청서 마감 후 1주일 이내 제출이었어.</div>
</div>
<div style=\\"margin-bottom:10px; padding-bottom:8px; border-bottom:1px dashed #e2e8f0;\\">
  <div style=\\"font-size:14px; line-height:1.7; color:#0f172a; word-break:keep-all;\\"><b style=\'color:#2563eb;\'>女：</b>え、そうだったの？私もホームページ見たのに気がつかなかった。ごめんね。</div>
  <div style=\\"font-size:13px; line-height:1.6; color:#475569; margin-top:3px; word-break:keep-all;\\">↳ 여: 어, 그랬던 거야? 나도 홈페이지 봤는데 알아채지 못했네. 미안해.</div>
</div>
<div style=\\"margin-bottom:10px; padding-bottom:8px; border-bottom:1px dashed #e2e8f0;\\">
  <div style=\\"font-size:14px; line-height:1.7; color:#0f172a; word-break:keep-all;\\"><b style=\'color:#475569;\'>男：</b>うん。間に合いそうだから申し込もうよ。パソコンで申請書作ってくれたって言ってたけど、削除しちゃった？</div>
  <div style=\\"font-size:13px; line-height:1.6; color:#475569; margin-top:3px; word-break:keep-all;\\">↳ 남: 응. 시간 맞출 수 있을 것 같으니까 신청하자. 컴퓨터로 신청서 써 줬다고 했었는데, 삭제해 버렸어?</div>
</div>
<div style=\\"margin-bottom:10px; padding-bottom:8px; border-bottom:1px dashed #e2e8f0;\\">
  <div style=\\"font-size:14px; line-height:1.7; color:#0f172a; word-break:keep-all;\\"><b style=\'color:#2563eb;\'>女：</b>残してあるよ。</div>
  <div style=\\"font-size:13px; line-height:1.6; color:#475569; margin-top:3px; word-break:keep-all;\\">↳ 여: 남겨 뒀어.</div>
</div>
<div style=\\"margin-bottom:10px; padding-bottom:8px; border-bottom:1px dashed #e2e8f0;\\">
  <div style=\\"font-size:14px; line-height:1.7; color:#0f172a; word-break:keep-all;\\"><b style=\'color:#475569;\'>男：</b>じゃあ、それ使えるね。締め切り明日だから提出任せるね。</div>
  <div style=\\"font-size:13px; line-height:1.6; color:#475569; margin-top:3px; word-break:keep-all;\\">↳ 남: 그럼 그거 쓸 수 있겠네. 마감이 내일까지니까 제출 부탁할게.</div>
</div>
<div style=\\"margin-bottom:10px; padding-bottom:8px; border-bottom:1px dashed #e2e8f0;\\">
  <div style=\\"font-size:14px; line-height:1.7; color:#0f172a; word-break:keep-all;\\"><b style=\'color:#2563eb;\'>女：</b>了解。動画作成もすぐに取りかかんなきゃ。応募する以上は絶対出たいからね。</div>
  <div style=\\"font-size:13px; line-height:1.6; color:#475569; margin-top:3px; word-break:keep-all;\\">↳ 여: 알겠어. 영상 제작도 바로 시작해야겠네. 응모하는 이상은 꼭 나가고 싶으니까.</div>
</div>
<div style=\\"margin-bottom:10px; padding-bottom:8px; border-bottom:1px dashed #e2e8f0;\\">
  <div style=\\"font-size:14px; line-height:1.7; color:#0f172a; word-break:keep-all;\\"><b style=\'color:#0369a1;\'>問い：</b>女の学生はこの後まず何をしますか。</div>
  <div style=\\"font-size:13px; line-height:1.6; color:#475569; margin-top:3px; word-break:keep-all;\\">↳ 질문: 여학생은 이 후 우선 무엇을 합니까?</div>
</div>"""

files = [
    'jlpt-calendar-site/public/exams/n2-mock-error-review-pool.html',
    'quiz_sites/n2-mock-error-review-pool.html'
]

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if OLD_SCRIPT_HTML in content:
        content = content.replace(OLD_SCRIPT_HTML, NEW_SCRIPT_HTML)
        # Also update explanation text if needed
        old_exp_text = "【청해 해설】 남학생이 마감이 내일인 신청서 제출을 부탁했고, 여학생이 만들어 둔 파일이 컴퓨터에 남아있어 이를 바로 제출하기로 수락(了解)했습니다. 동영상 제작은 그 다음입니다."
        new_exp_text = "【청해 해설】 남학생이 마감이 내일인 신청서 제출을 부탁했고(締め切り明日だから提出任せるね), 여학생이 컴퓨터에 남아있는 기존 신청서를 제출하기로 수락(了解)했습니다. 영상 제작은 그 다음 단계이므로(動画作成もすぐに取りかかんなきゃ) 여학생이 가장 먼저 할 일은 '4번: 응모 신청서를 제출하는 것(応募申請書を提出する)'입니다."
        content = content.replace(old_exp_text, new_exp_text)

        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] Replaced in {fp}")
    else:
        print(f"[NOT FOUND] Target script not found in {fp}")
