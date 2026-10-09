# -*- coding: utf-8 -*-
import json, sys, shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT / 'scripts' / 'n2_grammar_dataset.json'

with open(DATASET_PATH, 'r', encoding='utf-8') as f:
    items = json.load(f)

json_str = json.dumps(items, ensure_ascii=False)

def update_html_file(file_path: Path):
    content = file_path.read_text(encoding='utf-8')
    marker_start = 'const ALL_PATTERNS = ['
    idx_start = content.find(marker_start)
    if idx_start == -1:
        raise ValueError(f"Could not find marker '{marker_start}' in {file_path}")
    
    # Find start of class SoundEngine
    marker_next = 'class SoundEngine'
    idx_next = content.find(marker_next, idx_start)
    if idx_next == -1:
        raise ValueError(f"Could not find 'class SoundEngine' in {file_path}")

    new_content = content[:idx_start] + 'const ALL_PATTERNS = ' + json_str + ';\n\n' + content[idx_next:]
    file_path.write_text(new_content, encoding='utf-8')
    print(f"Updated {file_path} (len: {len(new_content)} bytes)")

public_target = ROOT / 'jlpt-calendar-site' / 'public' / 'exams' / 'n2-grammar-speedrun.html'
quiz_target = ROOT / 'quiz_sites' / 'n2-grammar-speedrun.html'
dist_target = ROOT / 'jlpt-calendar-site' / 'dist' / 'client' / 'exams' / 'n2-grammar-speedrun.html'

# 1. Update public HTML with json dataset
update_html_file(public_target)

# 2. Mirror complete public HTML to quiz_sites and dist
shutil.copy2(public_target, quiz_target)
print(f"Mirrored public HTML to {quiz_target}")

if dist_target.exists():
    shutil.copy2(public_target, dist_target)
    print(f"Mirrored public HTML to {dist_target}")

print("All Grammar Speedrun HTML targets synchronized successfully!")
