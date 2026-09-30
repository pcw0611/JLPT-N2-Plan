import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/cleaned_transcript.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Find start of 問題4
idx_m4 = text.find('問題 4')
if idx_m4 == -1:
    idx_m4 = text.find('問題4')

idx_m5 = text.find('問題 5')
if idx_m5 == -1:
    idx_m5 = text.find('問題5')

print(f"Index m4: {idx_m4}, Index m5: {idx_m5}")

print("=== M4 snippet ===")
print(text[idx_m4:idx_m4+3000])

print("=== M5 snippet ===")
print(text[idx_m5:idx_m5+4000])
