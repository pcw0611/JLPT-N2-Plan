# -*- coding: utf-8 -*-
"""Inspect Problem 4 cards choices in front."""
import sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_25_listening_cards.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

for idx in [3, 4, 5, 6, 17, 18, 19, 20, 21, 22, 23]:
    c = cards[idx]
    print(f"=== CARD {idx+1}: {c['exam']} Q{c['qid']} ===")
    front = c['front']
    
    # choices
    choices = re.findall(r'<div[^>]*padding:10px 14px;[^>]*>\s*<b[^>]*>([1-5]\.)</b>\s*([^<]+)</div>', front)
    if not choices:
        choices = re.findall(r'<div[^>]*font-size:15px;[^>]*>([1-5]\.\s*[^<]+)</div>', front)
    print("Choices:", choices)
    
    # prompt
    m_prompt = re.search(r'margin-bottom:16px; word-break:keep-all;">\s*(.*?)\s*</div>', front, re.DOTALL)
    if not m_prompt:
        m_prompt = re.search(r'font-size:18px;[^>]*>\s*(.*?)\s*</div>', front, re.DOTALL)
    prompt_txt = m_prompt.group(1).strip() if m_prompt else 'None'
    print("Prompt:", prompt_txt)
    print('-' * 50)
