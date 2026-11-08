"""Build six weekday banks from reviewed 3-connection × 2-context matrices.

Monday is retained exactly. Each matrix row specifies three complete leading
clauses, their Korean translations/anchors/forms, and two compatible outcomes.
This is deliberate spaced reuse of connections with different continuations,
not an assertion that all 1,200 combinations were written independently.
"""
import json
import re
from pathlib import Path
from functools import lru_cache
from build_grammar_monday import BASE, marked, ruby

ROOT = Path(__file__).resolve().parents[1]
FORMS = {
 'Vる':'동사 사전형', 'Vた':'동사 た형', 'V普':'동사 보통형',
 'Vます':'동사 ます를 뺀 형태', 'Vて':'동사 て형', 'Vない':'동사 ない형',
 'Vている':'동사 ている형', 'V意向':'동사 의지형', 'V可能':'동사 가능형',
 'V無意志':'무의지 동사 사전형', 'V否幹':'동사 ない를 뺀 형태',
 'する否定':'する→せ', 'するまい':'する→すまい', 'Vん':'동사 ない를 뺀 형태＋ん',
 'Vる反復':'사전형＋か＋같은 동사 ない형', 'Vば幹':'동사 조건형 ば 직전',
 'Vなければ':'동사 부정 조건형 なければ 직전',
 'Vる決定':'동사 사전형·자기 결정', 'Vない決定':'동사 ない형·외부 결정',
 'Vる外部':'동사 사전형·외부 결정', 'V可能変化':'동사 가능형·변화',
 'Vない習慣':'동사 ない형·의식적 습관', 'Vない義務':'동사 ない형·해야 함',
 'Vる助言':'동사 사전형·조언', 'Vない助言':'동사 ない형·조언', 'Vても':'동사 ても형',
 'Aい':'い형용사 기본형', 'A過去':'い형용사 과거형', 'Aな':'な형용사＋な',
 'Aだ':'な형용사＋だ', 'A幹':'형용사 어간', 'Aで':'な형용사 で형',
 'Aくて':'い형용사 くて형', 'A否定':'い형용사 부정형 くない',
 'Aでない':'な형용사 부정형 でない', 'Aければ':'い형용사 조건형 ければ 직전',
 'Aの':'い형용사＋の', 'Aなの':'な형용사＋な＋の', 'A過去の':'い형용사 과거형＋の',
 'N':'명사 직접 접속', 'Nの':'명사＋の', 'Nだ':'명사＋だ', 'Nな':'명사＋な',
 'Nだった':'명사＋だった', 'Nである':'명사＋である', 'Nで':'명사＋で',
 'N範囲':'명사＋から＋명사＋にかけて', 'N条件':'명사＋さえ＋조건형',
 'Vます条件':'동사 ます를 뺀 형태＋さえすれば', 'Nこと':'동사구의 명사화 こと',
 'N人':'사람 명사＋もいれば', 'N感情':'감정·반응 명사', 'N受身':'명사＋수동 표현',
 'N使役':'명사＋사역 표현', 'N挨拶':'인사 명사', '数量':'시간·기간·범위 수량',
 '後N':'뒤의 명사 수식', '慣用':'정착된 표현 ありげ', 'ごN':'ご＋한자 명사',
 'おVます':'お＋동사 ます를 뺀 형태', '場所に':'존경 대상의 존재 장소＋に',
 '方向へ':'존경 대상의 이동 방향＋へ', '相手に':'만나는 상대＋に',
}

@lru_cache(maxsize=None)
def readings(text): return ruby(text)

