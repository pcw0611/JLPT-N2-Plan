import os
import subprocess

os.makedirs('scratch/audio_clips', exist_ok=True)

VOL2_CLIPS = [
    {
        'qid': 76,
        'src': 'references/official_vol2_listening/N2Q1_mondai1_kadai.mp3',
        'start': 156.0,
        'duration': 77.5,
        'out': 'scratch/audio_clips/vol2_q76.mp3'
    },
    {
        'qid': 80,
        'src': 'references/official_vol2_listening/N2Q1_mondai1_kadai.mp3',
        'start': 535.5,
        'duration': 96.0,
        'out': 'scratch/audio_clips/vol2_q80.mp3'
    },
    {
        'qid': 90,
        'src': 'references/official_vol2_listening/N2Q3_mondai3_gaiyou.mp3',
        'start': 427.1,
        'duration': 82.5,
        'out': 'scratch/audio_clips/vol2_q90.mp3'
    },
    {
        'qid': 94,
        'src': 'references/official_vol2_listening/N2Q4_mondai4_sokuji.mp3',
        'start': 185.7,
        'duration': 24.7,
        'out': 'scratch/audio_clips/vol2_q94.mp3'
    },
    {
        'qid': 97,
        'src': 'references/official_vol2_listening/N2Q4_mondai4_sokuji.mp3',
        'start': 318.8,
        'duration': 25.1,
        'out': 'scratch/audio_clips/vol2_q97.mp3'
    },
    {
        'qid': 99,
        'src': 'references/official_vol2_listening/N2Q4_mondai4_sokuji.mp3',
        'start': 386.7,
        'duration': 25.0,
        'out': 'scratch/audio_clips/vol2_q99.mp3'
    },
    {
        'qid': 102,
        'src': 'references/official_vol2_listening/N2Q4_mondai4_sokuji.mp3',
        'start': 454.1,
        'duration': 26.1,
        'out': 'scratch/audio_clips/vol2_q102.mp3'
    },
    {
        'qid': 106,
        'src': 'references/official_vol2_listening/N2Q5_mondai5_tougou.mp3',
        'start': 331.9,
        'duration': 151.8,
        'out': 'scratch/audio_clips/vol2_q106.mp3'
    }
]

def slice_all():
    for item in VOL2_CLIPS:
        cmd = [
            'ffmpeg', '-y',
            '-ss', str(item['start']),
            '-t', str(item['duration']),
            '-i', item['src'],
            '-q:a', '2',
            item['out']
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            size_kb = os.path.getsize(item['out']) / 1024
            print(f"[OK] Q{item['qid']}: {item['out']} ({size_kb:.1f} KB, dur={item['duration']}s)")
        else:
            print(f"[FAIL] Q{item['qid']}: {res.stderr}")

if __name__ == '__main__':
    slice_all()
