# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

lines = open('database/past_exams/2023_12.json', encoding='utf-8').readlines()
for i, l in enumerate(lines):
    if '"id": 43,' in l or '"id": 47,' in l:
        print(f"Line {i+1}: {l.strip()}")
