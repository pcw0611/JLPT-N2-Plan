"""Author the 2026-11-02 self-made set; never touch the baseline examples.

TSV fields are deliberately human-reviewable. pykakasi is already installed;
readings below are generated offline, with contextual overrides reviewed here.
"""
import html
import json
import re
from pathlib import Path
from pykakasi import kakasi

ROOT = Path(__file__).resolve().parents[1]
BASE = json.loads((ROOT / 'scripts/n2_grammar_dataset.json').read_text(encoding='utf-8'))
converter = kakasi()

# Full-word contextual readings that a dictionary-only transliterator may miss.
READINGS = {'一日': 'いちにち', '一人': 'ひとり', '二人': 'ふたり',
            '人気': 'にんき', '一等': 'いっとう', '方々': 'かたがた',
            '皆様': 'みなさま', '何時': 'なんじ', '一号店': 'いちごうてん',
            '方': 'かた', '足跡': 'あしあと', '末': 'すえ', '入っ': 'はいっ',
            '人': 'ひと', '今年': 'ことし', '市場': 'いちば', '別と': 'べつと',
            '通り': 'とおり', '日': 'ひ', '入ろ': 'はいろ', '堪え': 'たえ',
            '通行止': 'つうこうど', '皮切': 'かわき', '相': 'あい',
            '際に': 'ぎわに', '彼の': 'かれの', '今日は': 'きょうは',
            '偉': 'えら', '床': 'ゆか', '品': 'しな', '方を': 'かたを'}
PHRASES = {'十分以上': 'じゅっぷんいじょう', '十分しか': 'じゅっぷんしか',
           'バス停': 'ばすてい', '十分おきに': 'じゅっぷんおきに', '十分で': 'じゅっぷんで',
           '二か月': 'にかげつ', '通っていた': 'かよっていた', '暮らし方': 'くらしかた',
           '説明を行った': 'せつめいをおこなった',
           '新店舗': 'しんてんぽ', '出産後': 'しゅっさんご', '一号店': 'いちごうてん',
           '別れ際': 'わかれぎわ', '通行止め': 'つうこうどめ', '皮切り': 'かわきり'}

def ruby(text):
    pattern = '(' + '|'.join(sorted(map(re.escape, PHRASES), key=len, reverse=True)) + ')'
    segments = re.split(pattern, text)
    return ''.join(f'<ruby>{html.escape(s)}<rt>{PHRASES[s]}</rt></ruby>'
                   if s in PHRASES else auto_ruby(s) for s in segments)

def auto_ruby(text):
    parts = []
    for token in converter.convert(text):
        word = token['orig']
        reading = READINGS.get(word, token['hira'])
        if re.search(r'[一-龯々]', word):
            parts.append(f'<ruby>{html.escape(word)}<rt>{reading}</rt></ruby>')
        else:
            parts.append(html.escape(word))
    return ''.join(parts)

def marked(text):
    match = re.search(r'\[([^\[\]]+)\]', text)
    assert match and text.count('[') == 1 and text.count(']') == 1, text
    target = match[1]
    return text[:match.start()] + target + text[match.end():], target, text[:match.start()] + '（　　）' + text[match.end():]

