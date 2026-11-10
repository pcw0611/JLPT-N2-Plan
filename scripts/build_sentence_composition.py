"""Build original N2 practice; never writes learning records or references/."""
from pathlib import Path
import json, re
from build_202112_mock_exam import review

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'jlpt-calendar-site/public/exams'

def main():
    rows=(ROOT/'scripts/n2_sentence_composition_100.tsv').read_text(encoding='utf-8').splitlines()
    # Exclude weak/unnatural splits, flexible adverb placement, and the N1-target item.
    excluded={12,23,30,31,37,46,56,63,64,81}
    questions=[]
    for source_no,row in enumerate(rows,1):
        if source_no in excluded: continue
        subtype,before,chunks,after,translation,reason,trap,example,example_ko=row.split('|')
        if source_no==73:
            chunks='ばかりに、多くの^人に迷惑を^かけて^しまった'
        if source_no==88:
            chunks='からすると、彼は^まだ内容を^確認していない^ようだ'
        if source_no==89:
            chunks='失敗する^はずが^ないと^思っていた'
        parts=chunks.split('^')
        assert len(parts)==4 and len(set(parts))==4,(source_no,parts)
        full=before+''.join(parts)+after
        assert not re.search('[가-힣]',full+example),source_no
        questions.append(dict(id=len(questions)+1,sourceNo=source_no,subtype=subtype,
            before=before,parts=parts,after=after,star=3,answer=2,full=full,
            translation=translation,reason=reason,trap=trap,example=example,exampleKo=example_ko,
            reviewFull=review(full),reviewParts=[review(x) for x in parts],reviewExample=review(example)))
    assert len(questions)==100
    assert len({q['full'] for q in questions})==100
    config=dict(id='n2-sentence-composition-100',version=1,questions=questions)
    (OUT/'n2-sentence-composition-100.json').write_text(json.dumps(config,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'jlpt-calendar-site/lib/composition-key.mjs').write_text('export default '+json.dumps({q['id']:dict(parts=q['parts'],answer=q['answer']) for q in questions},ensure_ascii=False)+';\n',encoding='utf-8')
    audit=dict(count=100,duplicatePrompts=0,duplicateChoices=0,source='original practice; no official-paper transcription',
               exclusions=sorted(excluded),revisedSources=[73,88,89],
               items=[dict(id=q['id'],sourceNo=q['sourceNo'],full=q['full'],canonicalOrder=[0,1,2,3],starSlot=3,answerStableId=2,reason=q['reason']) for q in questions])
    (ROOT/'docs/N2_SENTENCE_COMPOSITION_100_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Built 100 original questions; 0 duplicate prompts/choices; star=third slot.')

if __name__=='__main__': main()
