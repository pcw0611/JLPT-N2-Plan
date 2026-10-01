import os
import sys
import subprocess
import shutil

sys.stdout.reconfigure(encoding='utf-8')

SRC_AUDIO = os.path.abspath('scratch/audio_202312_full.mp3')
OUT_DIR = os.path.abspath('scratch/audio_clips')
MEDIA_DIR = os.path.join(os.environ['APPDATA'], 'Anki2', '사용자 1', 'collection.media')
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True)

SLICES_EXAM2 = [
    (75, "問題1 3番 (留学生 役割分担/調べる国)", 190.0, 276.0, "e2_q75.mp3"),
    (76, "問題1 4番 (女の学生 応募申請書)", 276.0, 361.0, "e2_q76.mp3"),
    (77, "問題1 5番 (男の人 植物 日光窓際)", 361.0, 462.0, "e2_q77.mp3"),
    (78, "問題2 1番 (アナウンサー評価点)", 462.0, 572.0, "e2_q78.mp3"),
    (80, "問題2 3番 (着なくなったシャツ クッションカバー)", 680.0, 778.0, "e2_q80.mp3"),
    (82, "問題2 5番 (海岸 流木 イス・テーブル)", 892.0, 1026.0, "e2_q82.mp3"),
    (85, "問題3 2番 (地方への移住 支援)", 1356.0, 1459.0, "e2_q85.mp3"),
    (86, "問題3 3番 (果樹園 リンゴ ネズミ被害工夫)", 1459.0, 1561.0, "e2_q86.mp3"),
    (88, "問題3 5番 (和紙職人 きっかけ)", 1655.0, 1755.0, "e2_q88.mp3"),
    (89, "問題4 1番", 1805.0, 1835.0, "e2_q89.mp3"),
    (90, "問題4 2番", 1835.0, 1865.0, "e2_q90.mp3"),
    (91, "問題4 3番", 1865.0, 1895.0, "e2_q91.mp3"),
    (95, "問題4 7番 (今日の作業はこの辺で切り上げましょうか)", 1984.0, 2022.0, "e2_q95.mp3"),
    (97, "問題4 9番 (今日の花火大会は延期にしましょう)", 2049.0, 2087.0, "e2_q97.mp3"),
    (98, "問題4 10番 (課長の代わりに進行役)", 2087.0, 2119.0, "e2_q98.mp3"),
    (99, "問題4 11番 (私どもではお引き受けいたしかねます)", 2119.0, 2145.0, "e2_q99.mp3"),
    (101, "問題5 2番 (留学・寮 タイプ1)", 2326.0, 2515.0, "e2_q101.mp3"),
]

print(f"=== SLICING {len(SLICES_EXAM2)} AUTHENTIC 2023.12 EXAM CLIPS ===")
for qid, label, start_s, end_s, fn in SLICES_EXAM2:
    out_path = os.path.join(OUT_DIR, fn)
    dur = end_s - start_s
    # Slice using ffmpeg
    cmd = [
        'ffmpeg', '-y',
        '-ss', str(start_s),
        '-i', SRC_AUDIO,
        '-t', str(dur),
        '-c:a', 'libmp3lame',
        '-b:a', '128k',
        out_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    sz = os.path.getsize(out_path)
    # Copy to collection.media
    media_dst = os.path.join(MEDIA_DIR, fn)
    shutil.copy2(out_path, media_dst)
    
    print(f"  [OK] Q{qid:03d} -> {fn:12s} ({sz:>9,d} bytes, {dur:5.1f}s) | {label}")

print("\nAll 17 authentic 2023.12 clips sliced and copied to collection.media!")
