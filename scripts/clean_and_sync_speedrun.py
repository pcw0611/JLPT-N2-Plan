# -*- coding: utf-8 -*-
import json, re, sys, shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def clean_file(path: Path):
    text = path.read_text(encoding='utf-8')
    idx1 = text.find('const ALL_PATTERNS = [')
    idx2 = text.find('];\n\nclass SoundEngine', idx1)
    if idx1 == -1 or idx2 == -1:
        print(f"Failed to find ALL_PATTERNS in {path}")
        return
    
    data = json.loads(text[idx1 + len('const ALL_PATTERNS = '):idx2 + 1])
    
    def repl(m):
        ja = m.group(1)
        ko = m.group(2)
        return f"{ja} {ko}"
    
    cleaned_count = 0
    for item in data:
        dp = item.get('diff_point', '')
        if not dp: continue
        # Japanese chars followed immediately by Korean chars: insert space
        new_dp = re.sub(r'([〜~][\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFFー]+)([\uac00-\ud7a3])', repl, dp)
        if new_dp != dp:
            item['diff_point'] = new_dp
            cleaned_count += 1
            
    print(f"Cleaned {cleaned_count} diff_points in {path.name}")
    
    # Also ensure the generateQuestions logic inside text is updated
    # Replace ALL_PATTERNS JSON
    new_json = json.dumps(data, ensure_ascii=False)
    new_text = text[:idx1 + len('const ALL_PATTERNS = ')] + new_json + text[idx2:]
    
    path.write_text(new_text, encoding='utf-8')
    print(f"Successfully saved {path}")

# 1. Clean public and quiz_sites
public_path = Path('jlpt-calendar-site/public/exams/n2-grammar-speedrun.html')
quiz_path = Path('quiz_sites/n2-grammar-speedrun.html')
dist_path = Path('jlpt-calendar-site/dist/client/exams/n2-grammar-speedrun.html')

clean_file(public_path)
clean_file(quiz_path)

# 2. Copy the cleaned public file directly to dist/client
shutil.copy2(public_path, dist_path)
print(f"Copied updated file to {dist_path}")
