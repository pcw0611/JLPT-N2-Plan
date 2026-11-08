"""Build the July 2023 paper with the shared Mincho/paper runner.

The user's PDF and recording are inputs; references/ is never modified.
No study data is written by this builder.
"""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pykakasi import kakasi

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'jlpt-calendar-site/public/exams'
SOURCE_PDF = Path('C:/Users/pcw06/Downloads/Đề N2 T7-2023 (230710).pdf')
SOURCE_AUDIO = Path('C:/Users/pcw06/Downloads/Nghe N2 T7-2023 Bản chuẩn Yuuki Bui.mp3')
KAKASI = kakasi()
TYPE_IDS = ['kanji_reading', 'kanji_orthography', 'word_formation', 'context_definition',
            'paraphrase', 'word_usage', 'grammar_form', 'sentence_composition',
            'text_grammar', 'short_content', 'medium_content', 'integrated_comprehension',
            'thematic_comprehension', 'information_retrieval', 'listening_task',
            'listening_point', 'listening_summary', 'listening_quick_response', 'listening_integrated']
RANGES = [(1,5),(6,10),(11,13),(14,20),(21,25),(26,30),(31,42),(43,47),(48,51),
          (52,56),(57,64),(65,66),(67,69),(70,71),(72,76),(77,82),(83,87),(88,98),(99,101)]
ALLOWED = {'ruby','rt','rp','u','b','strong','em','sup','sub','p','br','div','span','table',
           'thead','tbody','tr','th','td','caption','ul','ol','li','h3','h4'}

