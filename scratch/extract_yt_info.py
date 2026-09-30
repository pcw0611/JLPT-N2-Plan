import re

with open(r'C:\Users\pcw06\.gemini\antigravity\brain\11e51aca-0126-45eb-8197-831762519c5a\.system_generated\steps\1087\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

m_title = re.search(r'<title>(.*?)</title>', text)
print('Title:', m_title.group(1) if m_title else 'None')

m_desc = re.search(r'"shortDescription":"(.*?)"', text)
if m_desc:
    print('Description:', m_desc.group(1)[:500].encode('utf-8', errors='ignore').decode('utf-8'))
