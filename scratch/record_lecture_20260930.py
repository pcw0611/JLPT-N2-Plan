import sqlite3
from datetime import datetime

DB_PATH = 'database/jlpt_learning.db'

def update_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Check current 2026-09-30 session
    cursor.execute("SELECT id, verified_minutes, summary FROM study_sessions WHERE session_date = '2026-09-30'")
    row = cursor.fetchone()
    if not row:
        print("Error: No session for 2026-09-30")
        return

    session_id, current_minutes, current_summary = row
    new_minutes = 127 + 60 # 187 minutes (3 hours 7 minutes)

    new_summary = (
        "[2026-09-30] 당일 총 학습시간 187분 (3시간 7분 / Anki 127.88분 + N2 정규 강의 60분). "
        "1) N2 정규 인강/강의 1시간(60분) 집중 수강 완료. "
        "2) Anki 단어·한자 1,111회 학습 완료 (08:03~15:13, 순 카드 540장, 카드당 6.91초, JLPT 단어장 Voca N2 825회 등). "
        "3) 오늘 20:00 제2회 실전 모의고사 (2023.12 過去問完本 104문항) 응시 예정."
    )

    # 2. Update study_sessions
    cursor.execute("""
        UPDATE study_sessions 
        SET verified_minutes = ?, summary = ?, updated_at = CURRENT_TIMESTAMP
        WHERE session_date = '2026-09-30'
    """, (new_minutes, new_summary))

    # 3. Insert study_interval for the 1-hour lecture
    cursor.execute("""
        INSERT INTO study_intervals (session_date, started_at, ended_at, duration_seconds, status, source, notes)
        VALUES ('2026-09-30', '2026-09-30T17:15:00+09:00', '2026-09-30T18:15:00+09:00', 3600, 'completed', 'chat_confirmed', '사용자 명시 보고: N2 인강/강의 1시간(60분) 시청 완료')
    """)

    conn.commit()
    print(f"Updated 2026-09-30 session in DB: {current_minutes}m -> {new_minutes}m (added 60m lecture)")

    # Verify
    cursor.execute("SELECT session_date, verified_minutes, summary FROM study_sessions WHERE session_date = '2026-09-30'")
    print("Verified session:", cursor.fetchone())
    cursor.execute("SELECT * FROM study_intervals WHERE session_date = '2026-09-30'")
    print("Verified intervals:", cursor.fetchall())
    conn.close()

if __name__ == '__main__':
    update_db()
