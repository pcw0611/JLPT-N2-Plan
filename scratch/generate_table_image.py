# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Data
headers = ["区分", "学習日数", "総純学習時間", "1日平均学習時間", "主な集中領域"]
rows = [
    ["全体累計", "75日 (皆勤 100%)", "14,426分 (240時間26分)", "192.3分 (3時間12分)", "カリキュラム全体の走破"],
    ["8月 (8/26~8/31)", "6日", "2,000分 (33.3時間)", "333.3分 (5時間33分)", "N3基礎完成およびN2文法入門"],
    ["9月 (9/01~9/30)", "30日", "7,827分 (130.5時間)", "260.9分 (4時間21分)", "N2文法150文型完講および実戦模試1・2回"],
    ["10月 (10/01~10/31)", "31日", "4,205分 (70.1時間)", "135.6分 (2시간16分)", "単語帳2,797語 100%走破および多周回"],
    ["11月 (11/01~11/08)", "8日 (進行中)", "394分 (6.6時間)", "49.2分 (0時間49分)", "単語の長期記憶維持・周回 (想起の高速化)"]
]

for r in rows:
    r[2] = r[2].replace("시간", "時間")
    r[3] = r[3].replace("시간", "時間")

scale = 2  # 2x Retina scale

col_widths = [int(w * scale) for w in [220, 190, 280, 250, 460]]
row_height = 58 * scale
header_height = 64 * scale
padding_x = 40 * scale
padding_y = 40 * scale
title_height = 50 * scale

img_width = sum(col_widths) + padding_x * 2
img_height = title_height + header_height + row_height * len(rows) + padding_y * 2

font_path = "C:/Windows/Fonts/YuGothM.ttc"
font_bold_path = "C:/Windows/Fonts/YuGothB.ttc"

try:
    font_main_title = ImageFont.truetype(font_bold_path, 22 * scale)
    font_header = ImageFont.truetype(font_bold_path, 17 * scale)
    font_bold = ImageFont.truetype(font_bold_path, 16 * scale)
    font = ImageFont.truetype(font_path, 16 * scale)
except Exception:
    font_main_title = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 22 * scale)
    font_header = font_bold = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 16 * scale)
    font = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 16 * scale)

img = Image.new("RGB", (img_width, img_height), "#F8FAFC")
draw = ImageDraw.Draw(img)

# Title
draw.text((padding_x + 8 * scale, padding_y - 8 * scale), "■ JLPT N2 学習時間および推移（75日間累計）", font=font_main_title, fill="#0F172A")

card_x1 = padding_x
card_y1 = padding_y + title_height
card_x2 = img_width - padding_x
card_y2 = img_height - padding_y

# Background of card
draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=16 * scale, fill="#FFFFFF", outline="#E2E8F0", width=scale)

# Header background
draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y1 + header_height], radius=16 * scale, fill="#F1F5F9")
draw.rectangle([card_x1, card_y1 + header_height - 16 * scale, card_x2, card_y1 + header_height], fill="#F1F5F9")
draw.line([card_x1, card_y1 + header_height, card_x2, card_y1 + header_height], fill="#CBD5E1", width=scale)

# Draw Headers
curr_x = card_x1
for i, h in enumerate(headers):
    w = col_widths[i]
    draw.text((curr_x + 20 * scale, card_y1 + (header_height - 24 * scale) // 2), h, font=font_header, fill="#334155")
    curr_x += w

# Draw Rows
curr_y = card_y1 + header_height
for row_idx, r in enumerate(rows):
    is_total = (row_idx == 0)
    row_bg = "#FFFFFF" if row_idx % 2 == 0 else "#F8FAFC"
    if is_total:
        row_bg = "#F1F5F9"
    
    if row_idx == len(rows) - 1:
        draw.rounded_rectangle([card_x1, curr_y, card_x2, curr_y + row_height], radius=16 * scale, fill=row_bg)
        draw.rectangle([card_x1, curr_y, card_x2, curr_y + 16 * scale], fill=row_bg)
    else:
        draw.rectangle([card_x1, curr_y, card_x2, curr_y + row_height], fill=row_bg)

    draw.line([card_x1, curr_y, card_x2, curr_y], fill="#E2E8F0", width=scale)

    curr_x = card_x1
    f = font_bold if is_total else font
    text_color = "#0F172A" if is_total else "#334155"

    for col_idx, cell in enumerate(r):
        w = col_widths[col_idx]
        draw.text((curr_x + 20 * scale, curr_y + (row_height - 22 * scale) // 2), cell, font=f, fill=text_color)
        curr_x += w

    curr_y += row_height

# Save image
out_path = Path("outputs/jlpt_75days_study_stats_ja.png")
out_path.parent.mkdir(exist_ok=True, parents=True)
img.save(out_path, quality=95)
print(f"Generated successfully: {out_path.resolve()}")
