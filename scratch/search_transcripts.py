import glob
import re

transcripts = glob.glob(r'C:\Users\pcw06\.gemini\antigravity\brain\**\transcript*.jsonl', recursive=True)
for t in transcripts:
    try:
        with open(t, 'r', encoding='utf-8', errors='ignore') as fp:
            for line in fp:
                if any(k in line for k in ['midterm-mock', 'official-vol2', 'past-exams', '모의고사', 'n2-past-exam']):
                    urls = re.findall(r'https?://[^\s\"\'`<>]+', line)
                    if urls:
                        print(f"File: {t}")
                        for u in set(urls):
                            print(f"  URL: {u}")
                        break
    except Exception as e:
        pass
