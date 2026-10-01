import json

data = json.load(open('database/past_exams/2023_12.json', encoding='utf-8'))
for q in data['questions'][88:99]:
    qid = q['id']
    num = qid - 88
    print(f"=== Q{qid} (즉시응답 {num}번) ===")
    print("상황/발화:", q.get('prompt'))
    print("번역:", q.get('translation'))
    print(f"정답: {q.get('answer')+1}번 - {q['choices'][q['answer']]}")
    print("핵심:", q.get('contrast') or q.get('meaning'))
    print()
