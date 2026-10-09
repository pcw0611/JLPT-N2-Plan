import socket
import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

_orig_getaddrinfo = socket.getaddrinfo
def _getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _getaddrinfo_ipv4

url = 'https://jlpt-study-calendar.pcw0611.workers.dev/api/study-days'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.load(resp)
    for d in data.get('days', []):
        if d.get('date') == '2026-10-09':
            print('Live Web Status for 2026-10-09:')
            print('  Date:', d.get('date'))
            print('  studyMinutes:', d.get('studyMinutes'))
            print('  questions:', d.get('questions'))
            print('  accuracy:', d.get('accuracy'))
            print('  tests count:', len(d.get('tests', [])))
            for t in d.get('tests', []):
                print(f"    - {t.get('title')} ({t.get('correct')}/{t.get('total')}, {t.get('durationMinutes')}분)")
