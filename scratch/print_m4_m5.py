import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('scratch/sections_extracted.txt', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('=== ')
for p in parts:
    if p.startswith('MONDAI 4') or p.startswith('MONDAI 5'):
        print(f"=== {p[:1500]}")
        print("...\n")
