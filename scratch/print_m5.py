import sys, io
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/reconstructed_transcript.txt', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('市民センター')
if pos != -1:
    print(text[pos:])
else:
    print("市民センター not found")
