with open('JLPT_STUDY_LOG.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<!-- anki-session-20261108 -->')
tail = text[idx:]
print(f"Tail length from anki-session-20261108: {len(tail)}")
with open('scratch/exact_tail.txt', 'w', encoding='utf-8') as f:
    f.write(tail)
