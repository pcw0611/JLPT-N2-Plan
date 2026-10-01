import sys, io
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/vol2_script.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find "問題 4" in vol2_script.txt
pos = text.find('問題 4')
if pos == -1:
    pos = text.find('問題４')
if pos == -1:
    pos = text.find('問題')

print("Searching for Mondai 4 in vol2_script.txt:")
while pos != -1:
    snippet = text[pos:pos+200].replace('\n', ' ')
    print(f"Pos {pos}: {snippet}")
    pos = text.find('問題 4', pos+1)
