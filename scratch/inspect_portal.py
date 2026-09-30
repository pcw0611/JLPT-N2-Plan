import re

with open('jlpt-calendar-site/public/exams/past-exams-portal.html', 'r', encoding='utf-8') as f:
    text = f.read()

titles = re.findall(r'<span class="font-bold text-base text-white">(.*?)</span>', text)
print(f"Total cards: {len(titles)}")
for t in titles:
    print('-', t)
