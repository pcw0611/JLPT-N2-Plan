"""Audit whether each selected example really contains the card's target word."""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "tmp" / "voca-example-work"
OUTPUT = ROOT / "outputs" / "anki" / "voca-examples-20260901"
sys.path.insert(0, str(WORK / "pydeps"))

from sudachipy import dictionary, tokenizer  # type: ignore


MODE = tokenizer.Tokenizer.SplitMode.C
TOKENIZER = dictionary.Dictionary().create()


def clean(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    return value.replace("〜", "").replace("~", "").strip()


def token_keys(token: object) -> set[str]:
    return {
        value
        for value in (
            token.surface(),
            token.dictionary_form(),
            token.normalized_form(),
        )
        if value
    }


def occurrence(item: dict[str, object]) -> tuple[list[int], str]:
    sentence = str(item["japanese"])
    target = clean(str(item["kanji"]))
    kana = clean(str(item["kana"]))
    highlight_surface = clean(str(item.get("highlight_surface") or ""))
    sentence_tokens = list(TOKENIZER.tokenize(sentence, MODE))
    target_tokens = list(TOKENIZER.tokenize(target, MODE))
    offsets: list[tuple[int, int]] = []
    cursor = 0
    for token in sentence_tokens:
        token_end = cursor + len(token.surface())
        offsets.append((cursor, token_end))
        cursor = token_end

    # A manually reviewed inflection or compound substring is allowed explicitly.
    if highlight_surface and highlight_surface in sentence:
        start = sentence.index(highlight_surface)
        end = start + len(highlight_surface)
        return [i for i, (left, right) in enumerate(offsets) if left < end and right > start], "exact"

    # Exact surface must align with token boundaries; this avoids かべ in 浮かべて.
    for exact_value in dict.fromkeys((target, kana)):
        if not exact_value:
            continue
        search_from = 0
        while True:
            start = sentence.find(exact_value, search_from)
            if start < 0:
                break
            end = start + len(exact_value)
            indices = [i for i, (left, right) in enumerate(offsets) if left < end and right > start]
            if indices and offsets[indices[0]][0] == start and offsets[indices[-1]][1] == end:
                kind = "exact" if exact_value in {highlight_surface, target} else "kana_exact"
                return indices, kind
            search_from = start + 1

    # A single lexical unit may be inflected or written in a normalized variant.
    if len(target_tokens) == 1:
        wanted = token_keys(target_tokens[0])
        for index, token in enumerate(sentence_tokens):
            if wanted & token_keys(token):
                return [index], "lemma"

    # Some cards use kana while the example uses the corresponding kanji spelling.
    if kana and len(target_tokens) == 1:
        for index, token in enumerate(sentence_tokens):
            reading = token.reading_form() or ""
            hira = "".join(chr(ord(ch) - 0x60) if "ァ" <= ch <= "ヶ" else ch for ch in reading)
            if hira == kana:
                return [index], "reading"
    return [], "missing"


def main() -> None:
    rows = json.loads((OUTPUT / "candidates.json").read_text(encoding="utf-8"))
    missing: list[dict[str, str]] = []
    counts = {"exact": 0, "kana_exact": 0, "lemma": 0, "reading": 0, "missing": 0}
    for item in rows:
        indices, kind = occurrence(item)
        counts[kind] += 1
        item["target_token_indices"] = indices
        item["target_match_kind"] = kind
        if kind == "missing":
            missing.append({key: str(item.get(key) or "") for key in (
                "id", "kanji", "kana", "meaning", "japanese", "english", "source_id"
            )})

    columns = ["id", "kanji", "kana", "meaning", "japanese", "english", "source_id"]
    with (OUTPUT / "target-occurrence-missing.tsv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, delimiter="\t")
        writer.writeheader()
        writer.writerows(missing)
    (OUTPUT / "target-occurrence-audit.json").write_text(
        json.dumps({"notes": len(rows), "counts": counts}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"notes": len(rows), "counts": counts}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
