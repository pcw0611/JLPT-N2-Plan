import json, sys

sys.stdout.reconfigure(encoding='utf-8')

for path in ['scratch/final_updated_cards.json', 'scratch/updated_cards_preview.json']:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        updated = False
        if isinstance(data, list):
            for item in data:
                back = item.get('back', '')
                if '青葉市' in back:
                    # check if old dialogue
                    if 'え、どういうこと？' in back or 'え？' in back:
                        print(f"Found old dialogue in {path}")
                        # update back
                        # Let's inspect where it is
        print(f"Checked {path}")
    except Exception as e:
        print(f"Error checking {path}: {e}")
