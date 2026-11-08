# -*- coding: utf-8 -*-
import json, sys, shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT / 'scripts' / 'n2_grammar_dataset.json'

with open(DATASET_PATH, 'r', encoding='utf-8') as f:
    items = json.load(f)

json_str = json.dumps(items, ensure_ascii=False)
weekly = json.loads((ROOT / 'scripts/n2_grammar_weekly.json').read_text(encoding='utf-8'))
weekly_str = json.dumps(weekly, ensure_ascii=False, separators=(',', ':'))

# The maintained runtime handles the lobby selection; sources stay inline/offline.
daily_runtime = 'const WEEKLY_SENTENCES = ' + weekly_str + ';\n' + (ROOT / 'scripts/grammar_weekly_selector.js').read_text(encoding='utf-8')

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

    new_content = content[:idx_start] + 'const ALL_PATTERNS = ' + json_str + ';\n' + daily_runtime + '\n' + content[idx_next:]
    tts_start = '// BEGIN GRAMMAR TTS'
    tts_end = '// END GRAMMAR TTS'
    tts_code = tts_start + '\n' + (ROOT / 'scripts/grammar_tts_runtime.js').read_text(encoding='utf-8') + '\n' + tts_end + '\n'
    if tts_start in new_content:
        a = new_content.index(tts_start)
        b = new_content.index(tts_end, a) + len(tts_end)
        new_content = new_content[:a] + tts_code.rstrip() + new_content[b:]
    else:
        a = new_content.index('const SYNONYM_GROUPS')
        new_content = new_content[:a] + tts_code + '\n' + new_content[a:]
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
