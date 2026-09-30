import re

with open('scratch/cleaned_transcript.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect each section
# In 問題4, the question is a short phrase, and choices 1, 2, 3 are read aloud!
# In 問題3, dialogue is read, then question, then choices 1, 2, 3, 4 are read aloud!
# In 問題1 and 2, choices are printed on the test paper!
# Let's check how choices are shown in the YouTube video or script.

print("--- Inspecting 問題4 (all 11 items) ---")
m4_text = text[text.find('問題 4例'):text.find('問題 51番')]
# find 1番 ~ 11番 in m4_text
items = re.split(r'(\d+番)', m4_text)
for i in range(1, len(items), 2):
    num = items[i]
    content = items[i+1] if i+1 < len(items) else ''
    print(f"\n[問題4 {num}]")
    print(content[:300].strip())
