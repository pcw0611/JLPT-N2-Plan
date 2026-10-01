import sys, io
sys.stdout.reconfigure(encoding='utf-8')

import importlib.util
spec = importlib.util.spec_from_file_location("up23", "scripts/update_202312_listening.py")
up23 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(up23)

lq = {q['id']: q for q in up23.LISTENING_QUESTIONS}

first_half = [75, 76, 77, 78, 80, 82, 85, 86, 88]

for qid in first_half:
    q = lq.get(qid)
    print(f"=== E2 Q{qid} ({q.get('problemNo')} / {q.get('category')}) ===")
    print("Prompt:", q.get('prompt'))
    print("Choices:", q.get('choices'))
    ans = q.get('answer')
    ans_text = q.get('choices')[ans] if ans is not None else None
    print(f"Answer: {ans} ({ans_text})")
    print("Meaning snippet:", q.get('meaning')[:200])
    print()
