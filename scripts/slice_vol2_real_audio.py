import os
import sys
import subprocess
import shutil

sys.stdout.reconfigure(encoding='utf-8')

SRC_DIR = os.path.abspath('references/official_vol2_listening')
OUT_DIR = os.path.abspath('scratch/audio_clips')
MEDIA_DIR = os.path.join(os.environ['APPDATA'], 'Anki2', '사용자 1', 'collection.media')
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True)

VOL2_SLICES = [
    (76, "N2Q1_mondai1_kadai.mp3", 30.0, 130.0, "vol2_q76.mp3", "問題1 例 (宿題の確認)"),
    (80, "N2Q1_mondai1_kadai.mp3", 539.0, 635.0, "vol2_q80.mp3", "問題1 5番 (お茶の葉の品質管理)"),
    (90, "N2Q3_mondai3_gaiyou.mp3", 430.0, 520.0, "vol2_q90.mp3", "問題3 4番 (日常生活に運動を取り入れる工夫)"),
    (94, "N2Q4_mondai4_sokuji.mp3", 154.5, 189.2, "vol2_q94.mp3", "問題4 3番 (山田さんを除いて全員回答)"),
    (97, "N2Q4_mondai4_sokuji.mp3", 253.9, 284.6, "vol2_q97.mp3", "問題4 6番 (プリンター修理 買い替え)"),
    (99, "N2Q4_mondai4_sokuji.mp3", 313.9, 355.6, "vol2_q99.mp3", "問題4 8番 (会議室 壁の色)"),
    (102, "N2Q4_mondai4_sokuji.mp3", 423.5, 456.4, "vol2_q102.mp3", "問題4 11番 (スキー5年ぶり)"),
    (106, "N2Q5_mondai5_tougou.mp3", 335.0, 515.0, "vol2_q106.mp3", "問題5 3番 (交通安全 夫婦の視察先)"),
]

print("=== SLICING 8 AUTHENTIC EXAM 1 CLIPS FROM OFFICIAL CD ===")
for qid, src_fn, start_s, end_s, out_fn, label in VOL2_SLICES:
    src_path = os.path.join(SRC_DIR, src_fn)
    out_path = os.path.join(OUT_DIR, out_fn)
    dur = round(end_s - start_s, 1)

    cmd = [
        'ffmpeg', '-y',
        '-ss', str(start_s),
        '-i', src_path,
        '-t', str(dur),
        '-c:a', 'libmp3lame',
        '-b:a', '128k',
        out_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    sz = os.path.getsize(out_path)

    # Copy to collection.media
    media_dst = os.path.join(MEDIA_DIR, out_fn)
    shutil.copy2(out_path, media_dst)

    print(f"  [OK] Q{qid:03d} -> {out_fn:13s} ({sz:>9,d} bytes, {dur:5.1f}s) | {label}")

print("\nAll 8 authentic Exam 1 clips sliced and copied to collection.media!")
