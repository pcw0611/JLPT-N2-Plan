import sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/perfect_dialogues_25.json', 'r', encoding='utf-8') as f:
    dialogues = json.load(f)

# Exam 1 keys: 1회_76, 1회_80, 1회_90, 1회_94, 1회_97, 1회_99, 1회_102, 1회_106
# Exam 2 keys: 2회_75, 2회_76, 2회_77, 2회_78, 2회_80, 2회_82, 2회_85, 2회_86, 2회_88, 2회_89, 2회_90, 2회_91, 2회_95, 2회_97, 2회_98, 2회_99, 2회_101

print(f"Total keys in perfect_dialogues_25.json: {len(dialogues)}")
for k, turns in dialogues.items():
    print(f"\n--- {k} ({len(turns)} turns) ---")
    for t in turns[:2]:
        print(f"  [{t['speaker']}] {t['ja'][:50]}")
