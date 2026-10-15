# -*- coding: utf-8 -*-
import os

files = [
    r'jlpt-calendar-site\public\exams\n2-grammar-speedrun.html',
    r'jlpt-calendar-site\dist\client\exams\n2-grammar-speedrun.html',
    r'quiz_sites\n2-grammar-speedrun.html',
    r'scripts\n2_grammar_dataset.json'
]

old_type = '"conn_type": "Vます형(연용형 어간)"'
new_type = '"conn_type": "1그룹 V사전형(기본형)"'
old_hint = '"conn_hint": "앞 단어 「行く」가 동사 마스형(ます語幹) 어간이므로 바로 결합합니다!"'
new_hint = '"conn_hint": "앞 단어 「行く」가 1그룹 동사 사전형(기본형)이므로 바로 결합합니다! (1그룹: 사전형＋まい)"'

for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
        if old_hint in content:
            content = content.replace(old_type, new_type)
            content = content.replace(old_hint, new_hint)
            with open(f, 'w', encoding='utf-8') as fp:
                fp.write(content)
            print('Successfully updated:', f)
        else:
            print('Pattern not found in:', f)
