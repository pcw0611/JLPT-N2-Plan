"""Record the live Anki time delta and user-reported lecture review for 2026-08-31."""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
DATE = "2026-08-31"
ANKI_MARKER = "[anki-live-time-sync-20260831-645]"
LECTURE_MARKER = "[lecture-video-review-20260831-40m]"

# Previous approved Anki snapshot: 522 reviews, 95m 06.6s, stored as 95 whole minutes.
# Current local revlog snapshot: 645 reviews, 152m 52.009s.
ANKI_ADDED_MINUTES = 57
LECTURE_MINUTES = 40

live_anki = {
    "source": "local collection revlog snapshot",
    "answeredCards": 645,
    "uniqueCards": 242,
    "studyMilliseconds": 9_172_009,
    "studyMinutesExact": 152.8668166667,
    "studyTimeText": "152분 52.009초",
    "secondsPerCard": 14.22,
    "againCount": 160,
    "againPct": 24.81,
    "learningCards": 415,
    "reviewCards": 187,
    "relearningCards": 43,
    "filteredCards": 0,
    "dayBoundary": "2026-08-31 04:00 KST; midnight query produced the same result",
    "capturedAt": datetime.now(timezone.utc).isoformat(),
}

con = sqlite3.connect(DB)
with con:
    row = con.execute(
        "SELECT verified_minutes, summary FROM study_sessions WHERE session_date=?", (DATE,)
    ).fetchone()
    if row is None:
        raise RuntimeError("The existing 2026-08-31 Anki session is missing")

    minutes, summary = row[0], row[1] or ""
    additions = []
    if ANKI_MARKER not in summary:
        minutes += ANKI_ADDED_MINUTES
        additions.append(
            f"{ANKI_MARKER} Anki 누적 645회·152분 52.009초. "
            "기존 522회·95분 06.6초 대비 123회·57분 45.409초 증가; "
            "DB 정수 시간 57분 추가."
        )
    if LECTURE_MARKER not in summary:
        minutes += LECTURE_MINUTES
        additions.append(
            f"{LECTURE_MARKER} 사용자 확인 강의 동영상 복습 약 40분; "
            "별도 학습으로 DB 정수 시간 40분 추가."
        )
    if additions:
        merged = (summary.rstrip() + "\n" + "\n".join(additions)).strip()
        con.execute(
            "UPDATE study_sessions SET verified_minutes=?, summary=?, updated_at=CURRENT_TIMESTAMP WHERE session_date=?",
            (minutes, merged, DATE),
        )

    stats = con.execute(
        "SELECT payload_json FROM anki_daily_stats WHERE snapshot_date=?", (DATE,)
    ).fetchone()
    if stats is None:
        raise RuntimeError("The existing 2026-08-31 Anki stats snapshot is missing")
    payload = json.loads(stats[0])
    payload.update(
        {
            "answeredCards": live_anki["answeredCards"],
            "studyMinutes": round(live_anki["studyMinutesExact"], 2),
            "secondsPerCard": live_anki["secondsPerCard"],
            "againCount": live_anki["againCount"],
            "againPct": live_anki["againPct"],
            "learningCards": live_anki["learningCards"],
            "reviewCards": live_anki["reviewCards"],
            "relearningCards": live_anki["relearningCards"],
            "filteredCards": live_anki["filteredCards"],
            "liveRevlogSnapshot": live_anki,
        }
    )
    payload["sourceNote"] = (
        "10:01 PDF의 예측·카드 구성·유지율은 보존. "
        "당일 누적 답변 수·시간·답변 유형은 로컬 revlog 실측으로 갱신."
    )
    con.execute(
        "UPDATE anki_daily_stats SET payload_json=?, updated_at=CURRENT_TIMESTAMP WHERE snapshot_date=?",
        (json.dumps(payload, ensure_ascii=False), DATE),
    )

assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()
session = con.execute(
    "SELECT verified_minutes, has_untracked_activity FROM study_sessions WHERE session_date=?", (DATE,)
).fetchone()
print(
    json.dumps(
        {
            "date": DATE,
            "anki": live_anki,
            "lectureReviewMinutes": LECTURE_MINUTES,
            "verifiedMinutes": session[0],
            "hasUntrackedActivity": bool(session[1]),
        },
        ensure_ascii=False,
    )
)
con.close()
