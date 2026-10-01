import re
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('scratch/cleaned_transcript.txt', 'r', encoding='utf-8') as f:
    raw_lines = f.readlines()

parsed = []
for line in raw_lines:
    line = line.strip()
    if not line:
        continue
    parts = line.split(': ', 1)
    if len(parts) == 2:
        ts, content = parts[0], parts[1].strip()
        parsed.append((ts, content))

print(f"Total parsed cues: {len(parsed)}")

# Reconstruct text by finding new text appended in subsequent cues
reconstructed = []
prev_text = ""

for ts, text in parsed:
    if not prev_text:
        reconstructed.append((ts, text))
        prev_text = text
        continue
    
    # If text starts with prev_text, take the new part
    if text.startswith(prev_text):
        new_part = text[len(prev_text):].strip()
        if new_part:
            reconstructed.append((ts, new_part))
            prev_text = text
    else:
        # find longest overlap suffix of prev_text that is prefix of text
        overlap_len = 0
        max_search = min(len(prev_text), len(text))
        for l in range(max_search, 0, -1):
            if prev_text.endswith(text[:l]):
                overlap_len = l
                break
        if overlap_len > 0:
            new_part = text[overlap_len:].strip()
            if new_part:
                reconstructed.append((ts, new_part))
        else:
            reconstructed.append((ts, text))
        prev_text = text

full_clean_text = "\n".join([f"[{ts}] {t}" for ts, t in reconstructed])
with open('scratch/reconstructed_transcript.txt', 'w', encoding='utf-8') as out:
    out.write(full_clean_text)

print(f"Reconstructed {len(reconstructed)} chunks into scratch/reconstructed_transcript.txt")
