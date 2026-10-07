# -*- coding: utf-8 -*-
"""Normalize Japanese dialogue lines and map to Korean translations."""
import sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/extracted_scripts.json', 'r', encoding='utf-8') as f:
    scripts = json.load(f)

# Normalize each script into a list of dialogues
# Each dialogue item is: {"speaker": str, "japanese": str}
def normalize_script(exam, qid, raw_lines):
    items = []
    
    # Special handling for Problem 4 (即時応答)
    # raw_lines usually:
    # [0] 【発話】
    # [1] A: text
    # [2] 1. text
    # [3] 2. text
    # [4] 3. text
    if (exam == '1회' and qid in [94, 97, 99, 102]) or (exam == '2회' and qid in [89, 90, 91, 95, 97, 98, 99]):
        current_speaker = ""
        for line in raw_lines:
            if line.strip() == "【発話】":
                continue
            m = re.match(r'^([^：:]+[：:])(.*)$', line)
            if m:
                spk = m.group(1).rstrip('：:')
                txt = m.group(2).strip()
                items.append({"speaker": spk, "japanese": txt})
            elif re.match(r'^[1-3]\.', line):
                items.append({"speaker": line[:2], "japanese": line[2:].strip()})
            else:
                items.append({"speaker": "", "japanese": line.strip()})
        return items

    # For other problems (1, 2, 3, 5):
    # If a line is just a speaker like "先生（男）：" or "女：", attach it to the next line
    i = 0
    curr_spk = ""
    while i < len(raw_lines):
        line = raw_lines[i].strip()
        # Check if line is just speaker label
        if re.match(r'^[^：:]{1,15}[：:]$', line):
            curr_spk = line.rstrip('：:')
            i += 1
            if i < len(raw_lines):
                next_line = raw_lines[i].strip()
                items.append({"speaker": curr_spk, "japanese": next_line})
                curr_spk = ""
                i += 1
            continue
        
        # Check if line has speaker at start
        m = re.match(r'^([^：:]+[：:])(.*)$', line)
        if m:
            spk = m.group(1).rstrip('：:')
            txt = m.group(2).strip()
            items.append({"speaker": spk, "japanese": txt})
            i += 1
            continue
        
        # Header line like 【説明】： or 【会話】：
        if line.startswith('【'):
            items.append({"speaker": "구분", "japanese": line})
            i += 1
            continue
            
        # Regular text line without speaker
        items.append({"speaker": curr_spk, "japanese": line})
        curr_spk = ""
        i += 1
        
    return items

normalized_all = {}
for s in scripts:
    key = f"{s['exam']}_{s['qid']}"
    norm = normalize_script(s['exam'], s['qid'], s['script_lines'])
    normalized_all[key] = norm
    print(f"{key}: {len(norm)} normalized dialogue turns")

with open('scratch/normalized_dialogues.json', 'w', encoding='utf-8') as f:
    json.dump(normalized_all, f, ensure_ascii=False, indent=2)

print("Saved all normalized dialogues to scratch/normalized_dialogues.json")
