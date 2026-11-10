"""Build the user-supplied December 2021 paper; no learning writes.

The source JSON is reviewed transcription. Source PDFs/MP3 remain untouched.
"""
from pathlib import Path
import json,re,hashlib
from html import escape
from build_202307_mock_exam import annotate
from audit_exam_data import audit

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'jlpt-calendar-site/public/exams'

# Contextual readings reviewed against the text; do not accept dictionary-token
# defaults such as 朝一/人, 十八歳=じゅうろくさい or 日本文/学.
READINGS={
    '朝一人で':'あさひとりで','本登録':'ほんとうろく','仮登録':'かりとうろく',
    '食べ頃':'たべごろ','書きましょう':'かきましょう','人たち':'ひとたち',
    '十八歳':'じゅうはっさい','四十八時間':'よんじゅうはちじかん','三時間':'さんじかん',
    '一日の三分の一':'いちにちのさんぶんのいち','一日目':'いちにちめ',
    '五年生':'ごねんせい','日本文学':'にほんぶんがく','ご飯':'ごはん',
    '鮮やか':'あざやか','経って':'たって','並べて':'ならべて','入って':'はいって',
    '入った':'はいった','入る':'はいる','小さく':'ちいさく','欲しく':'ほしく',
    '通らない':'とおらない','厳しい':'きびしい','疑問を抱く':'ぎもんをいだく',
    '灯台下暗し':'とうだいもとくらし','袋を開ける':'ふくろをあける','この際':'このさい',
    '二分程度':'にふんていど','今やっている':'いまやっている','乗った':'のった',
    '高校生の方':'こうこうせいのかた','中学生の方':'ちゅうがくせいのかた',
    '利用される方':'りようされるかた','使用される方':'しようされるかた',
    '利用する方':'りようするかた','上の表':'うえのひょう','間に':'あいだに',
    '力んで':'りきんで','何役':'なんやく','今年':'ことし','明後日':'あさって',
}
def review(text):
    # Operate on text nodes only, preserving the original safe HTML attributes.
    def apply(m):
        s=m.group(0)
        pattern='|'.join(map(re.escape,sorted(READINGS,key=len,reverse=True)))
        return re.sub(pattern,lambda x:'<ruby>'+escape(x[0])+'<rt>'+READINGS[x[0]]+'</rt></ruby>',s)
    s=''.join(piece if piece.startswith('<') else apply(re.match(r'[\s\S]*',piece)) for piece in re.split(r'(<[^>]*>)',text or '') if piece)
    s=annotate(s)
    for token,reading in {'人':'ひと','間':'あいだ','入っ':'はいっ','並べて':'ならべて','欲し':'ほし','通ら':'とおら','生の':'せいの','四十':'よんじゅう','経っ':'たっ'}.items():
        s=re.sub(r'<ruby>'+re.escape(token)+r'<rt>[^<]*</rt></ruby>',f'<ruby>{token}<rt>{reading}</rt></ruby>',s)
    return s

def main():
    questions=json.loads((ROOT/'scripts/n2_202112_questions.json').read_text(encoding='utf-8'))
    assert len(questions)==101
    assert [q['id'] for q in questions]==list(range(1,102))
    for q in questions:
        for field in ['translation','reason','trap','contrast','exampleJa','exampleKo']:
            assert q['explanation'].get(field),(q['id'],field)
        for field in ['instruction','passage','prompt']:
            assert not re.search('[가-힣]',q.get(field,'')),(q['id'],field)
            annotate(q.get(field,''))
        assert not any(re.search('[가-힣]',c) for c in q['choices']),q['id']
        if q.get('passage'):q['passageId']=hashlib.sha256(q['passage'].encode()).hexdigest()[:12]
        q['reviewPassage']=review(q.get('passage',''))
        q['reviewPrompt']=review(q['prompt'])
        q['reviewChoices']=[review(c) for c in q['choices']]
        q['reviewExample']=review(q['explanation']['exampleJa'])
        if q.get('transcript'):q['reviewTranscript']=review(q['transcript'])
    report=audit({'questions':questions,'totalItems':101})
    assert report['structuralCheckPassed'],report['errors']
    config={'id':'n2-past-202112','version':1,'title':'2021年12月 JLPT N2 実戦模試',
        'course':'2021年12月 N2 · 受験者提供資料・録音','writtenCount':71,'ready':True,'validationIssues':[],
        'audio':{'url':'/exams/assets/n2-202112-recording.mp3','durationSeconds':2602.925,
                 'kind':'受験者提供録音（TTSではありません）','sourceFile':'Nghe N2 T12-2021 Ver 2.0 (Yuuki Bùi).mp3',
                 'sourceUrl':'https://drive.google.com/file/d/1BKN6K_2Nj8fOvXdHSAp79jFDnTmNsHeJ/view',
                 'adaptation':'全長を保持。モノラルMP3 64kbpsに変換。冒頭案内・問題間の解答時間を追加/削除しない。'},
        'sourceFiles':['Đề N2 T12-2021 Mark.pdf','Nghe N2 T12-2021 Ver 2.0 (Yuuki Bùi).mp3','Dap-anScript-N2-12-2021.pdf'],
        'provenanceNote':'사용자가 제공한 2021.12 비공식 재편집 기출자료 기반 개인 응시 화면. 기관 공식 배포 원본이 아니다. 원자료의 명백한 오탈자를 교정했으며 문법37·배열43·47은 지문/별표 기준으로 정답표와 다른 정답을 적용했다. sourcePages는 PDF 뷰어의 실제 페이지 순서다.',
        'questions':questions}
    raw=json.dumps(config,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    html=(ROOT/'quiz_templates/past_exam_template.html').read_text(encoding='utf-8')
    html=html.replace('__TITLE__',config['title']).replace('__EXAM_DATA__',raw).replace('__AUDIO_DURATION__','43分23秒')
    html=html.replace('2023年 第1回（7月）','2021年 第2回（12月）')
    html=html.replace('__SOURCE_NOTE__','受験者提供の再編集問題・録音を使用した個人学習用です。公式配布版ではありません。誤植と解答表の不一致は問題文・★の位置に照らして校正しました。原資料ページはPDFビューアーのページ順です。')
    html=html.replace('past-exam-runtime.js?v=reference-score-v1','past-exam-runtime.js?v=202112-v1')
    for p in [ROOT/'quiz_sites/n2-past-exam-202112-mock.html',OUT/'n2-past-exam-202112-mock.html']:p.write_text(html,encoding='utf-8')
    (ROOT/'database/past_exams/2021_12_exam.json').write_text(json.dumps(config,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Built 101 questions; structural check passed; source/answer corrections retained.')

if __name__=='__main__':main()
