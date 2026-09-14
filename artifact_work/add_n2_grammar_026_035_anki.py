"""Append N2 grammar 026-035 cards to the existing 001-025 Anki deck via local MCP."""
from __future__ import annotations

import json
import urllib.request

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
    ("026", "〜きる／〜きれない", "Vます語幹＋きる／きれない", "끝까지 완전히 해내다 / 다 하지 못하다",
     "最後まで・全部라는 완결 신호와 잘 결합한다.",
     "長い小説だったが、一晩で読みきった。", "긴 소설이었지만 하룻밤에 다 읽었다.",
     "料理が多すぎて、一人では食べきれない。", "음식이 너무 많아 혼자서는 다 먹을 수 없다.",
     "〜終わる는 단순 종료, 〜きる는 남김없이 완수함을 강조한다.", "全部・最後まで와 완전한 완료 여부를 본다."),
    ("027", "〜くせに", "普通形＋くせに／Nの＋くせに／ナAな＋くせに", "~인 주제에, ~이면서도",
     "예상에 어긋난 행동을 비난·불만의 감정과 함께 나타낸다.",
     "彼は知っているくせに、何も教えてくれなかった。", "그는 알고 있으면서도 아무것도 알려주지 않았다.",
     "子どものくせに、大人のような話し方をする。", "아이인 주제에 어른 같은 말투를 쓴다.",
     "〜のに보다 화자의 비난·불만이 강하므로 공손한 상대에게 주의한다.", "단순 역접인가, 상대를 탓하는 감정까지 있는가?"),
    ("028", "〜こそ／〜からこそ", "N＋こそ／普通形＋からこそ", "바로 ~야말로 / 바로 ~이기 때문에",
     "다른 것이 아니라 해당 대상·이유를 강하게 한정하고 강조한다.",
     "今度こそ、試験に合格したい。", "이번에야말로 시험에 합격하고 싶다.",
     "苦しい時だからこそ、互いに助け合うべきだ。", "힘든 때이기 때문에야말로 서로 도와야 한다.",
     "〜から는 보통 이유, 〜からこそ는 그 이유만을 특별히 강조한다.", "강조하려는 것이 대상인가, 이유인가?"),
    ("029", "〜ことか", "疑問語＋普通形＋ことか", "얼마나 ~했는가, 얼마나 ~인지",
     "수량 질문이 아니라 감정의 정도가 매우 크다는 감탄을 나타낸다.",
     "合格の知らせを聞いて、どんなにうれしかったことか。", "합격 소식을 듣고 얼마나 기뻤는지 모른다.",
     "あなたの帰りを何度待ったことか。", "당신이 돌아오기를 몇 번이나 기다렸는지 모른다.",
     "실제 답을 요구하는 의문문이 아니라 どんなに・どれほど・何度와 감정을 강조한다.", "질문인가, 강한 감탄인가?"),
    ("030", "〜ことから／〜ところから", "普通形＋ことから／ところから", "~라는 사실로부터, ~라는 점 때문에",
     "관찰 가능한 사실을 근거로 판단하거나 이름·유래의 이유를 설명한다.",
     "窓が開いていることから、誰かが中にいると分かった。", "창문이 열려 있는 것으로 보아 누군가 안에 있음을 알았다.",
     "形が星に似ているところから、この名前が付けられた。", "모양이 별과 닮은 점에서 이 이름이 붙었다.",
     "〜からすると는 근거에서 추측, 〜ことから는 근거가 되는 사실 자체를 제시한다.", "뒤가 판단·명칭의 유래인가?"),
    ("031", "〜ことだから", "Nの＋ことだから", "~인 사람이니까 분명",
     "잘 아는 사람의 성격·평소 모습을 근거로 그 사람의 행동을 추측한다.",
     "責任感の強い田中さんのことだから、最後までやるだろう。", "책임감이 강한 다나카 씨니까 끝까지 할 것이다.",
     "彼女のことだから、もう準備を終えているに違いない。", "그녀니까 이미 준비를 끝냈을 것이다.",
     "일반 사물의 원인보다 사람의 성격·습관에 근거한 추측에 쓴다.", "앞의 인물을 평소부터 잘 안다는 전제가 있는가?"),
    ("032", "〜ことなく", "V辞書形＋ことなく", "~하지 않고, ~하는 일 없이",
     "어떤 행동을 전혀 하지 않은 채 뒤 행동이나 상태가 이어짐을 격식 있게 나타낸다.",
     "彼は一度も休むことなく、最後まで走り続けた。", "그는 한 번도 쉬지 않고 끝까지 계속 달렸다.",
     "困難に負けることなく、研究を続けた。", "어려움에 지지 않고 연구를 계속했다.",
     "〜ないで보다 문어적·격식적이며 一度も 같은 완전 부정 신호와 잘 맞는다.", "하지 않은 행동과 계속된 행동을 나눠 본다."),
    ("033", "〜ことに", "Vた形／イAい／ナAな＋ことに", "~하게도, ~한 것은",
     "뒤 사실에 대한 화자의 놀람·기쁨·유감 같은 평가를 문두에서 제시한다.",
     "驚いたことに、彼は一人で問題を解決した。", "놀랍게도 그는 혼자 문제를 해결했다.",
     "残念なことに、試合は中止になった。", "유감스럽게도 시합은 중지되었다.",
     "〜ことか는 감정의 정도를 감탄하고, 〜ことに는 뒤 사실에 대한 평가를 먼저 붙인다.", "놀랍게도·다행히·유감스럽게도로 바꿀 수 있는가?"),
    ("034", "〜ことになる／〜ことにはならない／〜ことにする", "V辞書形・Vない形＋各文型", "외부 결정·귀결 / 그런 결과는 아님 / 스스로 결정",
     "ことになる는 규칙·상황의 결정, ことにする는 화자의 의지적 결정이다.",
     "来月から大阪へ転勤することになった。", "다음 달부터 오사카로 전근하게 되었다.",
     "毎日運動することにした。<br>少し手伝っただけでは、全部終えたことにはならない。",
     "매일 운동하기로 했다.<br>조금 도왔을 뿐이면 전부 끝낸 셈은 되지 않는다.",
     "ことになる=외부 결정, ことにする=스스로 결정, ことにはならない=그 결과로 인정되지 않음.",
     "누가 결정했는지와 앞 행동만으로 뒤 결과가 성립하는지 확인한다."),
    ("035", "〜ことはない", "V辞書形＋ことはない", "~할 필요는 없다",
     "상대의 걱정을 덜거나 불필요한 행동을 하지 않아도 된다고 조언한다.",
     "まだ時間はあるから、そんなに急ぐことはない。", "아직 시간이 있으니 그렇게 서두를 필요는 없다.",
     "一度失敗しただけで、あきらめることはない。", "한 번 실패했을 뿐이라고 포기할 필요는 없다.",
     "〜ないことはない는 불가능하지는 않다는 부분 긍정으로 뜻이 다르다.", "조언·안심 문맥에서 ‘할 필요 없다’인가?"),
]


