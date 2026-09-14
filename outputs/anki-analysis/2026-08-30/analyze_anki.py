import csv
import html
import json
import re
import sqlite3
import statistics
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DB = ROOT / "collection-full.anki2"
TODAY = date(2026, 8, 30)
TZ = timezone(timedelta(hours=9), name="Asia/Seoul")


def clean(value: str) -> str:
    value = re.sub(r"<br\s*/?>", " / ", value or "", flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
con.create_collation(
    "unicase",
    lambda a, b: (a.casefold() > b.casefold()) - (a.casefold() < b.casefold()),
)

decks = {
    row["id"]: row["name"].replace("\x1f", "::")
    for row in con.execute("SELECT id, name FROM decks")
}


def level_for(deck_name: str) -> str:
    for level in ("N5", "N4", "N3", "N2"):
        if f"-{level}" in deck_name:
            return level
    return "기타"


def fields(row):
    vals = row["flds"].split("\x1f")
    if row["mid"] == 1760303581300:
        vals += [""] * (6 - len(vals))
        return {
            "source_id": clean(vals[0]),
            "word": clean(vals[1]),
            "reading": clean(vals[2]),
            "meaning": clean(vals[3]),
            "sentences": clean(vals[4]),
        }
    vals += [""] * (3 - len(vals))
    return {
        "source_id": "",
        "word": clean(vals[0]),
        "reading": clean(vals[1]) if len(vals) > 1 else "",
        "meaning": clean(vals[2]) if len(vals) > 2 else "",
        "sentences": "",
    }


card_rows = list(
    con.execute(
        """
        SELECT c.id AS cid, c.did, c.reps, c.lapses, c.ivl, c.queue, c.type,
               n.id AS nid, n.mid, n.flds
        FROM cards c JOIN notes n ON n.id = c.nid
        """
    )
)
cards = {}
for row in card_rows:
    item = dict(row)
    item.update(fields(row))
    item["deck"] = decks.get(row["did"], str(row["did"]))
    item["level"] = level_for(item["deck"])
    cards[row["cid"]] = item

review_rows = []
for row in con.execute("SELECT id, cid, ease, ivl, lastIvl, factor, time, type FROM revlog ORDER BY id"):
    ts = datetime.fromtimestamp(row["id"] / 1000, TZ)
    item = dict(row)
    item["timestamp"] = ts.isoformat()
    item["local_date"] = ts.date().isoformat()
    item["card"] = cards.get(row["cid"])
    review_rows.append(item)

today = [r for r in review_rows if r["local_date"] == TODAY.isoformat()]


def review_stats(rows):
    times = [r["time"] / 1000 for r in rows]
    return {
        "events": len(rows),
        "unique_cards": len({r["cid"] for r in rows}),
        "ratings": dict(sorted(Counter(r["ease"] for r in rows).items())),
        "again_events": sum(r["ease"] == 1 for r in rows),
        "pass_events": sum(r["ease"] > 1 for r in rows),
        "event_pass_rate": round(100 * sum(r["ease"] > 1 for r in rows) / len(rows), 1) if rows else None,
        "answer_time_seconds": round(sum(times), 1),
        "answer_time_minutes": round(sum(times) / 60, 1),
        "median_seconds": round(statistics.median(times), 1) if times else None,
        "mean_seconds": round(statistics.mean(times), 1) if times else None,
    }


deck_summary = []
for level in ("N5", "N4", "N3", "N2", "기타"):
    subset = [c for c in cards.values() if c["level"] == level]
    if not subset:
        continue
    revs = [r for r in today if r["card"] and r["card"]["level"] == level]
    all_revs = [r for r in review_rows if r["card"] and r["card"]["level"] == level]
    deck_summary.append(
        {
            "level": level,
            "cards": len(subset),
            "introduced": sum(c["reps"] > 0 for c in subset),
            "unseen": sum(c["reps"] == 0 for c in subset),
            "mature_ivl_ge_21d": sum(c["reps"] > 0 and c["ivl"] >= 21 for c in subset),
            "cards_with_lapses": sum(c["lapses"] > 0 for c in subset),
            "total_lapses": sum(c["lapses"] for c in subset),
            "today": review_stats(revs),
            "all_time": review_stats(all_revs),
        }
    )

by_card_today = defaultdict(list)
for row in today:
    by_card_today[row["cid"]].append(row)

difficult_today = []
for cid, rows in by_card_today.items():
    if not any(r["ease"] in (1, 2) for r in rows):
        continue
    card = cards[cid]
    difficult_today.append(
        {
            "level": card["level"],
            "deck": card["deck"],
            "word": card["word"],
            "reading": card["reading"],
            "meaning": card["meaning"],
            "ratings_today": [r["ease"] for r in rows],
            "final_rating_today": rows[-1]["ease"],
            "answer_seconds_today": round(sum(r["time"] for r in rows) / 1000, 1),
            "reps": card["reps"],
            "lapses": card["lapses"],
            "current_interval_days": card["ivl"] if card["ivl"] >= 0 else None,
        }
    )
difficult_today.sort(key=lambda x: (x["final_rating_today"], -x["lapses"], x["level"], x["word"]))

repeated_lapses = []
for card in cards.values():
    if card["lapses"] < 2:
        continue
    repeated_lapses.append(
        {
            "level": card["level"],
            "deck": card["deck"],
            "word": card["word"],
            "reading": card["reading"],
            "meaning": card["meaning"],
            "reps": card["reps"],
            "lapses": card["lapses"],
            "current_interval_days": card["ivl"] if card["ivl"] >= 0 else None,
        }
    )
repeated_lapses.sort(key=lambda x: (-x["lapses"], -x["reps"], x["word"]))

last_rating_counts = Counter(rows[-1]["ease"] for rows in by_card_today.values())
result = {
    "source": {
        "path": r"C:\Users\pcw06\바탕 화면\모든 덱.apkg",
        "sha256": "7593c0ab2b46bbe405a6a037a57d377e24ba549a580beb88c2dabec1a851ecb1",
        "read_only": True,
    },
    "collection": {
        "notes": len({c["nid"] for c in cards.values()}),
        "cards": len(cards),
        "review_events": len(review_rows),
        "decks": len(decks),
    },
    "today": {
        **review_stats(today),
        "last_rating_per_card": dict(sorted(last_rating_counts.items())),
        "cards_with_any_again": sum(any(r["ease"] == 1 for r in rows) for rows in by_card_today.values()),
        "cards_with_any_hard": sum(any(r["ease"] == 2 for r in rows) for rows in by_card_today.values()),
        "cards_ending_again": sum(rows[-1]["ease"] == 1 for rows in by_card_today.values()),
        "cards_ending_hard": sum(rows[-1]["ease"] == 2 for rows in by_card_today.values()),
    },
    "by_level": deck_summary,
    "difficult_today": difficult_today,
    "repeated_lapses_2plus": repeated_lapses,
}

(ROOT / "anki-analysis-20260830.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
)

with (ROOT / "anki-today-difficult-20260830.csv").open("w", encoding="utf-8-sig", newline="") as f:
    fields_out = list(difficult_today[0].keys()) if difficult_today else ["word"]
    writer = csv.DictWriter(f, fieldnames=fields_out)
    writer.writeheader()
    writer.writerows(difficult_today)

with (ROOT / "anki-repeated-lapses-20260830.csv").open("w", encoding="utf-8-sig", newline="") as f:
    fields_out = list(repeated_lapses[0].keys()) if repeated_lapses else ["word"]
    writer = csv.DictWriter(f, fieldnames=fields_out)
    writer.writeheader()
    writer.writerows(repeated_lapses)

print(json.dumps(result, ensure_ascii=False, indent=2))
