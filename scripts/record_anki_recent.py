import sqlite3
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta

DB_PATH = 'database/jlpt_learning.db'
ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_recent')

def run():
    TEMP_DIR.mkdir(exist_ok=True)
    shutil.copy2(ANKI_SRC / 'collection.anki2', TEMP_DIR / 'collection.anki2')
    if (ANKI_SRC / 'collection.anki2-wal').exists():
        shutil.copy2(ANKI_SRC / 'collection.anki2-wal', TEMP_DIR / 'collection.anki2-wal')

    con_anki = sqlite3.connect(TEMP_DIR / 'collection.anki2')
    cur_anki = con_anki.cursor()

    cur_anki.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
    queue_counts = dict(cur_anki.fetchall())
    new_rem = queue_counts.get(0, 0)
    learn_rem = queue_counts.get(1, 0) + queue_counts.get(3, 0)
    rev_rem = queue_counts.get(2, 0)

    cur_anki.execute('SELECT id, name FROM decks')
    deck_names = {r[0]: r[1] for r in cur_anki.fetchall()}

    KST = timezone(timedelta(hours=9))
    dt_19_start = datetime(2026, 9, 19, 4, 0, 0, tzinfo=KST)
    dt_20_start = datetime(2026, 9, 20, 4, 0, 0, tzinfo=KST)
    dt_21_start = datetime(2026, 9, 21, 4, 0, 0, tzinfo=KST)

    ms_19 = int(dt_19_start.timestamp() * 1000)
    ms_20 = int(dt_20_start.timestamp() * 1000)
    ms_21 = int(dt_21_start.timestamp() * 1000)

    days_data = [
        ('2026-09-19', ms_19, ms_20, 0),    # 0 exam minutes
        ('2026-09-20', ms_20, ms_21, 115)  # 115 exam minutes (115m 36s)
    ]

    con_db = sqlite3.connect(DB_PATH)
    cur_db = con_db.cursor()

    for date_str, s_ms, e_ms, exam_mins in days_data:
        # Reviews count & time
        cur_anki.execute('''
            SELECT count(*), sum(time), count(distinct cid)
            FROM revlog
            WHERE id >= ? AND id < ?
        ''', (s_ms, e_ms))
        cnt, total_time_ms, distinct_cards = cur_anki.fetchone()
        cnt = cnt or 0
        total_time_ms = total_time_ms or 0
        sec = total_time_ms / 1000.0
        anki_mins = sec / 60.0
        sec_per_card = round(sec / cnt, 2) if cnt > 0 else 0

        # Ratings
        cur_anki.execute('''
            SELECT ease, count(*)
            FROM revlog
            WHERE id >= ? AND id < ?
            GROUP BY ease
        ''', (s_ms, e_ms))
        rating_map = dict(cur_anki.fetchall())
        again_c = rating_map.get(1, 0)
        hard_c = rating_map.get(2, 0)
        good_c = rating_map.get(3, 0)
        easy_c = rating_map.get(4, 0)
        again_pct = round((again_c / cnt) * 100, 2) if cnt > 0 else 0

        # Learning reviews vs review done
        cur_anki.execute('''
            SELECT type, count(*)
            FROM revlog
            WHERE id >= ? AND id < ?
            GROUP BY type
        ''', (s_ms, e_ms))
        type_map = dict(cur_anki.fetchall())
        # type 0: learn, 1: review, 2: relearn, 3: filtered
        learn_revs = type_map.get(0, 0) + type_map.get(2, 0)
        revs_done = type_map.get(1, 0)

        # Deck breakdown
        cur_anki.execute('''
            SELECT c.did, count(*), count(distinct r.cid), sum(r.time)
            FROM revlog r
            JOIN cards c ON r.cid = c.id
            WHERE r.id >= ? AND r.id < ?
            GROUP BY c.did
            ORDER BY count(*) DESC
        ''', (s_ms, e_ms))
        deck_breakdown = []
        for did, d_count, d_dist, d_tms in cur_anki.fetchall():
            dname = deck_names.get(did, f'did:{did}')
            d_sec = d_tms / 1000.0
            deck_breakdown.append({
                'name': dname,
                'reviews': d_count,
                'cards': d_dist,
                'minutes': round(d_sec / 60.0, 1),
                'seconds': round(d_sec, 1)
            })

        payload = {
            'schema': 'daily_summary_v1',
            'scope': 'all_decks',
            'scopeLabel': '전체 덱',
            'answeredCards': cnt,
            'studyMinutes': round(anki_mins, 2),
            'secondsPerCard': sec_per_card,
            'againCount': again_c,
            'againPct': again_pct,
            'learningReviews': learn_revs,
            'reviewsDone': revs_done,
            'ratings': {
                'again': again_c,
                'hard': hard_c,
                'good': good_c,
                'easy': easy_c
            },
            'cardsRemaining': {
                'new': new_rem,
                'learning': learn_rem,
                'review': rev_rem
            },
            'decks': deck_breakdown
        }

        # 1. Update anki_daily_stats
        cur_db.execute('''
            INSERT INTO anki_daily_stats (snapshot_date, scope_label, payload_json, source_filename, captured_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(snapshot_date) DO UPDATE SET
                scope_label = excluded.scope_label,
                payload_json = excluded.payload_json,
                source_filename = excluded.source_filename,
                captured_at = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
        ''', (date_str, '전체 덱', json.dumps(payload, ensure_ascii=False), f'Anki revlog snapshot {date_str}'))

        # 2. Update study_sessions
        if date_str == '2026-09-19':
            total_sec = sec
            whole_mins = int(total_sec // 60)
            rem_sec = round(total_sec % 60, 2)
            summary = (
                f"[2026-09-19] 총 순수 학습시간 {whole_mins}분 {rem_sec}초 ({round(total_sec/60, 2)}분 / 약 2시간 1분). "
                f"Anki 단어 세션 741회 실측 (고유 카드 153장): "
                f"1) JLPT 한끝 Voca 4-N2 집중 회독 646회 (125장, 111.1분), N3 86회 (23장, 9.7분), N5 5회, 공통의상 2회, N4 2회. "
                f"2) 학습 반응 분포: Again 652 (87.99%), Hard 1 (0.13%), Good 13 (1.75%), Easy 75 (10.12%). "
                f"잔여 {rem_sec}초 보존."
            )
            cur_db.execute('''
                INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary)
                VALUES ('2026-09-19', ?, 0, ?)
                ON CONFLICT(session_date) DO UPDATE SET
                    verified_minutes = excluded.verified_minutes,
                    summary = excluded.summary,
                    updated_at = CURRENT_TIMESTAMP
            ''', (whole_mins, summary))

        elif date_str == '2026-09-20':
            exam_sec = 6936.0 # 115m 36s
            combined_sec = sec + exam_sec # anki sec + exam sec
            combined_whole_mins = int(combined_sec // 60) # 290 mins
            combined_rem_sec = round(combined_sec % 60, 2) # 51.65 sec
            summary = (
                f"[2026-09-20] 총 순수 학습시간 {combined_whole_mins}분 {combined_rem_sec}초 (약 4시간 51분 / {round(combined_sec/60, 2)}분). "
                f"1) ★JLPT N2 공식 문제집 제2집 전 영역 완본 실전모의고사 (107문항) 완주★: 115분 36초 (115.6분), 119/180점(66.4%), 독해 76%·청해 75% 고득점, 전 영역 과락 0건 달성. "
                f"2) ★Anki 단어·문법 세션 1,031회 실측 (175분 15.65초 / 2시간 55분 16초, 고유 카드 213장)★: "
                f"★N2 단어장 전량 1차 완독(미학습 new 0장, 100% 진입) 대달성!★ (N2 집중 907회 157.4분, N2문법 001-150 예문 복습 61회 8.0분, N3 52회 9.2분, N4 7회, 공통의상 2회, N5 2회). "
                f"3) 학습 반응: Again 850 (82.44%), Hard 53 (5.14%), Good 21 (2.04%), Easy 107 (10.38%). "
                f"잔여 {combined_rem_sec}초 보존."
            )
            cur_db.execute('''
                INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary)
                VALUES ('2026-09-20', ?, 0, ?)
                ON CONFLICT(session_date) DO UPDATE SET
                    verified_minutes = excluded.verified_minutes,
                    summary = excluded.summary,
                    updated_at = CURRENT_TIMESTAMP
            ''', (combined_whole_mins, summary))

        print(f"Recorded Anki stats for {date_str}: {cnt} reviews, anki_mins={round(anki_mins, 1)}")

    con_db.commit()
    con_db.close()
    con_anki.close()
    print("All Anki records for 9/19 and 9/20 successfully updated in DB!")

if __name__ == '__main__':
    run()
