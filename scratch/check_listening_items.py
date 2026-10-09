import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

with open('jlpt-calendar-site/public/exams/n2-mock-error-review-pool.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract ALL_ERROR_QUESTIONS array
start = html.find('const ALL_ERROR_QUESTIONS = [')
end = html.find('];\n\nlet currentQuestions = [];', start)
if end == -1:
    end = html.find('];', start)

pool_js = html[start + len('const ALL_ERROR_QUESTIONS = '):end + 1]

# Let's count items where section == '聴解' or audio_file is present
# Use regex to find objects
item_blocks = re.findall(r'\{\s*id:\s*\d+,\s*exam:[^\}]+\}', html[start:end+100])
print(f"Total objects found: {len(item_blocks)}")

listening_items = []
for block in item_blocks:
    if '聴解' in block or 'audio_file' in block:
        m_id = re.search(r'id:\s*(\d+)', block)
        m_exam = re.search(r'exam:\s*[\'\"]([^\'\"]+)[\'\"]', block)
        m_num = re.search(r'orig_num:\s*(\d+)', block)
        m_audio = re.search(r'audio_file:\s*[\'\"]([^\'\"]+)[\'\"]', block)
        m_title = re.search(r'title:\s*[\'\"]([^\'\"]+)[\'\"]', block)
        listening_items.append({
            'id': m_id.group(1) if m_id else None,
            'exam': m_exam.group(1) if m_exam else None,
            'num': m_num.group(1) if m_num else None,
            'audio': m_audio.group(1) if m_audio else None,
            'title': m_title.group(1) if m_title else None
        })

print(f"Total listening items: {len(listening_items)}")
for it in listening_items:
    print(f"id={it['id']:3s} | exam={it['exam']} | orig_num=Q{it['num']} | audio={it['audio']} | title={it['title']}")
