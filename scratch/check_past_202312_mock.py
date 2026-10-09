import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('jlpt-calendar-site/public/exams/n2-past-exam-202312-mock.html', 'r', encoding='utf-8') as f:
    text = f.read()

# find questions array
# let's search for "Q76" or id: 76 or number 76
pos = text.find('id: 76')
if pos == -1:
    pos = text.find('"id": 76')
if pos == -1:
    pos = text.find('76')

print("Found at pos:", pos)
if pos != -1:
    print(text[pos-100:pos+800])
