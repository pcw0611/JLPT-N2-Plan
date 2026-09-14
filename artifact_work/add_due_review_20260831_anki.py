"""Add the 16 weak items from the 2026-08-31 due review to Anki via local MCP."""
from __future__ import annotations

import json
import urllib.request

ENDPOINT = "http://127.0.0.1:3141/"
DECK = "JLPT N2::오늘 오답 2026-08-31"
MODEL = "Basic"
COMMON_TAGS = ["JLPT_N2", "due_review_20260831", "self_made_due_review"]


def mcp(method: str, params: dict, request_id: int) -> dict:
    data = json.dumps({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}, ensure_ascii=False).encode()
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        body = response.read().decode("utf-8")
    line = next(line for line in body.splitlines() if line.startswith("data: "))
    payload = json.loads(line[6:])
    if "error" in payload:
        raise RuntimeError(payload["error"])
    return payload["result"]


def tool(name: str, arguments: dict, request_id: int) -> dict:
    result = mcp("tools/call", {"name": name, "arguments": arguments}, request_id)
    if result.get("isError"):
        raise RuntimeError(result)
    if "structuredContent" in result:
        return result["structuredContent"]
    text = next(part["text"] for part in result.get("content", []) if part.get("type") == "text")
    return json.loads(text)


def front(item: int, label: str, instruction: str, prompt: str, choices: list[str]) -> str:
    options = "".join(f'<div style="padding:7px 0">{i}. {choice}</div>' for i, choice in enumerate(choices, 1))
    return f'''<!-- due-review-20260831-item-{item:02d} -->
<div style="color:#6b7280;font-size:13px">復習 {item:02d} · {label}</div>
<div style="color:#52606d;margin:10px 0 16px">{instruction}</div>
<div style="font-size:24px;line-height:1.65;margin-bottom:15px">{prompt}</div>
<div style="font-size:17px;line-height:1.45">{options}</div>'''


def back(answer: str, completed: str, translation: str, connection: str, meaning: str,
         selected: str, trap: str, contrast: str, example: str, check: str) -> str:
    return f'''
<div style="font-size:13px;color:#52606d;font-weight:700">정답</div>
<div style="font-size:27px;font-weight:700;color:#173b2e;margin:6px 0 12px">{answer}</div>
<div style="font-size:20px;line-height:1.6">{completed}</div>
<div style="color:#5f6368;line-height:1.55;margin-top:5px">{translation}</div>
<hr style="border:0;border-top:1px solid #d6d9dc;margin:18px 0">
<div><b>접속</b>　{connection}</div>
<div style="margin-top:9px"><b>핵심 의미</b>　{meaning}</div>
<div style="margin-top:9px"><b>내 선택</b>　{selected}</div>
<div style="margin-top:9px"><b>함정</b>　{trap}</div>
<div style="margin-top:9px"><b>구별</b>　{contrast}</div>
<div style="margin-top:13px;font-size:19px">{example}</div>
<div style="margin-top:15px;padding:10px 12px;background:#e8f3ec;border-left:4px solid #2f6f50"><b>직전 체크</b>　{check}</div>'''


