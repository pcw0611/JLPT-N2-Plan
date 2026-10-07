# -*- coding: utf-8 -*-
import json, sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT / 'scripts' / 'n2_grammar_dataset.json'

with open(DATASET_PATH, 'r', encoding='utf-8') as f:
    items = json.load(f)

# Fix for 125 typo
for x in items:
    if x['num'] == '125':
        x['sentence_ja'] = x['sentence_ja'].replace('返すべきた', '返すべきだ')

# Manual fixes for ja_target where extraction needs surgical precision
SURGICAL_JA = {
    "002": "あまり",
    "007": "うちに",
    "009": "鳴るか鳴らないかのうちに",
    "012": "かけの",
    "018": "にかけて",
    "021": "ことからすると",
    "022": "からといって",
    "023": "からには",
    "025": "きり",
    "026": "きった",
    "028": "こそ",
    "033": "ことに",
    "034": "ことになった",
    "036": "最中に",
    "038": "さえ",
    "039": "ざるを得なかった",
    "043": "末",
    "044": "ずに",
    "045": "かずに済んだ",
    "046": "ずにはいられなかった",
    "048": "そうになった",
    "049": "それなりの",
    "050": "以上は",
    "051": "だけあって",
    "052": "ところ",
    "054": "ばかりなのに",
    "057": "ついでに",
    "060": "つつも",
    "061": "つもりで",
    "065": "たまらない",
    "066": "てでも",
    "067": "でならない",
    "068": "てはじめて",
    "076": "ようと思います",
    "078": "ところです",
    "079": "ところに",
    "080": "ところを",
    "081": "としたら",
    "086": "ことはない",
    "097": "にこたえて",
    "101": "にしては",
    "106": "に次いで",
    "107": "につれて",
    "109": "にともなって",
    "110": "には",
    "111": "に反して",
    "112": "にほかならない",
    "115": "にわたって",
    "116": "ぬきには",
    "117": "抜いた",
    "118": "のだ",
    "119": "すればするほど",
    "120": "ばかりに",
    "121": "始めた",
    "122": "はともかく",
    "123": "ばよかった",
    "124": "ぶりに",
    "125": "べきだ",
    "126": "ほかない",
    "127": "ほど",
    "128": "まい",
    "129": "向き",
    "130": "向けに",
    "131": "もよければ",
    "132": "もあれば",
    "133": "ものか",
    "134": "ものではない",
    "135": "ものだから",
    "136": "ものなら",
    "137": "ものの",
    "138": "ようとした",
    "139": "しようがない",
    "140": "ようでは",
    "141": "ないように",
    "142": "ようになってきた",
    "143": "わけにはいかない",
    "144": "わりに",
    "145": "を契機として",
    "146": "を込めて",
    "147": "を通じて",
    "148": "を問わず",
    "149": "をはじめとして",
    "150": "をめぐって"
}

# Manual fixes for target_ko
SURGICAL_KO = {
    "012": "읽다 만",
    "022": "싸다고 해서",
    "023": "맡은 이상",
    "024": "피곤한 기색",
    "025": "나간 뒤",
    "036": "한창 하던 중에",
    "039": "이용하지 않을 수 없었다",
    "043": "논의한 끝에",
    "045": "가지 않고 해결되었다",
    "046": "웃지 않고는 못 배겼다",
    "049": "그 나름의 방법",
    "050": "약속한 이상",
    "052": "부탁드렸더니",
    "054": "막 먹었을 뿐인데",
    "061": "죽은 셈치고",
    "066": "빚을 져서라도",
    "067": "걱정되어 견딜 수가 없다",
    "086": "먹지 못할 것도 없지만",
    "106": "에 이어",
    "107": "접근함에 따라서",
    "108": "유학생에게 있어서",
    "109": "증가에 수반하여",
    "111": "기대에 반하여",
    "113": "에 의해",
    "114": "에 상관없이",
    "117": "완주해 냈다",
    "119": "공부하면 할수록",
    "121": "내리기 시작해서",
    "122": "가격은 어쨌든",
    "123": "가져왔으면 좋았을 텐데",
    "125": "갚아야(돌려주어야) 마땅하다",
    "127": "쏟아질 뻔할 정도로",
    "129": "고령자에게 적합한",
    "130": "유학생들을 대상",
    "131": "경치도 좋거니와",
    "133": "갈까 보냐",
    "134": "말하는 게 아니다",
    "137": "취득했지만",
    "138": "나서려던",
    "139": "취할 방법이 없다",
    "140": "꼴이라면",
    "141": "않도록",
    "144": "비해서는"
}

cleaned = []
errors = []

for x in items:
    num = x['num']
    ja = x['sentence_ja']
    ko = x['sentence_ko']
    
    # Clean ko punctuation
    ko = re.sub(r'\s+([.,!?])', r'\1', ko)
    ko = ko.replace('취득했 지만', '취득했지만')
    ko = ko.replace('나서 려던', '나서려던')
    ko = ko.replace('유학생 에게', '유학생에게')
    ko = ' '.join(ko.split())
    
    # Determine JA target
    if num in SURGICAL_JA:
        t_ja = SURGICAL_JA[num]
    else:
        t_ja = x.get('sentence_ja_target', '')
        # If contains comma, take part before comma
        if '、' in t_ja:
            t_ja = t_ja.split('、')[0].strip()
            
    if t_ja not in ja:
        errors.append(f"[{num}] JA target '{t_ja}' not in '{ja}'")
        blank = ja + " （　　）"
    else:
        blank = ja.replace(t_ja, "（　　）", 1)
        
    # Determine KO target
    if num in SURGICAL_KO:
        t_ko = SURGICAL_KO[num]
    else:
        t_ko = x.get('target_ko', '')
        
    if t_ko not in ko:
        errors.append(f"[{num}] KO target '{t_ko}' not in '{ko}'")
        
    cleaned.append({
        'id': x['id'],
        'num': num,
        'pattern': x['pattern'],
        'meaning': x['meaning'],
        'connection': x.get('connection', ''),
        'core_meaning': x.get('core_meaning', ''),
        'sentence_ja': ja,
        'sentence_ja_target': t_ja,
        'sentence_ja_blank': blank,
        'sentence_ko': ko,
        'target_ko': t_ko,
        'diff_point': x.get('diff_point', ''),
        'exam_signal': x.get('exam_signal', '')
    })

print(f"Total processed: {len(cleaned)}")
print(f"Total errors: {len(errors)}")
for e in errors:
    print("  ERROR:", e)

if not errors:
    with open(DATASET_PATH, 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    print("Dataset cleaned and saved successfully!")
