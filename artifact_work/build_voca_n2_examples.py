"""Build and apply one N2-style example sentence to every 한끝 Voca note.

The script reads notes through the local Anki MCP server, selects examples from
the public-domain 2008 Tanaka Corpus, adds generated ruby readings with Sudachi,
and can dry-run or apply batched `sentences` field updates.
"""
from __future__ import annotations

import argparse
import bz2
import hashlib
import html
import json
import re
import sys
import urllib.request
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "tmp" / "voca-example-work"
OUTPUT = ROOT / "outputs" / "anki" / "voca-examples-20260901"
PYDEPS = WORK / "pydeps"
CORPUS_ZIP = WORK / "examples_pd-2008-10-10-tabbed-ck.zip"
CORPUS_MEMBER = "examples_pd-2008-10-10-tabbed-ck.txt"
CC0_PATH = WORK / "jpn_sentences_CC0.tsv.bz2"
ENDPOINT = "http://127.0.0.1:3141/"
DECK_QUERY = 'deck:"日本語::JLPT 한끝 Voca"'
MODEL = "JLPT 한권으로 끝내기 단어장"

N2_MARKERS = (
    "にもかかわらず", "というわけ", "わけでは", "わけには", "ことから",
    "ことなく", "ことには", "だけでなく", "ばかりでなく", "に応じて",
    "に伴って", "に基づ", "に関して", "について", "に対して", "にとって",
    "によって", "によると", "一方で", "反面", "ものの", "とは限ら",
    "ないことはない", "ざるを得ない", "かねない", "おそれが", "上で",
    "以上", "限り", "次第", "につれて", "に従って", "を通じて", "をめぐって",
    "にすぎない", "どころか", "どころでは", "に違いない", "に決まって",
)
FORMAL_TERMS = (
    "社会", "制度", "政府", "企業", "地域", "環境", "調査", "結果", "影響",
    "問題", "必要", "判断", "状況", "対応", "方針", "計画", "目的", "原因",
    "報告", "情報", "資料", "研究", "技術", "経済", "教育", "文化", "意見",
    "立場", "方法", "可能", "一方", "しかし", "そのため", "したがって",
)
BAD_FRAGMENTS = (
    "・・・", "....", "．．．", "ちくしょう", "くそ", "てめえ", "お前ら",
    "セックス", "殺して", "死ね", "馬鹿野郎", "！ ！", "？？",
)
MANUAL_SENTENCES = {
    "JLPT-한끝-N2-0083": "順調だった交渉は、担当者の発言をきっかけに一転して厳しい状況になった。",
    "JLPT-한끝-N2-0086": "同じ国であっても、緯度によって気候が大きく異なることがある。",
    "JLPT-한끝-N2-0109": "薬品を水で薄める際は、決められた割合を必ず守ってください。",
    "JLPT-한끝-N2-0113": "会社は報道内容を打ち消したものの、疑惑が完全に晴れたわけではない。",
    "JLPT-한끝-N2-0121": "通信販売の拡大に伴って、商品の運送を担う人手が不足している。",
    "JLPT-한끝-N2-0138": "応援団の声が会場全体に響き、選手たちの緊張も次第にほぐれていった。",
    "JLPT-한끝-N2-0173": "休日の博物館は親子連れで混雑するため、事前予約をしたほうがよい。",
    "JLPT-한끝-N2-0209": "気温が急激に下降するおそれがあるため、十分な防寒対策が必要だ。",
    "JLPT-한끝-N2-0217": "この施設は家族連れでも利用しやすいよう、休憩室が広く設けられている。",
    "JLPT-한끝-N2-0239": "雨の日に革靴を履くと傷みやすいため、帰宅後すぐ手入れしたほうがよい。",
    "JLPT-한끝-N2-0255": "個人情報を会社の管理下に置く以上、厳重な安全対策が求められる。",
    "JLPT-한끝-N2-0290": "旧制度では支援を受けられなかった人も、新制度の対象となる可能性がある。",
    "JLPT-한끝-N2-0326": "厚い雲に覆われているものの、午後には晴れる見込みだ。",
    "JLPT-한끝-N2-0363": "現社長は就任以来、働き方の見直しを進めてきた。",
    "JLPT-한끝-N2-0369": "申請書は県庁に直接提出するか、郵送することになっている。",
    "JLPT-한끝-N2-0390": "両社は事故の原因を明らかにするため、合同で調査を行うことを決めた。",
    "JLPT-한끝-N2-0400": "この地域は外国人住民が多く、国際色豊かな行事が毎年開かれている。",
    "JLPT-한끝-N2-0409": "目標を達成するには、毎日こつこつ努力を続けるほかない。",
    "JLPT-한끝-N2-0427": "書類に不備があったため、期限内に再提出しなければならない。",
    "JLPT-한끝-N2-0446": "この作品集を通じて、作家の考え方がどのように変化したかが分かる。",
    "JLPT-한끝-N2-0493": "締め切り直前になってじたばたしても、状況が改善するとは限らない。",
    "JLPT-한끝-N2-0526": "景気の回復にもかかわらず、若者の就職率は思ったほど上がっていない。",
    "JLPT-한끝-N2-0527": "駅に近い住宅街では、交通量の増加が問題となっている。",
    "JLPT-한끝-N2-0537": "商品の主成分に関しては、容器の裏側に詳しく表示されている。",
    "JLPT-한끝-N2-0548": "決勝で敗れて準優勝に終わったものの、選手たちは最後まで全力を尽くした。",
    "JLPT-한끝-N2-0589": "大学への進学率が上昇する一方で、地域による差も広がっている。",
    "JLPT-한끝-N2-0628": "治療の成功率は高いものの、危険がまったくないわけではない。",
    "JLPT-한끝-N2-0653": "前社長の方針を引き継ぎつつ、新たな事業にも取り組むことになった。",
    "JLPT-한끝-N2-0656": "前町長が進めた計画について、住民から見直しを求める声が上がった。",
    "JLPT-한끝-N2-0666": "不審なメールを受け取った場合は、まず送信元を確認してください。",
    "JLPT-한끝-N2-0673": "新しい制度の導入後、手続きに関する問い合わせが続出した。",
    "JLPT-한끝-N2-0747": "応募者が定員を超えた場合、参加者は抽選によって決められる。",
    "JLPT-한끝-N2-0750": "国家予算は百兆円を超え、支出の見直しが避けられない状況だ。",
    "JLPT-한끝-N2-0759": "災害に備えて食料を長期間貯蔵するには、温度管理が欠かせない。",
    "JLPT-한끝-N2-0786": "低価格だからといって、品質まで低いとは限らない。",
    "JLPT-한끝-N2-0803": "通勤にかかる電車賃は、原則として会社から支給される。",
    "JLPT-한끝-N2-0813": "若者の投票率を高めるため、学校でも選挙について学ぶ機会が設けられた。",
    "JLPT-한끝-N2-0832": "作業中に破片が飛び散るおそれがあるため、保護眼鏡を着用してください。",
    "JLPT-한끝-N2-0872": "主演俳優の熱演によって、観客は物語の世界に引き込まれた。",
    "JLPT-한끝-N2-0881": "地方の会場へ行くには、電車を二度乗り継がなければならない。",
    "JLPT-한끝-N2-0912": "新しい担当になった彼は張り切っているものの、無理をしすぎないか心配だ。",
    "JLPT-한끝-N2-0920": "この仕切りは半透明になっているため、明るさを保ちながら視線を遮れる。",
    "JLPT-한끝-N2-0958": "通信販売で買った上着はぶかぶかで、交換せざるを得なかった。",
    "JLPT-한끝-N2-0961": "副大臣は記者会見で、今後の支援策について説明した。",
    "JLPT-한끝-N2-0985": "彼の小説は文学賞を受賞したことから、広く知られるようになった。",
    "JLPT-한끝-N2-1001": "災害による被害を減らすには、地域全体で防災意識を高める必要がある。",
    "JLPT-한끝-N2-1024": "駅前に建った真新しい図書館は、地域交流の拠点として期待されている。",
    "JLPT-한끝-N2-1026": "周囲に急かされても、彼はマイペースを崩すことなく作業を続けた。",
    "JLPT-한끝-N2-1044": "未使用の商品に限り、購入後一週間以内であれば返品できる。",
    "JLPT-한끝-N2-1066": "無計画に開発を進めれば、自然環境を損なうおそれがある。",
    "JLPT-한끝-N2-1131": "診察は予約制となっているため、来院前に電話で申し込んでください。",
    "JLPT-한끝-N2-1168": "難しいと聞いていたが、実際に解いてみるとわりと簡単だった。",
    "JLPT-한끝-N3-070": "あと一点で合格だっただけに、不合格という結果が惜しい。",
    "JLPT-한끝-N3-171": "経営学を学んだからといって、すぐ会社を運営できるわけではない。",
    "JLPT-한끝-N4-057": "都市部であっても、空き地を利用して野菜を植える人が増えている。",
    "JLPT-한끝-N4-090": "長期出張から戻った父に、家族全員で『おかえりなさい』と声をかけた。",
    "JLPT-한끝-N4-120": "助けてもらったおれいに、地元の菓子を送ることにした。",
    "JLPT-한끝-N4-121": "強風で枝が折れるおそれがあるため、公園への立ち入りが禁止された。",
    "JLPT-한끝-N4-146": "カッターを使用する際は、刃を出しすぎないよう注意してください。",
    "JLPT-한끝-N4-169": "北区では高齢者を対象とした相談会が定期的に開かれている。",
    "JLPT-한끝-N4-190": "厚い雲に覆われているものの、午後には晴れる見込みだ。",
    "JLPT-한끝-N4-200": "山頂から眺めるけしきは美しく、疲れを忘れるほどだった。",
    "JLPT-한끝-N4-210": "研究会に参加するには、事前に資料を読んでおく必要がある。",
    "JLPT-한끝-N4-477": "昼休みだからといって、許可なく職場を離れてよいわけではない。",
    "JLPT-한끝-N5-325": "会場へは駅の西口を出て、線路沿いに進んでください。",
    "JLPT-한끝-N5-368": "工事に伴い、東口は来週まで利用できないことになっている。",
    "JLPT-한끝-N5-382": "工場では一日に鉛筆を百本検査することになっている。",
}
KANJI_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
META_RE = re.compile(r"\[[^\]]*\]\s*$")
INDEX_DECORATION_RE = re.compile(r"(?:\[[^\]]*\]|\([^)]*\)|\{[^}]*\}|~)+")
SURFACE_RE = re.compile(r"\{([^}]*)\}")


