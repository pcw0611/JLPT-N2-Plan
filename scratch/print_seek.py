import re
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('quiz_sites/n2-past-exam-202312-mock.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('seekAudioTime')
print(text[pos-200:pos+1000])

