"""Append N2 grammar 051-059 cards to the existing Anki grammar deck via local MCP."""
from __future__ import annotations

import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

ENDPOINT = "http://127.0.0.1:3141/"
DECK = "JLPT N2::문법 001-025 예문 복습"
MODEL = "Basic"


def mcp(method: str, params: dict, request_id: int) -> dict:
    data = json.dumps({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}, ensure_ascii=False).encode()
    req = urllib.request.Request(ENDPOINT, data=data, headers={
        "Content-Type": "application/json", "Accept": "application/json, text/event-stream"
    }, method="POST")
    with urllib.request.urlopen(req, timeout=30) as response:
        body = response.read().decode("utf-8")
    payload = json.loads(next(line[6:] for line in body.splitlines() if line.startswith("data: ")))
    if "error" in payload:
        raise RuntimeError(payload["error"])
    return payload["result"]


def tool(name: str, arguments: dict, request_id: int) -> dict:
    result = mcp("tools/call", {"name": name, "arguments": arguments}, request_id)
    if result.get("isError"):
        raise RuntimeError(result)
    return result.get("structuredContent") or json.loads(next(x["text"] for x in result["content"] if x["type"] == "text"))


CARDS = [
    (
        "051",
        "〜だけあって・〜だけに／〜だけのことはある",
        "普通形（ナAな／である・Nである）＋だけあって／だけに<br>V・A・N＋だけのことはある",
        "과연 ~인 만큼 / ~인 만큼 더욱 / ~한 보람이 있다",
        "1) だけあって: 자격·조건에 걸맞게 훌륭하다는 칭찬<br>2) だけに: 그 이유 때문에 한층 더 (기대/아쉬움 등 감정 고조)<br>3) だけ의ことはある: 노력이나 가치에 알맞은 결과가 나옴을 칭찬",
        "さすがに一流の料理人が作っただけあって、味も見た目も素晴らしい。",
        "과연 일류 요리사가 만든 만큼 맛도 모양도 훌륭하다.",
        "期待が大きかっただけに、不合格の知らせを聞いたときのショックは大きかった。",
        "기대가 컸던 만큼 불합격 소식을 들었을 때의 충격은 컸다.",
        "だけあって는 칭찬·플러스 평가에 주로 쓰이고, だけに는 마이너스 결과나 심리적 아쉬움에도 쓰인다.",
        "さすが・やはり 등 칭찬 부사가 보이면 だけあって, 기대/걱정 뒤 감정 고조는 だけに를 확인한다."
    ),
    (
        "052",
        "〜たところ",
        "Vた形＋ところ",
        "~했더니 (그 결과 ~를 알게 되었다)",
        "어떤 동작을 시도해 보았더니, 그 결과 새로운 사실을 발견하거나 상황을 알게 됨을 나타낸다.",
        "先生にお願いしてみたところ、快く引き受けてくださった。",
        "선생님께 부탁드렸더니 흔쾌히 수락해 주셨다.",
        "駅の案内所で道を尋ねたところ、親切に地図をくれた。",
        "역 안내소에서 길을 물었더니 친절하게 지도를 주었다.",
        "〜たら와 비슷하지만, 뒤 절에 화자의 의지·명령·희망(〜たい, 〜てください)이 올 수 없다.",
        "앞의 확인·조사·시도 동작 뒤에 뜻밖의 사실을 알게 된 문맥인지 확인한다."
    ),
    (
        "053",
        "〜たとたん（に）",
        "Vた形＋とたん（に）",
        "~하자마자 (바로 그 순간)",
        "어떤 동작이나 변화가 일어난 바로 그 순간, 예상치 못한 다음 사건이 돌발적으로 발생함을 나타낸다.",
        "窓を開けたとたんに、冷たい風が吹き込んできた。",
        "창문을 열자마자 차가운 바람이 불어 들어왔다.",
        "犯人は警察の姿を見たとたん、逃げ出した。",
        "범인은 경찰의 모습을 보자마자 달아났다.",
        "돌발적인 사건의 발생을 나타내므로 뒤 절에 화자의 의지·계획·요청은 올 수 없다.",
        "앞의 계기 직후 순식간에 일어난 우연적·돌발적 사건인지 본다."
    ),
    (
        "054",
        "〜たばかり",
        "Vた形＋ばかり",
        "막 ~함 / ~한 지 얼마 안 됨",
        "어떤 동작이 끝난 뒤 시간이 얼마 지나지 않았다고 화자가 주관적으로 인식함을 나타낸다.",
        "さっき昼ご飯を食べたばかりなのに、もうお腹が空いた。",
        "조금 전에 점심을 막 먹었을 뿐인데 벌써 배가 고프다.",
        "このカメラは先週買ったばかりで、まだ使い方がよく分からない。",
        "이 카메라는 지난주에 막 산 것이라 아직 사용법을 잘 모른다.",
        "〜たところ는 객관적으로 바로 직후(방금), 〜たばかり는 화자의 주관에 따라 몇 달 전 일에도 쓸 수 있다.",
        "시간이 다소 흘렀더라도 화자의 심리상 '얼마 안 됨'을 강조하는지 본다."
    ),
    (
        "055",
        "〜たび（に）",
        "V辞書形＋たび（に）／Nの＋たび（に）",
        "~할 때마다",
        "어떤 일을 할 때마다 매번 예외 없이 같은 일이나 감정이 반복해서 일어남을 나타낸다.",
        "この写真を見るたびに、故郷の家族を思い出す。",
        "이 사진을 볼 때마다 고향 가족이 생각난다.",
        "出張のたびに、各地のおいしい名物を食べるのを楽しみにしている。",
        "출장을 갈 때마다 각지의 맛있는 명물을 먹는 것을 기대하고 있다.",
        "자연현상이나 일상 필수 습관(아침에 일어날 때 등)에는 쓰지 않고 특별한 계기에 쓴다.",
        "앞의 행동이 일어날 때마다 뒤의 생각·반응이 항상 따라붙는지 확인한다."
    ),
    (
        "056",
        "〜だらけ",
        "N＋だらけ",
        "온통 ~투성이 (보기 싫은 것 가득)",
        "사물의 표면이나 공간 전체에 보기 싫고 바람직하지 못한 것이 어지럽게 널려 있음을 나타낸다.",
        "彼の部屋は掃除をしていなくて、ゴミだらけだった。",
        "그의 방은 청소를 하지 않아서 쓰레기투성이였다.",
        "急いで書いたレポートを読み直したら、間違いだらけだった。",
        "급하게 쓴 보고서를 다시 읽어 보았더니 틀린 것투성이였다.",
        "〜まみれ는 피·땀·진흙 등 액체/가루가 묻은 더러움, 〜だらけ는 흠집, 실수, 쓰레기 등 대상물이 많은 상태.",
        "ゴミ, 泥, 傷, 間違い, 借金 등 부정적인 명사와 결합하는지 본다."
    ),
    (
        "057",
        "〜ついでに・〜がてら・〜をかねて",
        "V辞書形・Vた形＋ついでに／Nの＋ついでに<br>Vます語幹＋がてら／N＋がてら<br>N＋をかねて",
        "~하는 김에 / ~를 겸해서",
        "1) ついでに: 주된 행동을 하는 기회에 곁들여 다른 일도 함<br>2) がてら: 하나의 이동 동작을 하면서 다른 목적도 아울러 겸함<br>3) をかねて: 두 가지 대등한 목적을 동시에 가지고 행동함",
        "郵便局へ行くついでに、コンビニで公共料金を払ってきた。",
        "우체국에 가는 김에 편의점에서 공과금을 내고 왔다.",
        "散歩がてら、近くの本屋に寄って雑誌を買った。",
        "산책도 할 겸 근처 서점에 들러 잡지를 샀다.",
        "ついでに는 주(본래 일)+부(곁가지 일), がてら/かねて는 이동을 수반하며 두 목적을 겸함. 접속(散歩がてら) 주의.",
        "이동 중에 가볍게 처리하는 일인지, 주된 행동에 덤으로 하는지 접속 형태를 함께 본다."
    ),
    (
        "058",
        "〜っけ",
        "普通形過去形＋っけ（〜だっけ／〜だったっけ／〜たっけ）",
        "~였던가? ~였지? (회상·재확인)",
        "과거의 기억이 불확실하여 혼잣말로 떠올리거나 상대방에게 가볍게 확인할 때 쓰는 구어 표현.",
        "明日の会議は何時からだっけ？",
        "내일 회의가 몇 시부터였더라?",
        "田中さんって、前にもこのプロジェクトに参加したっけ？",
        "다나카 씨는 전에도 이 프로젝트에 참가했었던가?",
        "반말 구어체이며 이미 알았지만 기억이 가물가물할 때 쓴다. 격식 있는 자리에서는 쓰지 않는다.",
        "과거형 だ／た 뒤에 가볍게 되묻는 구어 대화문에서 자주 출제된다."
    ),
    (
        "059",
        "〜っこない",
        "Vます語幹＋っこない",
        "절대로 ~할 리 없다 / ~할 턱이 없다",
        "화자의 강한 확신을 담아 '그런 일은 절대 불가능하다'고 단정하여 부정하는 구어적 표현.",
        "こんなに難しい問題、子どもに解けっこない。",
        "이렇게 어려운 문제, 아이가 풀 수 있을 리 없다.",
        "あと5分で駅まで歩いて行きっこないよ。",
        "앞으로 5분 만에 역까지 걸어갈 수 있을 리가 없어.",
        "〜わけがない・〜はずがない보다 화자의 주관적 확신과 단정이 강한 구어체.",
        "가능형 ます어간(解けっこない, 間に合いっこない)과 결합하여 절대 불가능을 나타내는지 본다."
    ),
]


