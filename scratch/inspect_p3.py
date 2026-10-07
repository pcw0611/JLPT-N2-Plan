# -*- coding: utf-8 -*-
"""Inspect Problem 3 cards questions and choices."""
import sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_25_listening_cards.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

for i in [2, 14, 15, 16]:
    c = cards[i]
    print(f"=== CARD {i+1}: {c['exam']} Q{c['qid']} ===")
    front = c['front']
    # extract choices
    choices = re.findall(r'<div[^>]*padding:10px 14px;[^>]*>\s*<b[^>]*>([1-5]\.)</b>\s*([^<]+)</div>', front)
    if not choices:
        choices = re.findall(r'<div[^>]*font-size:15px;[^>]*>([1-5]\.\s*[^<]+)</div>', front)
    print("Choices:", choices)
    
    # extract prompt
    m_prompt = re.search(r'margin-bottom:16px; word-break:keep-all;">\s*(.*?)\s*</div>', front, re.DOTALL)
    if not m_prompt:
        m_prompt = re.search(r'font-size:18px;[^>]*>\s*(.*?)\s*</div>', front, re.DOTALL)
    prompt_txt = m_prompt.group(1).strip() if m_prompt else 'None'
    print("Prompt:", prompt_txt)
    print('-' * 50)
