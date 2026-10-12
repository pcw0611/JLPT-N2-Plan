# -*- coding: utf-8 -*-
import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()

print("--- Recent study_intervals ---")
cur.execute("SELECT id, session_date, source, duration_seconds, notes FROM study_intervals ORDER BY id DESC LIMIT 5")
for row in cur.fetchall():
    print(row)

print("\n--- Recent study_sessions ---")
cur.execute("SELECT session_date, verified_minutes, summary FROM study_sessions WHERE session_date >= '2026-10-12'")
for row in cur.fetchall():
    print(row)

print("\n--- Recent tests ---")
cur.execute("SELECT test_id, title, test_date, score, total_questions, duration_seconds FROM tests ORDER BY id DESC LIMIT 5")
for row in cur.fetchall():
    print(row)

con.close()