def front(number: str, pattern: str) -> str:
    return (f'<!-- n2-grammar-{number} -->'
            f'<div style="color:#6b7280;font-size:14px">{number}</div>'
            f'<div style="font-size:30px;font-weight:700;margin:8px 0 14px">{pattern}</div>'
            '<div style="color:#6b7280">접속 · 핵심 의미 · 예문을 떠올려 보세요.</div>')


def back(row: tuple[str, ...]) -> str:
    number, pattern, connection, gloss, meaning, ex1, tr1, ex2, tr2, contrast, signal = row
    return f'''<div style="font-size:21px;font-weight:700;color:#52606d">{gloss}</div>
<div style="margin-top:15px"><b>접속</b>　{connection}</div>
<div style="margin-top:9px"><b>핵심 의미</b>　{meaning}</div>
<div style="font-size:20px;margin-top:16px">{ex1}</div><div style="color:#5f6368">{tr1}</div>
<div style="font-size:20px;margin-top:14px">{ex2}</div><div style="color:#5f6368">{tr2}</div>
<div style="margin-top:15px"><b>구별</b>　{contrast}</div>
<div style="margin-top:13px;padding:10px 12px;background:#e8f3ec;border-left:4px solid #2f6f50"><b>시험 신호</b>　{signal}</div>'''


def main() -> None:
    mcp("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "codex-local", "version": "1.0"}}, 1)
    existing = tool("find_notes", {"query": "deck:\"" + DECK + "\" tag:문법_026_035", "limit": 100, "offset": 0, "include_first_field": True}, 2)
    if existing["count"] == 10:
        print(json.dumps({"created": 0, "existing": 10, "deck": DECK, "note_ids": existing["noteIds"]}, ensure_ascii=False))
        return
    if existing["count"]:
        raise RuntimeError(f"Partial 026-035 set exists: {existing['count']}")
    notes = [{
        "fields": {"Front": front(row[0], row[1]), "Back": back(row)},
        "tags": ["JLPT_N2", "문법_026_035", f"문법_{row[0]}", "priority_new"],
    } for row in CARDS]
    added = tool("add_notes", {
        "deck_name": DECK, "model_name": MODEL, "notes": notes,
        "tags": ["JLPT_N2", "문법_026_035"], "allow_duplicate": False,
    }, 3)
    verified = tool("find_notes", {"query": "deck:\"" + DECK + "\" tag:문법_026_035", "limit": 100, "offset": 0, "include_first_field": True}, 4)
    if verified["count"] != 10:
        raise RuntimeError({"added": added, "verified": verified})
    all_notes = tool("find_notes", {"query": "deck:\"" + DECK + "\"", "limit": 100, "offset": 0, "include_first_field": False}, 5)
    print(json.dumps({"created": added.get("created", 10), "failed": added.get("failed", 0), "verified_new": 10,
                      "deck_total": all_notes["count"], "deck": DECK, "note_ids": verified["noteIds"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
