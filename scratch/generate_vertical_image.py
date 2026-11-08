# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Dimensions: 1080 x 1660 (Vertical 2:3 ratio / mobile card format)
width = 1080
height = 1660

img = Image.new("RGB", (width, height), "#F8FAFC")
draw = ImageDraw.Draw(img)

# Fonts
font_bold_path = "C:/Windows/Fonts/YuGothB.ttc"
font_med_path = "C:/Windows/Fonts/YuGothM.ttc"

try:
    f_title = ImageFont.truetype(font_bold_path, 36)
    f_subtitle = ImageFont.truetype(font_med_path, 21)
    f_section = ImageFont.truetype(font_bold_path, 25)
    f_card_title = ImageFont.truetype(font_bold_path, 24)
    f_badge = ImageFont.truetype(font_bold_path, 17)
    f_tag = ImageFont.truetype(font_bold_path, 16)
    f_stat_num = ImageFont.truetype(font_bold_path, 32)
    f_stat_label = ImageFont.truetype(font_med_path, 18)
    f_body = ImageFont.truetype(font_med_path, 20)
    f_body_bold = ImageFont.truetype(font_bold_path, 20)
    f_footer_title = ImageFont.truetype(font_bold_path, 20)
    f_footer = ImageFont.truetype(font_med_path, 19)
except Exception:
    f_title = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 36)
    f_subtitle = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 21)
    f_section = f_card_title = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 24)
    f_badge = f_tag = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 16)
    f_stat_num = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 32)
    f_stat_label = f_body = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 20)
    f_body_bold = f_footer_title = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 20)
    f_footer = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 19)

margin_x = 48
curr_y = 56

# Header Card
header_h = 160
draw.rounded_rectangle([margin_x, curr_y, width - margin_x, curr_y + header_h], radius=24, fill="#1E293B")

# Top mini tag inside header
draw.rounded_rectangle([margin_x + 36, curr_y + 26, margin_x + 130, curr_y + 54], radius=6, fill="#3B82F6")
draw.text((margin_x + 48, curr_y + 30), "REPORT", font=f_tag, fill="#FFFFFF")

# Title inside header
draw.text((margin_x + 36, curr_y + 64), "JLPT N2 学習記録 & 推移", font=f_title, fill="#FFFFFF")
draw.text((margin_x + 36, curr_y + 114), "75日間 Anki学習・日本語単語2,797語 90%暗記完了", font=f_subtitle, fill="#94A3B8")

curr_y += header_h + 30

# 3-Column Hero Metrics Cards
hero_h = 150
hero_gap = 18
hero_w = (width - margin_x * 2 - hero_gap * 2) // 3

heroes = [
    ("学習日数", "75日", "皆勤 100%（無休）", "#3B82F6"),
    ("総純学習時間", "240.4h", "14,426分 (実測)", "#10B981"),
    ("1日平均時間", "3h 12m", "192.3分 / 日", "#8B5CF6")
]

for idx, (label, num, sub, color) in enumerate(heroes):
    hx = margin_x + idx * (hero_w + hero_gap)
    draw.rounded_rectangle([hx, curr_y, hx + hero_w, curr_y + hero_h], radius=20, fill="#FFFFFF", outline="#E2E8F0", width=2)
    # top accent line
    draw.rounded_rectangle([hx + 12, curr_y + 12, hx + hero_w - 12, curr_y + 18], radius=3, fill=color)
    draw.text((hx + 24, curr_y + 30), label, font=f_stat_label, fill="#64748B")
    draw.text((hx + 24, curr_y + 60), num, font=f_stat_num, fill="#0F172A")
    draw.text((hx + 24, curr_y + 106), sub, font=f_stat_label, fill=color)

curr_y += hero_h + 34

# Section Title
draw.text((margin_x + 4, curr_y), "■ 月別 学習推移 & 集中領域", font=f_section, fill="#0F172A")
curr_y += 46

