import sqlite3, json, sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_check')
con = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur = con.cursor()

# Check tables in col
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("Tables:", tables)

if 'deck_config' in tables:
    cur.execute('SELECT id, name, config FROM deck_config')
    for dcid, name, conf in cur.fetchall():
        try:
            conf_obj = json.loads(conf.decode('utf-8') if isinstance(conf, bytes) else conf)
            print(f"DeckConfig ID {dcid} ({name}):")
            print("  new:", conf_obj.get('new'))
            print("  rev:", conf_obj.get('rev'))
            print("  lapse:", conf_obj.get('lapse'))
        except Exception as e:
            print("Error parsing deck_config:", e)

if 'decks' in tables:
    cur.execute('SELECT id, name, common FROM decks')
    for did, name, common in cur.fetchall():
        if 'Voca' in name:
            try:
                c_obj = json.loads(common.decode('utf-8') if isinstance(common, bytes) else common)
                print(f"Deck {name} (id={did}): common={c_obj}")
            except Exception as e:
                print(f"Deck {name}: error {e}")
