import json

with open('anki_error_notes_exams_1_2.tsv', 'r', encoding='utf-8') as f:
    lines = [l.strip() for l in f if l.strip()]

reading_lines = []
listening_lines = []

for line in lines:
    parts = line.split('\t')
    tags = parts[2] if len(parts) >= 3 else ''
    if '청해' in tags:
        listening_lines.append(line)
    else:
        reading_lines.append(line)

print(f"Reading lines: {len(reading_lines)}")
print(f"Listening lines: {len(listening_lines)}")

with open('anki_error_notes_reading_vocab_62.tsv', 'w', encoding='utf-8') as f:
    f.write("\n".join(reading_lines))

with open('anki_error_notes_listening_25.tsv', 'w', encoding='utf-8') as f:
    f.write("\n".join(listening_lines))

print("Saved separated TSV files successfully!")
