import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

def call_mcp(name, arguments=None):
    if arguments is None:
        arguments = {}
    req = urllib.request.Request(
        'http://127.0.0.1:3141/',
        data=json.dumps({
            'jsonrpc': '2.0', 'id': 1,
            'method': 'tools/call',
            'params': {'name': name, 'arguments': arguments}
        }).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        for line in resp.read().decode('utf-8').splitlines():
            if line.startswith('data: '):
                return json.loads(line[6:])['result']

test_notes = [
    {
        "fields": {
            "Word": "schedule",
            "PartOfSpeech": "noun/verb",
            "Meaning": "일정; 일정을 잡다",
            "Example": "Please check the schedule before confirming the appointment.",
            "ExampleKo": "약속을 확인하기 전에 일정을 확인해 주세요.",
            "Tier": "1-기초"
        },
        "tags": ["TOEIC", "Test"]
    }
]

res = call_mcp('add_notes', {
    'deck_name': 'TOEIC 900+::1-기초 (600점 도달)',
    'model_name': 'TOEIC 단어장',
    'notes': test_notes,
    'allow_duplicate': True
})

print("Result:", json.dumps(res, indent=2, ensure_ascii=False))
