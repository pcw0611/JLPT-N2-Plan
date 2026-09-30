import json

with open('scratch/raw_submission.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

records = data['questionsRecord']

# Breakdown by section
vocab = records[:30]
grammar = records[30:51]
reading = records[51:72]
listening = records[72:]

def stats(subset, name):
    total = len(subset)
    correct = sum(1 for q in subset if q['isCorrect'])
    pct = (correct / total) * 100 if total else 0
    return f"{name}: {correct}/{total} ({pct:.1f}%)"

print(stats(vocab, "Vocab (1~30)"))
print(stats(grammar, "Grammar (31~51)"))
print(stats(reading, "Reading (52~72)"))
print(stats(listening, "Listening (73~102)"))
print(f"Total: {sum(1 for q in records if q['isCorrect'])}/{len(records)}")

# Problem level breakdown for listening
prob_counts = {}
for q in listening:
    p = q['problemNo']
    if p not in prob_counts:
        prob_counts[p] = {'total': 0, 'correct': 0}
    prob_counts[p]['total'] += 1
    if q['isCorrect']:
        prob_counts[p]['correct'] += 1

print("\nListening by Problem:")
for p, s in prob_counts.items():
    print(f"  {p}: {s['correct']}/{s['total']} ({(s['correct']/s['total'])*100:.1f}%)")

# Scaled score estimate
# Official JLPT N2 scoring:
# Language Knowledge (Vocab + Grammar): 60 points max (cutoff: 19 points)
# Reading: 60 points max (cutoff: 19 points)
# Listening: 60 points max (cutoff: 19 points)
# Total: 180 points max (Passing score: 90 points, and each section >= 19 points)

v_c = sum(1 for q in vocab if q['isCorrect'])
g_c = sum(1 for q in grammar if q['isCorrect'])
r_c = sum(1 for q in reading if q['isCorrect'])
l_c = sum(1 for q in listening if q['isCorrect'])

lang_total = len(vocab) + len(grammar) # 51 items
lang_score = round(((v_c + g_c) / lang_total) * 60)
reading_score = round((r_c / len(reading)) * 60)
listening_score = round((l_c / len(listening)) * 60)
total_score = lang_score + reading_score + listening_score

print(f"\nEstimated Scaled Scores:")
print(f"Language Knowledge (51 items): {v_c + g_c}/51 -> {lang_score}/60")
print(f"Reading (21 items): {r_c}/21 -> {reading_score}/60")
print(f"Listening (30 items): {l_c}/30 -> {listening_score}/60")
print(f"Total Scaled: {total_score}/180")
print(f"Cutoff threshold: 19 points each. Has cutoff risk? Language: {lang_score < 19}, Reading: {reading_score < 19}, Listening: {listening_score < 19}")
