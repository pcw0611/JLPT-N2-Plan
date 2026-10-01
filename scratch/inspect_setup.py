import json
import re

with open('quiz_sites/n2-past-exam-202312-mock.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'(https://www\.youtube\.com/embed/[a-zA-Z0-9_-]+)', text):
    print('Found YouTube URL:', m.group(1))

# Check audio tags or players
for m in re.finditer(r'<iframe[^>]+>', text):
    print('Found iframe:', m.group(0))

