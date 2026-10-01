import json
import sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total questions in 2023_12: {len(data['questions'])}")

probs = []
for q in data['questions']:
    probs.append((q.get('sectionName'), q.get('part'), q.get('problemNo')))

counts = Counter(probs)
for (s, p, prob), count in sorted(counts.items(), key=lambda x: (str(x[0][0]), str(x[0][1]), str(x[0][2]))):
    print(f"[{s}] {p} - {prob}: {count}문항")
