# -*- coding: utf-8 -*-
"""
JLPT N2 03 동사 활용 덱 생성 및 Anki 반영 스크립트
총 118장:
- 1그룹 vs 2그룹 판별 (예외 포함): 12장
- 1그룹 て형/た형 음편 집중 훈련: 16장
- ない형 특수/규칙 (う->わ): 8장
- 가능형 (생성 & 역방향): 12장
- 수동형 (생성 & 역방향): 12장
- 사역형 (생성 & 역방향): 12장
- 사역수동형 (단축형 포함): 14장
- 의향형 & 명령형: 12장
- 가정형 (ば형): 10장
- 종합 핵심 동사 관통 마스터: 10장
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ENDPOINT = "http://127.0.0.1:3141/"
DECK_NAME = "JLPT N2::03 동사 활용"
MODEL = "Basic"
OUTPUT_FILE = Path(__file__).resolve().parent.parent / "outputs" / "anki" / "jlpt-n2-verb-conjugations-118cards.txt"

CSS_BLOCK = """<style>
.vt-wrap { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; text-align: left; max-width: 520px; margin: 0 auto; box-sizing: border-box; }
.vt-center { text-align: center; }
.vt-title { font-size: 28px; font-weight: 700; margin: 14px 0; color: #f8fafc; }
.vt-sub { font-size: 16px; color: #cbd5e1; }
.vt-badge { display: inline-block; font-size: 13px; font-weight: 700; border-radius: 14px; padding: 4px 12px; margin-bottom: 8px; }
.vt-badge-gen { color: #34d399; background: rgba(16, 185, 129, 0.18); border: 1px solid rgba(52, 211, 153, 0.45); }
.vt-badge-rev { color: #60a5fa; background: rgba(59, 130, 246, 0.18); border: 1px solid rgba(96, 165, 250, 0.45); }
.vt-badge-grp { color: #fbbf24; background: rgba(245, 158, 11, 0.18); border: 1px solid rgba(251, 191, 36, 0.45); }
.vt-badge-comp { color: #c084fc; background: rgba(192, 132, 252, 0.18); border: 1px solid rgba(192, 132, 252, 0.45); }
.vt-highlight-green { color: #34d399; font-weight: 700; }
.vt-highlight-blue { color: #60a5fa; font-weight: 700; }
.vt-highlight-amber { color: #fbbf24; font-weight: 700; }
.vt-ans-head { font-size: 24px; font-weight: 700; color: #34d399; margin-bottom: 12px; text-align: center; }
.vt-ans-head-blue { font-size: 24px; font-weight: 700; color: #60a5fa; margin-bottom: 12px; text-align: center; }
.vt-sec { border-left: 4px solid #10b981; background: rgba(16, 185, 129, 0.08); border-radius: 0 8px 8px 0; padding: 12px 14px; margin-bottom: 14px; }
.vt-sec-blue { border-left: 4px solid #3b82f6; background: rgba(59, 130, 246, 0.08); border-radius: 0 8px 8px 0; padding: 12px 14px; margin-bottom: 14px; }
.vt-meaning { font-size: 16px; font-weight: 600; color: #f1f5f9; margin: 4px 0; }
.vt-rule-box { background: #27272a; border: 1px solid #3f3f46; border-radius: 8px; padding: 12px 14px; margin-top: 10px; }
.vt-rule-title { font-weight: 700; font-size: 14.5px; color: #f8fafc; margin-bottom: 4px; }
.vt-rule-content { font-size: 13px; color: #cbd5e1; margin-top: 4px; line-height: 1.5; }
.vt-ex-ja { font-size: 15px; color: #f8fafc; margin-top: 8px; }
.vt-ex-ko { font-size: 13.5px; color: #94a3b8; margin-top: 2px; }
.vt-tag { color: #64748b; font-weight: 700; }

html:not(.nightMode):not(.night_mode) body:not(.nightMode):not(.night_mode) .vt-title { color: #111827; }
html:not(.nightMode):not(.night_mode) body:not(.nightMode):not(.night_mode) .vt-sub { color: #4b5563; }
html:not(.nightMode):not(.night_mode) body:not(.nightMode):not(.night_mode) .vt-ans-head { color: #059669; }
html:not(.nightMode):not(.night_mode) body:not(.nightMode):not(.night_mode) .vt-ans-head-blue { color: #2563eb; }
html:not(.nightMode):not(.night_mode) body:not(.nightMode):not(.night_mode) .vt-highlight-green { color: #059669; }
html:not(.nightMode):not(.night_mode) body:not(.nightMode):not(.night_mode) .vt-highlight-blue { color: #2563eb; }
html:not(.nightMode):not(.night_mode) body:not(.nightMode):not(.night_mode) .vt-highlight-amber { color: #b45309; }
html:not(.nightMode):not(.night_mode) body:not(.nightMode):not(.night_mode) .vt-sec { background: #f0fdf4; border-left-color: #059669; }
html:not(.nightMode):not(.night_mode) body:not(.nightMode):not(.night_mode) .vt-sec-blue { background: #eff6ff; border-left-color: #2563eb; }
html:not(.nightMode):not(.night_mode) body:not(.nightMode):not(.night_mode) .vt-meaning { color: #1f2937; }
html:not(.nightMode):not(.night_mode) body:not(.nightMode):not(.night_mode) .vt-rule-box { background: #f8fafc; border-color: #e2e8f0; }
html:not(.nightMode):not(.night_mode) body:not(.nightMode):not(.night_mode) .vt-rule-title { color: #0f172a; }
html:not(.nightMode):not(.night_mode) body:not(.nightMode):not(.night_mode) .vt-rule-content { color: #475569; }
html:not(.nightMode):not(.night_mode) body:not(.nightMode):not(.night_mode) .vt-ex-ja { color: #1f2937; }
html:not(.nightMode):not(.night_mode) body:not(.nightMode):not(.night_mode) .vt-ex-ko { color: #64748b; }
html:not(.nightMode):not(.night_mode) body:not(.nightMode):not(.night_mode) .vt-tag { color: #475569; }
</style>"""

CARDS_DATA = [
    # -------------------------------------------------------------------------
    # 1. 동사 그룹 판별 (1그룹 vs 2그룹) - 예외 1그룹 집중 (12장)
    # -------------------------------------------------------------------------
    {
        "cat": "그룹판별",
        "badge": ("vt-badge-grp", "동사 그룹 판별 (1그룹 vs 2그룹) #01"),
        "q_title": "帰る（かえる）",
        "q_sub": "이 동사는 몇 그룹 동사인가? (ます형/ない형은?)",
        "a_head": "1그룹 동사 (예외)",
        "a_sub": "겉모습은 える(2그룹) 같지만 대표적인 1그룹 예외 동사!",
        "sec_class": "vt-sec",
        "meaning": "돌아가다 / 돌아오다",
        "rule_title": "📌 1그룹 활용 확인",
        "rule_content": "• ます형: <b>帰ります</b> (かえります)<br>• ない형: <b>帰らない</b> (かえらない)<br>• て형/た형: <b>帰って / 帰った</b><br>• 가능형: <b>帰れる</b> / 의향형: <b>帰ろう</b>",
        "ex_ja": "用事を済ませて、急いで家に帰った。",
        "ex_ko": "볼일을 마치고 서둘러 집으로 돌아갔다.",
        "tags": ["JLPT_N2", "동사활용", "그룹판별", "1그룹예외"]
    },
    {
        "cat": "그룹판별",
        "badge": ("vt-badge-grp", "동사 그룹 판별 (1그룹 vs 2그룹) #02"),
        "q_title": "入る（はいる）",
        "q_sub": "이 동사는 몇 그룹 동사인가? (ます형/ない형은?)",
        "a_head": "1그룹 동사 (예외)",
        "a_sub": "어미가 いる 형태지만 1그룹으로 활용합니다.",
        "sec_class": "vt-sec",
        "meaning": "들어가다 / 들어오다",
        "rule_title": "📌 1그룹 활용 확인",
        "rule_content": "• ます형: <b>入ります</b> (はいります)<br>• ない형: <b>入らない</b> (はいらない)<br>• て형/た형: <b>入って / 入った</b><br>• 가능형: <b>入れる</b> (はいれる)",
        "ex_ja": "靴を脱いで部屋に入ってください。",
        "ex_ko": "신발을 벗고 방에 들어가세요.",
        "tags": ["JLPT_N2", "동사활용", "그룹판별", "1그룹예외"]
    },
    {
        "cat": "그룹판별",
        "badge": ("vt-badge-grp", "동사 그룹 판별 (1그룹 vs 2그룹) #03"),
        "q_title": "走る（はしる）",
        "q_sub": "이 동사는 몇 그룹 동사인가? (ます형/ない형은?)",
        "a_head": "1그룹 동사 (예외)",
        "a_sub": "어미가 いる 형태지만 1그룹으로 활용합니다.",
        "sec_class": "vt-sec",
        "meaning": "달리다",
        "rule_title": "📌 1그룹 활용 확인",
        "rule_content": "• ます형: <b>走ります</b> (はしります)<br>• ない형: <b>走らない</b> (はしらない)<br>• て형/た형: <b>走って / 走った</b><br>• 사역형: <b>走らせる</b> (はしらせる)",
        "ex_ja": "毎朝公園の周りを軽く走っている。",
        "ex_ko": "매일 아침 공원 주변을 가볍게 달리고 있다.",
        "tags": ["JLPT_N2", "동사활용", "그룹판별", "1그룹예외"]
    },
    {
        "cat": "그룹판별",
        "badge": ("vt-badge-grp", "동사 그룹 판별 (1그룹 vs 2그룹) #04"),
        "q_title": "切る（きる）",
        "q_sub": "이 동사는 몇 그룹 동사인가? (着る와의 차이는?)",
        "a_head": "1그룹 동사 (예외)",
        "a_sub": "切る(자르다)는 1그룹! 반면 着る(입다)는 2그룹!",
        "sec_class": "vt-sec",
        "meaning": "자르다 / 끊다",
        "rule_title": "📌 切る vs 着る 비교",
        "rule_content": "• 切る (1그룹): <b>切ります / 切らない / 切って / 切った</b><br>• 着る (2그룹): <b>着ます / 着ない / 着て / 着た</b>",
        "ex_ja": "ハサミで紙をきれいに切った。",
        "ex_ko": "가위로 종이를 깨끗하게 잘랐다.",
        "tags": ["JLPT_N2", "동사활용", "그룹판별", "1그룹예외"]
    },
    {
        "cat": "그룹판별",
        "badge": ("vt-badge-grp", "동사 그룹 판별 (1그룹 vs 2그룹) #05"),
        "q_title": "知る（しる）",
        "q_sub": "이 동사는 몇 그룹 동사인가? (ない형은?)",
        "a_head": "1그룹 동사 (예외)",
        "a_sub": "어미가 いる 형태지만 1그룹으로 활용합니다.",
        "sec_class": "vt-sec",
        "meaning": "알다",
        "rule_title": "📌 1그룹 활용 확인",
        "rule_content": "• ます형: <b>知ります</b><br>• ない형: <b>知らない</b> (しらない)<br>• て형: <b>知って</b> (현재 상태: 知っている)<br>• 가능형: <b>知れる</b>",
        "ex_ja": "そのニュースの真相はまだ誰も知らない。",
        "ex_ko": "그 뉴스의 진상은 아직 아무도 모른다.",
        "tags": ["JLPT_N2", "동사활용", "그룹판별", "1그룹예외"]
    },
    {
        "cat": "그룹판별",
        "badge": ("vt-badge-grp", "동사 그룹 판별 (1그룹 vs 2그룹) #06"),
        "q_title": "要る（いる）",
        "q_sub": "이 동사는 몇 그룹 동사인가? (居る와의 차이는?)",
        "a_head": "1그룹 동사 (예외)",
        "a_sub": "要る(필요하다)는 1그룹! 반면 居る(있다)는 2그룹!",
        "sec_class": "vt-sec",
        "meaning": "필요하다",
        "rule_title": "📌 要る vs 居る 비교",
        "rule_content": "• 要る (1그룹): <b>要ります / 要らない / 要って</b><br>• 居る (2그룹): <b>居ます / 居ない / 居て</b>",
        "ex_ja": "旅行にはパスポートが絶対に要る。",
        "ex_ko": "여행에는 여권이 절대로 필요하다.",
        "tags": ["JLPT_N2", "동사활용", "그룹판별", "1그룹예외"]
    },
    {
        "cat": "그룹판별",
        "badge": ("vt-badge-grp", "동사 그룹 판별 (1그룹 vs 2그룹) #07"),
        "q_title": "滑る（すべる）",
        "q_sub": "이 동사는 몇 그룹 동사인가? (て형은?)",
        "a_head": "1그룹 동사 (예외)",
        "a_sub": "어미가 える 형태지만 1그룹으로 활용합니다.",
        "sec_class": "vt-sec",
        "meaning": "미끄러지다",
        "rule_title": "📌 1그룹 활용 확인",
        "rule_content": "• ます형: <b>滑ります</b><br>• ない형: <b>滑らない</b><br>• て형/た형: <b>滑って / 滑った</b> (촉음편!)",
        "ex_ja": "雪道で足が滑って転んでしまった。",
        "ex_ko": "눈길에서 발이 미끄러져 넘어지고 말았다.",
        "tags": ["JLPT_N2", "동사활용", "그룹판별", "1그룹예외"]
    },
    {
        "cat": "그룹판별",
        "badge": ("vt-badge-grp", "동사 그룹 판별 (1그룹 vs 2그룹) #08"),
        "q_title": "減る（へる）",
        "q_sub": "이 동사는 몇 그룹 동사인가? (ます형/ない형은?)",
        "a_head": "1그룹 동사 (예외)",
        "a_sub": "어미가 える 형태지만 1그룹으로 활용합니다.",
        "sec_class": "vt-sec",
        "meaning": "줄다 / 감소하다",
        "rule_title": "📌 1그룹 활용 확인",
        "rule_content": "• ます형: <b>減ります</b><br>• ない형: <b>減らない</b><br>• て형/た형: <b>減って / 減った</b>",
        "ex_ja": "不景気で会社の売上が大幅に減った。",
        "ex_ko": "불경기로 회사의 매출이 대폭 줄었다.",
        "tags": ["JLPT_N2", "동사활용", "그룹판별", "1그룹예외"]
    },
    {
        "cat": "그룹판별",
        "badge": ("vt-badge-grp", "동사 그룹 판별 (1그룹 vs 2그룹) #09"),
        "q_title": "喋る（しゃべる）",
        "q_sub": "이 동사는 몇 그룹 동사인가? (て형은?)",
        "a_head": "1그룹 동사 (예외)",
        "a_sub": "어미가 える 형태지만 1그룹으로 활용합니다.",
        "sec_class": "vt-sec",
        "meaning": "수다 떨다 / 말하다",
        "rule_title": "📌 1그룹 활용 확인",
        "rule_content": "• ます형: <b>喋ります</b><br>• ない형: <b>喋らない</b><br>• て형/た형: <b>喋って / 喋った</b>",
        "ex_ja": "授業中に隣の席の人と喋ってはいけない。",
        "ex_ko": "수업 중에 옆자리 사람과 수다를 떨어서는 안 된다.",
        "tags": ["JLPT_N2", "동사활용", "그룹판별", "1그룹예외"]
    },
    {
        "cat": "그룹판별",
        "badge": ("vt-badge-grp", "동사 그룹 판별 (1그룹 vs 2그룹) #10"),
        "q_title": "限る（かぎる）",
        "q_sub": "이 동사는 몇 그룹 동사인가? (ば형/ない형은?)",
        "a_head": "1그룹 동사 (예외)",
        "a_sub": "N2 필수 문형 〜にかぎる, 〜とはかぎらない의 1그룹 동사!",
        "sec_class": "vt-sec",
        "meaning": "한하다 / 제한하다",
        "rule_title": "📌 1그룹 활용 확인",
        "rule_content": "• ます형: <b>限ります</b><br>• ない형: <b>限らない</b> (〜とは限らない)<br>• ば형: <b>限れば</b> (〜に限れば)",
        "ex_ja": "高い店が必ずしも美味しいとは限らない。",
        "ex_ko": "비싼 가게가 반드시 맛있다고는 볼 수 없다(한정할 수 없다).",
        "tags": ["JLPT_N2", "동사활용", "그룹판별", "1그룹예외"]
    },
    {
        "cat": "그룹판별",
        "badge": ("vt-badge-grp", "동사 그룹 판별 (1그룹 vs 2그룹) #11"),
        "q_title": "着る（きる）",
        "q_sub": "이 동사는 몇 그룹 동사인가? (切る와의 차이는?)",
        "a_head": "2그룹 동사 (상1단)",
        "a_sub": "着る(입다)는 2그룹! 어미 る가 탈락하며 활용합니다.",
        "sec_class": "vt-sec",
        "meaning": "입다 (옷을)",
        "rule_title": "📌 2그룹 활용 확인",
        "rule_content": "• ます형: <b>着ます</b><br>• ない형: <b>着ない</b><br>• て형/た형: <b>着て / 着た</b> (촉음편 없음!)",
        "ex_ja": "寒いので厚いコートを着て出かけた。",
        "ex_ko": "날씨가 추워서 두꺼운 코트를 입고 외출했다.",
        "tags": ["JLPT_N2", "동사활용", "그룹판별", "2그룹"]
    },
    {
        "cat": "그룹판별",
        "badge": ("vt-badge-grp", "동사 그룹 판별 (1그룹 vs 2그룹) #12"),
        "q_title": "見る（みる）",
        "q_sub": "이 동사는 몇 그룹 동사인가? (가능/수동형은?)",
        "a_head": "2그룹 동사 (상1단)",
        "a_sub": "어간 見에 2그룹 어미가 결합합니다.",
        "sec_class": "vt-sec",
        "meaning": "보다",
        "rule_title": "📌 2그룹 활용 확인",
        "rule_content": "• ます형: <b>見ます</b> / ない형: <b>見ない</b><br>• て형/た형: <b>見て / 見た</b><br>• 가능/수동: <b>見られる</b> (구어 가능형: 見れる)",
        "ex_ja": "毎晩寝る前に好きなアニメを見ている。",
        "ex_ko": "매일 밤 자기 전에 좋아하는 애니메이션을 보고 있다.",
        "tags": ["JLPT_N2", "동사활용", "그룹판별", "2그룹"]
    },

    # -------------------------------------------------------------------------
    # 2. 1그룹 て형/た형 음편(音便) 집중 훈련 (16장)
    # -------------------------------------------------------------------------
    {
        "cat": "음편훈련",
        "badge": ("vt-badge-gen", "1그룹 음편 훈련 (う ➔ って) #01"),
        "q_title": "買う（かう） → て形 / た形",
        "q_sub": "어미가 「う」로 끝나는 1그룹 동사의 음편 형태는?",
        "a_head": "買って / 買った",
        "a_sub": "촉음편: [う・つ・る] ➔ って / った",
        "sec_class": "vt-sec",
        "meaning": "사다",
        "rule_title": "📌 촉음편(促音便) 규칙",
        "rule_content": "어미가 <b>う・つ・る</b>로 끝나는 1그룹 동사는 작은 っ로 바뀌어 <b>って / った</b>가 됩니다.",
        "ex_ja": "スーパーで新鮮な果物を買って帰った。",
        "ex_ko": "마트에서 신선한 과일을 사서 돌아왔다.",
        "tags": ["JLPT_N2", "동사활용", "음편", "촉음편"]
    },
    {
        "cat": "음편훈련",
        "badge": ("vt-badge-gen", "1그룹 음편 훈련 (つ ➔ って) #02"),
        "q_title": "待つ（まつ） → て形 / た形",
        "q_sub": "어미가 「つ」로 끝나는 1그룹 동사의 음편 형태는?",
        "a_head": "待って / 待った",
        "a_sub": "촉음편: [う・つ・る] ➔ って / った",
        "sec_class": "vt-sec",
        "meaning": "기다리다",
        "rule_title": "📌 촉음편(促音便) 규칙",
        "rule_content": "待つ ➔ <b>待って / 待った</b> (まて+っ+て)",
        "ex_ja": "駅の改札口で友達を30分も待った。",
        "ex_ko": "역 개찰구에서 친구를 30분이나 기다렸다.",
        "tags": ["JLPT_N2", "동사활용", "음편", "촉음편"]
    },
    {
        "cat": "음편훈련",
        "badge": ("vt-badge-gen", "1그룹 음편 훈련 (る ➔ って) #03"),
        "q_title": "取る（とる） → て形 / た形",
        "q_sub": "어미가 「る」로 끝나는 1그룹 동사의 음편 형태는?",
        "a_head": "取って / 取った",
        "a_sub": "촉음편: [う・つ・る] ➔ って / った",
        "sec_class": "vt-sec",
        "meaning": "집다 / 취하다 / 받다",
        "rule_title": "📌 촉음편(促音便) 규칙",
        "rule_content": "1그룹 동사 어미 <b>る</b>는 <b>って / った</b>가 됩니다. (※ 2그룹 食べる는 食べて)",
        "ex_ja": "棚の上から辞書を取って調べた。",
        "ex_ko": "선반 위에서 사전을 꺼내어(집어서) 찾아보았다.",
        "tags": ["JLPT_N2", "동사활용", "음편", "촉음편"]
    },
    {
        "cat": "음편훈련",
        "badge": ("vt-badge-gen", "1그룹 음편 훈련 (む ➔ んで) #04"),
        "q_title": "読む（よむ） → て形 / た形",
        "q_sub": "어미가 「む」로 끝나는 1그룹 동사의 음편 형태는?",
        "a_head": "読んで / 読んだ",
        "a_sub": "발음편(탁음): [む・ぶ・ぬ] ➔ んで / んだ",
        "sec_class": "vt-sec",
        "meaning": "읽다",
        "rule_title": "📌 발음편(撥音便) 규칙",
        "rule_content": "어미가 <b>む・ぶ・ぬ</b>로 끝나는 1그룹 동사는 ん로 바뀌며 탁음이 붙어 <b>んで / んだ</b>가 됩니다.",
        "ex_ja": "説明書をよく読んでから組み立ててください。",
        "ex_ko": "설명서를 잘 읽고 나서 조립해 주세요.",
        "tags": ["JLPT_N2", "동사활용", "음편", "발음편"]
    },
    {
        "cat": "음편훈련",
        "badge": ("vt-badge-gen", "1그룹 음편 훈련 (ぶ ➔ んで) #05"),
        "q_title": "遊ぶ（あそぶ） → て形 / た形",
        "q_sub": "어미가 「ぶ」로 끝나는 1그룹 동사의 음편 형태는?",
        "a_head": "遊んで / 遊んだ",
        "a_sub": "발음편(탁음): [む・ぶ・ぬ] ➔ んで / んだ",
        "sec_class": "vt-sec",
        "meaning": "놀다",
        "rule_title": "📌 발음편(撥音便) 규칙",
        "rule_content": "遊ぶ ➔ <b>遊んで / 遊んだ</b> (あそ+ん+で)",
        "ex_ja": "休みの日は一日中家でゲームをして遊んだ。",
        "ex_ko": "쉬는 날에는 하루 종일 집에서 게임을 하며 놀았다.",
        "tags": ["JLPT_N2", "동사활용", "음편", "발음편"]
    },
    {
        "cat": "음편훈련",
        "badge": ("vt-badge-gen", "1그룹 음편 훈련 (ぬ ➔ んで) #06"),
        "q_title": "死ぬ（しぬ） → て形 / た形",
        "q_sub": "어미가 「ぬ」로 끝나는 1그룹 동사의 음편 형태는?",
        "a_head": "死んで / 死んだ",
        "a_sub": "발음편(탁음): [む・ぶ・ぬ] ➔ んで / んだ",
        "sec_class": "vt-sec",
        "meaning": "죽다",
        "rule_title": "📌 일본어 유일의 ぬ 어미 동사",
        "rule_content": "현대 일본어에서 어미가 ぬ인 동사는 死ぬ가 유일합니다. ➔ <b>死んで / 死んだ</b>",
        "ex_ja": "草木が枯れて死んでしまった。",
        "ex_ko": "풀과 나무가 말라 죽어 버렸다.",
        "tags": ["JLPT_N2", "동사활용", "음편", "발음편"]
    },
    {
        "cat": "음편훈련",
        "badge": ("vt-badge-gen", "1그룹 음편 훈련 (く ➔ いて) #07"),
        "q_title": "書く（かく） → て形 / た形",
        "q_sub": "어미가 「く」로 끝나는 1그룹 동사의 음편 형태는?",
        "a_head": "書いて / 書いた",
        "a_sub": "이음편: [く] ➔ いて / いた",
        "sec_class": "vt-sec",
        "meaning": "쓰다",
        "rule_title": "📌 이음편(イ音便) 규칙",
        "rule_content": "어미 <b>く</b>는 い로 바뀌어 <b>いて / いた</b>가 됩니다.",
        "ex_ja": "メモ用紙に重要な連絡先を書いておいた。",
        "ex_ko": "메모지에 중요한 연락처를 써 두었다.",
        "tags": ["JLPT_N2", "동사활용", "음편", "이음편"]
    },
    {
        "cat": "음편훈련",
        "badge": ("vt-badge-gen", "1그룹 음편 훈련 (く ➔ いて) #08"),
        "q_title": "咲く（さく） → て形 / た形",
        "q_sub": "어미가 「く」로 끝나는 1그룹 동사의 음편 형태는?",
        "a_head": "咲いて / 咲いた",
        "a_sub": "이음편: [く] ➔ いて / いた",
        "sec_class": "vt-sec",
        "meaning": "피다 (꽃이)",
        "rule_title": "📌 이음편(イ音便) 규칙",
        "rule_content": "咲く ➔ <b>咲いて / 咲いた</b>",
        "ex_ja": "春になって庭の桜の花がきれいに咲いた。",
        "ex_ko": "봄이 되어 정원의 벚꽃이 아름답게 피었다.",
        "tags": ["JLPT_N2", "동사활용", "음편", "이음편"]
    },
    {
        "cat": "음편훈련",
        "badge": ("vt-badge-gen", "1그룹 음편 훈련 (ぐ ➔ いで) #09"),
        "q_title": "泳ぐ（およぐ） → て形 / た形",
        "q_sub": "어미가 「ぐ」로 끝나는 1그룹 동사의 음편 형태는?",
        "a_head": "泳いで / 泳いだ",
        "a_sub": "이음편+탁음: [ぐ] ➔ いで / いだ",
        "sec_class": "vt-sec",
        "meaning": "헤엄치다 / 수영하다",
        "rule_title": "📌 탁음 이음편 규칙",
        "rule_content": "어미 <b>ぐ</b>는 い로 바뀌며 뒤에 탁음이 이어져 <b>いで / いだ</b>가 됩니다.",
        "ex_ja": "海で一日中泳いで、とても疲れた。",
        "ex_ko": "바다에서 하루 종일 수영해서 몹시 지쳤다.",
        "tags": ["JLPT_N2", "동사활용", "음편", "이음편"]
    },
    {
        "cat": "음편훈련",
        "badge": ("vt-badge-gen", "1그룹 음편 훈련 (ぐ ➔ いで) #10"),
        "q_title": "急ぐ（いそぐ） → て形 / た形",
        "q_sub": "어미가 「ぐ」로 끝나는 1그룹 동사의 음편 형태는?",
        "a_head": "急いで / 急いだ",
        "a_sub": "이음편+탁음: [ぐ] ➔ いで / いだ",
        "sec_class": "vt-sec",
        "meaning": "서두르다",
        "rule_title": "📌 탁음 이음편 규칙",
        "rule_content": "急ぐ ➔ <b>急いで / 急いだ</b>",
        "ex_ja": "電車の時間に間に合うように急いで駅へ向かった。",
        "ex_ko": "전철 시간에 늦지 않도록 서둘러 역으로 향했다.",
        "tags": ["JLPT_N2", "동사활용", "음편", "이음편"]
    },
    {
        "cat": "음편훈련",
        "badge": ("vt-badge-gen", "1그룹 음편 훈련 (す ➔ して) #11"),
        "q_title": "話す（はなす） → て形 / た形",
        "q_sub": "어미가 「す」로 끝나는 1그룹 동사의 형태는?",
        "a_head": "話して / 話した",
        "a_sub": "음편 없음: [す] ➔ して / した",
        "sec_class": "vt-sec",
        "meaning": "이야기하다 / 말하다",
        "rule_title": "📌 す는 음편 현상이 생기지 않음",
        "rule_content": "어미 <b>す</b>는 음편(촉음, 발음, 이음)으로 바뀌지 않고 連用形(し) 그대로 <b>して / した</b>가 됩니다.",
        "ex_ja": "先生と今後の進路について詳しく話した。",
        "ex_ko": "선생님과 향후 진로에 대해 자세히 이야기했다.",
        "tags": ["JLPT_N2", "동사활용", "음편"]
    },
    {
        "cat": "음편훈련",
        "badge": ("vt-badge-gen", "1그룹 음편 훈련 (す ➔ して) #12"),
        "q_title": "探す（さがす） → て形 / た形",
        "q_sub": "어미가 「す」로 끝나는 1그룹 동사의 형태는?",
        "a_head": "探して / 探した",
        "a_sub": "음편 없음: [す] ➔ して / した",
        "sec_class": "vt-sec",
        "meaning": "찾다",
        "rule_title": "📌 す 활용 규칙",
        "rule_content": "探す ➔ <b>探して / 探した</b>",
        "ex_ja": "失くした鍵を部屋の隅々まで探した。",
        "ex_ko": "잃어버린 열쇠를 방 구석구석까지 찾았다.",
        "tags": ["JLPT_N2", "동사활용", "음편"]
    },
    {
        "cat": "음편훈련",
        "badge": ("vt-badge-gen", "★음편 최빈출 예외 (く ➔ って) #13"),
        "q_title": "行く（いく） → て形 / た形",
        "q_sub": "어미가 「く」이지만 이음편(いて)이 아닌 유일한 예외는?",
        "a_head": "行って / 行った",
        "a_sub": "★절대주의: 行いて(X) ➔ 行って / 行った(O) 촉음편 예외!",
        "sec_class": "vt-sec",
        "meaning": "가다",
        "rule_title": "📌 行く의 유일한 음편 예외 규칙",
        "rule_content": "모든 く 동사는 いて가 되지만, 오직 <b>行く</b>만은 <b>行って / 行った</b>로 촉음편이 일어납니다.",
        "ex_ja": "昨日友達と一緒に美術館へ行ってきた。",
        "ex_ko": "어제 친구와 함께 미술관에 다녀왔다.",
        "tags": ["JLPT_N2", "동사활용", "음편", "예외"]
    },
    {
        "cat": "음편훈련",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형/음편 역방향 판별 #14"),
        "q_title": "急いだ（いそいだ）",
        "q_sub": "원형과 일어난 음편 규칙은?",
        "a_head": "急ぐ（いそぐ）",
        "a_sub": "「ぐ」 어미의 이음편 + 탁음화 (いで / いだ)",
        "sec_class": "vt-sec-blue",
        "meaning": "서둘렀다 (과거)",
        "rule_title": "📌 역방향 추론 공식",
        "rule_content": "<b>〜いだ / 〜いで</b>로 끝나면 원형 어미는 <b>〜ぐ</b>입니다.<br>예: 急いだ ➔ 急ぐ / 泳いだ ➔ 泳ぐ / 漕いだ ➔ 漕ぐ",
        "ex_ja": "約束の時間に遅れそうだったので急いだ。",
        "ex_ko": "약속 시간에 늦을 것 같아서 서둘렀다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "음편"]
    },
    {
        "cat": "음편훈련",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형/음편 역방향 판별 #15"),
        "q_title": "頼んだ（たのんだ）",
        "q_sub": "원형과 일어난 음편 규칙은?",
        "a_head": "頼む（たのむ）",
        "a_sub": "「む」 어미의 발음편 + 탁음화 (んで / んだ)",
        "sec_class": "vt-sec-blue",
        "meaning": "부탁했다 (과거)",
        "rule_title": "📌 역방향 추론 공식",
        "rule_content": "<b>〜んだ / 〜んで</b>로 끝나면 원형 어미는 <b>む / ぶ / ぬ</b> 중 하나입니다.<br>頼んだ ➔ 頼む / 呼んだ ➔ 呼ぶ / 死んだ ➔ 死ぬ",
        "ex_ja": "先輩に資料のチェックを頼んだ。",
        "ex_ko": "선배에게 자료 검토를 부탁했다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "음편"]
    },
    {
        "cat": "음편훈련",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형/음편 역방향 판별 #16"),
        "q_title": "払った（はらった）",
        "q_sub": "원형과 일어난 음편 규칙은?",
        "a_head": "払う（はらう）",
        "a_sub": "「う」 어미의 촉음편 (って / った)",
        "sec_class": "vt-sec-blue",
        "meaning": "지불했다 (과거)",
        "rule_title": "📌 역방향 추론 공식",
        "rule_content": "<b>〜った / 〜って</b>로 끝나면 원형 어미는 <b>う / つ / る</b> 중 하나입니다.<br>払った ➔ 払う / 勝った ➔ 勝つ / 取った ➔ 取る",
        "ex_ja": "レジでクレジットカードを使って代金を払った。",
        "ex_ko": "계산대에서 신용카드를 사용하여 대금을 지불했다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "음편"]
    },

    # -------------------------------------------------------------------------
    # 3. ない형 특수/규칙 (う➔わ 포함) (8장)
    # -------------------------------------------------------------------------
    {
        "cat": "부정형",
        "badge": ("vt-badge-gen", "ない형 규칙 (う ➔ わない) #01"),
        "q_title": "買う（かう） → ない形",
        "q_sub": "어미 「う」의 ない형은?",
        "a_head": "買わない（かわない）",
        "a_sub": "★주의: かあない(X) ➔ かわない(O) [う ➔ わ]",
        "sec_class": "vt-sec",
        "meaning": "사지 않다",
        "rule_title": "📌 어미 「う」는 「わ」로 변환",
        "rule_content": "1그룹 동사 중 어미가 <b>う</b>인 동사는 아(あ)단 변환 시 あ가 아니라 <b>わ</b>가 됩니다.<br>買う ➔ 買<b>わ</b>ない / 言う ➔ 言<b>わ</b>ない / 会う ➔ 会<b>わ</b>ない",
        "ex_ja": "今は無駄なものは買わないようにしている。",
        "ex_ko": "지금은 쓸데없는 물건은 사지 않도록 하고 있다.",
        "tags": ["JLPT_N2", "동사활용", "ない형", "う_わ"]
    },
    {
        "cat": "부정형",
        "badge": ("vt-badge-gen", "ない형 규칙 (う ➔ わない) #02"),
        "q_title": "払う（はらう） → ない形",
        "q_sub": "어미 「う」의 ない형은?",
        "a_head": "払わない（はらわない）",
        "a_sub": "う ➔ わ 변환: 払わない",
        "sec_class": "vt-sec",
        "meaning": "지불하지 않다",
        "rule_title": "📌 어미 「う」는 「わ」로 변환",
        "rule_content": "払う ➔ 払<b>わ</b>ない",
        "ex_ja": "納得がいかない料金は払わないつもりだ。",
        "ex_ko": "납득이 가지 않는 요금은 지불하지 않을 작정이다.",
        "tags": ["JLPT_N2", "동사활용", "ない형", "う_わ"]
    },
    {
        "cat": "부정형",
        "badge": ("vt-badge-gen", "ない형 규칙 (う ➔ わない) #03"),
        "q_title": "習う（ならう） → ない形",
        "q_sub": "어미 「う」의 ない형은?",
        "a_head": "習わない（ならわない）",
        "a_sub": "う ➔ わ 변환: 習わない",
        "sec_class": "vt-sec",
        "meaning": "배우지 않다",
        "rule_title": "📌 어미 「う」는 「わ」로 변환",
        "rule_content": "習う ➔ 習<b>わ</b>ない",
        "ex_ja": "学校で習わない実用的な表現を身につけたい。",
        "ex_ko": "학교에서 배우지 않는 실용적인 표현을 익히고 싶다.",
        "tags": ["JLPT_N2", "동사활용", "ない형", "う_わ"]
    },
    {
        "cat": "부정형",
        "badge": ("vt-badge-gen", "ない형 규칙 (う ➔ わない) #04"),
        "q_title": "言う（いう） → ない形",
        "q_sub": "어미 「う」의 ない형은?",
        "a_head": "言わない（いわない）",
        "a_sub": "う ➔ わ 변환: 言わない",
        "sec_class": "vt-sec",
        "meaning": "말하지 않다",
        "rule_title": "📌 어미 「う」는 「わ」로 변환",
        "rule_content": "言う ➔ 言<b>わ</b>ない",
        "ex_ja": "余計なことは言わないほうが賢명だ。",
        "ex_ko": "불필요한 말은 하지 않는 편이 현명하다.",
        "tags": ["JLPT_N2", "동사활용", "ない형", "う_わ"]
    },
    {
        "cat": "부정형",
        "badge": ("vt-badge-gen", "★특수 부정형 #05"),
        "q_title": "ある（존재/소유 동사） → ない形",
        "q_sub": "동사 「ある」의 부정(ない)형태는?",
        "a_head": "ない",
        "a_sub": "★절대주의: あらない(X) ➔ ない(O) 완전 불규칙!",
        "sec_class": "vt-sec",
        "meaning": "없다",
        "rule_title": "📌 ある의 부정형 규칙",
        "rule_content": "동사 ある의 부정형은 あらない가 아니라 단독 형용사 형태인 <b>ない</b>가 됩니다.",
        "ex_ja": "今手元には十分なお金がない。",
        "ex_ko": "지금 수중에는 충분한 돈이 없다.",
        "tags": ["JLPT_N2", "동사활용", "ない형", "특수"]
    },
    {
        "cat": "부정형",
        "badge": ("vt-badge-gen", "3그룹 부정형 #06"),
        "q_title": "する（3그룹 변격） → ない形",
        "q_sub": "동사 「する」의 ない형태는?",
        "a_head": "しない",
        "a_sub": "3그룹 변격: する ➔ しない",
        "sec_class": "vt-sec",
        "meaning": "하지 않다",
        "rule_title": "📌 3그룹 する 활용",
        "rule_content": "• ます형: します / ない형: <b>しない</b><br>• て형: して / た형: した",
        "ex_ja": "無理な残業はしない方針だ。",
        "ex_ko": "무리한 잔업은 하지 않는 방침이다.",
        "tags": ["JLPT_N2", "동사활용", "ない형", "3그룹"]
    },
    {
        "cat": "부정형",
        "badge": ("vt-badge-gen", "3그룹 발음 변화 부정형 #07"),
        "q_title": "来る（くる / 3그룹） → ない形",
        "q_sub": "동사 「来る」의 ない형태와 읽기는?",
        "a_head": "来ない（こない）",
        "a_sub": "★발음 주의: きない(X) ➔ こない(O)",
        "sec_class": "vt-sec",
        "meaning": "오지 않다",
        "rule_title": "📌 来る의 한자 읽기 변화",
        "rule_content": "• 사전형: 来る（<b>くる</b>）<br>• ます형: 来ます（<b>きます</b>）<br>• ない형: 来ない（<b>こない</b>）★<br>• て형: 来て（<b>きて</b>）",
        "ex_ja": "約束の時間になっても彼が来ない。",
        "ex_ko": "약속 시간이 되어도 그가 오지 않는다.",
        "tags": ["JLPT_N2", "동사활용", "ない형", "3그룹"]
    },
    {
        "cat": "부정형",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형 역방향 판별 #08"),
        "q_title": "使わない（つかわない）",
        "q_sub": "원형과 활용 종류는?",
        "a_head": "使う（つかう） / ない形",
        "a_sub": "「う」 어미 ➔ 「わ」 + ない",
        "sec_class": "vt-sec-blue",
        "meaning": "사용하지 않다",
        "rule_title": "📌 역방향 추론 공식",
        "rule_content": "<b>〜わない</b>로 끝나는 부정형은 원형 어미가 <b>〜う</b>인 1그룹 동사입니다.<br>使わない ➔ 使う / 買わない ➔ 買う / 追わない ➔ 追う",
        "ex_ja": "最近は現金をほとんど使わない生活をしている。",
        "ex_ko": "최근에는 현금을 거의 사용하지 않는 생활을 하고 있다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "ない형"]
    },

    # -------------------------------------------------------------------------
    # 4. 가능형 (可能形) 생성 & 복원 (12장)
    # -------------------------------------------------------------------------
    {
        "cat": "가능형",
        "badge": ("vt-badge-gen", "1그룹 가능형 생성 #01"),
        "q_title": "読む（よむ） → 可能形",
        "q_sub": "1그룹 동사 「読む」의 가능형은?",
        "a_head": "読める（よめる）",
        "a_sub": "1그룹 가능형 공식: う단 ➔ え단 + る",
        "sec_class": "vt-sec",
        "meaning": "읽을 수 있다",
        "rule_title": "📌 1그룹 가능형 규칙",
        "rule_content": "1그룹 동사는 어미를 <b>え단으로 바꾸고 る를 접속</b>합니다.<br>読む (む) ➔ 読<b>め</b>る (よめる)<br>※ 가능동사화되면 2그룹으로 취급됨 (読めない, 読めます)",
        "ex_ja": "専門用語が多くて、一人では読めない。",
        "ex_ko": "전문용어가 많아서 혼자서는 읽을 수 없다.",
        "tags": ["JLPT_N2", "동사활용", "가능형", "1그룹"]
    },
    {
        "cat": "가능형",
        "badge": ("vt-badge-gen", "1그룹 가능형 생성 #02"),
        "q_title": "書く（かく） → 可能形",
        "q_sub": "1그룹 동사 「書く」의 가능형은?",
        "a_head": "書ける（かける）",
        "a_sub": "う단(く) ➔ え단(け) + る",
        "sec_class": "vt-sec",
        "meaning": "쓸 수 있다",
        "rule_title": "📌 1그룹 가능형 규칙",
        "rule_content": "書く ➔ 書<b>け</b>る",
        "ex_ja": "パソコンがあれば、きれいな文章が書ける。",
        "ex_ko": "컴퓨터가 있으면 깔끔한 문장을 쓸 수 있다.",
        "tags": ["JLPT_N2", "동사활용", "가능형", "1그룹"]
    },
    {
        "cat": "가능형",
        "badge": ("vt-badge-gen", "1그룹 가능형 생성 #03"),
        "q_title": "待つ（まつ） → 可能形",
        "q_sub": "1그룹 동사 「待つ」의 가능형은?",
        "a_head": "待てる（まてる）",
        "a_sub": "う단(つ) ➔ え단(て) + る",
        "sec_class": "vt-sec",
        "meaning": "기다릴 수 있다",
        "rule_title": "📌 1그룹 가능형 규칙",
        "rule_content": "待つ ➔ 待<b>て</b>る",
        "ex_ja": "あと10分くらいならここで待てる。",
        "ex_ko": "앞으로 10분 정도라면 여기서 기다릴 수 있다.",
        "tags": ["JLPT_N2", "동사활용", "가능형", "1그룹"]
    },
    {
        "cat": "가능형",
        "badge": ("vt-badge-gen", "1그룹 가능형 생성 #04"),
        "q_title": "話す（はなす） → 可能形",
        "q_sub": "1그룹 동사 「話す」의 가능형은?",
        "a_head": "話せる（はなせる）",
        "a_sub": "う단(す) ➔ え단(せ) + る",
        "sec_class": "vt-sec",
        "meaning": "말할 수 있다",
        "rule_title": "📌 1그룹 가능형 규칙",
        "rule_content": "話す ➔ 話<b>せ</b>る",
        "ex_ja": "彼は日本語と英語の両方を流暢に話せる。",
        "ex_ko": "그는 일본어와 영어 둘 다 유창하게 말할 수 있다.",
        "tags": ["JLPT_N2", "동사활용", "가능형", "1그룹"]
    },
    {
        "cat": "가능형",
        "badge": ("vt-badge-gen", "1그룹 예외 가능형 #05"),
        "q_title": "帰る（かえる） → 可能形",
        "q_sub": "1그룹 예외 동사 「帰る」의 가능형은?",
        "a_head": "帰れる（かえれる）",
        "a_sub": "1그룹이므로 帰られる(X) ➔ 帰れる(O)",
        "sec_class": "vt-sec",
        "meaning": "돌아갈 수 있다",
        "rule_title": "📌 1그룹 예외의 가능형",
        "rule_content": "帰る는 1그룹이므로 る를 え단(れ)으로 바꾸어 <b>帰れる</b>가 됩니다. (2그룹처럼 帰られる로 쓰지 않도록 주의!)",
        "ex_ja": "仕事が早く終われば、定時に帰れる。",
        "ex_ko": "일이 일찍 끝나면 정시에 퇴근할 수 있다.",
        "tags": ["JLPT_N2", "동사활용", "가능형", "1그룹예외"]
    },
    {
        "cat": "가능형",
        "badge": ("vt-badge-gen", "2그룹 가능형 생성 #06"),
        "q_title": "食べる（たべる） → 可能形",
        "q_sub": "2그룹 동사 「食べる」의 정석 가능형은? (구어 표현은?)",
        "a_head": "食べられる（たべられる）",
        "a_sub": "2그룹 공식: 어간 + られる (구어: 食べれる)",
        "sec_class": "vt-sec",
        "meaning": "먹을 수 있다",
        "rule_title": "📌 2그룹 가능형과 ら抜き(라 탈락)",
        "rule_content": "• 표준/시험: <b>食べられる</b> (수동형과 동일 형태)<br>• 회화/청해(ら抜き): <b>食べれる</b><br>※ 시험 지문에서는 食べられる가 표준입니다.",
        "ex_ja": "辛い料理は苦手だが、これなら食べられる。",
        "ex_ko": "매운 요리는 잘 못 먹지만, 이것이라면 먹을 수 있다.",
        "tags": ["JLPT_N2", "동사활용", "가능형", "2그룹"]
    },
    {
        "cat": "가능형",
        "badge": ("vt-badge-gen", "2그룹 가능형 생성 #07"),
        "q_title": "見る（みる） → 可能形",
        "q_sub": "2그룹 동사 「見る」의 정석 가능형은? (見える와의 차이는?)",
        "a_head": "見られる（みられる）",
        "a_sub": "의지 가능: 見られる / 자연 발생적 보임: 見える",
        "sec_class": "vt-sec",
        "meaning": "볼 수 있다 (의도를 가지고)",
        "rule_title": "📌 見られる vs 見える 구분",
        "rule_content": "• <b>見られる</b>: 수단/능력이 있어 스스로 '볼 수 있다'<br>• <b>見える</b>: 눈을 뜨면 시야에 자연스럽게 '보이다'",
        "ex_ja": "展望台からは富士山がきれいに見られる。",
        "ex_ko": "전망대에서는 후지산을 아름답게 볼 수 있다.",
        "tags": ["JLPT_N2", "동사활용", "가능형", "2그룹"]
    },
    {
        "cat": "가능형",
        "badge": ("vt-badge-gen", "3그룹 가능형 #08"),
        "q_title": "する（3그룹） → 可能形",
        "q_sub": "동사 「する」의 가능형은?",
        "a_head": "できる",
        "a_sub": "완전 불규칙 형태: する ➔ できる",
        "sec_class": "vt-sec",
        "meaning": "할 수 있다",
        "rule_title": "📌 する의 가능형",
        "rule_content": "する의 가능형은 고유 어휘인 <b>できる</b>를 사용합니다.<br>조사 주의: 〜を する ↔ <b>〜が できる</b>",
        "ex_ja": "努力を重ねれば、必ず目標を達成できる。",
        "ex_ko": "노력을 거듭하면 반드시 목표를 달성할 수 있다.",
        "tags": ["JLPT_N2", "동사활용", "가능형", "3그룹"]
    },
    {
        "cat": "가능형",
        "badge": ("vt-badge-gen", "3그룹 가능형 #09"),
        "q_title": "来る（くる / 3그룹） → 可能形",
        "q_sub": "동사 「来る」의 정석 가능형과 읽기는?",
        "a_head": "来られる（こられる）",
        "a_sub": "읽기 주의: きられる(X) ➔ こられる(O) (구어: 来れる)",
        "sec_class": "vt-sec",
        "meaning": "올 수 있다",
        "rule_title": "📌 来る의 가능형",
        "rule_content": "• 표준형: <b>来られる（こられる）</b><br>• 회화(ら抜き): 来れる（これる）",
        "ex_ja": "明日の飲み会には参加できる？ ― うん、来られるよ。",
        "ex_ko": "내일 회식에는 참석할 수 있어? ― 응, 올 수 있어.",
        "tags": ["JLPT_N2", "동사활용", "가능형", "3그룹"]
    },
    {
        "cat": "가능형",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형 역방향 판별 #10"),
        "q_title": "書ける（かける）",
        "q_sub": "원형과 활용 종류는?",
        "a_head": "書く（かく） / 可能形",
        "a_sub": "1그룹 동사 え단화: 書く ➔ 書ける",
        "sec_class": "vt-sec-blue",
        "meaning": "쓸 수 있다",
        "rule_title": "📌 1그룹 가능형 판별 요령",
        "rule_content": "1그룹 동사의 어미가 <b>え단 + る</b>로 끝나면 <b>가능형</b>입니다.<br>書ける ➔ 書く / 読める ➔ 読む / 話せる ➔ 話す",
        "ex_ja": "漢字が正しく書けるように毎日練習している。",
        "ex_ko": "한자를 올바르게 쓸 수 있도록 매일 연습하고 있다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "가능형"]
    },
    {
        "cat": "가능형",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형 역방향 판별 #11"),
        "q_title": "見られる（みられる）",
        "q_sub": "원형과 가능한 활용 종류 2가지는?",
        "a_head": "見る（みる） / 可能形 또는 受身形",
        "a_sub": "2그룹 동사의 〜られる는 [가능 / 수동] 형태가 동일함!",
        "sec_class": "vt-sec-blue",
        "meaning": "볼 수 있다 (가능) / 보여지다·관찰되다 (수동)",
        "rule_title": "📌 2그룹 〜られる의 문맥 판별",
        "rule_content": "문맥에서 <b>주어가 능동적으로 할 수 있는지(가능)</b> vs <b>남에게 당하거나 관찰되는지(수동)</b>로 구별합니다.",
        "ex_ja": "夜空には無数の星が見られた。（가능: 볼 수 있었다）",
        "ex_ko": "밤하늘에는 무수한 별을 볼 수 있었다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "가능형"]
    },
    {
        "cat": "가능형",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형 역방향 판별 #12"),
        "q_title": "走れる（はしれる）",
        "q_sub": "원형과 활용 종류는?",
        "a_head": "走る（はしる） / 可能形",
        "a_sub": "1그룹 예외 동사의 가능형 (走る ➔ 走れる)",
        "sec_class": "vt-sec-blue",
        "meaning": "달릴 수 있다",
        "rule_title": "📌 1그룹 예외 판별",
        "rule_content": "走る는 1그룹 예외 동사이므로 え단 변환되어 <b>走れる</b>가 됩니다.",
        "ex_ja": "怪我が治って、また走れるようになった。",
        "ex_ko": "부상이 나아서 다시 달릴 수 있게 되었다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "가능형"]
    },

    # -------------------------------------------------------------------------
    # 5. 수동형 (受身形) 생성 & 복원 (12장)
    # -------------------------------------------------------------------------
    {
        "cat": "수동형",
        "badge": ("vt-badge-gen", "1그룹 수동형 생성 #01"),
        "q_title": "叱る（しかる） → 受身形",
        "q_sub": "1그룹 동사 「叱る」의 수동형은?",
        "a_head": "叱られる（しかられる）",
        "a_sub": "1그룹 수동형 공식: あ단 + れる",
        "sec_class": "vt-sec",
        "meaning": "꾸중을 듣다 / 혼나다",
        "rule_title": "📌 1그룹 수동형 규칙",
        "rule_content": "1그룹 동사는 어미를 <b>あ단으로 바꾸고 れる를 접속</b>합니다.<br>叱る (る) ➔ 叱<b>ら</b>れる",
        "ex_ja": "宿題を忘れて、先生にひどく叱られた。",
        "ex_ko": "숙제를 잊어버려서 선생님께 심하게 혼났다.",
        "tags": ["JLPT_N2", "동사활용", "수동형", "1그룹"]
    },
    {
        "cat": "수동형",
        "badge": ("vt-badge-gen", "1그룹 수동형 생성 #02"),
        "q_title": "踏む（ふむ） → 受身形",
        "q_sub": "1그룹 동사 「踏む」의 수동형은?",
        "a_head": "踏まれる（ふまれる）",
        "a_sub": "う단(む) ➔ あ단(ま) + れる",
        "sec_class": "vt-sec",
        "meaning": "밟히다",
        "rule_title": "📌 1그룹 수동형 규칙",
        "rule_content": "踏む ➔ 踏<b>ま</b>れる",
        "ex_ja": "満員電車の中で、誰かに足を踏まれた。",
        "ex_ko": "만원 전철 안에서 누군가에게 발을 밟혔다(피해 수동).",
        "tags": ["JLPT_N2", "동사활용", "수동형", "1그룹"]
    },
    {
        "cat": "수동형",
        "badge": ("vt-badge-gen", "1그룹 수동형 생성 #03"),
        "q_title": "頼む（たのむ） → 受身形",
        "q_sub": "1그룹 동사 「頼む」의 수동형은?",
        "a_head": "頼まれる（たのまれる）",
        "a_sub": "う단(む) ➔ あ단(ま) + れる",
        "sec_class": "vt-sec",
        "meaning": "부탁받다",
        "rule_title": "📌 1그룹 수동형 규칙",
        "rule_content": "頼む ➔ 頼<b>ま</b>れる",
        "ex_ja": "上司から急ぎの仕事を頼まれた。",
        "ex_ko": "상사로부터 급한 일을 부탁받았다.",
        "tags": ["JLPT_N2", "동사활용", "수동형", "1그룹"]
    },
    {
        "cat": "수동형",
        "badge": ("vt-badge-gen", "1그룹 수동형 (う ➔ われる) #04"),
        "q_title": "誘う（さそう） → 受身形",
        "q_sub": "어미 「う」의 수동형은?",
        "a_head": "誘われる（さそわれる）",
        "a_sub": "★주의: さそあれる(X) ➔ さそわれる(O)",
        "sec_class": "vt-sec",
        "meaning": "권유받다 / 권유당하다",
        "rule_title": "📌 어미 「う」는 「わ」 + れる",
        "rule_content": "어미가 う인 동사의 수동형은 <b>われる</b>가 됩니다.<br>誘う ➔ 誘<b>わ</b>れる / 笑う ➔ 笑<b>わ</b>れる",
        "ex_ja": "同僚に誘われて、仕事帰りに食事に行った。",
        "ex_ko": "동료에게 권유를 받아서 퇴근길에 식사하러 갔다.",
        "tags": ["JLPT_N2", "동사활용", "수동형", "う_わ"]
    },
    {
        "cat": "수동형",
        "badge": ("vt-badge-gen", "2그룹 수동형 생성 #05"),
        "q_title": "褒める（ほめる） → 受身形",
        "q_sub": "2그룹 동사 「褒める」의 수동형은?",
        "a_head": "褒められる（ほめられる）",
        "a_sub": "2그룹 공식: 어간 + られる",
        "sec_class": "vt-sec",
        "meaning": "칭찬받다",
        "rule_title": "📌 2그룹 수동형 규칙",
        "rule_content": "2그룹 동사는 어미 る를 떼고 <b>られる</b>를 붙입니다.<br>褒める ➔ 褒め<b>られる</b>",
        "ex_ja": "テストで満点を取って、先生に褒められた。",
        "ex_ko": "시험에서 만점을 받아서 선생님께 칭찬받았다.",
        "tags": ["JLPT_N2", "동사활용", "수동형", "2그룹"]
    },
    {
        "cat": "수동형",
        "badge": ("vt-badge-gen", "2그룹 수동형 생성 #06"),
        "q_title": "捨てる（すてる） → 受身形",
        "q_sub": "2그룹 동사 「捨てる」의 수동형은?",
        "a_head": "捨てられる（すてられる）",
        "a_sub": "2그룹 공식: 어간 + られる",
        "sec_class": "vt-sec",
        "meaning": "버려지다 / 버림받다",
        "rule_title": "📌 2그룹 수동형 규칙",
        "rule_content": "捨てる ➔ 捨て<b>られる</b>",
        "ex_ja": "大切にしていた宝物を勝手に捨てられた。",
        "ex_ko": "소중히 여기던 보물을 멋대로 버려졌다(피해 수동).",
        "tags": ["JLPT_N2", "동사활용", "수동형", "2그룹"]
    },
    {
        "cat": "수동형",
        "badge": ("vt-badge-gen", "3그룹 수동형 #07"),
        "q_title": "する（3그룹） → 受身形",
        "q_sub": "동사 「する」의 수동형은?",
        "a_head": "される",
        "a_sub": "3그룹 불규칙: する ➔ される",
        "sec_class": "vt-sec",
        "meaning": "당하다 / ~되다",
        "rule_title": "📌 3그룹 する 수동",
        "rule_content": "• 단독: <b>される</b><br>• 한자어: 設計される (설계되다) / 発表される (발표되다)",
        "ex_ja": "このビルは世界的に有名な建築家によって設計された。",
        "ex_ko": "이 빌딩은 세계적으로 유명한 건축가에 의해 설계되었다.",
        "tags": ["JLPT_N2", "동사활용", "수동형", "3그룹"]
    },
    {
        "cat": "수동형",
        "badge": ("vt-badge-gen", "3그룹 수동형 #08"),
        "q_title": "来る（くる / 3그룹） → 受身形",
        "q_sub": "동사 「来る」의 수동형과 발음은?",
        "a_head": "来られる（こられる）",
        "a_sub": "발음: こられる (피해 수동으로 자주 쓰임)",
        "sec_class": "vt-sec",
        "meaning": "(누군가가 와서) 곤란해지다",
        "rule_title": "📌 迷惑受身(피해 수동)의 来られる",
        "rule_content": "자동사 来る의 수동형은 대표적인 <b>간접/피해 수동</b>입니다.<br>예: 雨に来られる (비가 와서 곤란하다) / 友達に来られる (친구가 불쑥 찾아와서 곤란하다)",
        "ex_ja": "休日に突然客に来られて、休む暇がなかった。",
        "ex_ko": "휴일에 갑자기 손님이 찾아와서 쉴 틈이 없었다(피해 수동).",
        "tags": ["JLPT_N2", "동사활용", "수동형", "3그룹"]
    },
    {
        "cat": "수동형",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형 역방향 판별 #09"),
        "q_title": "盗まれる（ぬすまれる）",
        "q_sub": "원형과 활용 종류는?",
        "a_head": "盗む（ぬすむ） / 受身形",
        "a_sub": "う단(む) ➔ あ단(ま) + れる",
        "sec_class": "vt-sec-blue",
        "meaning": "도둑맞다 / 도난당하다",
        "rule_title": "📌 1그룹 수동형 판별",
        "rule_content": "<b>〜まれる</b> ➔ 원형 어미는 <b>〜む</b>",
        "ex_ja": "旅行中に財布を盗まれて大変な目に遭った。",
        "ex_ko": "여행 중에 지갑을 도둑맞아 큰 곤욕을 치렀다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "수동형"]
    },
    {
        "cat": "수동형",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형 역방향 판별 #10"),
        "q_title": "追われる（おわれる）",
        "q_sub": "원형과 활용 종류는?",
        "a_head": "追う（おう） / 受身形",
        "a_sub": "う ➔ わ + れる",
        "sec_class": "vt-sec-blue",
        "meaning": "쫓기다",
        "rule_title": "📌 1그룹 수동형 판별",
        "rule_content": "<b>〜われる</b> ➔ 원형 어미는 <b>〜う</b>",
        "ex_ja": "毎日の仕事に追われて、自分の時間がない。",
        "ex_ko": "매일의 업무에 쫓겨서 자신의 시간이 없다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "수동형"]
    },
    {
        "cat": "수동형",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형 역방향 판별 #11"),
        "q_title": "雨に降られた（ふられた）",
        "q_sub": "원형과 문법적 수동 용법은?",
        "a_head": "降る（ふる） / 間接受身 (迷惑受身)",
        "a_sub": "비가 내려서 화자가 '곤란/피해'를 입음!",
        "sec_class": "vt-sec-blue",
        "meaning": "비를 맞았다 (곤란을 겪음)",
        "rule_title": "📌 자동사의 피해 수동",
        "rule_content": "일본어에서는 자동사(降る, 泣く, 死ぬ)도 수동형으로 만들어 <b>'그 일로 인해 화자가 피해를 입었음'</b>을 나타냅니다.",
        "ex_ja": "傘を持たずに出かけたら、途中で雨に降られた。",
        "ex_ko": "우산을 챙기지 않고 외출했더니 도중에 비를 맞고 말았다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "수동형", "피해수동"]
    },
    {
        "cat": "수동형",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형 역방향 판별 #12"),
        "q_title": "断られた（ことわられた）",
        "q_sub": "원형과 활용 종류는?",
        "a_head": "断る（ことわる） / 受身形",
        "a_sub": "う단(る) ➔ あ단(ら) + れる",
        "sec_class": "vt-sec-blue",
        "meaning": "거절당했다",
        "rule_title": "📌 1그룹 수동형 판별",
        "rule_content": "<b>〜られた</b> ➔ 원형 어미는 <b>〜る</b> (1그룹 断る)",
        "ex_ja": "思い切って提案したが、あっさりと断られた。",
        "ex_ko": "과감하게 제안해 보았지만 단번에 거절당했다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "수동형"]
    },

    # -------------------------------------------------------------------------
    # 6. 사역형 (使役形) 생성 & 복원 (12장)
    # -------------------------------------------------------------------------
    {
        "cat": "사역형",
        "badge": ("vt-badge-gen", "1그룹 사역형 생성 #01"),
        "q_title": "読む（よむ） → 使役形",
        "q_sub": "1그룹 동사 「読む」의 사역형은?",
        "a_head": "読ませる（よませる）",
        "a_sub": "1그룹 사역형 공식: あ단 + せる",
        "sec_class": "vt-sec",
        "meaning": "읽게 하다 / 읽히다",
        "rule_title": "📌 1그룹 사역형 규칙",
        "rule_content": "1그룹 동사는 어미를 <b>あ단으로 바꾸고 せる를 접속</b>합니다.<br>読む (む) ➔ 読<b>ま</b>せる",
        "ex_ja": "親は子どもに毎日本を読ませている。",
        "ex_ko": "부모는 아이에게 매일 책을 읽히고(읽게 하고) 있다.",
        "tags": ["JLPT_N2", "동사활용", "사역형", "1그룹"]
    },
    {
        "cat": "사역형",
        "badge": ("vt-badge-gen", "1그룹 사역형 생성 #02"),
        "q_title": "書く（かく） → 使役形",
        "q_sub": "1그룹 동사 「書く」의 사역형은?",
        "a_head": "書かせる（かかせる）",
        "a_sub": "う단(く) ➔ あ단(か) + せる",
        "sec_class": "vt-sec",
        "meaning": "쓰게 하다",
        "rule_title": "📌 1그룹 사역형 규칙",
        "rule_content": "書く ➔ 書<b>か</b>せる",
        "ex_ja": "先生は学生に反省文を書かせた。",
        "ex_ko": "선생님은 학생에게 반성문을 쓰게 했다.",
        "tags": ["JLPT_N2", "동사활용", "사역형", "1그룹"]
    },
    {
        "cat": "사역형",
        "badge": ("vt-badge-gen", "1그룹 사역형 생성 #03"),
        "q_title": "行く（いく） → 使役形",
        "q_sub": "1그룹 동사 「行く」의 사역형은?",
        "a_head": "行かせる（いかせる）",
        "a_sub": "う단(く) ➔ あ단(か) + せる",
        "sec_class": "vt-sec",
        "meaning": "가게 하다 / 보내다",
        "rule_title": "📌 1그룹 사역형 규칙",
        "rule_content": "行く ➔ 行<b>か</b>せる (※ 음편과 달리 사역형은 규칙대로 かせる)",
        "ex_ja": "息子を海外の語学留学に行かせることにした。",
        "ex_ko": "아들을 해외 어학연수에 보내기로(가게 하기로) 했다.",
        "tags": ["JLPT_N2", "동사활용", "사역형", "1그룹"]
    },
    {
        "cat": "사역형",
        "badge": ("vt-badge-gen", "1그룹 사역형 생성 #04"),
        "q_title": "待つ（まつ） → 使役形",
        "q_sub": "1그룹 동사 「待つ」의 사역형은?",
        "a_head": "待たせる（またせる）",
        "a_sub": "う단(つ) ➔ あ단(た) + せる",
        "sec_class": "vt-sec",
        "meaning": "기다리게 하다",
        "rule_title": "📌 1그룹 사역형 규칙",
        "rule_content": "待つ ➔ 待<b>た</b>せる",
        "ex_ja": "お待たせして申し訳ありませんでした。",
        "ex_ko": "기다리게 해 드려서 대단히 죄송했습니다.",
        "tags": ["JLPT_N2", "동사활용", "사역형", "1그룹"]
    },
    {
        "cat": "사역형",
        "badge": ("vt-badge-gen", "1그룹 사역형 (う ➔ わせる) #05"),
        "q_title": "歌う（うたう） → 使役形",
        "q_sub": "어미 「う」의 사역형은?",
        "a_head": "歌わせる（うたわせる）",
        "a_sub": "う ➔ わ + せる",
        "sec_class": "vt-sec",
        "meaning": "노래하게 하다",
        "rule_title": "📌 어미 「う」는 「わ」 + せる",
        "rule_content": "歌う ➔ 歌<b>わ</b>せる / 買う ➔ 買<b>わ</b>せる",
        "ex_ja": "みんなの前で無理やり歌わされた。（사역수동 연결）",
        "ex_ko": "모두의 앞에서 억지로 노래를 불려야 했다.",
        "tags": ["JLPT_N2", "동사활용", "사역형", "う_わ"]
    },
    {
        "cat": "사역형",
        "badge": ("vt-badge-gen", "2그룹 사역형 생성 #06"),
        "q_title": "食べる（たべる） → 使役形",
        "q_sub": "2그룹 동사 「食べる」의 사역형은?",
        "a_head": "食べさせる（たべさせる）",
        "a_sub": "2그룹 공식: 어간 + させる",
        "sec_class": "vt-sec",
        "meaning": "먹게 하다 / 먹이다",
        "rule_title": "📌 2그룹 사역형 규칙",
        "rule_content": "2그룹 동사는 어미 る를 떼고 <b>させる</b>를 붙입니다.<br>食べる ➔ 食べ<b>させる</b>",
        "ex_ja": "子どもに嫌いな野菜を無理に食べさせてはいけない。",
        "ex_ko": "아이에게 싫어하는 채소를 억지로 먹여서는 안 된다.",
        "tags": ["JLPT_N2", "동사활용", "사역형", "2그룹"]
    },
    {
        "cat": "사역형",
        "badge": ("vt-badge-gen", "2그룹 사역형 생성 #07"),
        "q_title": "見る（みる） → 使役形",
        "q_sub": "2그룹 동사 「見る」의 사역형은?",
        "a_head": "見させる（みさせる）",
        "a_sub": "2그룹 공식: 어간 + させる",
        "sec_class": "vt-sec",
        "meaning": "보게 하다",
        "rule_title": "📌 2그룹 사역형 규칙",
        "rule_content": "見る ➔ 見<b>させる</b> (※ 見せる는 별도의 타동사 '보여주다')",
        "ex_ja": "生徒に実験の様子を間近で見させた。",
        "ex_ko": "학생들에게 실험 모습을 가까이서 보게 했다.",
        "tags": ["JLPT_N2", "동사활용", "사역형", "2그룹"]
    },
    {
        "cat": "사역형",
        "badge": ("vt-badge-gen", "3그룹 사역형 #08"),
        "q_title": "する（3그룹） → 使役形",
        "q_sub": "동사 「する」의 사역형은?",
        "a_head": "させる",
        "a_sub": "3그룹 불규칙: する ➔ させる",
        "sec_class": "vt-sec",
        "meaning": "하게 하다 / 시키다",
        "rule_title": "📌 3그룹 する 사역",
        "rule_content": "• 単独: <b>させる</b><br>• 複合: 勉強させる (공부시키다) / 残業させる (야근시키다)",
        "ex_ja": "部下に新しいプロジェクトを担当させた。",
        "ex_ko": "부하 직원에게 새로운 프로젝트를 담당하게 했다.",
        "tags": ["JLPT_N2", "동사활용", "사역형", "3그룹"]
    },
    {
        "cat": "사역형",
        "badge": ("vt-badge-gen", "3그룹 사역형 #09"),
        "q_title": "来る（くる / 3그룹） → 使役形",
        "q_sub": "동사 「来る」의 사역형과 발음은?",
        "a_head": "来させる（こさせる）",
        "a_sub": "발음 주의: きさせる(X) ➔ こさせる(O)",
        "sec_class": "vt-sec",
        "meaning": "오게 하다",
        "rule_title": "📌 来る의 사역형",
        "rule_content": "来る ➔ 来させる（<b>こさせる</b>）",
        "ex_ja": "明日急ぎの用件で彼を事務所に来させた。",
        "ex_ko": "내일 급한 용건으로 그를 사무소로 오게 했다.",
        "tags": ["JLPT_N2", "동사활용", "사역형", "3그룹"]
    },
    {
        "cat": "사역형",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형 역방향 판별 #10"),
        "q_title": "働かせる（はたらかせる）",
        "q_sub": "원형과 활용 종류는?",
        "a_head": "働く（はたらく） / 使役形",
        "a_sub": "う단(く) ➔ あ단(か) + せる",
        "sec_class": "vt-sec-blue",
        "meaning": "일하게 하다 / 작동시키다",
        "rule_title": "📌 사역형 판별",
        "rule_content": "<b>〜かせる</b> ➔ 원형 어미는 <b>〜く</b><br>知恵を働かせる (지혜를 발휘하다)",
        "ex_ja": "若い社員を現場でしっかり働かせる。",
        "ex_ko": "젊은 사원을 현장에서 확실하게 일하게 한다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "사역형"]
    },
    {
        "cat": "사역형",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형 역방향 판별 #11"),
        "q_title": "待たせる（またせる）",
        "q_sub": "원형과 활용 종류는?",
        "a_head": "待つ（まつ） / 使役形",
        "a_sub": "う단(つ) ➔ あ단(た) + せる",
        "sec_class": "vt-sec-blue",
        "meaning": "기다리게 하다",
        "rule_title": "📌 사역형 판별",
        "rule_content": "<b>〜たせる</b> ➔ 원형 어미는 <b>〜つ</b>",
        "ex_ja": "お客様を長く待たせてはいけない。",
        "ex_ko": "손님을 오래 기다리게 해서는 안 된다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "사역형"]
    },
    {
        "cat": "사역형",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형 역방향 판별 #12"),
        "q_title": "知らせる（しらせる）",
        "q_sub": "원형과 활용 종류는?",
        "a_head": "知る（しる） / 使役形",
        "a_sub": "1그룹 예외 知る의 사역형 (知る ➔ 知らせる)",
        "sec_class": "vt-sec-blue",
        "meaning": "알리다 / 알게 하다",
        "rule_title": "📌 1그룹 예외의 사역형",
        "rule_content": "知る는 1그룹이므로 あ단(ら) + せる ➔ <b>知らせる</b>가 됩니다.",
        "ex_ja": "結果が分かり次第、すぐに知らせてください。",
        "ex_ko": "결과를 아는 대로 즉시 알려 주세요.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "사역형"]
    },

    # -------------------------------------------------------------------------
    # 7. 사역수동형 (使役受身形) 집중 훈련 - 정식 vs 단축형 (14장)
    # -------------------------------------------------------------------------
    {
        "cat": "사역수동",
        "badge": ("vt-badge-gen", "사역수동 생성 & 단축형 #01"),
        "q_title": "読む（よむ） → 使役受身形（정식 & 단축형）",
        "q_sub": "1그룹 「読む」의 사역수동형 정식 형태와 실전 단축형은?",
        "a_head": "読ませられる / 読まされる",
        "a_sub": "정식: 読ませられる ↔ 단축형: 読まされる",
        "sec_class": "vt-sec",
        "meaning": "(억지로/어쩔 수 없이) 읽게 됨을 당하다",
        "rule_title": "📌 1그룹 사역수동의 단축형(短縮形) 공식",
        "rule_content": "1그룹 동사(す 제외)는 <b>[あ단 + される]</b>로 줄여 씁니다.<br>• 정식: 読ませられる<br>• <b>실전 단축형: 読まされる</b> (시험에 훨씬 많이 등장!)",
        "ex_ja": "興味のない本を何時間も読まされた。",
        "ex_ko": "흥미 없는 책을 몇 시간이나 억지로 읽어야 했다.",
        "tags": ["JLPT_N2", "동사활용", "사역수동", "단축형"]
    },
    {
        "cat": "사역수동",
        "badge": ("vt-badge-gen", "사역수동 생성 & 단축형 #02"),
        "q_title": "書く（かく） → 使役受身形（정식 & 단축형）",
        "q_sub": "1그룹 「書く」의 정식 형태와 단축형은?",
        "a_head": "書かせられる / 書かされる",
        "a_sub": "정식: 書かせられる ↔ 단축형: 書かされる",
        "sec_class": "vt-sec",
        "meaning": "(억지로) 쓰게 되다",
        "rule_title": "📌 단축형 형성",
        "rule_content": "書く ➔ 書<b>かせられる</b> (정식) / 書<b>かされる</b> (단축)",
        "ex_ja": "反省文を何枚も書かされた。",
        "ex_ko": "반성문을 몇 장이나 억지로 써야 했다.",
        "tags": ["JLPT_N2", "동사활용", "사역수동", "단축형"]
    },
    {
        "cat": "사역수동",
        "badge": ("vt-badge-gen", "사역수동 생성 & 단축형 #03"),
        "q_title": "行く（いく） → 使役受身形（정식 & 단축형）",
        "q_sub": "1그룹 「行く」의 정식 형태와 단축형은?",
        "a_head": "行かせられる / 行かされる",
        "a_sub": "정식: 行かせられる ↔ 단축형: 行かされる",
        "sec_class": "vt-sec",
        "meaning": "(원치 않는데) 가게 되다",
        "rule_title": "📌 단축형 형성",
        "rule_content": "行く ➔ 行<b>かせられる</b> / 行<b>かされる</b>",
        "ex_ja": "休日なのに上司の用事で遠くまで行かされた。",
        "ex_ko": "휴일인데도 상사의 용무로 먼 곳까지 가야만 했다.",
        "tags": ["JLPT_N2", "동사활용", "사역수동", "단축형"]
    },
    {
        "cat": "사역수동",
        "badge": ("vt-badge-gen", "사역수동 생성 & 단축형 #04"),
        "q_title": "待つ（まつ） → 使役受身形（정식 & 단축형）",
        "q_sub": "1그룹 「待つ」의 정식 형태와 단축형은?",
        "a_head": "待たせられる / 待たされる",
        "a_sub": "정식: 待たせられる ↔ 단축형: 待たされる",
        "sec_class": "vt-sec",
        "meaning": "(어쩔 수 없이) 기다리게 되다",
        "rule_title": "📌 단축형 형성",
        "rule_content": "待つ ➔ 待<b>たせられる</b> / 待<b>たされる</b>",
        "ex_ja": "病院で2時間も待たされて、イライラした。",
        "ex_ko": "병원에서 2시간이나 기다려야 해서 짜증이 났다.",
        "tags": ["JLPT_N2", "동사활용", "사역수동", "단축형"]
    },
    {
        "cat": "사역수동",
        "badge": ("vt-badge-gen", "사역수동 생성 & 단축형 #05"),
        "q_title": "歌う（うたう） → 使役受身形（정식 & 단축형）",
        "q_sub": "어미 「う」의 정식 형태와 단축형은?",
        "a_head": "歌わせられる / 歌わされる",
        "a_sub": "う ➔ わ: 歌わせられる / 歌わされる",
        "sec_class": "vt-sec",
        "meaning": "(억지로) 노래를 부르게 되다",
        "rule_title": "📌 단축형 형성",
        "rule_content": "歌う ➔ 歌<b>わせられる</b> / 歌<b>わされる</b>",
        "ex_ja": "カラオケで先輩に苦手な歌を歌わされた。",
        "ex_ko": "노래방에서 선배에게 잘 못 부르는 노래를 억지로 불려야 했다.",
        "tags": ["JLPT_N2", "동사활용", "사역수동", "단축형"]
    },
    {
        "cat": "사역수동",
        "badge": ("vt-badge-gen", "★단축형 불가 예외 동사 #06"),
        "q_title": "話す（はなす） → 使役受身形",
        "q_sub": "어미가 「す」인 동사는 단축형(話さされる)이 가능한가?",
        "a_head": "話させられる (단축형 없음!)",
        "a_sub": "★절대주의: 話さされる(X) ➔ 오직 話させられる(O)",
        "sec_class": "vt-sec",
        "meaning": "(억지로) 이야기하게 되다",
        "rule_title": "📌 어미 「す」는 단축형 불가 규칙",
        "rule_content": "어미가 <b>す</b>인 동사는 발음이 겹치므로(さされる) <b>단축형을 만들 수 없습니다!</b><br>오직 정식 형태인 <b>話させられる</b>만 가능합니다.",
        "ex_ja": "警察で事件の詳しい経緯を話させられた。",
        "ex_ko": "경찰서에서 사건의 자세한 경위를 진술해야(이야기해야) 했다.",
        "tags": ["JLPT_N2", "동사활용", "사역수동", "예외"]
    },
    {
        "cat": "사역수동",
        "badge": ("vt-badge-gen", "2그룹 사역수동 #07"),
        "q_title": "食べる（たべる） → 使役受身形",
        "q_sub": "2그룹 동사 「食べる」의 사역수동형은? (단축형이 있는가?)",
        "a_head": "食べさせられる (단축형 없음)",
        "a_sub": "2그룹은 단축형이 성립하지 않습니다! (食べさされる는 오문)",
        "sec_class": "vt-sec",
        "meaning": "(억지로) 먹게 되다",
        "rule_title": "📌 2그룹 사역수동 규칙",
        "rule_content": "2그룹 동사는 사역형(させ)에 수동(られる)이 붙어 <b>〜させられる</b>만 가능합니다.<br>食べる ➔ 食べ<b>させられる</b>",
        "ex_ja": "子どもの頃、嫌いなピーマンを食べさせられた。",
        "ex_ko": "어릴 적 싫어하던 피망을 억지로 먹어야 했다.",
        "tags": ["JLPT_N2", "동사활용", "사역수동", "2그룹"]
    },
    {
        "cat": "사역수동",
        "badge": ("vt-badge-gen", "2그룹 사역수동 #08"),
        "q_title": "辞める（やめる） → 使役受身形",
        "q_sub": "2그룹 동사 「辞める」의 사역수동형은?",
        "a_head": "辞めさせられる",
        "a_sub": "2그룹: 어간 + させられる",
        "sec_class": "vt-sec",
        "meaning": "(본의 아니게) 그만두게 되다 / 해고당하다",
        "rule_title": "📌 2그룹 사역수동 규칙",
        "rule_content": "辞める ➔ 辞め<b>させられる</b>",
        "ex_ja": "会社の都合で仕事を辞めさせられた。",
        "ex_ko": "회사 사정으로 일을 그만두게 되었다(잘렸다).",
        "tags": ["JLPT_N2", "동사활용", "사역수동", "2그룹"]
    },
    {
        "cat": "사역수동",
        "badge": ("vt-badge-gen", "3그룹 사역수동 #09"),
        "q_title": "する（3그룹） → 使役受身形",
        "q_sub": "동사 「する」의 사역수동형은?",
        "a_head": "させられる",
        "a_sub": "3그룹 불규칙: する ➔ させられる",
        "sec_class": "vt-sec",
        "meaning": "(억지로) 하게 되다",
        "rule_title": "📌 3그룹 する 사역수동",
        "rule_content": "残業する ➔ 残業<b>させられる</b> (야근당하다)<br>我慢する ➔ 我慢<b>させられる</b> (참아야만 하다)",
        "ex_ja": "毎晩遅くまで残業させられて、体が持たない。",
        "ex_ko": "매일 밤 늦게까지 야근을 당해서 몸이 버티지 못한다.",
        "tags": ["JLPT_N2", "동사활용", "사역수동", "3그룹"]
    },
    {
        "cat": "사역수동",
        "badge": ("vt-badge-gen", "3그룹 사역수동 #10"),
        "q_title": "来る（くる / 3그룹） → 使役受身形",
        "q_sub": "동사 「来る」의 사역수동형과 발음은?",
        "a_head": "来させられる（こさせられる）",
        "a_sub": "발음 주의: こさせられる",
        "sec_class": "vt-sec",
        "meaning": "(억지로) 오게 되다",
        "rule_title": "📌 3그룹 来る 사역수동",
        "rule_content": "来る ➔ 来させられる（<b>こさせられる</b>）",
        "ex_ja": "休みなのに朝早くから会社に来させられた。",
        "ex_ko": "휴일인데도 아침 일찍부터 회사에 불려 나와야(오게 되어야) 했다.",
        "tags": ["JLPT_N2", "동사활용", "사역수동", "3그룹"]
    },
    {
        "cat": "사역수동",
        "badge": ("vt-badge-rev", "사역수동 역방향 판별 #11"),
        "q_title": "歩かされた（あるかされた）",
        "q_sub": "원형과 활용 종류는?",
        "a_head": "歩く（あるく） / 使役受身形（단축형）",
        "a_sub": "정식 형태: 歩かせられた",
        "sec_class": "vt-sec-blue",
        "meaning": "(억지로) 걸어야 했다",
        "rule_title": "📌 단축형 역방향 판별",
        "rule_content": "<b>〜かされる</b> ➔ 원형 어미는 <b>〜く</b><br>歩かされた ➔ 歩く",
        "ex_ja": "バスが故障して、炎天下を2キロも歩かされた。",
        "ex_ko": "버스가 고장 나서 뙤약볕 속을 2km나 걸어야 했다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "사역수동"]
    },
    {
        "cat": "사역수동",
        "badge": ("vt-badge-rev", "사역수동 역방향 판별 #12"),
        "q_title": "待たされた（またされた）",
        "q_sub": "원형과 활용 종류는?",
        "a_head": "待つ（まつ） / 使役受身形（단축형）",
        "a_sub": "정식 형태: 待たせられた",
        "sec_class": "vt-sec-blue",
        "meaning": "(어쩔 수 없이) 기다려야 했다",
        "rule_title": "📌 단축형 역방향 판별",
        "rule_content": "<b>〜たされる</b> ➔ 원형 어미는 <b>〜つ</b><br>待たされた ➔ 待つ",
        "ex_ja": "連絡もなく約束の場所で1時間も待たされた。",
        "ex_ko": "연락도 없이 약속 장소에서 1시간이나 기다려야 했다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "사역수동"]
    },
    {
        "cat": "사역수동",
        "badge": ("vt-badge-rev", "사역수동 역방향 판별 #13"),
        "q_title": "飲まされた（のまされた）",
        "q_sub": "원형과 활용 종류는?",
        "a_head": "飲む（のむ） / 使役受身形（단축형）",
        "a_sub": "정식 형태: 飲ませられた",
        "sec_class": "vt-sec-blue",
        "meaning": "(억지로) 마셔야 했다",
        "rule_title": "📌 단축형 역방향 판별",
        "rule_content": "<b>〜まされる</b> ➔ 원형 어미는 <b>〜む</b><br>飲まされた ➔ 飲む",
        "ex_ja": "飲み会で苦いお酒を無理やり飲まされた。",
        "ex_ko": "회식에서 쓴 술을 억지로 마셔야 했다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "사역수동"]
    },
    {
        "cat": "사역수동",
        "badge": ("vt-badge-rev", "사역수동 역방향 판별 #14"),
        "q_title": "考えさせられた（かんがえさせられた）",
        "q_sub": "원형과 활용 종류 및 N2 뉘앙스는?",
        "a_head": "考える（かんがえる / 2그룹） / 使役受身形",
        "a_sub": "N2 빈출: 깊이 생각하게 되다 / 많은 점을 느끼게 하다",
        "sec_class": "vt-sec-blue",
        "meaning": "깊이 생각하게 되었다 (많은 교훈을 얻음)",
        "rule_title": "📌 N2 빈출 사역수동 표현",
        "rule_content": "피해의 의미뿐 아니라 <b>'상황이나 경험으로 인해 깊은 생각을 품게 됨'</b>을 나타낼 때 자주 씁니다.<br>예: 考えさせられる問題 (생각하게 만드는 문제)",
        "ex_ja": "そのドキュメンタリーを見て、環境問題について深く考えさせられた。",
        "ex_ko": "그 다큐멘터리를 보고 환경 문제에 대해 깊이 생각하게 되었다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "사역수동", "N2빈출"]
    },

    # -------------------------------------------------------------------------
    # 8. 의향형 (意向形) & 명령형 (命令形) (12장)
    # -------------------------------------------------------------------------
    {
        "cat": "의향_명령",
        "badge": ("vt-badge-gen", "1그룹 의향형 생성 #01"),
        "q_title": "行く（いく） → 意向形",
        "q_sub": "1그룹 동사 「行く」의 의향형은?",
        "a_head": "行こう（いこう）",
        "a_sub": "1그룹 공식: お단 + う",
        "sec_class": "vt-sec",
        "meaning": "가자 / 가려고 한다",
        "rule_title": "📌 1그룹 의향형 규칙",
        "rule_content": "1그룹 동사는 어미를 <b>お단으로 바꾸고 う를 접속</b>합니다.<br>行く (く) ➔ 行<b>こ</b>う<br>※ 〜ようと思う (~하려고 생각하다) 문형과 결합 빈출!",
        "ex_ja": "週末は映画を見に行こうと思っている。",
        "ex_ko": "주말에는 영화를 보러 가려고 생각하고 있다.",
        "tags": ["JLPT_N2", "동사활용", "의향형", "1그룹"]
    },
    {
        "cat": "의향_명령",
        "badge": ("vt-badge-gen", "1그룹 의향형 생성 #02"),
        "q_title": "泳ぐ（およぐ） → 意向形",
        "q_sub": "1그룹 동사 「泳ぐ」의 의향형은?",
        "a_head": "泳ごう（およごう）",
        "a_sub": "う단(ぐ) ➔ お단(ご) + う",
        "sec_class": "vt-sec",
        "meaning": "수영하자",
        "rule_title": "📌 1그룹 의향형 규칙",
        "rule_content": "泳ぐ ➔ 泳<b>ご</b>う",
        "ex_ja": "暑いから市民プールへ泳ぎに行こう。",
        "ex_ko": "더우니까 시민 수영장에 수영하러 가자.",
        "tags": ["JLPT_N2", "동사활용", "의향형", "1그룹"]
    },
    {
        "cat": "의향_명령",
        "badge": ("vt-badge-gen", "1그룹 의향형 생성 #03"),
        "q_title": "話す（はなす） → 意向形",
        "q_sub": "1그룹 동사 「話す」의 의향형은?",
        "a_head": "話そう（はなそう）",
        "a_sub": "う단(す) ➔ お단(そ) + う",
        "sec_class": "vt-sec",
        "meaning": "이야기하자",
        "rule_title": "📌 1그룹 의향형 규칙",
        "rule_content": "話す ➔ 話<b>そ</b>う",
        "ex_ja": "これからの計画についてみんなで話そう。",
        "ex_ko": "앞으로의 계획에 대해 다 함께 이야기하자.",
        "tags": ["JLPT_N2", "동사활용", "의향형", "1그룹"]
    },
    {
        "cat": "의향_명령",
        "badge": ("vt-badge-gen", "2그룹 의향형 생성 #04"),
        "q_title": "食べる（たべる） → 意向形",
        "q_sub": "2그룹 동사 「食べる」의 의향형은?",
        "a_head": "食べよう（たべよう）",
        "a_sub": "2그룹 공식: 어간 + よう",
        "sec_class": "vt-sec",
        "meaning": "먹자 / 먹으려고 한다",
        "rule_title": "📌 2그룹 의향형 규칙",
        "rule_content": "2그룹 동사는 어미 る를 떼고 <b>よう</b>를 붙입니다.<br>食べる ➔ 食べ<b>よう</b> / 見る ➔ 見<b>よう</b>",
        "ex_ja": "お昼は何を食べようか。",
        "ex_ko": "점심은 무엇을 먹을까?",
        "tags": ["JLPT_N2", "동사활용", "의향형", "2그룹"]
    },
    {
        "cat": "의향_명령",
        "badge": ("vt-badge-gen", "3그룹 의향형 생성 #05"),
        "q_title": "する / 来る → 意向形",
        "q_sub": "3그룹 동사 「する」와 「来る」의 의향형은?",
        "a_head": "しよう / 来よう（こよう）",
        "a_sub": "する ➔ しよう / 来る ➔ こよう (발음 こ)",
        "sec_class": "vt-sec",
        "meaning": "하자 / 오자(오려고 한다)",
        "rule_title": "📌 3그룹 의향형",
        "rule_content": "• する ➔ <b>しよう</b><br>• 来る ➔ <b>来よう（こよう）</b>",
        "ex_ja": "明日もまたここに来よう。",
        "ex_ko": "내일도 또 여기에 오자.",
        "tags": ["JLPT_N2", "동사활용", "의향형", "3그룹"]
    },
    {
        "cat": "의향_명령",
        "badge": ("vt-badge-gen", "1그룹 명령형 생성 #06"),
        "q_title": "行く（いく） → 命令形",
        "q_sub": "1그룹 동사 「行く」의 명령형은?",
        "a_head": "行け（いけ）",
        "a_sub": "1그룹 공식: 어미 う단 ➔ え단 단독",
        "sec_class": "vt-sec",
        "meaning": "가라! (강한 명령)",
        "rule_title": "📌 1그룹 명령형 규칙",
        "rule_content": "1그룹 동사는 어미를 <b>え단으로 바꾸면 단독으로 명령형</b>이 됩니다.<br>行く (く) ➔ 行<b>け</b> / 書く ➔ 書<b>け</b>",
        "ex_ja": "ぐずぐずしないで早く行け！",
        "ex_ko": "우물쭈물하지 말고 빨리 가라!",
        "tags": ["JLPT_N2", "동사활용", "명령형", "1그룹"]
    },
    {
        "cat": "의향_명령",
        "badge": ("vt-badge-gen", "1그룹 명령형 생성 #07"),
        "q_title": "待つ（まつ） → 命令形",
        "q_sub": "1그룹 동사 「待つ」의 명령형은?",
        "a_head": "待て（まて）",
        "a_sub": "う단(つ) ➔ え단(て)",
        "sec_class": "vt-sec",
        "meaning": "기다려라! / 멈춰라!",
        "rule_title": "📌 1그룹 명령형 규칙",
        "rule_content": "待つ ➔ 待<b>て</b>",
        "ex_ja": "おい、待て！逃げるな！",
        "ex_ko": "야, 기다려(멈춰)! 도망치지 마라!",
        "tags": ["JLPT_N2", "동사활용", "명령형", "1그룹"]
    },
    {
        "cat": "의향_명령",
        "badge": ("vt-badge-gen", "1그룹 명령형 생성 #08"),
        "q_title": "止まる（とまる） → 命令形",
        "q_sub": "표지판/구호 빈출: 「止まる」의 명령형은?",
        "a_head": "止まれ（とまれ）",
        "a_sub": "도로 표지판 표준: 止まれ (정지/멈춤)",
        "sec_class": "vt-sec",
        "meaning": "멈춰라! / 정지",
        "rule_title": "📌 표지판의 명령형",
        "rule_content": "도로 표지판이나 비상 표시 등에서 <b>止まれ</b>가 빈출됩니다.",
        "ex_ja": "交差点の手前に「止まれ」の標識がある。",
        "ex_ko": "교차로 바로 앞에 '정지(멈춰라)' 표지판이 있다.",
        "tags": ["JLPT_N2", "동사활용", "명령형", "1그룹"]
    },
    {
        "cat": "의향_명령",
        "badge": ("vt-badge-gen", "2그룹 명령형 생성 #09"),
        "q_title": "見る / 食べる → 命令形",
        "q_sub": "2그룹 동사의 명령형 어미는?",
        "a_head": "見ろ / 食べろ（구어/문어: 見よ）",
        "a_sub": "2그룹 공식: 어간 + ろ (격식 문어: よ)",
        "sec_class": "vt-sec",
        "meaning": "봐라! / 먹어라!",
        "rule_title": "📌 2그룹 명령형 규칙",
        "rule_content": "2그룹 동사는 어미 る를 떼고 <b>ろ</b>를 붙입니다.<br>見る ➔ 見<b>ろ</b> / 食べる ➔ 食べ<b>ろ</b>",
        "ex_ja": "前をしっかり見ろ！",
        "ex_ko": "앞을 똑바로 봐라!",
        "tags": ["JLPT_N2", "동사활용", "명령형", "2그룹"]
    },
    {
        "cat": "의향_명령",
        "badge": ("vt-badge-gen", "3그룹 명령형 생성 #10"),
        "q_title": "する / 来る → 命令形",
        "q_sub": "3그룹 동사의 명령형은?",
        "a_head": "しろ（せよ） / 来い（こい）",
        "a_sub": "する ➔ しろ(せよ) / 来る ➔ こい",
        "sec_class": "vt-sec",
        "meaning": "해라! / 와라!",
        "rule_title": "📌 3그룹 명령형",
        "rule_content": "• する ➔ <b>しろ</b> (문어: せよ)<br>• 来る ➔ <b>来い（こい）</b>",
        "ex_ja": "早くこっちへ来い！",
        "ex_ko": "빨리 이쪽으로 와라!",
        "tags": ["JLPT_N2", "동사활용", "명령형", "3그룹"]
    },
    {
        "cat": "의향_명령",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형/종류 판별 #11"),
        "q_title": "始めよう（はじめよう）",
        "q_sub": "원형과 활용 종류는?",
        "a_head": "始める（はじめる / 2그룹） / 意向形",
        "a_sub": "2그룹 어미 る ➔ よう",
        "sec_class": "vt-sec-blue",
        "meaning": "시작하자 / 시작하려고 한다",
        "rule_title": "📌 의향형 판별",
        "rule_content": "<b>〜よう</b>로 끝나면 2그룹 또는 3그룹의 <b>의향형</b>입니다.",
        "ex_ja": "時間になったので、そろそろ会議を始めよう。",
        "ex_ko": "시간이 되었으니 슬슬 회의를 시작하자.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "의향형"]
    },
    {
        "cat": "의향_명령",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형/종류 판별 #12"),
        "q_title": "逃げろ（にげろ）",
        "q_sub": "원형과 활용 종류는?",
        "a_head": "逃げる（にげる / 2그룹） / 命令形",
        "a_sub": "2그룹 어미 る ➔ ろ",
        "sec_class": "vt-sec-blue",
        "meaning": "도망쳐라!",
        "rule_title": "📌 2그룹 명령형 판별",
        "rule_content": "<b>〜ろ</b>로 끝나면 2그룹 동사의 <b>명령형</b>입니다.",
        "ex_ja": "危ないから、早くあっちへ逃げろ！",
        "ex_ko": "위험하니까 빨리 저쪽으로 도망쳐라!",
        "tags": ["JLPT_N2", "동사활용", "역방향", "명령형"]
    },

    # -------------------------------------------------------------------------
    # 9. 가정형 (ば形) (10장)
    # -------------------------------------------------------------------------
    {
        "cat": "가정형",
        "badge": ("vt-badge-gen", "1그룹 ば형 생성 #01"),
        "q_title": "行く（いく） → ば形",
        "q_sub": "1그룹 동사 「行く」의 가정(ば)형은?",
        "a_head": "行けば（いけば）",
        "a_sub": "1그룹 공식: え단 + ば",
        "sec_class": "vt-sec",
        "meaning": "가면",
        "rule_title": "📌 1그룹 ば형 규칙",
        "rule_content": "1그룹 동사는 어미를 <b>え단으로 바꾸고 ば를 접속</b>합니다.<br>行く (く) ➔ 行<b>け</b>ば",
        "ex_ja": "まっすぐ行けば、右手に郵便局が見えます。",
        "ex_ko": "곧장 가면 오른쪽에 우체국이 보입니다.",
        "tags": ["JLPT_N2", "동사활용", "가정형", "ば형"]
    },
    {
        "cat": "가정형",
        "badge": ("vt-badge-gen", "1그룹 ば형 생성 #02"),
        "q_title": "読む（よむ） → ば形",
        "q_sub": "1그룹 동사 「読む」의 가정(ば)형은?",
        "a_head": "読めば（よめば）",
        "a_sub": "う단(む) ➔ え단(め) + ば",
        "sec_class": "vt-sec",
        "meaning": "읽으면",
        "rule_title": "📌 1그룹 ば형 규칙",
        "rule_content": "読む ➔ 読<b>め</b>ば",
        "ex_ja": "説明書を読めば、操作方法が分かります。",
        "ex_ko": "설명서를 읽으면 조작 방법을 알 수 있습니다.",
        "tags": ["JLPT_N2", "동사활용", "가정형", "ば형"]
    },
    {
        "cat": "가정형",
        "badge": ("vt-badge-gen", "1그룹 ば형 생성 #03"),
        "q_title": "話す（はなす） → ば形",
        "q_sub": "1그룹 동사 「話す」의 가정(ば)형은?",
        "a_head": "話せば（はなせば）",
        "a_sub": "う단(す) ➔ え단(せ) + ば",
        "sec_class": "vt-sec",
        "meaning": "이야기하면 / 털어놓으면",
        "rule_title": "📌 1그룹 ば형 규칙",
        "rule_content": "話す ➔ 話<b>せ</b>ば",
        "ex_ja": "正直に話せば、きっと理解してくれるはずだ。",
        "ex_ko": "솔직하게 이야기하면 분명히 이해해 줄 것이다.",
        "tags": ["JLPT_N2", "동사활용", "가정형", "ば형"]
    },
    {
        "cat": "가정형",
        "badge": ("vt-badge-gen", "1그룹 ば형 생성 #04"),
        "q_title": "待つ（まつ） → ば形",
        "q_sub": "1그룹 동사 「待つ」의 가정(ば)형은?",
        "a_head": "待てば（まてば）",
        "a_sub": "う단(つ) ➔ え단(て) + ば",
        "sec_class": "vt-sec",
        "meaning": "기다리면",
        "rule_title": "📌 1그룹 ば형 규칙",
        "rule_content": "待つ ➔ 待<b>て</b>ば",
        "ex_ja": "少し待てば、雨もやむだろう。",
        "ex_ko": "조금 기다리면 비도 그치겠지.",
        "tags": ["JLPT_N2", "동사활용", "가정형", "ば형"]
    },
    {
        "cat": "가정형",
        "badge": ("vt-badge-gen", "2그룹 ば형 생성 #05"),
        "q_title": "食べる（たべる） → ば形",
        "q_sub": "2그룹 동사 「食べる」의 가정(ば)형은?",
        "a_head": "食べれば（たべれば）",
        "a_sub": "2그룹 공식: 어미 る ➔ れば",
        "sec_class": "vt-sec",
        "meaning": "먹으면",
        "rule_title": "📌 2그룹 ば형 규칙",
        "rule_content": "2그룹 동사는 어미 る를 떼고 <b>れば</b>를 붙입니다.<br>食べる ➔ 食べ<b>れば</b> / 見る ➔ 見<b>れば</b>",
        "ex_ja": "一口食べれば、その美味しさが分かります。",
        "ex_ko": "한 입 먹어보면 그 맛을 알 수 있습니다.",
        "tags": ["JLPT_N2", "동사활용", "가정형", "ば형"]
    },
    {
        "cat": "가정형",
        "badge": ("vt-badge-gen", "2그룹 ば형 생성 #06"),
        "q_title": "見る（みる） → ば形",
        "q_sub": "2그룹 동사 「見る」의 가정(ば)형은?",
        "a_head": "見れば（みれば）",
        "a_sub": "2그룹 공식: 어미 る ➔ れば",
        "sec_class": "vt-sec",
        "meaning": "보면",
        "rule_title": "📌 2그룹 ば형 규칙",
        "rule_content": "見る ➔ 見<b>れば</b>",
        "ex_ja": "写真を見れば、当時の楽しかった思い出がよみがえる。",
        "ex_ko": "사진을 보면 당시의 즐거웠던 추억이 되살아난다.",
        "tags": ["JLPT_N2", "동사활용", "가정형", "ば형"]
    },
    {
        "cat": "가정형",
        "badge": ("vt-badge-gen", "3그룹 ば형 생성 #07"),
        "q_title": "する / 来る → ば形",
        "q_sub": "3그룹 동사의 가정(ば)형은?",
        "a_head": "すれば / 来れば（くれば）",
        "a_sub": "する ➔ すれば / 来る ➔ くれば (발음 く)",
        "sec_class": "vt-sec",
        "meaning": "하면 / 오면",
        "rule_title": "📌 3그룹 ば형",
        "rule_content": "• する ➔ <b>すれば</b><br>• 来る ➔ <b>来れば（くれば）</b>",
        "ex_ja": "連絡さえしてくれれば、迎えに行ったのに。",
        "ex_ko": "연락이라도 해 주었으면 마중 나갔을 텐데.",
        "tags": ["JLPT_N2", "동사활용", "가정형", "ば형"]
    },
    {
        "cat": "가정형",
        "badge": ("vt-badge-gen", "★부정형의 ば형 (〜なければ) #08"),
        "q_title": "書かない（かかない） → ば形",
        "q_sub": "부정(ない)형의 가정(ば)형태는?",
        "a_head": "書かなければ（かかなければ）",
        "a_sub": "ない(이형용사 활용) ➔ なければ (~하지 않으면)",
        "sec_class": "vt-sec",
        "meaning": "쓰지 않으면",
        "rule_title": "📌 부정형의 가정법 공식",
        "rule_content": "ない형의 어미 い를 <b>ければ</b>로 바꿉니다. (N2 핵심 의무 문형: 〜なければならない)",
        "ex_ja": "期日までに申請書を出さなければならない。",
        "ex_ko": "기일까지 신청서를 제출하지 않으면 안 된다(제출해야 한다).",
        "tags": ["JLPT_N2", "동사활용", "가정형", "부정가정"]
    },
    {
        "cat": "가정형",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형/종류 판별 #09"),
        "q_title": "急げば（いそげば）",
        "q_sub": "원형과 활용 종류는?",
        "a_head": "急ぐ（いそぐ） / ば形（가정형）",
        "a_sub": "1그룹 어미 ぐ ➔ げ + ば",
        "sec_class": "vt-sec-blue",
        "meaning": "서두르면",
        "rule_title": "📌 ば형 판별",
        "rule_content": "<b>〜げば</b> ➔ 원형 어미는 <b>〜ぐ</b>",
        "ex_ja": "今から急げば、終電に間に合うかもしれない。",
        "ex_ko": "지금부터 서두르면 막차 시간에 댈 수 있을지도 모른다.",
        "tags": ["JLPT_N2", "동사활용", "역방향", "ば형"]
    },
    {
        "cat": "가정형",
        "badge": ("vt-badge-rev", "활용형 ➔ 원형/종류 판별 #10"),
        "q_title": "安ければ（やすければ）",
        "q_sub": "원형 품사와 활용 종류는?",
        "a_head": "安い（やすい / イ형용사） / ば形",
        "a_sub": "이형용사의 가정형 어미: 〜ければ",
        "sec_class": "vt-sec-blue",
        "meaning": "저렴하다면 / 싸다면",
        "rule_title": "📌 이형용사의 ば형 규칙",
        "rule_content": "이형용사는 어미 い를 떼고 <b>ければ</b>를 붙입니다.<br>安い ➔ 安<b>ければ</b> / いい(よい) ➔ <b>よければ</b>",
        "ex_ja": "値段が安ければ、多少の不便は我慢できる。",
        "ex_ko": "가격이 저렴하다면 다소의 불편함은 참을 수 있다.",
        "tags": ["JLPT_N2", "동사활용", "형용사", "ば형"]
    },

    # -------------------------------------------------------------------------
    # 10. 종합 핵심 동사 10대 관통 마스터 (10장)
    # -------------------------------------------------------------------------
    {
        "cat": "종합관통",
        "badge": ("vt-badge-comp", "종합 활용 관통 마스터 #01"),
        "q_title": "書く（かく / 1그룹） — 10대 핵심 활용 총정리",
        "q_sub": "ます・ない・て・た・可能・受身・使役・使役受身・意向・ば 형태는?",
        "a_head": "書く（かく） 10대 활용 일람",
        "a_sub": "1그룹 대표 어미 く의 완벽한 궤도",
        "sec_class": "vt-sec",
        "meaning": "쓰다",
        "rule_title": "📌 書く 10대 활용표",
        "rule_content": "• ます: <b>書きます</b><br>• ない: <b>書かない</b><br>• て/た: <b>書いて / 書いた</b><br>• 가능: <b>書ける</b><br>• 수동: <b>書かれる</b><br>• 사역: <b>書かせる</b><br>• 사역수동: <b>書かせられる / 書かされる</b><br>• 의향: <b>書こう</b><br>• 명령: <b>書け</b><br>• 가정: <b>書けば</b>",
        "ex_ja": "論文を最後まで書ききった。",
        "ex_ko": "논문을 끝까지 다 써냈다.",
        "tags": ["JLPT_N2", "동사활용", "종합관통", "1그룹"]
    },
    {
        "cat": "종합관통",
        "badge": ("vt-badge-comp", "종합 활용 관통 마스터 #02"),
        "q_title": "読む（よむ / 1그룹） — 10대 핵심 활용 총정리",
        "q_sub": "ます・ない・て・た・可能・受身・使役・使役受身・意向・ば 형태는?",
        "a_head": "読む（よむ） 10대 활용 일람",
        "a_sub": "1그룹 발음편(む)의 완벽한 궤도",
        "sec_class": "vt-sec",
        "meaning": "읽다",
        "rule_title": "📌 読む 10대 활용표",
        "rule_content": "• ます: <b>読みます</b><br>• ない: <b>読まない</b><br>• て/た: <b>読んで / 読んだ</b> (발음편!)<br>• 가능: <b>読める</b><br>• 수동: <b>読まれる</b><br>• 사역: <b>読ませる</b><br>• 사역수동: <b>読ませられる / 読まされる</b><br>• 의향: <b>読もう</b><br>• 명령: <b>読め</b><br>• 가정: <b>読めば</b>",
        "ex_ja": "一晩中小説を読みふけった。",
        "ex_ko": "밤새도록 소설에 푹 빠져 읽었다.",
        "tags": ["JLPT_N2", "동사활용", "종합관통", "1그룹"]
    },
    {
        "cat": "종합관통",
        "badge": ("vt-badge-comp", "종합 활용 관통 마스터 #03"),
        "q_title": "話す（はなす / 1그룹） — 10대 핵심 활용 총정리",
        "q_sub": "ます・ない・て・た・可能・受身・使役・使役受身・意向・ば 형태는?",
        "a_head": "話す（はなす） 10대 활용 일람",
        "a_sub": "어미 す 동사의 단축형 불가 주의!",
        "sec_class": "vt-sec",
        "meaning": "말하다",
        "rule_title": "📌 話す 10대 활용표",
        "rule_content": "• ます: <b>話します</b><br>• ない: <b>話さない</b><br>• て/た: <b>話して / 話した</b><br>• 가능: <b>話せる</b><br>• 수동: <b>話される</b><br>• 사역: <b>話させる</b><br>• 사역수동: <b>話させられる</b> (※話さされる 불가!)<br>• 의향: <b>話そう</b><br>• 명령: <b>話せ</b><br>• 가정: <b>話せば</b>",
        "ex_ja": "本音を包み隠さず話した。",
        "ex_ko": "본심을 숨김없이 솔직히 털어놓았다.",
        "tags": ["JLPT_N2", "동사활용", "종합관통", "1그룹"]
    },
    {
        "cat": "종합관통",
        "badge": ("vt-badge-comp", "종합 활용 관통 마스터 #04"),
        "q_title": "食べる（たべる / 2그룹） — 10대 핵심 활용 총정리",
        "q_sub": "ます・ない・て・た・可能・受身・使役・使役受身・意向・ば 형태는?",
        "a_head": "食べる（たべる） 10대 활용 일람",
        "a_sub": "2그룹 하1단 동사의 규칙적 궤도",
        "sec_class": "vt-sec",
        "meaning": "먹다",
        "rule_title": "📌 食べる 10대 활용표",
        "rule_content": "• ます: <b>食べます</b><br>• ない: <b>食べない</b><br>• て/た: <b>食べて / 食べた</b><br>• 가능/수동: <b>食べられる</b><br>• 사역: <b>食べさせる</b><br>• 사역수동: <b>食べさせられる</b><br>• 의향: <b>食べよう</b><br>• 명령: <b>食べろ</b><br>• 가정: <b>食べれば</b>",
        "ex_ja": "バランスの良い食事を食べるようにしている。",
        "ex_ko": "균형 잡힌 식사를 하도록(먹도록) 하고 있다.",
        "tags": ["JLPT_N2", "동사활용", "종합관통", "2그룹"]
    },
    {
        "cat": "종합관통",
        "badge": ("vt-badge-comp", "종합 활용 관통 마스터 #05"),
        "q_title": "見る（みる / 2그룹） — 10대 핵심 활용 총정리",
        "q_sub": "ます・ない・て・た・可能・受身・使役・使役受身・意向・ば 형태는?",
        "a_head": "見る（みる） 10대 활용 일람",
        "a_sub": "2그룹 상1단 동사의 규칙적 궤도",
        "sec_class": "vt-sec",
        "meaning": "보다",
        "rule_title": "📌 見る 10대 활용표",
        "rule_content": "• ます: <b>見ます</b><br>• ない: <b>見ない</b><br>• て/た: <b>見て / 見た</b><br>• 가능/수동: <b>見られる</b><br>• 사역: <b>見させる</b><br>• 사역수동: <b>見させられる</b><br>• 의향: <b>見よう</b><br>• 명령: <b>見ろ</b><br>• 가정: <b>見れば</b>",
        "ex_ja": "物事を多角的な視点から見る。",
        "ex_ko": "사물을 다각적인 관점에서 보다.",
        "tags": ["JLPT_N2", "동사활용", "종합관통", "2그룹"]
    },
    {
        "cat": "종합관통",
        "badge": ("vt-badge-comp", "종합 활용 관통 마스터 #06"),
        "q_title": "する（3그룹 변격） — 10대 핵심 활용 총정리",
        "q_sub": "ます・ない・て・た・可能・受身・使役・使役受身・意向・ば 형태는?",
        "a_head": "する 10대 활용 일람",
        "a_sub": "불규칙 사행 변격 동사의 완전 정리",
        "sec_class": "vt-sec",
        "meaning": "하다",
        "rule_title": "📌 する 10대 활용표",
        "rule_content": "• ます: <b>します</b><br>• ない: <b>しない</b><br>• て/た: <b>して / した</b><br>• 가능: <b>できる</b>★<br>• 수동: <b>される</b><br>• 사역: <b>させる</b><br>• 사역수동: <b>させられる</b><br>• 의향: <b>しよう</b><br>• 명령: <b>しろ（せよ）</b><br>• 가정: <b>すれば</b>",
        "ex_ja": "全力を尽くして後悔のないようにする。",
        "ex_ko": "전력을 다해 후회가 없도록 한다.",
        "tags": ["JLPT_N2", "동사활용", "종합관통", "3그룹"]
    },
    {
        "cat": "종합관통",
        "badge": ("vt-badge-comp", "종합 활용 관통 마스터 #07"),
        "q_title": "来る（くる / 3그룹） — 10대 핵심 활용 총정리",
        "q_sub": "한자 읽기 변화(くる, きます, こない, こられる)에 주의한 전 형태는?",
        "a_head": "来る（くる） 10대 활용 일람",
        "a_sub": "카행 변격 동사의 한자 음독 변화 완벽 정복!",
        "sec_class": "vt-sec",
        "meaning": "오다",
        "rule_title": "📌 来る 10대 활용표",
        "rule_content": "• ます: 来ます（<b>きます</b>）<br>• ない: 来ない（<b>こない</b>）★<br>• て/た: 来て / 来た（<b>きて / きた</b>）<br>• 가능/수동: 来られる（<b>こられる</b>）★<br>• 사역: 来させる（<b>こさせる</b>）★<br>• 사역수동: 来させられる（<b>こさせられる</b>）<br>• 의향: 来よう（<b>こよう</b>）★<br>• 명령: 来い（<b>こい</b>）★<br>• 가정: 来れば（<b>くれば</b>）",
        "ex_ja": "苦しい時期を乗り越えてここまで来た。",
        "ex_ko": "힘든 시기를 극복하고 여기까지 왔다.",
        "tags": ["JLPT_N2", "동사활용", "종합관통", "3그룹"]
    },
    {
        "cat": "종합관통",
        "badge": ("vt-badge-comp", "종합 활용 관통 마스터 #08"),
        "q_title": "帰る（かえる / 1그룹 예외） — 10대 핵심 활용 총정리",
        "q_sub": "2그룹이 아닌 1그룹으로 활용하는 帰る의 10대 형태는?",
        "a_head": "帰る（かえる） 10대 활용 일람",
        "a_sub": "1그룹 예외 동사의 실수 없는 전 형태",
        "sec_class": "vt-sec",
        "meaning": "돌아가다",
        "rule_title": "📌 帰る 10대 활용표",
        "rule_content": "• ます: <b>帰ります</b><br>• ない: <b>帰らない</b><br>• て/た: <b>帰って / 帰った</b> (촉음편!)<br>• 가능: <b>帰れる</b><br>• 수동: <b>帰られる</b><br>• 사역: <b>帰らせる</b><br>• 사역수동: <b>帰らせられる / 帰らされる</b><br>• 의향: <b>帰ろう</b><br>• 명령: <b>帰れ</b><br>• 가정: <b>帰れば</b>",
        "ex_ja": "故郷に帰って新しい事業を始める予定だ。",
        "ex_ko": "고향에 돌아가서 새로운 사업을 시작할 예정이다.",
        "tags": ["JLPT_N2", "동사활용", "종합관통", "1그룹예외"]
    },
    {
        "cat": "종합관통",
        "badge": ("vt-badge-comp", "종합 활용 관통 마스터 #09"),
        "q_title": "行く（いく / 음편 예외） — 10대 핵심 활용 총정리",
        "q_sub": "촉음편(行って) 예외를 지닌 行く의 10대 핵심 형태는?",
        "a_head": "行く（いく） 10대 활용 일람",
        "a_sub": "음편 특수 예외 行く의 정확한 궤도",
        "sec_class": "vt-sec",
        "meaning": "가다",
        "rule_title": "📌 行く 10대 활용표",
        "rule_content": "• ます: <b>行きます</b><br>• ない: <b>行かない</b><br>• て/た: <b>行って / 行った</b>★ (촉음편 예외!)<br>• 가능: <b>行ける</b><br>• 수동: <b>行かれる</b><br>• 사역: <b>行かせる</b><br>• 사역수동: <b>行かせられる / 行かされる</b><br>• 의향: <b>行こう</b><br>• 명령: <b>行け</b><br>• 가정: <b>行けば</b>",
        "ex_ja": "目的地に向かってまっすぐ歩いて行った。",
        "ex_ko": "목적지를 향해 곧장 걸어갔다.",
        "tags": ["JLPT_N2", "동사활용", "종합관통", "음편예외"]
    },
    {
        "cat": "종합관통",
        "badge": ("vt-badge-comp", "종합 활용 관통 마스터 #10"),
        "q_title": "買う（かう / う➔わ형） — 10대 핵심 활용 총정리",
        "q_sub": "어미 う의 わ단 변환을 지닌 買う의 10대 핵심 형태는?",
        "a_head": "買う（かう） 10대 활용 일람",
        "a_sub": "어미 う의 규칙적 궤도",
        "sec_class": "vt-sec",
        "meaning": "사다",
        "rule_title": "📌 買う 10대 활용표",
        "rule_content": "• ます: <b>買います</b><br>• ない: <b>買わない</b>★ (う➔わ)<br>• て/た: <b>買って / 買った</b> (촉음편)<br>• 가능: <b>買える</b><br>• 수동: <b>買われる</b><br>• 사역: <b>買わせる</b><br>• 사역수동: <b>買わせられる / 買わされる</b><br>• 의향: <b>買おう</b><br>• 명령: <b>買え</b><br>• 가정: <b>買えば</b>",
        "ex_ja": "安さにつられて余計なものまで買ってしまった。",
        "ex_ko": "저렴한 가격에 이끌려 쓸데없는 것까지 사 버렸다.",
        "tags": ["JLPT_N2", "동사활용", "종합관통", "1그룹"]
    },
]


def render_front(item: dict) -> str:
    badge_cls, badge_text = item["badge"]
    return (
        f'{CSS_BLOCK}'
        f'<div class="vt-wrap vt-center">'
        f'<span class="vt-badge {badge_cls}">{badge_text}</span>'
        f'<div class="vt-title">{item["q_title"]}</div>'
        f'<div class="vt-sub">{item["q_sub"]}</div>'
        f'</div>'
    )


def render_back(item: dict) -> str:
    sec_cls = item.get("sec_class", "vt-sec")
    is_blue = "blue" in sec_cls
    head_cls = "vt-ans-head-blue" if is_blue else "vt-ans-head"

    return (
        f'{CSS_BLOCK}'
        f'<div class="vt-wrap">'
        f'<div class="{head_cls}">{item["a_head"]}</div>'
        f'<div class="{sec_cls}">'
        f'<div class="vt-meaning">＝ {item["meaning"]}</div>'
        f'<div style="font-size:14px; color:#cbd5e1; margin-top:2px;">{item["a_sub"]}</div>'
        f'<div class="vt-ex-ja"><span class="vt-tag">예문:</span> {item["ex_ja"]}</div>'
        f'<div class="vt-ex-ko">{item["ex_ko"]}</div>'
        f'</div>'
        f'<div class="vt-rule-box">'
        f'<div class="vt-rule-title">{item["rule_title"]}</div>'
        f'<div class="vt-rule-content">{item["rule_content"]}</div>'
        f'</div>'
        f'</div>'
    )


def mcp(method: str, params: dict, request_id: int) -> dict:
    data = json.dumps({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        body = response.read().decode("utf-8")
    payload = json.loads(next(line[6:] for line in body.splitlines() if line.startswith("data: ")))
    if "error" in payload:
        raise RuntimeError(payload["error"])
    return payload["result"]


def tool(name: str, arguments: dict, request_id: int) -> dict:
    result = mcp("tools/call", {"name": name, "arguments": arguments}, request_id)
    if result.get("isError"):
        raise RuntimeError(result)
    if "structuredContent" in result:
        return result["structuredContent"]
    return json.loads(next(x["text"] for x in result["content"] if x["type"] == "text"))


def main():
    print(f"Total curated cards in dataset: {len(CARDS_DATA)}")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # 1. Export TSV
    tsv_rows = [
        "#separator:Tab",
        "#html:true",
        f"#deck:{DECK_NAME}",
        "#tags column:3",
        "#columns:Front\tBack\tTags"
    ]

    notes_to_add = []
    for item in CARDS_DATA:
        f_raw = render_front(item).replace("\t", " ").replace("\n", "")
        b_raw = render_back(item).replace("\t", " ").replace("\n", "")
        tags_str = " ".join(item["tags"])
        tsv_rows.append(f"{f_raw}\t{b_raw}\t{tags_str}")

        notes_to_add.append({
            "fields": {"Front": f_raw, "Back": b_raw},
            "tags": item["tags"],
        })

    OUTPUT_FILE.write_text("\n".join(tsv_rows) + "\n", encoding="utf-8")
    print(f"Saved clean TSV to: {OUTPUT_FILE}")

    # 2. Add to Anki via MCP
    mcp("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "verb-deck-builder", "version": "1.0"}}, 1)

    # Create deck
    deck_res = tool("create_deck", {"deck_name": DECK_NAME}, 2)
    print("Create deck response:", deck_res)

    # Check existing notes
    exist_check = tool("find_notes", {"query": f'deck:"{DECK_NAME}"', "limit": 200}, 3)
    existing_count = exist_check.get("count", 0)
    print(f"Existing notes in deck '{DECK_NAME}': {existing_count}")

    if existing_count == len(CARDS_DATA):
        print("All cards already exist in deck. Verifying note count...")
    else:
        if existing_count > 0:
            print(f"Deleting partial {existing_count} notes before clean import...")
            tool("delete_notes", {"notes": exist_check["noteIds"], "confirmDeletion": True}, 4)

        # Batch add notes in chunks of 50
        chunk_size = 50
        req_id = 10
        total_created = 0
        for i in range(0, len(notes_to_add), chunk_size):
            chunk = notes_to_add[i:i + chunk_size]
            res = tool("add_notes", {
                "deck_name": DECK_NAME,
                "model_name": MODEL,
                "notes": chunk,
                "tags": ["JLPT_N2", "동사활용"],
                "allow_duplicate": False,
            }, req_id)
            req_id += 1
            created = res.get("created", len(chunk))
            total_created += created
            print(f"Batch {i//chunk_size + 1} added: {created} notes")

        print(f"Successfully added {total_created} notes to '{DECK_NAME}'!")

    # Verify final count
    verified = tool("find_notes", {"query": f'deck:"{DECK_NAME}"', "limit": 300}, 20)
    final_count = verified.get("count", 0)
    print(f"Verified final note count in '{DECK_NAME}': {final_count}")
    assert final_count == len(CARDS_DATA), f"Expected {len(CARDS_DATA)}, got {final_count}"

    # Sample note check
    sample_ids = verified["noteIds"][:2] + verified["noteIds"][-2:]
    info = tool("notes_info", {"notes": sample_ids}, 21)
    for idx, n in enumerate(info.get("notes", []), 1):
        print(f"\n--- Sample Note {idx} (ID: {n['noteId']}) ---")
        f = n["fields"]["Front"]["value"]
        b = n["fields"]["Back"]["value"]
        print("Front (snippet):", f[-120:])
        print("Back (snippet):", b[-120:])
        assert not f.endswith('"'), "Found trailing quote in Front!"
        assert not b.endswith('"'), "Found trailing quote in Back!"

    print("\n[SUCCESS] JLPT N2::03 동사 활용 덱이 완벽하게 생성 및 반영되었습니다!")


if __name__ == "__main__":
    main()
