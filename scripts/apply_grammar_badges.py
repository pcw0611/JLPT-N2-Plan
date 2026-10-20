# -*- coding: utf-8 -*-
"""
Update n2_grammar_dataset.json with verified conn_anchor and conn_badge for all 150 items.
"""
import json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT / 'scripts' / 'n2_grammar_dataset.json'

with open(DATASET_PATH, 'r', encoding='utf-8') as f:
    items = json.load(f)

# Specific anchor fixes for cut-off tokens to make them complete natural words
ANCHOR_FIXES = {
    "021": "閉まっていること",
    "029": "うれしかった",
    "041": "分かり",
    "120": "話してしまった",
    "132": "楽しいこと",
    "135": "巻き込まれた",
    "142": "理解できる",
    "143": "遊んでいる"
}

def derive_badge(item, anc):
    num = item['num']
    conn = item.get('connection', '')
    ctype = item.get('conn_type', '')
    
    # 1. Specific curated overrides by grammar pattern number
    if num in ["012", "013", "014", "016", "017", "024", "026", "041", "047", "048", "060", "117", "121", "139"]:
        return "ます형"
    if num in ["039", "044", "045", "046", "083", "085", "141"]:
        return "ない형"
    if num in ["007", "086"]:
        return "ない형"
    if num in ["076", "138"]:
        return "의지형"
    if num in ["123", "131"]:
        return "ば형"
    if num in ["059", "136"]:
        return "가능형"
    if num in ["002", "031", "057", "075", "084"]:
        return "명사+の"
    if num in ["011", "067", "082"]:
        return "나형용사"
    if num in ["005", "015", "022", "029", "062", "080", "089", "096"]:
        return "이형용사"
    if num in ["008", "018", "019", "020", "028", "037", "038", "042", "049", "051", "056", "058", "073", "077", "081", "087", "088", "090", "091", "092", "093", "094", "095", "097", "098", "099", "100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "114", "115", "116", "119", "122", "124", "129", "130", "145", "146", "147", "148", "149", "150"]:
        return "명사"
    if num in ["021", "132"]:
        return "명사"
    if num in ["054", "063", "064", "065", "066", "068", "069", "070", "071", "072"]:
        return "て형"
    if num in ["001", "004", "006", "010", "023", "025", "033", "043", "050", "052", "053", "113", "120", "135", "137"]:
        return "た형"
    if num in ["003", "009", "027", "030", "032", "034", "035", "036", "040", "055", "061", "074", "078", "079", "083", "094", "096", "099", "101", "107", "110", "118", "125", "126", "127", "128", "133", "134", "140", "142", "143", "144"]:
        return "사전형"
        
    # Default fallbacks
    if "ます" in ctype or "ます" in conn:
        return "ます형"
    if "た형" in ctype:
        return "た형"
    if "て형" in ctype:
        return "て형"
    if "ない" in ctype:
        return "ない형"
    if "명사" in ctype or conn.startswith("N"):
        return "명사"
    if "사전형" in ctype:
        return "사전형"
    return "접속"

for item in items:
    num = item['num']
    if num in ANCHOR_FIXES:
        item['conn_anchor'] = ANCHOR_FIXES[num]
    anc = item.get('conn_anchor', '')
    badge = derive_badge(item, anc)
    item['conn_badge'] = badge
    
    # Ensure conn_type is also updated accurately
    if badge == "ます형":
        item['conn_type'] = "Vます형(연용형 어간)"
        item['conn_hint'] = f"앞 단어 「{anc}」가 동사 마스형(ます語幹) 어간이므로 결합합니다!"

# Verify that all anchors exist in before text of sentence_ja_blank
errors = []
for item in items:
    blank = item.get('sentence_ja_blank', '')
    anc = item.get('conn_anchor', '')
    if '（　　）' not in blank:
        errors.append(f"[{item['num']}] No blank in {blank}")
        continue
    before = blank.split('（　　）')[0]
    if anc not in before:
        errors.append(f"[{item['num']}] Anchor '{anc}' not in before '{before}'")

if errors:
    print(f"Validation failed with {len(errors)} errors:")
    for e in errors:
        print(" ", e)
    sys.exit(1)

with open(DATASET_PATH, 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"Successfully updated all {len(items)} items in {DATASET_PATH} with clean conn_anchor & conn_badge!")
