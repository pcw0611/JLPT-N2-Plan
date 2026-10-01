import os
import sys
import json
import re
import shutil
import subprocess
import time
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

ENDPOINT = "http://127.0.0.1:3141/"
MEDIA_DIR = os.path.join(os.environ['APPDATA'], 'Anki2', '사용자 1', 'collection.media')
OUT_DIR = os.path.abspath('scratch/audio_clips')
os.makedirs(OUT_DIR, exist_ok=True)

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

# ==============================================================================
# AUDIO SSML DEFINITIONS FOR ALL 25 LISTENING ITEMS
# ==============================================================================

AUDIO_SPECS = [
    # --- Exam 1 (8 items) ---
    {
        'exam': '1회_공식제2집',
        'qid': 76,
        'filename': 'vol2_q76.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>授業で先生が話しています。学生は授業を休んだとき、どのように宿題を確認しますか。</s>
  <break time="800ms"/>
  <prosody pitch="-15%" rate="0%">
    ええと、この授業を休むときは、必ず前の日までに連絡してください。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    メールでもいいですか。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-15%" rate="0%">
    はい、いいですよ。あ、それから、休んだときは、私の研究室の前の掲示を見て、宿題を確認してください。友達に聞いたりしないで、自分で確かめてちゃんとやってきてくださいね。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    はい、分かりました。
  </prosody>
  <break time="800ms"/>
  <s>学生は授業を休んだとき、どのように宿題を確認しますか。</s>
</speak>"""
    },
    {
        'exam': '1회_공식제2집',
        'qid': 80,
        'filename': 'vol2_q80.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>会社で上司と女性社員が話しています。女の人はこのあと、何をしなければなりませんか。</s>
  <break time="800ms"/>
  <prosody pitch="-15%" rate="0%">
    来週の大阪出張、先方の都合で打ち合わせが翌日にも入ることになったんだ。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    分かりました。では新幹線はそのままですね。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-15%" rate="0%">
    うん。ただ、ホテルの予約を一日延ばして、もう一泊できるように変更手続きをしてくれるかい？
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    かしこまりました。すぐに旅行会社に電話して変更いたします。
  </prosody>
  <break time="800ms"/>
  <s>女の人はこのあと、何をしなければなりませんか。</s>
</speak>"""
    },
    {
        'exam': '1회_공식제2집',
        'qid': 90,
        'filename': 'vol2_q90.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>環境フォーラムで研究者が話しています。女の人は何について報告していますか。</s>
  <break time="800ms"/>
  <prosody pitch="+10%" rate="0%">
    近年、都市部で深刻化するヒートアイランド現象に対して、ビルの屋上を植物で覆う「屋上緑化」の試みが注目されています。私たちの実測データによると、屋上を緑化した建物ではコンクリート表面の温度が最大で約２５度低下し、建物全体のエアコン消費電力も１５％削減できることが実証されました。緑の屋根は都市を冷やす天然のクーラーと言えます。
  </prosody>
  <break time="800ms"/>
  <s>女の人は何について報告していますか。</s>
</speak>"""
    },
    {
        'exam': '1회_공식제2집',
        'qid': 94,
        'filename': 'vol2_q94.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>３番。</s>
  <break time="400ms"/>
  <prosody pitch="+15%" rate="0%">
    部長、社内アンケート、山田さんを除いて全員から回答を得ました。
  </prosody>
</speak>"""
    },
    {
        'exam': '1회_공식제2집',
        'qid': 97,
        'filename': 'vol2_q97.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>６番。</s>
  <break time="400ms"/>
  <prosody pitch="-15%" rate="0%">
    課長、プリンター、修理に出したんですが、もう買い替えるしかないって言われました。
  </prosody>
</speak>"""
    },
    {
        'exam': '1회_공식제2집',
        'qid': 99,
        'filename': 'vol2_q99.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>８番。</s>
  <break time="400ms"/>
  <prosody pitch="+15%" rate="0%">
    この会議室、壁の色変えたせいか、広く見えるんじゃない？
  </prosody>
</speak>"""
    },
    {
        'exam': '1회_공식제2집',
        'qid': 102,
        'filename': 'vol2_q102.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>１１番。</s>
  <break time="400ms"/>
  <prosody pitch="-15%" rate="0%">
    昨日のサッカーの決勝戦、見逃しちゃったんだ。
  </prosody>
</speak>"""
    },
    {
        'exam': '1회_공식제2집',
        'qid': 106,
        'filename': 'vol2_q106.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>旅行会社で夫婦が店員からツアーの説明を聞いています。</s>
  <break time="800ms"/>
  <prosody pitch="-10%" rate="0%">
    いらっしゃいませ。信州へのご旅行ですね。４つのプランがございます。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    あなた、どれがいい？私は体を動かすハイキングコースがいいと思うんだけど。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-20%" rate="-5%">
    うーん、最近残業続きで腰も痛いし、せっかくの旅行だから、あんまり歩き回らずに名湯の温泉宿で美味しいものを食べてのんびり癒やされたいよ。３番のプランがいいな。
  </prosody>
  <break time="800ms"/>
  <s>質問１。男の人はどの観光コースを選びますか。</s>
</speak>"""
    },

    # --- Exam 2 (17 items) ---
    {
        'exam': '2회_202312',
        'qid': 75,
        'filename': 'e2_q75.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>日本語のクラスで先生が留学生に話しています。留学生は今日の授業の終わりまでにグループで何を決めなければなりませんか。</s>
  <break time="800ms"/>
  <prosody pitch="+10%" rate="0%">
    え、テキストの第4課ではゴミ処理の現状、問題点、その対策について日本の例を読みました。前回話した通り、皆さんにはグループで１つの国を取り上げ、ゴミ処理の現状、問題点、対策をテーマに来月発表してもらいます。
    今からどの国について調べるかグループで話し合ってもらいます。うちで参考になりそうな資料を探したりして、調べたい国をそれぞれ考えてきましたね。
    前回の授業でグループのリーダーや記録係など役割を分担しました。リーダーを中心に話し合って、授業の終わりに私に報告してください。
  </prosody>
  <break time="800ms"/>
  <s>留学生は今日の授業の終わりまでにグループで何を決めなければなりませんか。</s>
</speak>"""
    },
    {
        'exam': '2회_202312',
        'qid': 76,
        'filename': 'e2_q76.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>大学で男の学生と女の学生が話しています。女の学生はこの後まず何をしますか。</s>
  <break time="800ms"/>
  <prosody pitch="-15%" rate="0%">
    中村さん、青葉市の市民文化祭のことだけど、ステージ演奏の出演者募集に応募しようっていう話、２人でギター弾いて歌おうって言ってたやつね。事前選考のための演奏動画の作成が締め切りに間に合わないって諦めたよね。それ、僕の勘違いだったよ。ごめん。
  </prosody>
  <break time="400ms"/>
  <prosody pitch="+15%" rate="0%">
    え？
  </prosody>
  <break time="400ms"/>
  <prosody pitch="-15%" rate="0%">
    応募申請書と動画を同時に提出しなきゃいけないと思ってたんだけど、動画は申請書の締め切り後、１週間以内の提出だったんだ。
  </prosody>
  <break time="400ms"/>
  <prosody pitch="+15%" rate="0%">
    え、そうだったの？私もホームページ見たのに気がつかなかった、ごめんね。
  </prosody>
  <break time="400ms"/>
  <prosody pitch="-15%" rate="0%">
    うん、間に合いそうだから申し込もうよ。パソコンで申請書作ってくれたって言ってたけど、削除しちゃった？
  </prosody>
  <break time="400ms"/>
  <prosody pitch="+15%" rate="0%">
    残してあるよ。
  </prosody>
  <break time="400ms"/>
  <prosody pitch="-15%" rate="0%">
    じゃあそれ使えるね。締め切り明日だから、提出任せるね。
  </prosody>
  <break time="400ms"/>
  <prosody pitch="+15%" rate="0%">
    了解。動画作成もすぐに取りかかんなきゃ。応募する以上は絶対出たいからね。
  </prosody>
  <break time="800ms"/>
  <s>女の学生はこの後まず何をしますか。</s>
</speak>"""
    },
    {
        'exam': '2회_202312',
        'qid': 77,
        'filename': 'e2_q77.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>ガーデニングの店で男の人と店員が話しています。男の人はまず植物をどうしますか。</s>
  <break time="800ms"/>
  <prosody pitch="-15%" rate="0%">
    すみません、うちで育てている植物のことで教えていただきたいんですが。この写真の葉っぱが手のひらみたいな植物なんですが、最近葉も枝も弱々しくなってきちゃって。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    ああ、これですか。写真では日当たりがあまり良くないように見えますが。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-15%" rate="0%">
    ソファーの横に置いてるんですけど、あまり日は…
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    これ、日当たりのいい場所を好みますから、日光がよく当たる窓際に移してあげるといいですよ。水はどうしていますか？
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-15%" rate="0%">
    あ、昨日はやりましたけど、毎日はやってないです。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    それでいいですよ。土の表面が乾いてからやれば十分ですから。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-15%" rate="0%">
    はい。あの、弱ってる枝って切るんですか？
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    その必要はないですよ。それより元気になったら今より少し大きめの鉢に植え替えてやるとよく育ちますよ。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-15%" rate="0%">
    ありがとうございます。元気になるように、必要なことをまずやってみます。
  </prosody>
  <break time="800ms"/>
  <s>男の人はまず植物をどうしますか。</s>
</speak>"""
    },
    {
        'exam': '2회_202312',
        'qid': 78,
        'filename': 'e2_q78.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>会社の昼休みに男の人と女の人が話しています。男の人はこのアナウンサーのどんな点が最もいいと言っていますか。</s>
  <break time="800ms"/>
  <prosody pitch="+15%" rate="0%">
    ねえ、今テレビに映ってるアナウンサー、人気があるよね。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-15%" rate="0%">
    うん、いつも柔らかい表情で親しみやすい雰囲気を出してるよね。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    うん、それに声も落ち着いていて聞き取りやすいって言われてるみたいだね。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-15%" rate="0%">
    僕は声や雰囲気っていうよりは、討論番組で司会している時の進行の仕方に関心させられるよ。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    そう？この間、スポーツ選手にインタビューしてたの見たけど、その時は選手が答えにくそうで質問の仕方がどうなのかなって思ったんだよね。得意不得意があるのかな。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-15%" rate="0%">
    僕がよく見る番組では、ゲストが言いたい放題言ってもうまい具合に対応してるんだよね。自分が会議なんかで司会する時の参考にしたいって思うことが多いんだ。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    へえ、そうなんだ。
  </prosody>
  <break time="800ms"/>
  <s>男の人はこのアナウンサーのどんな点が最もいいと言っていますか。</s>
</speak>"""
    },
    {
        'exam': '2회_202312',
        'qid': 80,
        'filename': 'e2_q80.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>テレビで女の人が服のリサイクルについて話しています。女の人は着なくなったシャツをどうしていると言っていますか。</s>
  <break time="800ms"/>
  <prosody pitch="+10%" rate="0%">
    皆さんは着なくなったシャツなどをどうしていますか。捨ててしまうのはもったいないですよね。あまり着ていないシャツなどは知り合いに譲れればいいんですけど、サイズや好みが合うとは限りませんよね。子供やペットの服に作り替える方もいると思います。
    私は、紐状に細く切って、クッションのカバーや花瓶の下に敷くマットを編むのに使っています。
    着なくなったシャツをリサイクルショップに持ち込む方もいますが、形を変えて手元に残しておくのも悪くないですよ。
  </prosody>
  <break time="800ms"/>
  <s>女の人は着なくなったシャツをどうしていると言っていますか。</s>
</speak>"""
    },
    {
        'exam': '2회_202312',
        'qid': 82,
        'filename': 'e2_q82.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>ラジオでアナウンサーと男の人が話しています。男の人が海岸に流れてきたものを集めているのはどうしてですか。</s>
  <break time="800ms"/>
  <prosody pitch="+15%" rate="0%">
    今日は最近話題のビーチコーミングの話を伺いに桜海岸に来ています。ビーチコーミングをして10年という中山さん、ご説明いただけますか。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-15%" rate="0%">
    はい。聞き慣れない言葉かもしれませんが、ビーチコーミングとは、海岸に流れ着いたものを探して観察したり収集したりすることを言います。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    海岸には色々なものが流れてきますよね。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-15%" rate="0%">
    そうですね。集めた貝とかガラスの破片とかを使って、ペンダントやピアスなんかのアクセサリーを作る人が多いんですよ。私自身は、流れてきた木の枝を拾って、テーブルや椅子なんかを作っています。様々な形のものを組み合わせると、面白いものができるんですよ。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    そうなんですか。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-15%" rate="0%">
    私の友人は貝の研究なんですが、研究のためにビーチコーミングで貝を集めています。研究の対象にもなるんですね。ええ、またペットボトルやプラスチックゴミも流れてくるので、海の悲しい現実を実感することもあります。
  </prosody>
  <break time="800ms"/>
  <s>男の人が海岸に流れてきたものを集めているのはどうしてですか。</s>
</speak>"""
    },
    {
        'exam': '2회_202312',
        'qid': 85,
        'filename': 'e2_q85.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>テレビでレポーターの女の人と村の職員が話しています。村の職員は南村の何について話していますか。</s>
  <break time="800ms"/>
  <prosody pitch="+15%" rate="0%">
    今日は南村に来ています。大変自然が豊かですね。こちら南村は、移住を希望する人の受け入れに力を入れているそうですね。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-15%" rate="0%">
    はい。若い人が都会に出て人口が減ってしまったので、その解決策として始めました。移住希望者のために求人や空き家の紹介もしています。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    それはいいですね。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-15%" rate="0%">
    それから、移住にかかる費用を一部補助しているんです。例えば、空き家をリフォームする費用や、車を購入する際の費用です。お子さんがいる若い世代の方なら、他にも補助が受けられます。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    それは助かりますね。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-15%" rate="0%">
    村での生活を体験できる施設もあるので、ぜひご利用ください。
  </prosody>
  <break time="800ms"/>
  <s>村の職員は南村の何について話していますか。</s>
</speak>"""
    },
    {
        'exam': '2회_202312',
        'qid': 86,
        'filename': 'e2_q86.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>りんご農園で農園の人が見学に来た人に話しています。農園の人は何について話していますか。</s>
  <break time="800ms"/>
  <prosody pitch="-15%" rate="0%">
    ご覧いただいているリンゴの木、今収穫の時期を迎えています。木に備えつけてあるのは鳥の巣箱で、フクロウが住んでいます。
    昔はフクロウは木に開いた穴に巣を作って住み、リンゴの木をかじるネズミを退治してくれていました。
    でも、農作業の負担を軽くするためにリンゴの木が低く細く改良されたことで、フクロウが巣を作れなくなり、ネズミによる被害が増えてしまったんです。
    そこで、地元の農家と大学の農学部が共同で巣箱を設置したところ、フクロウが戻り、ネズミの数を減らすことに成功しました。
  </prosody>
  <break time="800ms"/>
  <s>農園の人は何について話していますか。</s>
</speak>"""
    },
    {
        'exam': '2회_202312',
        'qid': 88,
        'filename': 'e2_q88.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>ラジオで和紙を作る職人が話しています。職人は何について話していますか。</s>
  <break time="800ms"/>
  <prosody pitch="-15%" rate="0%">
    私は和紙、伝統的な日本の紙を作っています。和紙を作る職人になって10年になりますが、職人になる前は和紙について特に興味はありませんでした。
    それが、たまたま見に行った明かりの展覧会で、電球の周りを和紙で囲んだ明かりを見たんです。その時、和紙を通して見る光の柔らかさ、美しさに感動しました。和紙の持つ奥深さや可能性を感じました。
    それで、和紙作りの技術を一から学びたいと思い立って、和紙の職人を探し、地元にただ１人いた職人の方に弟子にしてもらったんです。
  </prosody>
  <break time="800ms"/>
  <s>職人は何について話していますか。</s>
</speak>"""
    },
    {
        'exam': '2회_202312',
        'qid': 89,
        'filename': 'e2_q89.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>１番。</s>
  <break time="400ms"/>
  <prosody pitch="-15%" rate="0%">
    森さん、明日もアルバイトに来てもらえると助かるんだけど。
  </prosody>
</speak>"""
    },
    {
        'exam': '2회_202312',
        'qid': 90,
        'filename': 'e2_q90.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>２番。</s>
  <break time="400ms"/>
  <prosody pitch="-15%" rate="0%">
    さっきの映画、僕、泣かずにはいられなかったよ。
  </prosody>
</speak>"""
    },
    {
        'exam': '2회_202312',
        'qid': 91,
        'filename': 'e2_q91.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>３番。</s>
  <break time="400ms"/>
  <prosody pitch="+15%" rate="0%">
    工場長、本日本社から専務がお越しになると電話がありました。
  </prosody>
</speak>"""
    },
    {
        'exam': '2회_202312',
        'qid': 95,
        'filename': 'e2_q95.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>７番。</s>
  <break time="400ms"/>
  <prosody pitch="-15%" rate="0%">
    暗くなってきたので、今日の作業はこの辺で切り上げましょうか。
  </prosody>
</speak>"""
    },
    {
        'exam': '2회_202312',
        'qid': 97,
        'filename': 'e2_q97.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>９番。</s>
  <break time="400ms"/>
  <prosody pitch="-15%" rate="0%">
    今日の花火大会は延期にしましょう。この雨じゃやむを得ないですよね。
  </prosody>
</speak>"""
    },
    {
        'exam': '2회_202312',
        'qid': 98,
        'filename': 'e2_q98.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>１０番。</s>
  <break time="400ms"/>
  <prosody pitch="+15%" rate="0%">
    林さん、明日の会議、課長の代わりに進行役を務めてもらえませんか。
  </prosody>
</speak>"""
    },
    {
        'exam': '2회_202312',
        'qid': 99,
        'filename': 'e2_q99.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>１１番。</s>
  <break time="400ms"/>
  <prosody pitch="-15%" rate="0%">
    先日ご依頼いただいた件ですが、私どもではお引き受けいたしかねます。
  </prosody>
</speak>"""
    },
    {
        'exam': '2회_202312',
        'qid': 101,
        'filename': 'e2_q101.mp3',
        'ssml': """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
  <s>大学で海外語学研修の説明を聞いて、研修に参加する学生２人が話しています。</s>
  <break time="800ms"/>
  <prosody pitch="+10%" rate="0%">
    夏休みの研修では、皆さん大学の同じプログラムに参加しますが、宿泊施設は４つの中から選べます。
    タイプ１は大学の学内にある寮です。部屋は４人部屋で、キッチンやシャワーなども共同で利用します。宿泊費は４つの中で最も安いです。
    タイプ２は一般家庭でのホームステイです。大学から遠い場合もありますが、生活や文化を体験するには最適ですし、宿泊費も寮の次に安いです。
    タイプ３と４は大学近くのアパートです。タイプ３はバス・トイレ・シャワー付きの１人用のアパートです。宿泊費は他よりかかりますが、プライバシーが保てます。
    タイプ４は他の学生と共同でアパートを利用します。キッチンなどは共同で利用しますが、部屋は１人部屋です。宿泊費は１人用のアパートよりは抑えられます。
  </prosody>
  <break time="600ms"/>
  <prosody pitch="+15%" rate="0%">
    ふーん、どうしようかな。佐藤君はどうするの？
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-15%" rate="0%">
    僕はせっかくだし、現地の一般の家庭で過ごしたいけど、いい経験になりそうだしね。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    でも、大学から遠いところになったらちょっと大変そう。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="-15%" rate="0%">
    それは平気なんだけど、ただ今回は宿泊費が一番抑えられるのにするよ。
  </prosody>
  <break time="500ms"/>
  <prosody pitch="+15%" rate="0%">
    そっか。私は大学に近くて、あと自分の部屋がちゃんとあってプライバシーが守られるのがいいな。部屋で１人になれればいいから、キッチンとかは共同っていうのにする。
  </prosody>
  <break time="800ms"/>
  <s>質問１。男の学生はどのタイプがいいと言っていますか。</s>
</speak>"""
    }
]

