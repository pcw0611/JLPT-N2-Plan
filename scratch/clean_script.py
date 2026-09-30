import re

with open('scratch/cleaned_transcript.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove duplicate timestamps and clean lines
lines = text.split('\n')
cleaned = []
last_s = ""
for line in lines:
    line = line.strip()
    if not line:
        continue
    # remove timestamp
    m = re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3}:\s*(.*)$', line)
    if m:
        content = m.group(1).strip()
    else:
        content = line
    if content != last_s:
        cleaned.append(content)
        last_s = content

full_cleaned_text = "\n".join(cleaned)
with open('scratch/full_cleaned_transcript.txt', 'w', encoding='utf-8') as f:
    f.write(full_cleaned_text)

print(f"Cleaned lines: {len(cleaned)}")
