"""Record N2 grammar completion (28~31강, 118~150번) and update study time for 2026-09-08."""

import sqlite3
import json
import shutil
from pathlib import Path

ROOT = Path(r"c:\Users\pcw06\Documents\Codex\JLPT-N2-Plan")
DB = ROOT / "database" / "jlpt_learning.db"
DATE = "2026-09-08"

# 1. Anki study time today: 16,524.05 seconds (275분 24.05초)
# 2. Lectures today (28~31강, 118~150번 완강):
#    - 28강 (118~125): 23분 01초 (1,381초)
#    - 29강 (126~133): 22분 30초 (1,350초)
#    - 30강 (134~141): 24분 24초 (1,464초)
#    - 31강 (142~150): 21분 30초 (1,290초)
#    - Total lecture time: 5,485초 (91분 25초 / 1시간 31분 25초)
# 3. Combined total: 16,524.05 + 5,485 = 22,009.05초
#    - 366분 49.05초 (6시간 6분 49.05초)
#    - Integer verified_minutes: 366분 (잔여 49.05초 보존)

WHOLE_MINUTES = 366

SESSION_SUMMARY = (
    "[2026-09-08] Anki 단어·문법 세션 1,968회(275분 24초, 4시간 35분 24초) + "
    "다락원 N2 문법 28~31강(118~150번 완강!) 4개 강의 91분 25초 (23:01, 22:30, 24:24, 21:30). "
    "당일 총 366분 49초 (6시간 6분 49초). N2 문법 150개 전 문형 100% 완강 대기록 달성! "
    "Anki 118~150번 예문 카드 33장 추가 완료(덱 총 143장 풀세트 구축). 잔여 49초 보존."
)

con = sqlite3.connect(DB)
with con:
    con.execute(
        "UPDATE study_sessions SET verified_minutes=?, summary=?, updated_at=CURRENT_TIMESTAMP WHERE session_date=?",
        (WHOLE_MINUTES, SESSION_SUMMARY, DATE)
    )
    assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    assert not con.execute("PRAGMA foreign_key_check").fetchall()

print("Successfully updated study_sessions in DB:")
row = con.execute("SELECT session_date, verified_minutes, summary FROM study_sessions WHERE session_date=?", (DATE,)).fetchone()
print(f"Date: {row[0]}, Minutes: {row[1]}")
print(f"Summary: {row[2]}")

con.close()

# Copy script to database folder
target_script = ROOT / "database" / "record_lecture_20260908.py"
shutil.copy2(__file__, target_script)
print(f"Copied script to {target_script}")