CARDS = [
    (4, "文の文法1", "（　）に入る最もよいものを一つ選んでください。",
     "このアプリは操作が簡単な（　）、無料で使える。", ["うえに", "うえで", "うえは", "あげく"],
     "うえに", "このアプリは操作が簡単なうえに、無料で使える。", "이 앱은 조작이 간단한 데다가 무료로 쓸 수 있다.",
     "普通形／ナAな＋うえに", "같은 방향의 정보를 하나 더 추가한다.", "うえで", "두 장점의 병렬을 절차로 읽었다.",
     "うえで=~한 뒤에, うえは=~한 이상, うえに=게다가", "この店は安いうえに、駅から近い。", "추가인가, 선후 관계인가?", "grammar", "uenI"),
    (5, "文の文法1", "（　）に入る最もよいものを一つ選んでください。",
     "今ちょうど、担当者が報告書を（　）ところです。", ["書く", "書いている", "書いた", "書かせる"],
     "書いている", "今ちょうど、担当者が報告書を書いているところです。", "지금 바로 담당자가 보고서를 쓰는 중이다.",
     "Vている＋ところ", "바로 지금 진행 중인 동작이다.", "書いた", "今ちょうど보다 완료형에 끌렸다.",
     "Vる=직전, Vている=진행 중, Vた=직후", "ただ今、確認しているところです。", "지금 전·중·후 중 어디인가?", "grammar", "tokoro"),
    (7, "文の文法1", "（　）に入る最もよいものを一つ選んでください。",
     "鍵が外からかかっている。中に人が（　）。", ["いるはずです", "いるはずがありません", "いないことがあります", "いるところです"],
     "いるはずがありません", "鍵が外からかかっている。中に人がいるはずがありません。", "열쇠가 밖에서 잠겨 있다. 안에 사람이 있을 리 없다.",
     "普通形＋はずがない", "객관적 근거에 비추어 불가능하다고 판단한다.", "分からない", "외부 잠금이라는 부정 근거를 문형에 연결하지 못했다.",
     "わけがない는 화자의 강한 확신, はずがない는 논리적 근거", "彼が約束を忘れるはずがない。", "앞 문장이 가능 근거인가, 불가능 근거인가?", "grammar", "hazu_ga_nai"),
    (8, "形容詞活用", "（　）に入る最もよいものを一つ選んでください。",
     "この町は昔ほど便利（　）。", ["ではありません", "ではありませんでした", "くありません", "ではなかったでした"],
     "ではありません", "この町は昔ほど便利ではありません。", "이 도시는 예전만큼 편리하지 않다.",
     "ナA＋ではありません", "な형용사의 현재 부정이다.", "ではありませんでした", "昔를 문장 전체의 과거 시제로 처리했다.",
     "현재 부정=ではありません, 과거 부정=ではありませんでした", "この部屋はあまり静かではありません。", "昔는 비교 기준일 뿐인가?", "adjective", "na_present_negative"),
    (15, "文の文法1", "（　）に入る最もよいものを一つ選んでください。",
     "安全性の観点（　）、この案をそのまま採用するのは難しい。", ["からといって", "からいうと", "からしても", "からには"],
     "からいうと", "安全性の観点からいうと、この案をそのまま採用するのは難しい。", "안전성 관점에서 이 안을 그대로 채택하기 어렵다.",
     "N＋からいうと", "특정 관점이나 측면을 기준으로 평가한다.", "からには", "직접 단서 観点보다 결심·의무 표현을 골랐다.",
     "からすると=근거→추측, からいうと=관점→평가", "費用の面からいうと、A案が現実的だ。", "관점·근거·결심 중 무엇인가?", "grammar", "kara_iu_to"),
    (17, "形容詞活用", "（　）に入る最もよいものを一つ選んでください。",
     "図書館の中は人が少なくて、とても（　）。", ["静かかった", "静かだった", "静かでしたか", "静かくなかった"],
     "静かだった", "図書館の中は人が少なくて、とても静かだった。", "도서관 안은 사람이 적어 매우 조용했다.",
     "ナA＋だった", "な형용사의 보통체 과거 긍정이다.", "静かかった", "静か를 い형용사처럼 활용했다.",
     "イA=高かった, ナA=静かだった", "昨日の駅前はにぎやかだった。", "사전형이 静かだ인가?", "adjective", "na_past"),
    (23, "文の文法1", "（　）に入る最もよいものを一つ選んでください。",
     "忙しくなると、連絡が遅れ（　）になる。", ["かけ", "がち", "がたい", "おき"],
     "がち", "忙しくなると、連絡が遅れがちになる。", "바빠지면 연락이 늦어지는 경향이 생긴다.",
     "Vます語幹＋がち", "바람직하지 않은 일이 자주 반복되는 경향이다.", "かけ", "반복 경향을 한 번의 미완료와 혼동했다.",
     "がち=반복 경향, かけ=미완료, 気味=현재 약간 그런 상태", "冬は運動不足になりがちだ。", "반복되는가, 하다 만 것인가?", "grammar", "gachi"),
    (24, "文の文法1", "（　）に入る最もよいものを一つ選んでください。",
     "半年も悩んだ（　）、会社を辞めて留学することにした。", ["うえに", "あげく", "おきに", "最中に"],
     "あげく", "半年も悩んだあげく、会社を辞めて留学することにした。", "반년이나 고민한 끝에 회사를 그만두고 유학하기로 했다.",
     "Vた＋あげく／Nの＋あげく", "긴 과정 끝에 결과에 이른다.", "うえに", "긴 과정과 결과를 단순 정보 추가로 읽었다.",
     "うえに=정보 추가, 末に=결과에 중립적, あげく=긴 과정 끝 결과", "何度も話し合ったあげく、計画は中止になった。", "과정 뒤 결과인가?", "grammar", "ageku"),
    (26, "敬語", "（　）に入る最もよいものを一つ選んでください。",
     "私は明日の午後、先生のお宅に（　）。", ["いらっしゃいます", "召し上がります", "伺います", "ご覧になります"],
     "伺います", "私は明日の午後、先生のお宅に伺います。", "저는 내일 오후 선생님 댁에 찾아뵙는다.",
     "行く／訪ねる→伺う（謙譲語）", "자기 행동을 낮추어 상대를 높인다.", "いらっしゃいます", "주어가 私인데 상대 행동의 존경어를 골랐다.",
     "伺う=내가 가다·방문하다, いらっしゃる=상대가 가다·오다·있다", "午後三時に御社へ伺います。", "누구의 행동을 높이거나 낮추는가?", "keigo", "ukagau"),
    (29, "文の文法1", "（　）に入る最もよいものを一つ選んでください。",
     "天気予報によると、明日は山で雪が（　）でしょう。", ["お降りになる", "降る", "降らせる", "伺う"],
     "降る", "天気予報によると、明日は山で雪が降るでしょう。", "예보에 따르면 내일 산에 눈이 내릴 것이다.",
     "雪が降る", "자연현상에는 일반 자동사를 사용한다.", "降らせる", "행위자 없는 자연현상에 사역형을 붙였다.",
     "降る=내리다, 降らせる=내리게 하다", "夜から雨が降るそうです。", "누가 누구에게 시키는 문장인가?", "grammar", "natural_event"),
    (30, "文の文法1", "（　）に入る最もよいものを一つ選んでください。",
     "この説明には、専門家でも理解し（　）点がある。", ["ないかぎりの", "がたい", "かけの", "がちの"],
     "がたい", "この説明には、専門家でも理解しがたい点がある。", "이 설명에는 전문가라도 이해하기 어려운 점이 있다.",
     "Vます語幹＋がたい＋N", "본질적·심리적으로 하기 어렵다.", "分からない", "뒤의 点을 수식할 형태를 만들지 못했다.",
     "がたい=추상적·강한 판단, にくい=물리적·일반적 난이도", "その行動には理解しがたい点が多い。", "빈칸 뒤 명사까지 연결되는가?", "grammar", "gatai"),
    (32, "敬語", "（　）に入る最もよいものを一つ選んでください。",
     "社長は会議で、計画を変更すると（　）。", ["申しました", "おっしゃいました", "伺いました", "いたしました"],
     "おっしゃいました", "社長は会議で、計画を変更するとおっしゃいました。", "사장님은 회의에서 계획을 바꾼다고 말씀하셨다.",
     "言う→おっしゃる（尊敬語）", "상대방의 말하기 동작을 높인다.", "いたしました", "동사 의미와 경어 방향을 함께 놓쳤다.",
     "おっしゃる=상대의 말하기, 申す=내 말하기, いたす=내 する", "先生は明日休むとおっしゃいました。", "주어가 높일 사람이고 원동사가 言う인가?", "keigo", "ossharu"),
    (34, "文の文法2", "文を完成させて、★に入るものを一つ選んでください。",
     "彼は何かを ＿＿ ★ ＿＿ ＿＿ 黙ってしまった。<br>【言い／かけた／が／急に】", ["言い", "かけた", "が", "急に"],
     "かけた", "彼は何かを言いかけたが、急に黙ってしまった。", "그는 무언가 말하려다가 갑자기 입을 다물었다.",
     "言い＋かけた＋が＋急に", "Vます語幹＋かける는 시작했지만 끝나지 않은 동작이다.", "言い", "전체 배열 전에 첫 조각을 ★로 골랐다.",
     "배열 문제는 문장 끝까지 완성한 뒤 ★ 위치를 확인한다.", "彼女は話し始めかけたが、やめた。", "네 조각을 모두 놓은 뒤 ★를 봤는가?", "grammar", "sentence_order"),
    (38, "聴解・課題理解（文字復習）", "手順を読んで、最初にすることを一つ選んでください。",
     "まず入口で番号札を取ります。次に申込書を書きます。記入後、二階の窓口へ行って、最後に料金を払います。", ["申込書を書く", "二階の窓口へ行く", "番号札を取る", "料金を払う"],
     "番号札を取る", "最初に、入口で番号札を取ります。", "가장 먼저 입구에서 번호표를 뽑는다.",
     "まず→次に→記入後→最後に", "순서표지를 행동과 묶어 첫 행동을 찾는다.", "二階の窓口へ行く", "이후 목적지를 첫 행동으로 골랐다.",
     "이 카드는 청취가 아닌 순서표지 문자 복습이다.", "まず番号札を取り、次に用紙を書きます。", "질문이 최초·다음·마지막 중 무엇을 묻는가?", "listening_task_text", "first_action"),
    (39, "聴解・課題理解（文字復習）", "手順を読んで、最初にすることを一つ選んでください。",
     "講座に参加する方は、最初に受付で用紙をもらいます。名前を記入してから会場に入ります。参加費は最後に払います。", ["参加費を払う", "受付で用紙をもらう", "会場に入る", "名前を呼ばれる"],
     "受付で用紙をもらう", "最初に、受付で用紙をもらいます。", "가장 먼저 접수처에서 용지를 받는다.",
     "最初に→〜てから→最後に", "선택지가 실제 대본에 있고 첫 순서표지와 연결되는지 본다.", "名前を呼ばれる", "대본에 없는 수동 행동을 선택했다.",
     "이 카드는 청취가 아닌 순서표지 문자 복습이다.", "最初に受付で用紙をもらってください。", "선택지가 실제로 제시됐고 最初に와 연결됐는가?", "listening_task_text", "reception_order"),
    (40, "聴解・課題理解（文字復習）", "手順を読んで、最初にすることを一つ選んでください。",
     "お客様が来る前に、まず窓を開けます。それからテーブルを拭きます。コーヒーはお客様が着いてから入れます。", ["窓を開ける", "テーブルを拭く", "コーヒーを入れる", "客に電話する"],
     "窓を開ける", "最初に、窓を開けます。", "가장 먼저 창문을 연다.",
     "まず→それから→〜てから", "각 행동 앞의 순서표지를 유지한다.", "テーブルを拭く", "두 번째 행동을 첫 행동으로 골랐다.",
     "이 카드는 청취가 아닌 순서표지 문자 복습이다.", "まず資料を配って、それから窓を閉めてください。", "선택한 행동 앞 표지가 まず인가?", "listening_task_text", "first_action"),
]