def build():
    matrices=[]
    for line in (ROOT/'scripts/grammar_weekly_matrix.tsv').read_text(encoding='utf-8').splitlines():
        if not line or line.startswith('#'): continue
        columns=line.split('\t')
        assert len(columns)==7, columns[0]
        num=columns[0]
        fields=[c.split('|') for c in columns[1:]]
        assert [len(f) for f in fields]==[3,3,3,3,2,2],num
        matrices.append((num,*fields))
    assert len(matrices)==200
    monday=json.loads((ROOT/'scripts/n2_grammar_monday.json').read_text(encoding='utf-8'))
    monday['key']='monday'
    banks=[monday]
    days=[('tuesday',2,'火曜'),('wednesday',3,'水曜'),('thursday',4,'木曜'),
          ('friday',5,'金曜'),('saturday',6,'土曜'),('sunday',0,'日曜')]
    for variant,(key,weekday,label) in enumerate(days):
        # Three connection/lexical cases recur with a second substantive outcome.
        leading=variant%3
        ending=variant//3
        rows=[]
        for num,jas,kos,anchors,forms,tails,ko_tails in matrices:
            b=BASE[int(num)-1]
            if num=='132':
                tails=[['暇な日もある。','忙しくない日もある。'],
                       ['相談しにくい人もいる。','話しかけにくい人もいる。'],
                       ['不便な場所もある。','交通の便が悪い場所もある。']][leading]
                ko_tails=[['한가한 날도 있다.','바쁘지 않은 날도 있다.'],
                          ['상담하기 어려운 사람도 있다.','말 걸기 어려운 사람도 있다.'],
                          ['불편한 곳도 있다.','교통편이 나쁜 곳도 있다.']][leading]
            ja,target,blank=marked(jas[leading]+tails[ending])
            ko,kot,_=marked(kos[leading]+ko_tails[ending])
            anchor=anchors[leading]; code=forms[leading]; form=FORMS[code]
            assert blank.split('（　　）')[0].endswith(anchor),(key,num,anchor)
            assert not re.search(r'[가-힣]',ja),(key,num)
            row={k:b[k] for k in ('id','num','pattern')}
            row.update(sentence_ja=ja,sentence_ja_target=target,sentence_ja_blank=blank,
              sentence_ko=ko,target_ko=kot,sentence_ja_ruby=readings(ja),
              conn_anchor=anchor,conn_badge=form,conn_type=form,conn_strict=False,
              conn_chips=[f'이번 문장: {anchor} → {form}',b['connection']],
              conn_hint=f'「{anchor}」: {form}.',accepted_pattern_forms={})
            note=b['core_meaning']
            if num=='034': note='ことにする는 스스로 정함, ことになる는 규칙·상황에 따른 결정. 현재 문장의 시제·부정형에도 주의한다.'
            if num=='060': note='이번 문장은 ながらも의 역접이다. い형용사는 い를 유지하고, 일부 な형용사·명사는 어간에 연결한다. 변화를 나타내는 つつある와 구별한다.'
            if num=='086': note='〜ないことはない는 전면 부정을 피한다. 悪くないことはない는 나쁜 점이 있기는 하다, 納得できないことはない는 납득할 수는 있다는 뜻. 앞말의 긍정·부정 의미를 먼저 확인한다.'
            if num=='093': note='이번 문장에서는 にかぎらず: 특정 대상만으로 범위를 제한하지 않고 다른 대상도 포함한다.'
            if num=='110': note='이번 문장에서는 목적을 이루기 위한 필요 조건을 제시한다. 読むには読んだ라는 양보와 구별한다.'
            if num=='134': note='이번 문장에서는 동사 사전형＋ものだ: 일반적인 도리·규범. 동사 た형＋ものだ의 과거 회상과 구별한다.'
            if num=='142': note='ようになった는 가능해진 변화, ないようにしている는 하지 않으려는 의식적 실천. 현재 문장의 접속 형태를 구별한다.'
            if num=='143': note='る／ている＋わけにはいかない는 사회적 사정상 할 수 없음. ない＋わけにはいかない는 안 할 수 없음, 즉 해야 함.'
            if num=='160': note='동사＋に堪えない는 차마 보고 들을 수 없음. 感謝に堪えない는 감사의 마음이 매우 큼. 같은 표현의 상반된 용법을 구별한다.'
            row['core_meaning']='문법 → 문형 선택 → 접속·의미\n'+note
            # New contexts replace, rather than inherit, old local alternatives.
            alternatives={
              '099':{'107':'につれて','109':'にともなって'},
              '107':{'099':'にしたがって','109':'にともなって'},
              '109':{'099':'にしたがって','107':'につれて'},
              '114':{'148':'を問わず'},'148':{'114':'によらず'},
              '145':{'178':'を機に'},'178':{'145':'をきっかけに'},
              '170':{'172':'はずがない'},'172':{'170':'わけがない'},
            }
            row['accepted_pattern_forms']={BASE[int(n)-1]['pattern']:v for n,v in alternatives.get(num,{}).items()}
            if num=='057':
                row['connection']='ついでに: Vる・Vた／Nの｜がてら: Vます어간／동작 N｜をかねて: N'
                row['conn_chips'][1]=row['connection']
            rows.append(row)
        banks.append({'key':key,'id':key+'-20261103','available_from':'2026-11-03',
          'weekday':weekday,'label':label+'・例文200','source':'self-made',
          'composition':'3 connection/lexical cases × 2 continuations','items':rows})
    assert len({r['sentence_ja'] for bank in banks for r in bank['items']})==1400
    out={'version':'20261103','banks':banks}
    (ROOT/'scripts/n2_grammar_weekly.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Built seven banks: Monday retained, six banks added, 1400 distinct full prompts.')

if __name__=='__main__': build()