@dataclass(frozen=True)
class CorpusRow:
    sid: str
    english: str
    japanese: str
    index: str


def mcp(method: str, params: dict[str, Any], request_id: int) -> dict[str, Any]:
    data = json.dumps(
        {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params},
        ensure_ascii=False,
    ).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        body = response.read().decode("utf-8")
    line = next(line for line in body.splitlines() if line.startswith("data: "))
    payload = json.loads(line[6:])
    if "error" in payload:
        raise RuntimeError(payload["error"])
    return payload["result"]


def tool(name: str, arguments: dict[str, Any], request_id: int) -> dict[str, Any]:
    result = mcp("tools/call", {"name": name, "arguments": arguments}, request_id)
    if result.get("isError"):
        raise RuntimeError(result)
    if "structuredContent" in result:
        return result["structuredContent"]
    text = next(part["text"] for part in result.get("content", []) if part.get("type") == "text")
    return json.loads(text)


def fetch_notes() -> list[dict[str, Any]]:
    note_ids: list[int] = []
    request_id = 1
    for offset in range(0, 10000, 500):
        found = tool(
            "find_notes",
            {"query": DECK_QUERY, "limit": 500, "offset": offset, "include_first_field": False},
            request_id,
        )
        request_id += 1
        note_ids.extend(found["noteIds"])
        if not found["hasMore"]:
            break
    notes: list[dict[str, Any]] = []
    for start in range(0, len(note_ids), 100):
        info = tool("notes_info", {"notes": note_ids[start : start + 100]}, request_id)
        request_id += 1
        notes.extend(info["notes"])
    notes.sort(key=lambda note: note["fields"]["id"]["value"])
    return notes