# The merged pattern labels stay identical; these notes explain today's member.
FOCUS = {
 '034': ('이번 문장에서는 ことにはならない: 어떤 사실만으로 그 결론이 성립하지 않음을 나타낸다.', '동사 보통형＋ことにはならない'),
 '057': ('이번 문장에서는 がてら: 산책이라는 주된 행동을 하면서 다른 일도 겸한다. 散歩のがてら가 아니라 散歩がてら.', '동작 명사／동사 ます를 뺀 형태＋がてら'),
 '060': ('이번 문장에서는 つつある: 변화가 진행 중임을 나타낸다. 역접 つつも(알면서도)와 구별한다.', '동사 ます를 뺀 형태＋つつある'),
 '092': ('이번 문장에서는 を欠かさず: 정기적인 활동을 한 번도 거르지 않음을 나타낸다. に欠かせない는 필수적이라는 뜻이다.', '명사＋を欠かさず'),
 '093': ('이번 문장에서는 にかぎり: 할인 대상의 범위를 회원으로 제한한다. 불운한 날의 にかぎって와 구별한다.', '명사＋にかぎり'),
 '110': ('読むには読んだ는 읽었다는 사실은 인정하지만 이해는 부족하다는 양보이다. 목적을 나타내는 合格するには와 구별한다.', '동사 사전형＋には＋같은 동사'),
 '113': ('이번 문장에서는 によっては: 여러 출구 중 일부를 택하면 예외적으로 그런 결과가 생긴다는 뜻이다.', '명사＋によっては'),
 '116': ('이번 문장에서는 をぬきにして: 이론은 잠시 제쳐 두고 실습하자는 뜻. 協力ぬきには〜ない라는 필수 조건과 구별한다.', '명사＋をぬきにして'),
 '119': ('短い→短ければ短いほど. 형용사도 ば〜ほど를 만들 수 있다. 여기서는 비례를 언급한 뒤 とは限らない로 그 일반화를 부정한다.', 'い형용사 어간＋ければ＋같은 い형용사＋ほど'),
 '123': ('広い→広ければよかった. 동사뿐 아니라 い형용사의 조건형으로도 아쉬움을 나타낸다.', 'い형용사 어간＋ければよかった'),
 '128': ('する→すまい. 이 문장은 과거 추측이 아니라 앞으로 반복하지 않겠다는 부정 의지이다.', 'する→すまい'),
 '131': ('本屋もあれば映画館もある: 두 존재를 병렬한다. ある→あれば로 만들며, よければ처럼 형용사만 쓰는 구문이 아니다.', 'Nも＋あれば＋Nもある'),
 '134': ('이번 문장에서는 과거 회상 たものだ: 어릴 때 반복하던 일을 그리워한다. 도리·충고의 るものだ와 구별한다.', '동사 た형＋ものだ'),
 '136': ('의지형＋ものなら는 가벼운 가정이 아니라, 만약 그런 행동을 하면 심각한 결과가 따른다는 경고이다. 가능형＋ものなら와 구별한다.', '동사 의지형＋ものなら'),
 '142': ('이번 문장에서는 ないようにしている: 보지 않도록 습관적으로 노력한다. 자연스러운 변화인 ようになる와 구별한다.', '동사 ない형＋ようにしている'),
 '143': ('ない＋わけにはいかない는 안 할 수 없다, 즉 해야 한다는 뜻이다. 여기서는 초대받았으니 참석해야 한다.', '동사 ない형＋わけにはいかない'),
 '147': ('이번 문장에서는 기간 전체를 나타내는 一年を通じて. 매개·경험을 뜻하는 活動を通じて와 구별한다.', '기간 명사＋を通じて'),
 '160': ('感謝に堪えない는 감사의 마음을 억누르기 어려울 만큼 크다는 뜻이다. 見るに堪えない(차마 못 보다)와 의미가 반대처럼 보이므로 주의한다.', '감정 명사＋に堪えない'),
 '183': ('이번 문장에서는 立ちっぱなし: 계속 서 있는 상태이다. つけっぱなし처럼 방치·실수만 나타내는 표현이 아니다.', '동사 ます를 뺀 형태＋っぱなし'),
 '195': ('氷のごとき는 얼음과 같다는 문어적 비유. 私ごとき처럼 の 없이 낮추는 용법과 구별한다.', '명사＋の＋ごとき＋명사'),
}

def build():
    rows = []
    for line in (ROOT / 'scripts/grammar_sentences_monday.tsv').read_text(encoding='utf-8').splitlines():
        if not line or line.startswith('#'): continue
        num, ja, ko, anchor, form = line.split('\t')
        base = BASE[int(num) - 1]
        sentence, target, blank = marked(ja)
        translation, ko_target, _ = marked(ko)
        assert blank.split('（　　）')[0].endswith(anchor), num
        row = {key: base[key] for key in ('id', 'num', 'pattern')}
        row.update(sentence_ja=sentence, sentence_ja_target=target,
                   sentence_ja_blank=blank, sentence_ko=translation,
                   target_ko=ko_target, sentence_ja_ruby=ruby(sentence),
                   conn_anchor=anchor, conn_badge=form, conn_type=form,
                   conn_strict=False, conn_hint=f'이번 문장: 「{anchor}」는 {form}.',
                   # Old sentence-local alternatives must not leak into a new context.
                   accepted_pattern_forms={})
        # Only alternatives that fit this new sentence and the same meaning.
        alternatives = {
            '099': {'107': 'につれて', '109': 'にともなって'},
            '107': {'099': 'にしたがって', '109': 'にともなって'},
            '114': {'148': 'を問わず'}, '148': {'114': 'によらず'},
            '145': {'178': 'を機に'}, '178': {'145': 'を契機として'},
            '170': {'172': 'はずがない'}, '172': {'170': 'わけがない'},
        }
        row['accepted_pattern_forms'] = {BASE[int(n)-1]['pattern']: form
                                       for n, form in alternatives.get(num, {}).items()}
        # The actual case and the whole pattern's other possibilities are both shown.
        row['conn_chips'] = [f'이번 문장: {anchor} → {form}', base['connection']]
        if num in FOCUS:
            row['core_meaning'], case_rule = FOCUS[num]
            row['conn_chips'][0] = '이번 문장: ' + case_rule
        if num == '034':
            row['connection'] = 'ことになる・ことにする: Vる／Vない／ことにはならない: 보통형＋ことにはならない'
            row['conn_chips'][1] = row['connection']
        if num == '057':
            row['connection'] = 'ついでに: Vる・Vた／Nの｜がてら: Vます어간／동작 N｜をかねて: N'
            row['conn_chips'][1] = row['connection']
        rows.append(row)
    assert len(rows) == 200 and len({r['id'] for r in rows}) == 200
    out = {'id': 'monday-20261102', 'available_from': '2026-11-02',
           'weekday': 1, 'label': '月曜・新例文200', 'source': 'self-made',
           'items': rows}
    (ROOT / 'scripts/n2_grammar_monday.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Authored 200 Monday sentences; baseline unchanged.')

if __name__ == '__main__': build()
