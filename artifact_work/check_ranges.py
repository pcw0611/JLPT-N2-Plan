import json

with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('artifact_work/ranges_output.txt', 'w', encoding='utf-8') as out:
    out.write(f"Total: {len(data['questions'])}\n")
    curr_prob = None
    start_id = None
    prev_id = None

    for q in data['questions']:
        key = (q.get('sectionName'), q.get('part'), q.get('problemNo'), q.get('subtype'))
        if key != curr_prob:
            if curr_prob is not None:
                out.write(f"{curr_prob[0]} | {curr_prob[1]} | {curr_prob[2]} ({curr_prob[3]}): IDs {start_id} ~ {prev_id} ({prev_id - start_id + 1} items)\n")
            curr_prob = key
            start_id = q['id']
        prev_id = q['id']

    if curr_prob is not None:
        out.write(f"{curr_prob[0]} | {curr_prob[1]} | {curr_prob[2]} ({curr_prob[3]}): IDs {start_id} ~ {prev_id} ({prev_id - start_id + 1} items)\n")
print("Done writing ranges_output.txt")
