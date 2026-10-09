import sys, json

sys.stdout.reconfigure(encoding='utf-8')
with open('jlpt-calendar-site/public/exams/n2-past-exam-202312-mock.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('{"id": 76')
end = text.find('}, {"id": 77', pos)
print(text[pos:end+1])
