import re
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('JLPT_ERROR_NOTE.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find all entries
entries = re.split(r'### \[(2026-09-\d+)\] Q(\d+)', text)
print("Total split tokens:", len(entries))

# Parse items
items_map = {}
for i in range(1, len(entries), 3):
    date = entries[i]
    qid = int(entries[i+1])
    content = entries[i+2]
    key = (date, qid)
    items_map[key] = content

print(f"Total parsed items in error note: {len(items_map)}")
print("Sample keys:", list(items_map.keys())[:10])

# Check Exam 1 (2026-09-20)
e1_keys = [k for k in items_map if k[0] == '2026-09-20']
print("2026-09-20 items count:", len(e1_keys))

# Check Exam 2 (2026-09-30)
e2_keys = [k for k in items_map if k[0] == '2026-09-30']
print("2026-09-30 items count:", len(e2_keys))
