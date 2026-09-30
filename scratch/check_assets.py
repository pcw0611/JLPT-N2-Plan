import re

files = [
    'quiz_sites/n2-midterm-mock-exam-20260920.html',
    'quiz_sites/n2-past-exam-202312-mock.html',
    'quiz_sites/official-vol2-listening-player.html',
    'quiz_sites/past-exams-portal.html'
]

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        text = fp.read()
    print(f"=== {f} ===")
    audios = re.findall(r'src=["\']([^"\']+\.(?:mp3|wav|ogg|m4a))["\']', text)
    audio_urls = re.findall(r'https?://[^\s"\'`<>]+?\.(?:mp3|wav|ogg|m4a)', text)
    print("Audio tags:", set(audios))
    print("Audio URLs:", set(audio_urls))
