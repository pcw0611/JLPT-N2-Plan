import json
import glob
import sys
sys.stdout.reconfigure(encoding='utf-8')

files = glob.glob('database/past_exams/*.json')
files = [f for f in files if 'exam_index' not in f]

for f in sorted(files):
    try:
        with open(f, 'r', encoding='utf-8') as fp:
            d = json.load(fp)
            qs = d.get('questions', [])
            print(f"{f}: {len(qs)} questions")
    except Exception as e:
        print(f"{f}: error {e}")