VOCAB_CARDS = [
    ("簡単", "かんたん", "간단함, 쉽고 단순함", "な형용사", "操作や内容が 복잡하지 않고 하기 쉬운 상태를 나타낸다.",
     "このアプリは操作が簡単です。", "이 앱은 조작이 간단합니다.", "簡単な操作／操作が簡単だ", "kantan"),
    ("操作", "そうさ", "조작, 기계·시스템을 다룸", "명사·する동사", "기계·앱·장치 등을 목적에 맞게 움직이거나 다룬다.",
     "この機械は簡単に操作できます。", "이 기계는 간단히 조작할 수 있습니다.", "機械を操作する／操作方法", "sousa"),
    ("専門家", "せんもんか", "전문가", "명사", "특정 분야에 깊은 지식이나 기술을 가진 사람이다.",
     "この説明には、専門家でも理解しがたい点があります。", "이 설명에는 전문가라도 이해하기 어려운 점이 있습니다.", "法律の専門家／専門家に相談する", "senmonka"),
    ("鍵", "かぎ", "열쇠, 자물쇠", "명사", "문을 잠그거나 여는 열쇠와 잠금장치를 가리킨다.",
     "玄関の鍵が外からかかっています。", "현관문이 밖에서 잠겨 있습니다.", "鍵をかける／鍵を開ける／鍵がかかっている", "kagi"),
    ("保護者", "ほごしゃ", "보호자", "명사", "미성년자 등을 보호하고 책임지는 부모나 법적 보호자이다.",
     "保護者の同意が必要です。", "보호자의 동의가 필요합니다.", "保護者が同意する／保護者に連絡する", "hogosha"),
    ("担当者", "たんとうしゃ", "담당자", "명사", "특정 업무나 사안을 맡아 처리하는 사람이다.",
     "担当者が報告書を確認しています。", "담당자가 보고서를 확인하고 있습니다.", "担当者に確認する／担当者へ連絡する", "tantousha"),
    ("報告書", "ほうこくしょ", "보고서", "명사", "조사·업무의 경과나 결과를 정리해 보고하는 문서이다.",
     "今日中に報告書を提出してください。", "오늘 안에 보고서를 제출해 주세요.", "報告書を書く／作成する／提出する", "houkokusho"),
    ("会社を辞めて留学する", "かいしゃをやめて りゅうがくする", "회사를 그만두고 유학하다", "표현", "辞める의 て형으로 두 행동을 순서대로 연결한 표현이다.",
     "半年悩んだあげく、会社を辞めて留学することにしました。", "반년 고민한 끝에 회사를 그만두고 유학하기로 했습니다.", "会社を辞める／海外へ留学する", "yameru_ryuugaku"),
    ("飛び出した", "とびだした", "튀어나왔다, 뛰쳐나갔다", "동사 飛び出す의 과거형", "안쪽에서 밖으로 기세 좋게 나가거나 갑자기 튀어나오는 동작이다.",
     "ドアが開くと、子どもたちは外へ飛び出しました。", "문이 열리자 아이들은 밖으로 뛰쳐나갔습니다.", "外へ飛び出す／部屋から飛び出す", "tobidashita"),
    ("連絡が遅れる", "れんらくが おくれる", "연락이 늦어지다", "표현", "예정하거나 기대한 때보다 연락이 늦게 이루어지는 상태이다.",
     "忙しくなると、連絡が遅れがちになります。", "바빠지면 연락이 늦어지는 경향이 생깁니다.", "連絡が遅れる／返事が遅れる／連絡が遅れがちだ", "renraku_okureru"),
    ("お宅", "おたく", "댁, 상대방의 집", "명사·존중 표현", "상대 또는 제삼자의 집을 높여 말한다. 자기 집에는 보통 쓰지 않는다.",
     "明日の午後、先生のお宅に伺います。", "내일 오후 선생님 댁에 찾아뵙겠습니다.", "先生のお宅／お宅に伺う", "otaku_house"),
    ("丁寧", "ていねい", "정중함, 공손함; 꼼꼼함", "な형용사·명사", "말이나 태도가 예의 바르거나, 일 처리가 세심하고 빈틈없는 상태이다.",
     "店員は質問に丁寧に答えました。", "점원은 질문에 정중하고 세심하게 답했습니다.", "丁寧な説明／丁寧に答える／丁寧語", "teinei"),
    ("祭り", "まつり", "축제, 제례", "명사", "신사·지역 행사나 기념 축제 등을 가리킨다.",
     "昨日の祭りは人が多くて、とてもにぎやかでした。", "어제 축제는 사람이 많아 매우 활기찼습니다.", "祭りに行く／夏祭り／祭りが行われる", "matsuri"),
    ("個別の審査内容", "こべつの しんさないよう", "개별 심사 내용", "명사구", "각 신청·사례를 따로 심사한 구체적인 기준이나 결과 내용을 가리킨다.",
     "個別の審査内容については、お答えしかねます。", "개별 심사 내용에 관해서는 답변드리기 어렵습니다.", "個別の対応／審査内容／内容を公開する", "kobetsu_shinsa_naiyou"),
    ("丁寧語だけ", "ていねいごだけ", "정중어만", "명사구", "상대나 자신을 높이거나 낮추지 않고 です・ます로 문장만 정중하게 한 표현만을 뜻한다.",
     "「私は明日、図書館へ行きます」は丁寧語だけを使った文です。", "‘저는 내일 도서관에 갑니다’는 정중어만 사용한 문장입니다.", "丁寧語=です・ます／尊敬語=상대 높임／謙譲語=자기 낮춤", "teineigo_dake"),
    ("黙ってしまった", "だまって しまった", "입을 다물어 버렸다, 결국 말하지 않았다", "표현·黙る의 과거형", "黙る의 て형에 〜てしまう가 붙어 동작의 완료나 유감·예상 밖의 느낌을 더한다.",
     "彼は何かを言いかけたが、急に黙ってしまいました。", "그는 무언가 말하려다가 갑자기 입을 다물어 버렸습니다.", "黙る→黙って／〜てしまう→〜てしまった", "damatte_shimatta"),
    ("機械はいつまでに返さなければなりませんか。", "きかいは いつまでに かえさなければ なりませんか", "기계는 언제까지 반납해야 합니까?", "문장·기한 질문", "いつまでに는 마감 시점을 묻고, Vなければならない는 반드시 해야 하는 의무를 나타낸다.",
     "この機械は来週の火曜日の午後六時までに返さなければなりません。", "이 기계는 다음 주 화요일 오후 6시까지 반납해야 합니다.", "いつまでに=언제까지／返す→返さなければならない", "kikai_itsu_made_ni"),
]


