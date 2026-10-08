import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/namu_haruhikage.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("HTML length:", len(text))
# Find occurrences of '가사'
for m in re.finditer(r'가사', text):
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 500)
    print(f"\n--- Occurrence at {m.start()} ---")
    snippet = re.sub(r'<[^>]+>', ' ', text[start:end])
    print(' '.join(snippet.split())[:300])