def corpus_rows() -> list[CorpusRow]:
    if not CORPUS_ZIP.exists():
        raise FileNotFoundError(CORPUS_ZIP)
    with zipfile.ZipFile(CORPUS_ZIP) as archive:
        raw = archive.read(CORPUS_MEMBER).decode("euc_jp")
    rows: list[CorpusRow] = []
    for line in raw.splitlines():
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 4 or not parts[0].isdigit():
            continue
        japanese = META_RE.sub("", parts[2]).strip()
        if japanese:
            rows.append(CorpusRow(parts[0], parts[1], japanese, parts[3]))
    return rows


def index_keys(index: str) -> set[str]:
    keys: set[str] = set()
    for token in index.split():
        clean = token.rstrip("~")
        base = re.split(r"[\[({~]", clean, maxsplit=1)[0]
        if base:
            keys.add(base)
        keys.update(value for value in SURFACE_RE.findall(clean) if value)
    return keys


def build_index(rows: list[CorpusRow]) -> dict[str, list[int]]:
    result: dict[str, list[int]] = defaultdict(list)
    for index, row in enumerate(rows):
        for key in index_keys(row.index):
            if len(key) <= 30:
                result[key].append(index)
    return result


def candidate_score(row: CorpusRow, target: str) -> int:
    sentence = row.japanese
    length = len(sentence)
    score = 0
    if 24 <= length <= 52:
        score += 30
    elif 18 <= length <= 65:
        score += 15
    else:
        score -= abs(length - 38)
    score += 15 * sum(marker in sentence for marker in N2_MARKERS)
    score += 3 * sum(term in sentence for term in FORMAL_TERMS)
    score += 7 if re.search(r"[、。].+[、。]", sentence) else 0
    score += 6 if target and target in sentence else 0
    score += 5 if any(piece.startswith(target) and piece.endswith("~") for piece in row.index.split()) else 0
    score -= 35 * sum(fragment in sentence for fragment in BAD_FRAGMENTS)
    score -= 20 if sentence.startswith(("・", "―", "...", "…")) else 0
    score -= 10 if sentence.count("！") + sentence.count("?") + sentence.count("？") > 1 else 0
    score -= 8 if re.search(r"[A-Za-z]{3,}", sentence) else 0
    return score


