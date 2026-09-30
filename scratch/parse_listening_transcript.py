import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/cleaned_transcript.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Split into lines
lines = [l.strip() for l in text.split('\n') if l.strip()]

with open('scratch/transcript_by_question.txt', 'w', encoding='utf-8') as out:
    for line in lines:
        out.write(line + '\n')

print("Wrote transcript to scratch/transcript_by_question.txt")
