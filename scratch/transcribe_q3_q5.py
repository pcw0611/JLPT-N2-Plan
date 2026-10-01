import sys
import json
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding='utf-8')
model = WhisperModel('tiny', device='cpu', compute_type='int8')

# N2Q3
segs3, _ = model.transcribe('references/official_vol2_listening/N2Q3_mondai3_gaiyou.mp3', language='ja')
res3 = [{'start': round(s.start, 2), 'end': round(s.end, 2), 'text': s.text.strip()} for s in segs3]
with open('scratch/transcript_vol2_q3.json', 'w', encoding='utf-8') as f:
    json.dump(res3, f, ensure_ascii=False, indent=2)

# N2Q5
segs5, _ = model.transcribe('references/official_vol2_listening/N2Q5_mondai5_tougou.mp3', language='ja')
res5 = [{'start': round(s.start, 2), 'end': round(s.end, 2), 'text': s.text.strip()} for s in segs5]
with open('scratch/transcript_vol2_q5.json', 'w', encoding='utf-8') as f:
    json.dump(res5, f, ensure_ascii=False, indent=2)

print("Transcribed N2Q3 and N2Q5 successfully!")
