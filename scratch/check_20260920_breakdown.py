import re
import sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

with open('jlpt-calendar-site/public/exams/n2-midterm-mock-exam-20260920.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('const questions = [')
end_idx = content.find('];', idx)
snippet = content[idx:end_idx]

# Find all question objects
# Match problemNo, section, part
pattern = re.compile(r'problemNo:\s*["\']([^"\']+)["\'].*?part:\s*["\']([^"\']+)["\']', re.DOTALL)
matches = pattern.findall(snippet)
print(f"Total matched questions in 2026-09-20 exam: {len(matches)}")

counts = Counter(matches)
for (prob, part), cnt in sorted(counts.items()):
    print(f"  {part} - {prob}: {cnt}문항")