# Monthly Stacked Cards
months_data = [
    {
        "month": "全体累計",
        "tag": "75日累計 (8/26〜11/08)",
        "tag_bg": "#EEF2FF",
        "tag_fg": "#4338CA",
        "stats": "総 14,426分 (240時間26分)  |  1日平均 192.3分 (3時間12分)",
        "focus": "カリキュラム全体の走破（N3基礎 → N2文法150 → 語彙2,797語）",
        "card_bg": "#F8FAFC",
        "border": "#CBD5E1"
    },
    {
        "month": "8月",
        "tag": "6日 (8/26〜8/31)",
        "tag_bg": "#EFF6FF",
        "tag_fg": "#1D4ED8",
        "stats": "2,000分 (33.3時間)  |  1日平均 333.3分 (5時間33分)",
        "focus": "N3基礎の完成およびN2文法入門",
        "card_bg": "#FFFFFF",
        "border": "#E2E8F0"
    },
    {
        "month": "9月",
        "tag": "30日 (9/01〜9/30)",
        "tag_bg": "#ECFDF5",
        "tag_fg": "#047857",
        "stats": "7,827分 (130.5時間)  |  1日平均 260.9分 (4시간21分)".replace("시간", "時間"),
        "focus": "N2文法150文型完講および実戦模試1・2回 走破",
        "card_bg": "#FFFFFF",
        "border": "#E2E8F0"
    },
    {
        "month": "10月",
        "tag": "31日 (10/01〜10/31)",
        "tag_bg": "#FEF3C7",
        "tag_fg": "#B45309",
        "stats": "4,205分 (70.1時間)  |  1日平均 135.6分 (2時間16分)",
        "focus": "単語帳2,797語 100%走破・多周回・記憶定着",
        "card_bg": "#FFFFFF",
        "border": "#E2E8F0"
    },
    {
        "month": "11月",
        "tag": "8日 (11/01〜11/08 進行中)",
        "tag_bg": "#F3E8FF",
        "tag_fg": "#7E22CE",
        "stats": "394分 (6.6時間)  |  1日平均 49.2分 (0時間49分)",
        "focus": "単語の長期記憶維持・周回（想起8.15秒・Again 18.8%へ激減）",
        "card_bg": "#FFFFFF",
        "border": "#E2E8F0"
    }
]

card_h = 160
card_gap = 18

for item in months_data:
    card_top = curr_y
    draw.rounded_rectangle(
        [margin_x, card_top, width - margin_x, card_top + card_h], 
        radius=18, 
        fill=item["card_bg"], 
        outline=item["border"], 
        width=2
    )

    # Title & Badge
    draw.text((margin_x + 28, card_top + 22), item["month"], font=f_card_title, fill="#0F172A")
    badge_x = margin_x + 130
    badge_w = draw.textbbox((0, 0), item["tag"], font=f_badge)[2] + 20
    draw.rounded_rectangle([badge_x, card_top + 20, badge_x + badge_w, card_top + 50], radius=8, fill=item["tag_bg"])
    draw.text((badge_x + 10, card_top + 24), item["tag"], font=f_badge, fill=item["tag_fg"])

    # Bullet 1: Time stats
    draw.rounded_rectangle([margin_x + 28, card_top + 73, margin_x + 78, card_top + 97], radius=5, fill="#E2E8F0")
    draw.text((margin_x + 34, card_top + 75), "時間", font=f_tag, fill="#475569")
    draw.text((margin_x + 90, card_top + 72), item["stats"], font=f_body_bold, fill="#1E293B")

    # Bullet 2: Focus
    draw.rounded_rectangle([margin_x + 28, card_top + 111, margin_x + 78, card_top + 135], radius=5, fill="#E0F2FE")
    draw.text((margin_x + 34, card_top + 113), "重点", font=f_tag, fill="#0369A1")
    draw.text((margin_x + 90, card_top + 110), item["focus"], font=f_body, fill="#475569")

    curr_y += card_h + card_gap

curr_y += 10

# Bottom Key Takeaway Callout Card
callout_h = 100
draw.rounded_rectangle(
    [margin_x, curr_y, width - margin_x, curr_y + callout_h],
    radius=16,
    fill="#EFF6FF",
    outline="#BFDBFE",
    width=2
)
draw.text((margin_x + 24, curr_y + 18), "【POINT】 学習効率の変化", font=f_footer_title, fill="#1D4ED8")
draw.text((margin_x + 24, curr_y + 46), "初期は新規単語の負荷で毎日5時間以上の暗記が必要でしたが、", font=f_footer, fill="#1E40AF")
draw.text((margin_x + 24, curr_y + 70), "現在は90%以上が定着し、1日30〜40分へと大幅に短縮・安定化しました。", font=f_footer, fill="#1E40AF")

# Output path
out_file = Path("outputs/jlpt_75days_study_stats_vertical_ja.png")
out_file.parent.mkdir(exist_ok=True, parents=True)
img.save(out_file, quality=95)
print(f"Regenerated cleanly: {out_file.resolve()}")
