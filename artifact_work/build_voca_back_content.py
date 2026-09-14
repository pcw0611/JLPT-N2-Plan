"""Build final Anki Voca back-field HTML with ruby, target emphasis, and Korean translation."""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "anki" / "voca-examples-20260901"
WORK = ROOT / "tmp" / "voca-example-work"
CHUNK_DIR = OUTPUT / "phase2-update-chunks"
sys.path.insert(0, str(WORK / "pydeps"))

from sudachipy import dictionary, tokenizer  # type: ignore

from audit_voca_target_occurrence import occurrence


MODE = tokenizer.Tokenizer.SplitMode.C
TOKENIZER = dictionary.Dictionary().create()
KANJI_RE = __import__("re").compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


def katakana_to_hiragana(value: str) -> str:
    return "".join(chr(ord(ch) - 0x60) if "ァ" <= ch <= "ヶ" else ch for ch in value)


def render_japanese(item: dict[str, Any]) -> str:
    tokens = list(TOKENIZER.tokenize(item["japanese"], MODE))
    matched, kind = occurrence(item)
    if not matched or kind == "missing":
        raise RuntimeError(f'Target missing after QA: {item["id"]}')
    matched_set = set(matched)
    first, last = min(matched), max(matched)
    parts: list[str] = []
    for index, token in enumerate(tokens):
        surface = token.surface()
        reading = katakana_to_hiragana(token.reading_form() or "")
        if surface == item["kanji"] and item["kana"] and "〜" not in item["kana"]:
            reading = item["kana"]
        escaped_surface = html.escape(surface)
        if KANJI_RE.search(surface) and reading and reading != surface:
            rendered = f"<ruby>{escaped_surface}<rt>{html.escape(reading)}</rt></ruby>"
        else:
            rendered = escaped_surface
        if index == first:
            parts.append('<span class="target-word">')
        parts.append(rendered)
        if index == last:
            parts.append("</span>")
    if set(range(first, last + 1)) != matched_set:
        raise RuntimeError(f'Non-contiguous target span: {item["id"]}')
    return "".join(parts)


def main() -> None:
    candidates = json.loads((OUTPUT / "candidates.json").read_text(encoding="utf-8"))
    translation_payload = json.loads((OUTPUT / "translations-ko.json").read_text(encoding="utf-8"))
    translations = translation_payload["translations"]
    previous_updates = json.loads((OUTPUT / "prepared-updates.json").read_text(encoding="utf-8"))

    phase2_backup = {
        "description": "Japanese-only sentences field immediately before translation/highlight update",
        "count": len(previous_updates),
        "notes": previous_updates,
    }
    (OUTPUT / "sentences-ja-only-backup.json").write_text(
        json.dumps(phase2_backup, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    updates: list[dict[str, Any]] = []
    final_rows: list[dict[str, Any]] = []
    for item in candidates:
        korean = translations.get(item["japanese"], "").strip()
        if not korean:
            raise RuntimeError(f'Translation missing: {item["id"]}')
        japanese_html = render_japanese(item)
        field_html = (
            f'<div class="example-ja">{japanese_html}</div>'
            f'<div class="example-ko"><span class="translation-label">해석</span>'
            f'<span class="translation-text">{html.escape(korean)}</span></div>'
        )
        if field_html.count('class="target-word"') != 1:
            raise RuntimeError(f'Unexpected highlight count: {item["id"]}')
        updates.append({"id": item["note_id"], "fields": {"sentences": field_html}})
        final_rows.append({
            "id": item["id"],
            "note_id": item["note_id"],
            "kanji": item["kanji"],
            "japanese": item["japanese"],
            "korean": korean,
            "target_match_kind": occurrence(item)[1],
            "field_html": field_html,
        })

    if len(updates) != 2734:
        raise RuntimeError(f"Expected 2734 updates, got {len(updates)}")
    (OUTPUT / "phase2-prepared-updates.json").write_text(
        json.dumps(updates, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUTPUT / "phase2-final-content.json").write_text(
        json.dumps(final_rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    for old in CHUNK_DIR.glob("*.json"):
        old.unlink()
    for index, start in enumerate(range(0, len(updates), 100), start=1):
        (CHUNK_DIR / f"chunk-{index:02d}.json").write_text(
            json.dumps(updates[start : start + 100], ensure_ascii=False), encoding="utf-8"
        )
    report = {
        "notes": len(updates),
        "unique_sentences": len(set(row["japanese"] for row in final_rows)),
        "highlighted": sum('class="target-word"' in row["field_html"] for row in final_rows),
        "translated": sum(bool(row["korean"]) for row in final_rows),
        "chunks": len(list(CHUNK_DIR.glob("*.json"))),
    }
    (OUTPUT / "phase2-build-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
