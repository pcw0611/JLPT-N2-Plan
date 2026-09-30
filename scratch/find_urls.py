import os
import re

files = ['HANDOFF.md', 'JLPT_STUDY_LOG.md', 'PROJECT_GUIDE.md', 'JLPT_ERROR_NOTE.md']
urls = set()
for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            text = fp.read()
            found = re.findall(r'https?://[^\s\)\]\"\'`<>]+', text)
            for u in found:
                urls.add((f, u))

for f, u in sorted(urls):
    print(f'{f}: {u}')
