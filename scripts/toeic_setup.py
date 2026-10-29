import sys, urllib.request, json
sys.stdout.reconfigure(encoding='utf-8')

def call_mcp(name, arguments={}):
    req = urllib.request.Request(
        'http://127.0.0.1:3141/',
        data=json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call', 'params': {'name': name, 'arguments': arguments}}).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode('utf-8')
    for line in body.splitlines():
        if line.startswith('data: '):
            return json.loads(line[6:])['result']
    return None

# 1. Create TOEIC model with correct param name
print("Creating TOEIC model...")
res = call_mcp('create_model', {
    'model_name': 'TOEIC 단어장',
    'in_order_fields': ['Word', 'PartOfSpeech', 'Meaning', 'Example', 'ExampleKo', 'Tier'],
    'card_templates': [
        {
            'Name': 'EN→KO',
            'Front': '<div class="toeic-front"><div class="tier-badge">{{Tier}}</div><div class="word">{{Word}}</div><div class="pos">{{PartOfSpeech}}</div></div>',
            'Back': '<div class="toeic-back"><div class="tier-badge">{{Tier}}</div><div class="word">{{Word}}</div><div class="pos">{{PartOfSpeech}}</div><hr><div class="meaning">{{Meaning}}</div><div class="example">{{Example}}</div><div class="example-ko">{{ExampleKo}}</div></div>'
        }
    ],
    'css': '.card{font-family:Pretendard,Arial,sans-serif;background:#0f172a;color:#e2e8f0;text-align:center;padding:20px}.toeic-front,.toeic-back{max-width:500px;margin:0 auto}.tier-badge{display:inline-block;padding:2px 12px;border-radius:9999px;font-size:11px;font-weight:800;margin-bottom:12px;background:#1e293b;border:1px solid #475569;color:#94a3b8}.word{font-size:32px;font-weight:900;color:#f1f5f9;margin-bottom:6px}.pos{font-size:14px;color:#94a3b8;font-style:italic;margin-bottom:8px}hr{border:none;border-top:1px solid #334155;margin:16px 0}.meaning{font-size:22px;font-weight:700;color:#38bdf8;margin-bottom:14px}.example{font-size:15px;color:#cbd5e1;margin-bottom:6px;font-style:italic;text-align:left;padding:10px;background:#1e293b;border-radius:8px;border-left:3px solid #6366f1}.example-ko{font-size:13px;color:#94a3b8;text-align:left;padding:4px 10px}'
})
msg = res.get('structuredContent', {}).get('message', '') or str(res)
print(f"Model: {msg}")

# 2. Create grammar deck
res = call_mcp('create_deck', {'deck_name': 'TOEIC 900+::4-문법'})
msg = res.get('structuredContent', {}).get('message', '') or str(res)
print(f"Grammar deck: {msg}")

print("Setup complete!")
