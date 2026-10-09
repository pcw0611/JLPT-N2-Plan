import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/n2_grammar_dataset.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

def audit_range(start, end):
    print(f"=== Items {start:03d} to {end:03d} ===")
    for x in items[start-1:end]:
        parts = x['sentence_ja_blank'].split('（　　）')
        ja = x['sentence_ja']
        b = ja[len(parts[0]):len(ja)-len(parts[1])] if len(parts)==2 else x['sentence_ja_target']
        print(f"[{x['num']}] Pat: {x['pattern']}")
        print(f"   JA:      {ja}")
        print(f"   Blank:   {x['sentence_ja_blank']}")
        print(f"   Blanked: '{b}'")
        print()

start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
end = int(sys.argv[2]) if len(sys.argv) > 2 else 25
audit_range(start, end)
