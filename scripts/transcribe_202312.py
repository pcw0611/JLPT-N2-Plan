import os
import sys
import json
import subprocess
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding='utf-8')

AUDIO_FILE = os.path.abspath('scratch/audio_202312_full.mp3')
OUT_DIR = os.path.abspath('scratch/audio_clips')
os.makedirs(OUT_DIR, exist_ok=True)

print("Loading Whisper model (tiny)...")
model = WhisperModel('tiny', device='cpu', compute_type='int8')

print("Transcribing 2023.12 audio to find exact question timestamps...")
segments, info = model.transcribe(AUDIO_FILE, language='ja', beam_size=1)

transcript_log = []
for s in segments:
    transcript_log.append({
        'start': round(s.start, 2),
        'end': round(s.end, 2),
        'text': s.text.strip()
    })

with open('scratch/transcript_202312.json', 'w', encoding='utf-8') as f:
    json.dump(transcript_log, f, ensure_ascii=False, indent=2)

print(f"Transcribed {len(transcript_log)} segments. Saved to scratch/transcript_202312.json")