def front(number: str, pattern: str) -> str:
    return (f'<!-- n2-grammar-{number} -->'
            f'<div style="color:#6b7280;font-size:14px">{number}</div>'
            f'<div style="font-size:30px;font-weight:700;margin:8px 0 14px">{pattern}</div>'
            '<div style="color:#6b7280">접속 · 핵심 의미 · 예문을 떠올려 보세요.</div>')


def back(row: tuple[str, ...]) -> str:
    number, pattern, connection, gloss, meaning, ex1, tr1, ex2, tr2, contrast, signal = row
    return (
        f'<div style="font-size:20px;font-weight:700;margin:0 0 14px;color:#52606d">{gloss}</div>'
        f'<div style="color:#52606d;font-size:13px;font-weight:700;margin-top:14px">접속</div>'
        f'<div style="line-height:1.55;margin-top:4px">{connection}</div>'
        f'<div style="color:#52606d;font-size:13px;font-weight:700;margin-top:14px">핵심 의미</div>'
        f'<div style="line-height:1.55;margin-top:4px">{meaning}</div>'
        f'<div style="color:#52606d;font-size:13px;font-weight:700;margin-top:14px">예문 1</div>'
        f'<div style="line-height:1.55;margin-top:4px">{ex1}<br><span style="color:#6b7280">{tr1}</span></div>'
        f'<div style="color:#52606d;font-size:13px;font-weight:700;margin-top:14px">예문 2</div>'
        f'<div style="line-height:1.55;margin-top:4px">{ex2}<br><span style="color:#6b7280">{tr2}</span></div>'
        f'<div style="color:#52606d;font-size:13px;font-weight:700;margin-top:14px">구별 포인트</div>'
        f'<div style="line-height:1.55;margin-top:4px">{contrast}</div>'
        f'<div style="color:#52606d;font-size:13px;font-weight:700;margin-top:14px">시험 신호</div>'
        f'<div style="line-height:1.55;margin-top:4px">{signal}</div>'
    )


