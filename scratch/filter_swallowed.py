# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/swallowed_analysis.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    if "Pre: ''" not in line or "Post: ''" not in line or 'Match: None' in line:
        print(line.strip())
