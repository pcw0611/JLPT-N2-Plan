import sys
import json
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding='utf-8')

model = WhisperModel('tiny', device='cpu', compute_type='int8')
segments, info = model.transcribe('references/official_vol2_listening/N2Q4_mondai4_sokuji.mp3', language='ja')

res = []
for s in segments:
    res.append({'start': round(s.start, 2), 'end': round(s.end, 2), 'text': s.text.strip()})

with open('scratch/transcript_vol2_q4.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print(f"Transcribed {len(res)} segments in N2Q4.")
