with open('JLPT_STUDY_LOG.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('anki-session-20261108')
if idx != -1:
    print("Found at", idx)
    with open('scratch/found_text.txt', 'w', encoding='utf-8') as out:
        out.write(text[idx-50:idx+2500])
else:
    print("Not found")
