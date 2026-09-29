import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

res = subprocess.run(['curl', '-s', '-A', 'Mozilla/5.0', 'https://namu.wiki/raw/%E8%BF%B7%E6%98%9F%E5%8F%AB'], capture_output=True)
text = res.stdout.decode('utf-8', errors='ignore')
print(f"Output length: {len(text)}")
print("Sample:")
print(text[:500])
