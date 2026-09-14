"""Create deterministic QA reports for the generated Korean translations."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "anki" / "voca-examples-20260901"
JAPANESE_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]")
HANGUL_RE = re.compile(r"[가-힣]")


def main() -> None:
    candidates = json.loads((OUTPUT / "candidates.json").read_text(encoding="utf-8"))
    payload = json.loads((OUTPUT / "translations-ko.json").read_text(encoding="utf-8"))
    translations = payload["translations"]
    unique = list(dict.fromkeys(row["japanese"] for row in candidates))
    flags: list[dict[str, str]] = []
    rows: list[dict[str, str]] = []

    for item in candidates:
        source = item["japanese"]
        target = translations.get(source, "")
        reasons: list[str] = []
        if not target:
            reasons.append("empty")
        if target and not HANGUL_RE.search(target):
            reasons.append("no_hangul")
        if JAPANESE_RE.search(target):
            reasons.append("japanese_remaining")
        ratio = len(target) / max(1, len(source))
        if ratio < 0.25:
            reasons.append("very_short")
        if ratio > 3.0:
            reasons.append("very_long")
        if "<unk>" in target.lower() or "##" in target:
            reasons.append("token_artifact")
        row = {
            "id": item["id"],
            "kanji": item["kanji"],
            "kana": item["kana"],
            "meaning": item["meaning"],
            "japanese": source,
            "korean": target,
            "english": item.get("english") or "",
            "flags": ",".join(reasons),
        }
        rows.append(row)
        if reasons:
            flags.append(row)

    columns = ["id", "kanji", "kana", "meaning", "japanese", "korean", "english", "flags"]
    for name, selected in (
        ("translation-all.tsv", rows),
        ("translation-flags.tsv", flags),
        ("translation-review-sample.tsv", [rows[i] for i in range(0, len(rows), 31)]),
    ):
        with (OUTPUT / name).open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=columns, delimiter="\t")
            writer.writeheader()
            writer.writerows(selected)

    report = {
        "notes": len(candidates),
        "unique_sentences": len(unique),
        "translated_unique_sentences": sum(sentence in translations for sentence in unique),
        "flagged_notes": len(flags),
        "flag_counts": {
            reason: sum(reason in row["flags"].split(",") for row in flags)
            for reason in ("empty", "no_hangul", "japanese_remaining", "very_short", "very_long", "token_artifact")
        },
    }
    (OUTPUT / "translation-audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
