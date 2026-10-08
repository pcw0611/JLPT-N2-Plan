# -*- coding: utf-8 -*-
import json, re, sys, shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

paths = [
    ROOT / 'jlpt-calendar-site' / 'public' / 'exams' / 'n2-grammar-speedrun.html',
    ROOT / 'quiz_sites' / 'n2-grammar-speedrun.html'
]

for p in paths:
    text = p.read_text(encoding='utf-8')
    
    # 1. Fix static HTML fbDiff
    text = text.replace(
        '〜末に도 긴 과정 뒤의 결과지만 좋은 결과에도 쓴다',
        '〜末に: 긴 과정 뒤의 결과 (좋은 결과에도 사용 가능)'
    )
    
    # 2. Reinforce the purity check in JavaScript
    old_purity = '''    // 3. Absolute Purity Check: Never allow Korean characters in choices
    const rawChoices = [item.pattern, ...Array.from(distractors).slice(0, 3)];
    const choices = rawChoices.map(c => {
      if (/[ㄱ-ㅎㅏ-ㅣ가-힣]/.test(c)) {
        const fallback = ALL_PATTERNS[Math.floor(Math.random() * ALL_PATTERNS.length)];
        return fallback.pattern;
      }
      return c;
    });'''

    new_purity = '''    // 3. Absolute Purity Check: Strip any Korean or fallback to clean pattern
    const rawChoices = [item.pattern, ...Array.from(distractors).slice(0, 3)];
    const choices = rawChoices.map(c => {
      // First strip any attached Korean particles or characters
      let cleaned = (c || '').replace(/[ㄱ-ㅎㅏ-ㅣ가-힣].*$/g, '').trim();
      cleaned = cleaned.replace(/[ととはがのをにへで]+$/, '').trim();
      if (!cleaned || cleaned === '〜' || cleaned.length < 2 || /[ㄱ-ㅎㅏ-ㅣ가-힣]/.test(cleaned)) {
        const fallback = ALL_PATTERNS[Math.floor(Math.random() * ALL_PATTERNS.length)];
        return fallback.pattern;
      }
      return cleaned;
    });'''

    if old_purity in text:
        text = text.replace(old_purity, new_purity)
        print(f"Replaced purity check in {p.name}")
    else:
        print(f"Purity block not matched exactly in {p.name}, searching regex...")
        text = re.sub(
            r'// 3\. Absolute Purity Check:.*?return c;\s*\}\);',
            new_purity.strip(),
            text,
            flags=re.DOTALL
        )
        print(f"Regex replaced purity check in {p.name}")

    p.write_text(text, encoding='utf-8')
    print(f"Saved {p}")

# Copy public file directly to dist/client
dist_file = ROOT / 'jlpt-calendar-site' / 'dist' / 'client' / 'exams' / 'n2-grammar-speedrun.html'
shutil.copy2(paths[0], dist_file)
print(f"Copied updated file to {dist_file}")