def vocab_front(word: str) -> str:
    return f'''<!-- due-review-20260831-vocab-{word} -->
<div style="color:#6b7280;font-size:13px">語彙復習</div>
<div style="font-size:34px;font-weight:700;margin:14px 0">{word}</div>
<div style="color:#52606d">読み方と意味を思い出してください。</div>'''


def vocab_back(reading: str, gloss: str, part: str, meaning: str, example: str, translation: str, collocation: str) -> str:
    return f'''
<div style="font-size:26px;font-weight:700;color:#173b2e">{reading}</div>
<div style="font-size:21px;font-weight:700;margin:8px 0 15px">{gloss}</div>
<div><b>품사</b>　{part}</div>
<div style="margin-top:9px"><b>핵심</b>　{meaning}</div>
<div style="margin-top:14px;font-size:20px">{example}</div>
<div style="color:#5f6368;margin-top:4px">{translation}</div>
<div style="margin-top:14px;padding:10px 12px;background:#e8f3ec;border-left:4px solid #2f6f50"><b>결합</b>　{collocation}</div>'''


def main() -> None:
    mcp("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "codex-local", "version": "1.0"}}, 1)
    notes_with_keys = []
    for card in CARDS:
        (item, label, instruction, prompt, choices, answer, completed, translation,
         connection, meaning, selected, trap, contrast, example, check, category_tag, detail_tag) = card
        notes_with_keys.append((f"item_{item:02d}", {
            "fields": {
                "Front": front(item, label, instruction, prompt, choices),
                "Back": back(answer, completed, translation, connection, meaning, selected, trap, contrast, example, check),
            },
            "tags": [f"item_{item:02d}", category_tag, detail_tag],
        }))
    for word, reading, gloss, part, meaning, example, translation, collocation, detail_tag in VOCAB_CARDS:
        notes_with_keys.append((detail_tag, {
            "fields": {
                "Front": vocab_front(word),
                "Back": vocab_back(reading, gloss, part, meaning, example, translation, collocation),
            },
            "tags": ["vocabulary", detail_tag, "user_added_20260831"],
        }))

    missing = []
    known_ids = []
    request_id = 10
    for unique_tag, note in notes_with_keys:
        found = tool("find_notes", {
            "query": f"tag:due_review_20260831 tag:{unique_tag}",
            "limit": 10,
            "offset": 0,
            "include_first_field": False,
        }, request_id)
        request_id += 1
        if found["count"] == 0:
            missing.append(note)
        elif found["count"] == 1:
            known_ids.extend(found["noteIds"])
        else:
            raise RuntimeError(f"Duplicate unique tag {unique_tag}: {found['noteIds']}")

    if not missing:
        print(json.dumps({"created": 0, "existing": len(known_ids), "deck": DECK, "note_ids": known_ids}, ensure_ascii=False))
        return

    deck_result = tool("create_deck", {"deck_name": DECK}, request_id)
    request_id += 1
    added = tool("add_notes", {
        "deck_name": DECK,
        "model_name": MODEL,
        "notes": missing,
        "tags": COMMON_TAGS,
        "allow_duplicate": False,
    }, request_id)
    request_id += 1
    verified = tool("find_notes", {"query": "tag:due_review_20260831", "limit": 100, "offset": 0, "include_first_field": True}, request_id)
    if verified["count"] != len(notes_with_keys):
        raise RuntimeError({"added": added, "verified": verified})
    print(json.dumps({
        "created": added.get("created", 16),
        "skipped": added.get("skipped", 0),
        "failed": added.get("failed", 0),
        "verified": verified["count"],
        "deck": DECK,
        "deck_result": deck_result,
        "note_ids": verified["noteIds"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
