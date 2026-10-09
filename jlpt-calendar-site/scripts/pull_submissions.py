#!/usr/bin/env python3
"""
JLPT N2 Plan - Pull Online Quiz & Exam Submissions from Cloudflare D1
Fetches recent submissions from /api/submit-exam and merges them into database/jlpt_learning.db.
"""

import os
import sys
import json
import sqlite3
import socket
import urllib.request
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Force IPv4 socket resolution to prevent hanging on broken IPv6 networks on Windows
_orig_getaddrinfo = socket.getaddrinfo
def _getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _getaddrinfo_ipv4

ROOT = Path(__file__).resolve().parents[2]
SITE_ROOT = ROOT / "jlpt-calendar-site"
DB_PATH = ROOT / "database" / "jlpt_learning.db"
SECRET_FILE = SITE_ROOT / ".sync-secret"
LOG_FILE = ROOT / "JLPT_STUDY_LOG.md"

ENDPOINT = "https://jlpt-study-calendar.pcw0611.workers.dev/api/submit-exam"

def get_sync_secret():
    secret = os.environ.get("JLPT_SYNC_SECRET")
    if secret:
        return secret
    if SECRET_FILE.exists():
        return SECRET_FILE.read_text(encoding="utf-8").strip()
    return None

def fetch_submissions(secret):
    req = urllib.request.Request(
        f"{ENDPOINT}?limit=50",
        headers={
            "Authorization": f"Bearer {secret}",
            "User-Agent": "JLPT-Study-Sync/1.0",
        },
        method="GET"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
            if data.get("ok"):
                return data.get("submissions", [])
    except Exception as e:
        print(f"  [경고] 온라인 제출 데이터 조회 실패 ({type(e).__name__}): {e}")
    return []

def sync_submissions():
    secret = get_sync_secret()
    if not secret:
        print("  [알림] 동기화 시크릿이 없어 온라인 제출 조회를 건너뜁니다.")
        return 0

    submissions = fetch_submissions(secret)
    if not submissions:
        return 0

    new_count = 0
    with sqlite3.connect(str(DB_PATH)) as conn:
        cursor = conn.cursor()

        # Ensure unique index or check existing test IDs
        existing_test_ids = set(r[0] for r in cursor.execute("SELECT id FROM tests").fetchall())

        for sub in submissions:
            sub_id = sub.get("id")
            test_id = f"online-sub-{sub_id}"
            if test_id in existing_test_ids:
                continue

            date = sub.get("date")
            title = sub.get("title", "JLPT 온라인 퀴즈")
            course = sub.get("course") or ""

            # Ignore dummy probe tests
            if "검증 테스트" in course or "검증 테스트" in title:
                continue

            exam_type = sub.get("examType") or sub.get("exam_type", "exam")
            sec = int(sub.get("elapsedSeconds") or sub.get("elapsed_seconds") or 0)
            total = int(sub.get("totalQuestions") or sub.get("total_questions") or 0)
            correct = int(sub.get("correctCount") or sub.get("correct_count") or 0)
            accuracy = int(sub.get("accuracy") or 0)
            created_at = sub.get("createdAt") or sub.get("created_at") or datetime.now().isoformat()

            m = sec // 60
            s = sec % 60
            time_str = f"{m}분 {s}초" if m > 0 else f"{s}초"

            source_class = "공식 모의고사" if "模試" in title else "자체 제작"

            # 1. Insert into tests table
            cursor.execute("""
                INSERT INTO tests (
                    id, test_date, title, source_class, target_level, response_format,
                    total_items, correct_items, unknown_items, unanswered_items,
                    elapsed_seconds, time_limit_seconds, diagnostic_weight, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                test_id,
                date,
                f"{date} {title} ({course})".strip(),
                source_class,
                "N2",
                "선택형",
                total,
                correct,
                0,
                0,
                sec,
                None,
                0.3,
                f"[온라인 자동 제출] 코스: {course}, 정답률: {accuracy}%"
            ))

            # 2. Insert into study_intervals table
            note_text = f"[{date} {title}] {time_str} (코스: {course}, 정답: {correct}/{total}, 정답률: {accuracy}%)"
            cursor.execute("""
                INSERT INTO study_intervals (
                    session_date, started_at, duration_seconds, status, source, notes
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                date,
                created_at,
                sec,
                "completed",
                "quiz",
                note_text
            ))

            # 3. Update or Insert study_sessions table
            session_row = cursor.execute("SELECT verified_minutes FROM study_sessions WHERE session_date = ?", (date,)).fetchone()
            add_min = round(sec / 60)
            if session_row:
                new_min = session_row[0] + add_min
                cursor.execute("UPDATE study_sessions SET verified_minutes = ?, updated_at = CURRENT_TIMESTAMP WHERE session_date = ?", (new_min, date))
            else:
                cursor.execute("""
                    INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary)
                    VALUES (?, ?, 0, ?)
                """, (date, add_min, f"{title} 자동 기록"))

            existing_test_ids.add(test_id)
            new_count += 1
            print(f"  -> [자동 수집 등록] {title} ({time_str}, {correct}/{total}, {accuracy}%)")

        conn.commit()

    if new_count > 0:
        print(f"  -> 총 {new_count}건의 온라인 시험 결과가 로컬 DB에 자동 통합되었습니다.")
    return new_count

if __name__ == "__main__":
    count = sync_submissions()
    sys.exit(0)
