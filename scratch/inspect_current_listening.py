import json

with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

with open('scratch/current_listening_summary.txt', 'w', encoding='utf-8') as out:
    for q in d['questions'][72:]:
        out.write(f"Q{q['id']} (問題{q.get('problemNo')} {q.get('part')} - {q.get('category')} / {q.get('subtype')}):\n")
        out.write(f"Prompt: {q.get('prompt')}\n")
        out.write(f"Answer: {q.get('answer')}\n")
        for i, c in enumerate(q.get('choices', [])):
            out.write(f"  {i+1}. {c}\n")
        out.write("\n")

print("Done writing scratch/current_listening_summary.txt")