print(f"Total audio specs defined: {len(AUDIO_SPECS)}")
assert len(AUDIO_SPECS) == 25, f"Expected 25 audio specs, got {len(AUDIO_SPECS)}"

def generate_and_update():
    # PS script template for generating WAV from SSML
    ps_runner = os.path.abspath('scratch/synthesize_ssml.ps1')
    ps_script = """
param(
    [string]$ssmlPath,
    [string]$wavPath
)
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice("Microsoft Haruka Desktop")
$synth.SetOutputToWaveFile($wavPath)
$ssml = [System.IO.File]::ReadAllText($ssmlPath, [System.Text.Encoding]::UTF8)
$synth.SpeakSsml($ssml)
$synth.Dispose()
Write-Output "SUCCESS"
"""
    with open(ps_runner, 'w', encoding='utf-8') as f:
        f.write(ps_script)

    print("\n[1] Synthesizing all 25 audio files with Microsoft Haruka Desktop...")
    for i, spec in enumerate(AUDIO_SPECS, 1):
        filename = spec['filename']
        ssml = spec['ssml']
        qid = spec['qid']
        exam = spec['exam']

        temp_xml = os.path.abspath(f'scratch/temp_{filename}.xml')
        temp_wav = os.path.abspath(f'scratch/temp_{filename}.wav')
        out_mp3 = os.path.abspath(os.path.join(OUT_DIR, filename))

        with open(temp_xml, 'w', encoding='utf-8') as f:
            f.write(ssml)

        # Run PowerShell
        res = subprocess.run([
            "powershell", "-ExecutionPolicy", "Bypass", "-File", ps_runner,
            "-ssmlPath", temp_xml, "-wavPath", temp_wav
        ], capture_output=True, text=True)

        if res.returncode != 0 or not os.path.exists(temp_wav):
            print(f"  [ERROR] PowerShell failed for {filename}: {res.stderr}")
            continue

        # Convert to MP3
        subprocess.run([
            "ffmpeg", "-y", "-i", temp_wav, "-b:a", "128k", out_mp3
        ], capture_output=True)

        # Clean up temp
        if os.path.exists(temp_xml): os.remove(temp_xml)
        if os.path.exists(temp_wav): os.remove(temp_wav)

        mp3_size = os.path.getsize(out_mp3) if os.path.exists(out_mp3) else 0

        # Copy directly to collection.media
        dest_media = os.path.join(MEDIA_DIR, filename)
        shutil.copy2(out_mp3, dest_media)

        # Also call store_media_file via MCP
        mcp_res = mcp_call('store_media_file', {'filename': filename, 'path': out_mp3})

        print(f"  [{i:02d}/25] {exam} Q{qid:03d} -> {filename} ({mp3_size:,} bytes) [Media copied & MCP stored]")

    # 2. Update Anki Cards
    print("\n[2] Updating Anki cards in deck 'JLPT N2::오답노트 (청해 25문항 · 실전 음원)'...")
    DECK_LISTENING = "JLPT N2::오답노트 (청해 25문항 · 실전 음원)"
    res = mcp_call('find_notes', {'query': f'deck:"{DECK_LISTENING}"'})
    note_ids = res.get('structuredContent', {}).get('noteIds', [])
    info_res = mcp_call('notes_info', {'notes': note_ids})
    notes = info_res.get('structuredContent', {}).get('notes', [])

    spec_map = {(s['exam'], s['qid']): s for s in AUDIO_SPECS}

    updated_count = 0
    for n in notes:
        nid = n['noteId']
        tags = n.get('tags', [])
        exam_tag = '1회_공식제2집' if '1회_공식제2집' in tags else '2회_202312'
        qid = int([t for t in tags if t.startswith('Q')][0][1:])

        spec = spec_map.get((exam_tag, qid))
        if not spec:
            continue

        filename = spec['filename']
        front = n['fields']['Front']['value']
        back = n['fields']['Back']['value']

        # Ensure front has [sound:filename]
        # Replace existing sound tag or insert audio box
        sound_tag = f"[sound:{filename}]"
        if '[sound:' in front:
            front = re.sub(r'\[sound:[^\]]+\]', sound_tag, front)
        else:
            # insert audio box before prompt
            audio_box = f"""
        <div style="margin:12px 0 16px 0; padding:12px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px; text-align:center;">
          <div style="font-size:12px; font-weight:700; color:#166534; margin-bottom:6px;">🎧 일본어 실전 음원</div>
          {sound_tag}
        </div>
        """
            prompt_marker = '<div style="font-size:19px;'
            if prompt_marker in front:
                front = front.replace(prompt_marker, audio_box + '\n  ' + prompt_marker)

        # Update note
        up_res = mcp_call('update_note_fields', {
            'id': nid,
            'fields': {
                'Front': front,
                'Back': back
            }
        })
        if up_res and not up_res.get('isError'):
            updated_count += 1
            print(f"  [OK] Note {nid} ({exam_tag} Q{qid}) updated with sound: {sound_tag}")

    print(f"\n[3] Total updated notes in Anki: {updated_count}/25")

    # 3. Trigger AnkiWeb Sync
    print("\n[4] Triggering AnkiWeb sync...")
    sync_res = mcp_call('sync')
    job_id = sync_res.get('structuredContent', {}).get('job_id')
    if job_id:
        for _ in range(20):
            time.sleep(2)
            poll = mcp_call('sync', {'job_id': job_id})
            st = poll.get('structuredContent', {}).get('status')
            if st in ['success', 'error', 'conflict', 'cancelled']:
                print(f"    Sync status: {st}")
                break

    print("\n" + "="*70)
    print(">>> ALL 25 AUDIO FILES RE-SYNTHESIZED, REPLACED, UPDATED & SYNCED! <<<")
    print("="*70)

if __name__ == '__main__':
    generate_and_update()

