import sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

# Load the dialogues from build_perfect_dialogues.py / perfect_dialogues_25.json
with open('scratch/perfect_dialogues_25.json', 'r', encoding='utf-8') as f:
    dialogues = json.load(f)

# Load VTT file
with open('scratch/n2_2023_12_sub.ja.vtt', 'r', encoding='utf-8') as f:
    vtt_text = f.read()

# Also let's inspect the 17 2023.12 questions:
# Key mapping: '2회_75', '2회_76', '2회_77', '2회_78', '2회_80', '2회_82',
#              '2회_85', '2회_86', '2회_88', '2회_89', '2회_90', '2회_91',
#              '2회_95', '2회_97', '2회_98', '2회_99', '2회_101'

exam2_keys = [k for k in dialogues.keys() if k.startswith('2회_')]
print(f"Total Exam 2 dialogue keys: {len(exam2_keys)}")

for k in sorted(exam2_keys, key=lambda x: int(x.split('_')[1])):
    lines = dialogues[k]
    full_ja = " ".join([l['ja'] for l in lines])
    print(f"\n==================== {k} ====================")
    print("CURRENT DIALOGUE IN JSON:")
    for l in lines:
        print(f"  {l['speaker']}: {l['ja']}")