def lexical_keys(value: str, tokenizer_obj: Any, mode: Any) -> set[str]:
    cleaned = value.replace("〜", "").replace("~", "").strip()
    if not cleaned:
        return set()
    keys = {cleaned}
    tokens = list(tokenizer_obj.tokenize(cleaned, mode))
    for token in tokens:
        keys.update(
            key
            for key in (
                token.surface(),
                token.dictionary_form(),
                token.normalized_form(),
            )
            if key
        )
    if len(tokens) > 1:
        keys.add("".join(token.dictionary_form() for token in tokens))
        keys.add("".join(token.normalized_form() for token in tokens))
    return keys


def build_lexical_index(
    rows: list[CorpusRow], targets: set[str], tokenizer_obj: Any, mode: Any
) -> dict[str, list[int]]:
    result: dict[str, list[int]] = defaultdict(list)
    for row_id, row in enumerate(rows):
        seen: set[str] = set()
        for token in tokenizer_obj.tokenize(row.japanese, mode):
            values = (
                token.surface(),
                token.dictionary_form(),
                token.normalized_form(),
            )
            seen.update(value for value in values if value in targets)
        for value in seen:
            result[value].append(row_id)
    return result


def choose_candidates(
    notes: list[dict[str, Any]],
    rows: list[CorpusRow],
    corpus_index: dict[str, list[int]],
    lexical_index: dict[str, list[int]],
    tokenizer_obj: Any,
    mode: Any,
) -> list[dict[str, Any]]:
    selections: list[dict[str, Any]] = []
    for note in notes:
        fields = note["fields"]
        kanji = fields["kanji"]["value"].strip()
        kana = fields["kana"]["value"].strip()
        note_key = fields["id"]["value"]
        if note_key in MANUAL_SENTENCES:
            selections.append(
                {
                    "note_id": note["noteId"],
                    "id": note_key,
                    "kanji": kanji,
                    "kana": kana,
                    "meaning": fields["meaning"]["value"],
                    "old_sentences": fields["sentences"]["value"],
                    "candidate_count": 0,
                    "score": 100,
                    "source_id": "self-authored",
                    "japanese": MANUAL_SENTENCES[note_key],
                    "english": None,
                }
            )
            continue
        keys = lexical_keys(kanji, tokenizer_obj, mode)
        candidate_ids: set[int] = set()
        for key in keys:
            candidate_ids.update(corpus_index.get(key, []))
            candidate_ids.update(lexical_index.get(key, []))
        ranked = sorted(
            ((candidate_score(rows[row_id], kanji), row_id) for row_id in candidate_ids),
            key=lambda item: (-item[0], len(rows[item[1]].japanese), int(rows[item[1]].sid)),
        )
        best = rows[ranked[0][1]] if ranked else None
        selections.append(
            {
                "note_id": note["noteId"],
                "id": fields["id"]["value"],
                "kanji": kanji,
                "kana": kana,
                "meaning": fields["meaning"]["value"],
                "old_sentences": fields["sentences"]["value"],
                "candidate_count": len(candidate_ids),
                "score": ranked[0][0] if ranked else None,
                "source_id": best.sid if best else None,
                "japanese": best.japanese if best else None,
                "english": best.english if best else None,
            }
        )
    return selections


