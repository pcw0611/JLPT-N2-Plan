import re

with open('scratch/cleaned_transcript.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect 問題1 (items 1~5)
print("=== 問題 1 ===")
m1_text = text[text.find('問題 11番'):text.find('問題 21番')]
for item in ['1番', '2番', '3番', '4番', '5番']:
    pos = m1_text.find(item)
    if pos != -1:
        print(f"\n--- 問題1 {item} ---")
        print(m1_text[pos:pos+400].strip())

# Let's inspect 問題2 (items 1~6)
print("\n=== 問題 2 ===")
m2_text = text[text.find('問題 21番'):text.find('問題3')]
for item in ['1番', '2番', '3番', '4番', '5番', '6番']:
    pos = m2_text.find(item)
    if pos != -1:
        print(f"\n--- 問題2 {item} ---")
        print(m2_text[pos:pos+400].strip())