class Annotator(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.output, self.ruby_depth = [], 0
    def handle_starttag(self, tag, attrs):
        if tag not in ALLOWED:
            raise ValueError(f'Unexpected HTML tag: {tag}')
        for name, value in attrs:
            if name not in ('class', 'colspan', 'rowspan', 'scope'):
                raise ValueError(f'Unexpected attribute: {name}')
        self.output.append('<'+tag+''.join(f' {k}="{escape(v or "", quote=True)}"' for k,v in attrs)+'>')
        if tag == 'ruby': self.ruby_depth += 1
    def handle_endtag(self, tag):
        if tag not in ALLOWED: raise ValueError(tag)
        self.output.append(f'</{tag}>')
        if tag == 'ruby': self.ruby_depth -= 1
    def handle_data(self, data):
        if self.ruby_depth:
            self.output.append(escape(data)); return
        for token in KAKASI.convert(data):
            original, reading = token['orig'], token['hira']
            self.output.append(f'<ruby>{escape(original)}<rt>{escape(reading)}</rt></ruby>'
                               if re.search('[一-龯々]', original) and original != reading else escape(original))

def annotate(text):
    p=Annotator(); p.feed(text or ''); p.close(); return ''.join(p.output)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--audio',action='store_true');args=parser.parse_args()
    complete_path=ROOT/'scripts/n2_202307_complete_audio_timeline.json'
    complete=json.loads(complete_path.read_text(encoding='utf-8')) if complete_path.exists() else None
    questions=[]
    for part in ['written','reading','listening']:
        questions.extend(json.loads((ROOT/f'scripts/n2_202307_{part}.json').read_text(encoding='utf-8')))
    assert [q['id'] for q in questions] == list(range(1,102))
    for q in questions:
        assert len(q['choices']) in (3,4) and 0 <= q['answer'] < len(q['choices']), q['id']
        assert q['sourcePages'] and q['prompt'] and q['instruction'], q['id']
        q['itemTypeId']=next(t for (a,b),t in zip(RANGES,TYPE_IDS) if a<=q['id']<=b)
        if q.get('passage'):
            q['passageId']=hashlib.sha256(q['passage'].encode('utf-8')).hexdigest()[:12]
        for field in ['translation','reason','trap','contrast','exampleJa','exampleKo']:
            assert q['explanation'].get(field), (q['id'],field)
        if q.get('order'):
            assert sorted(q['order'])==[1,2,3,4]
            assert q['order'][q.get('starSlot',3)-1]-1==q['answer'],q['id']
        if q['explanation'].get('passageTranslation'):
            q['explanation']['translation']=q['explanation']['passageTranslation']+'\n\n'+q['explanation']['translation']
        for field in ['instruction','passage','prompt']:
            assert not re.search('[가-힣]',q.get(field,'')), (q['id'],field)
            annotate(q.get(field,''))  # Reject unsafe markup in original display as well.
        assert not any(re.search('[가-힣]',c) for c in q['choices']),q['id']
        q['reviewPassage']=annotate(q.get('passage',''))
        q['reviewPrompt']=annotate(q['prompt'])
        q['reviewChoices']=[annotate(c) for c in q['choices']]
        q['reviewExample']=annotate(q['explanation']['exampleJa'])
        if q.get('transcript'):q['reviewTranscript']=annotate(q['transcript'])
    if complete:
        # The supplied shorter MP3 is retained untouched. The attributed recording fills its missing item.
        for q in questions:
            if q.get('missingAudio'):
                q['missingAudio']=False
                q['validationStatus']='supplement_recording_cross_checked'
                q['sourceNotes'].append('누락된 녹음은 Ánh sensei의 2023년7월 녹음에서 확인하여 보완함. 배포 시험은 보완 녹음의 0~2533.0초를 사용함.')
    issues=[{'id':q['id'],'status':q.get('validationStatus'),'missingAudio':q.get('missingAudio',False)}
            for q in questions if q.get('validationStatus')=='uncertain' or q.get('missingAudio')]
    config={'id':'n2-past-202307','version':2,'title':'2023年7月 JLPT N2 実戦模試',
            'writtenCount':71,'ready':not issues,'validationIssues':issues,
            'audio':{'url':'/exams/assets/n2-202307-recording.mp3','durationSeconds':2533.0 if complete else 2254.5,
                     'kind':'録音（TTSではありません）',
                     'sourceUrl':'https://www.youtube.com/watch?v=akPmket15m0',
                     'attribution':'Ánh sensei — Choukai JLPT N2 7/2023 (Question and Answer)',
                     'license':'Uploader labels this video Creative Commons Attribution (reuse allowed)',
                     'adaptation':'Audio only, 0–2533.0s (answer-screen/outro excluded), MP3 80kbps'},
            'sourceFiles':[SOURCE_PDF.name,SOURCE_AUDIO.name],
            'provenanceNote':'사용자가 제공한 비공식 재편집 문제지와 교차 대조한 녹음에 기반한 개인 학습용 응시 화면. 사용자 MP3의 누락 문항은 Ánh sensei 게시 녹음으로 보완. 기관 공인 또는 공식 배포 원본으로 표시하지 않음.',
            'questions':questions}
    raw=json.dumps(config,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    html=(ROOT/'quiz_templates/past_exam_template.html').read_text(encoding='utf-8').replace('__TITLE__',config['title']).replace('__EXAM_DATA__',raw)
    source_note='問題：受験者提供PDF（Yuuki Bùi編集）。公式配布版ではありません。原文の順序・振り仮名を保持。'
    if complete:
        source_note+=' 録音：<a href="https://www.youtube.com/watch?v=akPmket15m0" target="_blank" rel="noopener">Ánh sensei — Choukai JLPT N2 7/2023</a>（投稿者表示：<a href="https://creativecommons.org/licenses/by/3.0/" target="_blank" rel="noopener">CC BY</a>）。音声のみ、解答発表前までを使用・配信用MP3に圧縮。'
    html=html.replace('__AUDIO_DURATION__','42分13秒' if complete else '約38分').replace('__SOURCE_NOTE__',source_note)
    OUT.mkdir(parents=True,exist_ok=True)
    for path in [ROOT/'quiz_sites/n2-past-exam-202307-mock.html', OUT/'n2-past-exam-202307-mock.html']:
        path.write_text(html,encoding='utf-8')
    (ROOT/'database/past_exams/2023_07_exam.json').write_text(json.dumps(config,ensure_ascii=False,indent=2),encoding='utf-8')
    if args.audio:
        target=OUT/'assets/n2-202307-recording.mp3';target.parent.mkdir(parents=True,exist_ok=True)
        source=ROOT/'tmp/exam202307/youtube-akPmket15m0.webm' if complete else SOURCE_AUDIO
        command=['ffmpeg','-v','error','-y','-i',str(source)]
        if complete:command+=['-t','2533.0']
        subprocess.run(command+['-map_metadata','-1','-c:a','libmp3lame','-b:a','80k',str(target)],check=True)
        assert target.stat().st_size<25*1024*1024
    print(f'Built {len(questions)} questions; readiness={config["ready"]}; unresolved={issues}')

if __name__=='__main__':main()
