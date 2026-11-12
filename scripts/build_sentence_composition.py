"""Build original N2 practice; never writes learning records or references/."""
from pathlib import Path
import json, re
from build_202112_mock_exam import review

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'jlpt-calendar-site/public/exams'
CONTRAST={
 '조건·전제':'ことには는 뒤의 부정 판단과 호응한다. 以上は·からには는 맡은 일의 책임·결심을, 次第는 일이 확인된 직후의 행동을 나타낸다.',
 '대조·양보':'一方で·反面은 두 측면을 대조하고, にもかかわらず·ものの는 기대와 다른 결과를 잇는다. からといって는 앞 사실만으로 결론 낼 수 없음을 나타낸다.',
 '범위·한정':'に限らず는 범위를 넓히고, を限りに는 마지막 시점을 정한다. を問わず는 그 조건으로 대상을 제한하지 않는다는 뜻이다.',
 '변화·연동':'につれて·にしたがって는 함께 진행하는 변화, に伴って는 변화에 따르는 영향, ば〜ほど는 정도의 비례를 나타낸다.',
 '판단·부정':'わけではない는 단정·해석을 부정하고, とは限らない는 예외 가능성을 남긴다. というものではない는 단순한 성립·일반화를 부정한다.',
 '가능·곤란':'かねる는 화자가 하기 어렵다는 완곡한 표현, かねない는 나쁜 일이 생길 가능성이다. ようがない는 방법이 없다는 뜻이다.',
 '의무·결심':'ざるを得ない는 상황상 불가피함, まい는 하지 않겠다는 결심, ずにはいられない는 감정·행동을 억제하지 못함을 나타낸다.',
 '경험·계기':'きっかけに는 변화의 계기, 以来는 그 시점 이후의 지속이다. 末に는 긴 과정 뒤의 결과이고 あげく는 흔히 좋지 않은 결과에 쓴다.',
 '시점·지속':'うちに는 상태가 유지되는 동안의 행동·변화, ところに는 바로 그 시점의 사건이다. てきた는 과거부터 현재까지 이어진 흐름이다.',
 '준비·순서':'た上で는 앞 행동을 마친 뒤의 판단·실행이고, からでないと는 앞 행동 없이는 뒤 행동이 불가능하다는 조건이다. に先立って는 사전 준비다.',
 '명사 수식':'명사 앞의 보통형은 그 명사를 수식한다. の는 명사 사이의 관계, こと는 행동·내용의 명사화다. 수식 범위를 먼저 끊어 읽는다.',
 '수동·사역':'させる는 누군가 하게 하는 사역, られる는 수동·가능일 수 있다. せずに済む는 하지 않아도 해결됨, ざるを得ない는 해야 하는 불가피함이다.',
 '경어·의뢰':'ていただく는 상대 행동으로 내가 도움을 받음, させていただく는 허락·배려를 받아 내가 행동함이다. ようお願いいたします는 요청 내용을 잇는다.',
 '비교·기준':'わりに는 정도에 비해 예상과 다른 결과, にしては는 특정 기준에 비해 의외의 평가, に反して는 예상과 반대의 결과다.',
 '이유·결과':'おかげでは 대체로 좋은 결과, ばかりには 아쉬운 나쁜 결과, せいか는 확신하지 않는 원인 추측이다. ことから는 판단·결정의 근거를 제시한다.',
 '관점·입장':'から見ると는 판단의 관점, にしてみれば는 당사자 입장이다. にすぎない는 정도의 한정이고 にもかかわらず는 기대와 다른 결과를 잇는다.',
 '강조·정도':'あまり는 과도함에 따른 결과, てたまらない는 강한 감정이다. どころではない는 여유 없음, どころか는 예상과 다른 실제 상황을 뜻한다.',
 '전언·추측':'によると·とのことだ는 정보 출처와 전언, ところを見ると·からすると는 단서에서의 추론이다. はずがない는 근거에 따른 강한 부정 판단이다.',
 '복합 명사절':'かどうか는 여부, どう〜か는 방법을 묻는다. のは〜からだ는 이유 설명, ということ는 인용한 내용을 명사로 묶는 표현이다.',
 '상황·양태':'ふり는 실제와 다른 척함, っぱなし는 방치·지속 상태, かけ는 진행 도중이다. たつもり는 했다고 여기는 인식이다.',
 '조건 통합':'に応じて는 요구·상황에 맞춘 조정, にかかわらず는 조건과 무관함이다. にあたって는 실행 시 주의·준비를 나타내며 にしても는 양보다.',
 '추상적 연결':'てこそ는 앞 행동이 중요한 성립 조건임을 강조한다. だけでなく〜にも는 추가, ではないだろうか는 조심스러운 문제 제기다.'}

def main():
    rows=(ROOT/'scripts/n2_sentence_composition_100.tsv').read_text(encoding='utf-8').splitlines()
    # Exclude weak/unnatural splits, flexible adverb placement, and the N1-target item.
    excluded={12,23,30,31,37,46,56,63,64,81}
    questions=[]
    for source_no,row in enumerate(rows,1):
        if source_no in excluded: continue
        subtype,before,chunks,after,translation,reason,trap,example,example_ko=row.split('|')
        if source_no==43:
            chunks='ところに、友人^から電話が^かかって^きた'
        if source_no==73:
            chunks='ばかりに、多くの^人に迷惑を^かけて^しまった'
        if source_no==88:
            chunks='からすると、彼は^まだ内容を^確認していない^ようだ'
        if source_no==89:
            chunks='失敗する^はずが^ないと^思っていた'
        parts=chunks.split('^')
        reason=re.sub(r'だ+\.$',' 순서다.',reason)
        assert len(parts)==4 and len(set(parts))==4,(source_no,parts)
        full=before+''.join(parts)+after
        assert not re.search('[가-힣]',full+example),source_no
        questions.append(dict(id=len(questions)+1,sourceNo=source_no,subtype=subtype,
            before=before,parts=parts,after=after,star=3,answer=2,full=full,
            translation=translation,reason=reason,trap=trap,example=example,exampleKo=example_ko,
            contrast=CONTRAST[subtype],reviewPrompt=review(before+' ＿＿ ＿＿ ★ ＿＿ '+after),
            reviewFull=review(full),reviewParts=[review(x) for x in parts],reviewExample=review(example)))
    assert len(questions)==100
    assert len({q['full'] for q in questions})==100
    config=dict(id='n2-sentence-composition-100',version=1,questions=questions)
    (OUT/'n2-sentence-composition-100.json').write_text(json.dumps(config,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'jlpt-calendar-site/lib/composition-key.mjs').write_text('export default '+json.dumps({q['id']:dict(parts=q['parts'],answer=q['answer']) for q in questions},ensure_ascii=False)+';\n',encoding='utf-8')
    audit=dict(count=100,duplicatePrompts=0,duplicateChoices=0,source='original practice; no official-paper transcription',
               exclusions=sorted(excluded),revisedSources=[43,73,88,89],
               items=[dict(id=q['id'],sourceNo=q['sourceNo'],full=q['full'],canonicalOrder=[0,1,2,3],starSlot=3,answerStableId=2,reason=q['reason']) for q in questions])
    (ROOT/'docs/N2_SENTENCE_COMPOSITION_100_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Built 100 original questions; 0 duplicate prompts/choices; star=third slot.')

if __name__=='__main__': main()
