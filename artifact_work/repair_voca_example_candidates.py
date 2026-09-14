"""Repair falsely matched examples using strict whole-word/lemma corpus matches."""
from __future__ import annotations

import json
from pathlib import Path

from audit_voca_target_occurrence import TOKENIZER, MODE, clean, occurrence, token_keys
from build_voca_n2_examples import candidate_score, corpus_rows


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "anki" / "voca-examples-20260901"


def main() -> None:
    path = OUTPUT / "candidates.json"
    candidates = json.loads(path.read_text(encoding="utf-8"))
    rows = corpus_rows()
    missing = [item for item in candidates if occurrence(item)[1] == "missing"]
    wanted_keys: set[str] = set()
    item_keys: dict[str, set[str]] = {}
    for item in missing:
        target = clean(item["kanji"])
        tokens = list(TOKENIZER.tokenize(target, MODE))
        keys = token_keys(tokens[0]) if len(tokens) == 1 else set()
        item_keys[item["id"]] = keys
        wanted_keys.update(keys)

    lexical_index: dict[str, list[int]] = {key: [] for key in wanted_keys}
    for row_index, row in enumerate(rows):
        seen: set[str] = set()
        for token in TOKENIZER.tokenize(row.japanese, MODE):
            seen.update(token_keys(token) & wanted_keys)
        for key in seen:
            lexical_index[key].append(row_index)

    repaired = 0
    for item in missing:
        target = clean(item["kanji"])
        kana = clean(item["kana"])
        row_ids = {
            index
            for index, row in enumerate(rows)
            if (target and target in row.japanese) or (kana and kana in row.japanese)
        }
        for key in item_keys[item["id"]]:
            row_ids.update(lexical_index.get(key, []))
        valid: list[tuple[int, int]] = []
        for row_id in row_ids:
            probe = {**item, "japanese": rows[row_id].japanese}
            if occurrence(probe)[1] != "missing":
                valid.append((candidate_score(rows[row_id], target), row_id))
        if not valid:
            continue
        score, row_id = max(valid, key=lambda pair: (pair[0], -len(rows[pair[1]].japanese), -int(rows[pair[1]].sid)))
        previous = item["japanese"]
        selected = rows[row_id]
        item.update({
            "source_id": selected.sid,
            "japanese": selected.japanese,
            "english": selected.english,
            "score": score,
            "repaired_from": previous,
            "repair_kind": occurrence({**item, "japanese": selected.japanese})[1],
        })
        repaired += 1

    path.write_text(json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8")
    remaining = sum(occurrence(item)[1] == "missing" for item in candidates)
    print(json.dumps({"initial_missing": len(missing), "repaired": repaired, "remaining": remaining}, ensure_ascii=False))


if __name__ == "__main__":
    main()