def main():
    mcp("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "codex-local", "version": "1.0"}}, 1)
    existing = tool("find_notes", {"query": 'deck:"' + DECK + '" tag:문법_051_059', "limit": 100, "offset": 0, "include_first_field": True}, 2)
    if existing["count"] == 9:
        print(json.dumps({"created": 0, "existing": 9, "deck": DECK, "note_ids": existing["noteIds"]}, ensure_ascii=False))
        return
    if existing["count"] > 0:
        raise RuntimeError(f"Partial 051-059 set already exists: {existing['count']}")

    notes = [{
        "fields": {"Front": front(row[0], row[1]), "Back": back(row)},
        "tags": ["JLPT_N2", "문법_051_059", f"문법_{row[0]}", "priority_new", "lecture_20260905"],
    } for row in CARDS]

    added = tool("add_notes", {
        "deck_name": DECK,
        "model_name": MODEL,
        "notes": notes,
        "tags": ["JLPT_N2", "문법_051_059"],
        "allow_duplicate": False,
    }, 3)

    verified = tool("find_notes", {"query": 'deck:"' + DECK + '" tag:문법_051_059', "limit": 100, "offset": 0, "include_first_field": True}, 4)
    if verified["count"] != 9:
        raise RuntimeError({"added": added, "verified": verified})

    all_notes = tool("find_notes", {"query": 'deck:"' + DECK + '"', "limit": 100, "offset": 0, "include_first_field": False}, 5)
    
    # Sync with AnkiWeb
    sync_res = tool("sync", {}, 6)
    
    print(json.dumps({
        "status": "success",
        "created": added.get("created", 9),
        "failed": added.get("failed", 0),
        "verified_new": 9,
        "deck_total": all_notes["count"],
        "deck": DECK,
        "note_ids": verified["noteIds"],
        "sync": sync_res
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
