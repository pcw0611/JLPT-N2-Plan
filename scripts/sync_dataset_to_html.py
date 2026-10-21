# -*- coding: utf-8 -*-
import json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT / 'scripts' / 'n2_grammar_dataset.json'
HTML_PATHS = [
    ROOT / 'quiz_sites' / 'n2-grammar-speedrun.html',
    ROOT / 'jlpt-calendar-site' / 'public' / 'exams' / 'n2-grammar-speedrun.html'
]

with open(DATASET_PATH, 'r', encoding='utf-8') as f:
    items = json.load(f)

json_str = json.dumps(items, ensure_ascii=False, indent=2)
replacement = f"const ALL_PATTERNS = {json_str};"

pattern = re.compile(r'const ALL_PATTERNS\s*=\s*\[.*?\];', re.DOTALL)

for path in HTML_PATHS:
    content = path.read_text(encoding='utf-8')
    m = pattern.search(content)
    if not m:
        print(f"Error: const ALL_PATTERNS not found in {path}")
        sys.exit(1)
    
    new_content = pattern.sub(replacement, content, count=1)
    path.write_text(new_content, encoding='utf-8')
    print(f"Successfully synced {len(items)} items to {path.name} ({len(new_content)} bytes)")
