# -*- coding: utf-8 -*-
"""Inspect lines of each extracted script."""
import sys, json

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/extracted_scripts.json', 'r', encoding='utf-8') as f:
    scripts = json.load(f)

for s in scripts:
    lines = s['script_lines']
    print(f"=== {s['exam']} Q{s['qid']} ({len(lines)} lines) ===")
    for idx, l in enumerate(lines):
        print(f"  [{idx}] {l}")
    print()
