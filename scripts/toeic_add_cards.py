"""
Batch-add TOEIC 900+ vocabulary & grammar cards to Anki via MCP.
Reads JSON data files and adds them to the appropriate decks.
"""
import json
import sys
import urllib.request
import time

sys.stdout.reconfigure(encoding='utf-8')

MCP_URL = 'http://127.0.0.1:3141/'
MODEL_NAME = 'TOEIC 단어장'

TIER_TO_DECK = {
    '1-기초': 'TOEIC 900+::1-기초 (600점 도달)',
    '2-중급': 'TOEIC 900+::2-중급 (700~800점)',
    '3-고급': 'TOEIC 900+::3-고급 (900+)',
    '문법':  'TOEIC 900+::4-문법',
}

TIER_TO_TAGS = {
    '1-기초': ['TOEIC', 'Tier1', '기초'],
    '2-중급': ['TOEIC', 'Tier2', '중급'],
    '3-고급': ['TOEIC', 'Tier3', '고급'],
    '문법':  ['TOEIC', 'Grammar', '문법'],
}

DATA_FILES = [
    'scripts/toeic_tier1.json',
    'scripts/toeic_tier2.json',
    'scripts/toeic_tier3.json',
    'scripts/toeic_grammar.json',
]


def call_mcp(name, arguments=None):
    if arguments is None:
        arguments = {}
    req = urllib.request.Request(
        MCP_URL,
        data=json.dumps({
            'jsonrpc': '2.0', 'id': 1,
            'method': 'tools/call',
            'params': {'name': name, 'arguments': arguments}
        }).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/event-stream'
        }
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = resp.read().decode('utf-8')
    for line in body.splitlines():
        if line.startswith('data: '):
            return json.loads(line[6:])['result']
    return None


def add_notes_batch(notes_data, deck_name, tags, batch_size=80):
    """Add notes in batches using the correct Anki MCP schema."""
    total = len(notes_data)
    added = 0
    failed = 0
    
    for i in range(0, total, batch_size):
        batch = notes_data[i:i + batch_size]
        note_entries = []
        for item in batch:
            note_entries.append({
                'fields': {
                    'Word': item['Word'],
                    'PartOfSpeech': item['PartOfSpeech'],
                    'Meaning': item['Meaning'],
                    'Example': item['Example'],
                    'ExampleKo': item['ExampleKo'],
                    'Tier': item['Tier'],
                },
                'tags': tags,
            })
        
        args = {
            'deck_name': deck_name,
            'model_name': MODEL_NAME,
            'notes': note_entries,
            'allow_duplicate': True,
        }
        
        result = call_mcp('add_notes', args)
        
        batch_created = 0
        if result and 'structuredContent' in result:
            batch_created = result['structuredContent'].get('created', 0)
        elif result and 'content' in result:
            try:
                sc = json.loads(result['content'][0]['text'])
                batch_created = sc.get('created', 0)
            except Exception:
                pass
        
        added += batch_created
        print(f'  [{deck_name}] {added}/{total} notes created (batch {i // batch_size + 1})')
        time.sleep(0.3)
    
    return added, failed


def main():
    grand_total = 0
    
    for filepath in DATA_FILES:
        print(f'\n📂 Loading {filepath}...')
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f'  ❌ File not found: {filepath}')
            continue
        except json.JSONDecodeError as e:
            print(f'  ❌ JSON error in {filepath}: {e}')
            continue
        
        print(f'  📊 {len(data)} items loaded')
        
        # Group by tier
        by_tier = {}
        for item in data:
            tier = item.get('Tier', '1-기초')
            by_tier.setdefault(tier, []).append(item)
        
        for tier, items in by_tier.items():
            deck_name = TIER_TO_DECK.get(tier)
            tags = TIER_TO_TAGS.get(tier, ['TOEIC'])
            
            if not deck_name:
                print(f'  ⚠️ Unknown tier "{tier}" — skipping {len(items)} items')
                continue
            
            print(f'  🃏 Adding {len(items)} cards to "{deck_name}"...')
            added, failed = add_notes_batch(items, deck_name, tags)
            grand_total += added
            print(f'  ✅ {added} cards created in {deck_name}')
    
    print(f'\n{"="*60}')
    print(f'🎉 Total: {grand_total} cards added to Anki!')
    print(f'{"="*60}')
    
    # Verify counts per deck
    print('\n📊 Verifying card counts in Anki...')
    for tier, deck_name in TIER_TO_DECK.items():
        result = call_mcp('find_notes', {'query': f'deck:"{deck_name}"'})
        if result and 'content' in result:
            txt = result['content'][0]['text']
            data = json.loads(txt)
            print(f'  {deck_name}: {len(data.get("notes", []))} notes')


if __name__ == '__main__':
    main()
