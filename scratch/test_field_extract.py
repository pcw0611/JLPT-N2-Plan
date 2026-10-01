import re
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from scratch.parse_error_note import items_map

def extract_fields(content):
    res = {}
    m_cat = re.search(r'\*\*카테고리:\s*([^\n]+)\*\*', content)
    res['category'] = m_cat.group(1).strip() if m_cat else ''

    patterns = [
        ('prompt', r'1\.\s*\*\*문제 원문\*\*:\s*\n?(.*?)(?=2\.|\Z)'),
        ('translation', r'2\.\s*\*\*자연스러운 번역\*\*:\s*(.*?)(?=3\.|\Z)'),
        ('answers', r'3\.\s*\*\*선택 답 ➔ 공식 정답\*\*:\s*(.*?)(?=4\.|\Z)'),
        ('connection_meaning', r'4\.\s*\*\*접속·핵심 의미\*\*:\s*(.*?)(?=5\.|\Z)'),
        ('trap', r'5\.\s*\*\*사용자 상태 및 함정 분석\*\*:\s*(.*?)(?=6\.|\Z)'),
        ('contrast', r'6\.\s*\*\*유사 문형 및 표현 비교\*\*:\s*(.*?)(?=7\.|\Z)'),
        ('example', r'7\.\s*\*\*추가 예문\*\*:\s*(.*?)(?=8\.|\Z)'),
        ('next_review', r'8\.\s*\*\*다음 복습일\*\*:\s*(.*?)(?=9\.|\Z)'),
        ('procedure', r'9\.\s*\*\*다음번 풀이 절차\*\*:\s*(.*?)(?=10\.|\Z)'),
        ('check', r'10\.\s*\*\*제출 직전 체크\*\*:\s*(.*?)(?=\n---|<!--|\Z)'),
    ]

    for key, pat in patterns:
        m = re.search(pat, content, re.DOTALL)
        res[key] = m.group(1).strip() if m else ''

    return res

# Test on 2026-09-20 Q15 and 2026-09-30 Q2
for key in [('2026-09-20', 15), ('2026-09-30', 2)]:
    f = extract_fields(items_map[key])
    print(f"\n=== Test {key} ===")
    for k, v in f.items():
        print(f"  {k}: {v[:60]}...")
