import sqlite3

conn = sqlite3.connect('database/jlpt_learning.db')
c = conn.cursor()
c.execute('SELECT id, test_date, title, source_class, target_level, difficulty_label, total_items, correct_items, unknown_items, unanswered_items, elapsed_seconds, notes FROM tests ORDER BY test_date DESC LIMIT 15')
rows = c.fetchall()

with open('artifact_work/tests_summary.txt', 'w', encoding='utf-8') as f:
    for row in rows:
        f.write(f"ID: {row[0]}\nDate: {row[1]}\nTitle: {row[2]}\nSource: {row[3]}\nTarget: {row[4]}\nScore: {row[7]}/{row[6]} (Unknown: {row[8]}, Unanswered: {row[9]})\nElapsed: {row[10]}s\nNotes: {str(row[11])[:200]}...\n{'-'*60}\n")
print("Written tests_summary.txt successfully")
