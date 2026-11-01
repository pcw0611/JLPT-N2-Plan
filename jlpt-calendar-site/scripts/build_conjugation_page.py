"""Build the existing conjugation content into the calendar's standalone study page."""
from pathlib import Path
import re

SITE = Path(__file__).resolve().parents[1]
SOURCE = SITE / 'content' / 'conjugation-lab.html'
TARGET = SITE / 'public' / 'learn' / 'conjugation.html'


def build():
    fragment = SOURCE.read_text(encoding='utf-8')
    fragment = re.sub(r'<style>[\s\S]*?</style>', '', fragment, count=1)
    fragment = fragment.replace('<h2>활용형 실험실</h2>', '''<header class="lab-hero">
      <div class="lab-heading"><p class="eyebrow">KATSUYO LAB · N2 FOUNDATION</p>
      <h2>활용형 학습실</h2><p class="lab-description">모양을 바꾸고, 문장을 풀고, 내 것으로.</p></div>
      <div class="hero-example" aria-hidden="true"><span>読む</span><span class="hero-arrow">→</span><strong>読める</strong><small>읽다 · 읽을 수 있다</small></div>
    </header>''')
    fragment = fragment.replace('>활용 지도</button>', '>01 <span>변화 보기</span></button>')
    fragment = fragment.replace('>문장 분해기</button>', '>02 <span>표현 분해</span></button>')
    fragment = fragment.replace('>적용 훈련</button>', '>03 <span>적용 훈련</span></button>')
    fragment = fragment.replace('<section id="kl-map" class="stack">', '''<section id="kl-map" class="stack lab-panel">
      <div class="panel-heading"><p class="eyebrow">EXPLORE</p><h3>끝부분만 바뀌는 이유를 찾아봐요.</h3><p>단어와 활용을 고르면 바뀐 부분에 밑줄이 표시돼요.</p></div>''')
    fragment = fragment.replace('<section id="kl-chain" class="stack" hidden>', '''<section id="kl-chain" class="stack lab-panel" hidden>
      <div class="panel-heading"><p class="eyebrow">UNPACK</p><h3>길어 보여도, 한 단계씩.</h3><p>‘다음 단계’를 누르며 형태와 의미가 어떻게 쌓이는지 살펴봐요.</p></div>''')
    fragment = fragment.replace('<section id="kl-train" class="stack" hidden lang="ja">', '<section id="kl-train" class="stack lab-panel" hidden lang="ja">')
    start = fragment.index('function persist(){')
    end = fragment.index('\nfunction useSaved', start)
    fragment = fragment[:start] + '''function persist(){try{localStorage.setItem('jlpt-conjugation-lab-v1',JSON.stringify(state))}catch{}}
''' + fragment[end:]
    fragment = fragment.replace('useSaved(window.openai?.widgetState);', "try{useSaved({privateContent:JSON.parse(localStorage.getItem('jlpt-conjugation-lab-v1')||'null')})}catch{}")
    fragment = fragment.replace("function paintMode(){", "function paintMode(){root.classList.toggle('is-testing',!!(state.exam&&!state.exam.done));")
    fragment = fragment.replace("{map:'활용 지도',chain:'문장 분해기',train:'적용 훈련'}", "{map:'01  변화 보기',chain:'02  표현 분해',train:'03  적용 훈련'}")
    fragment = fragment.replace("'활용형 실험실'", "'활용형 학습실'")
    fragment = fragment.replace("$('forms').querySelectorAll('button').forEach", "$('map').querySelector('details').hidden=!state.help;$('forms').querySelectorAll('button').forEach")
    fragment = fragment.replace('ある는 뜻에 맞는 형태를 골라 쓴다. 이 지도는 형태 규칙을 보여 주며, 가능·수동·사역처럼 단독으로 자연스럽게 쓰이지 않는 형태도 있다. 존재의 가능성은 문맥에 따라 あり得る 등으로 표현한다.', 'ある의 부정은 ない. 이 지도에서는 자주 쓰는 다섯 형태만 보여 줘요.')
    fragment = fragment.replace('학습 원장에는 아직 기록하지 않았어요. 재도전은 같은 문항이므로 독립적인 실력 측정과 구분해요.', '결과는 이 기기에 보관돼요. 캘린더 기록에 반영하려면 기록용 결과를 복사해 채팅에 보내 주세요. 재도전은 같은 문항의 반복 연습이에요.')
    fragment = re.sub(r"window.addEventListener\('openai:set_globals',[^\n]*\);", '', fragment)
    assert 'window.openai' not in fragment
    # Restore the saved elapsed time anchor after leaving/reloading a running session.
    # The timer deliberately remains wall-clock time from 開始する until submission.
    html = '''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="JLPT 활용형 학습실. 동사·형용사 변화를 살펴보고 긴 표현을 분해한 뒤 선택형 훈련으로 확인하세요.">
<meta name="theme-color" content="#0d0f0e"><title>활용형 학습실 · JLPT N2 PLAN</title>
<link rel="stylesheet" href="/learn/conjugation.css"><script src="/auth-gate.js"></script></head>
<body><main class="lab-shell"><nav class="lab-topbar" aria-label="ページナビゲーション"><a class="lab-brand" href="/">JLPT N2 <span>PLAN</span></a><a class="back-link" href="/">← 学習カレンダー</a></nav>
''' + fragment + '''
<footer class="lab-footer"><span>JLPT N2 PLAN · 活用トレーニング</span><a href="/">学習カレンダーへ戻る ↗</a></footer></main></body></html>
'''
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(html, encoding='utf-8')
    print(f'Built {TARGET.relative_to(SITE)}')


if __name__ == '__main__':
    build()