def load_tokenizer():
    sys.path.insert(0, str(PYDEPS))
    from sudachipy import dictionary, tokenizer  # type: ignore

    return dictionary.Dictionary().create(), tokenizer.Tokenizer.SplitMode.C


def katakana_to_hiragana(value: str) -> str:
    return "".join(chr(ord(ch) - 0x60) if "ァ" <= ch <= "ヶ" else ch for ch in value)


def ruby_sentence(
    sentence: str,
    tokenizer_obj: Any,
    mode: Any,
    target_kanji: str = "",
    target_kana: str = "",
) -> str:
    parts: list[str] = []
    for token in tokenizer_obj.tokenize(sentence, mode):
        surface = token.surface()
        reading = katakana_to_hiragana(token.reading_form() or "")
        if surface == target_kanji and target_kana and "〜" not in target_kana:
            reading = target_kana
        escaped_surface = html.escape(surface)
        if KANJI_RE.search(surface) and reading and reading != surface:
            parts.append(f"<ruby>{escaped_surface}<rt>{html.escape(reading)}</rt></ruby>")
        else:
            parts.append(escaped_surface)
    return "".join(parts)


def write_outputs(notes: list[dict[str, Any]], rows: list[CorpusRow], selections: list[dict[str, Any]]) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    backup = {
        "deck_query": DECK_QUERY,
        "count": len(notes),
        "notes": [
            {
                "note_id": note["noteId"],
                "id": note["fields"]["id"]["value"],
                "sentences": note["fields"]["sentences"]["value"],
            }
            for note in notes
        ],
    }
    (OUTPUT / "sentences-backup.json").write_text(json.dumps(backup, ensure_ascii=False, indent=2), encoding="utf-8")
    corpus_sha = hashlib.sha256(CORPUS_ZIP.read_bytes()).hexdigest()
    matched = sum(item["japanese"] is not None for item in selections)
    report = {
        "model": MODEL,
        "deck_query": DECK_QUERY,
        "note_count": len(notes),
        "corpus_rows": len(rows),
        "matched": matched,
        "unmatched": len(selections) - matched,
        "coverage_percent": round(matched * 100 / len(selections), 2),
        "corpus_file": CORPUS_ZIP.name,
        "corpus_sha256": corpus_sha,
    }
    (OUTPUT / "coverage.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUTPUT / "candidates.json").write_text(json.dumps(selections, ensure_ascii=False, indent=2), encoding="utf-8")
    with (OUTPUT / "unmatched.tsv").open("w", encoding="utf-8", newline="") as stream:
        stream.write("id\tkanji\tkana\tmeaning\n")
        for item in selections:
            if item["japanese"] is None:
                stream.write(f'{item["id"]}\t{item["kanji"]}\t{item["kana"]}\t{item["meaning"]}\n')


def prepare_updates(selections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tokenizer_obj, mode = load_tokenizer()
    updates: list[dict[str, Any]] = []
    for item in selections:
        if not item["japanese"]:
            continue
        rendered = ruby_sentence(
            item["japanese"],
            tokenizer_obj,
            mode,
            target_kanji=item["kanji"],
            target_kana=item["kana"],
        )
        item["rendered"] = rendered
        updates.append({"id": item["note_id"], "fields": {"sentences": rendered}})
    (OUTPUT / "prepared-updates.json").write_text(json.dumps(updates, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUTPUT / "candidates.json").write_text(json.dumps(selections, ensure_ascii=False, indent=2), encoding="utf-8")
    return updates


def apply_updates(updates: list[dict[str, Any]], dry_run: bool) -> dict[str, Any]:
    summaries: list[dict[str, Any]] = []
    request_id = 1000
    for start in range(0, len(updates), 100):
        result = tool(
            "update_notes",
            {"notes": updates[start : start + 100], "dry_run": dry_run},
            request_id,
        )
        request_id += 1
        summaries.append(result)
    return {"dry_run": dry_run, "batches": len(summaries), "results": summaries}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("inspect", "prepare", "dry-run", "apply"))
    args = parser.parse_args()

    notes = fetch_notes()
    if len(notes) != 2734:
        raise RuntimeError(f"Expected 2734 notes, found {len(notes)}")
    if {note["modelName"] for note in notes} != {MODEL}:
        raise RuntimeError("Unexpected note model in target deck")
    rows = corpus_rows()
    tokenizer_obj, mode = load_tokenizer()
    targets: set[str] = set()
    for note in notes:
        targets.update(lexical_keys(note["fields"]["kanji"]["value"], tokenizer_obj, mode))
    selections = choose_candidates(
        notes,
        rows,
        build_index(rows),
        build_lexical_index(rows, targets, tokenizer_obj, mode),
        tokenizer_obj,
        mode,
    )
    write_outputs(notes, rows, selections)
    report = json.loads((OUTPUT / "coverage.json").read_text(encoding="utf-8"))
    if args.mode == "inspect":
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    updates = prepare_updates(selections)
    report["prepared_updates"] = len(updates)
    if args.mode == "prepare":
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    if len(updates) != len(notes):
        raise RuntimeError(f"Refusing partial update: prepared {len(updates)} of {len(notes)}")
    result = apply_updates(updates, dry_run=args.mode == "dry-run")
    report["update_result"] = result
    destination = OUTPUT / ("dry-run-result.json" if args.mode == "dry-run" else "apply-result.json")
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"notes": len(notes), "updates": len(updates), "mode": args.mode, "batches": result["batches"]}, ensure_ascii=False))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
