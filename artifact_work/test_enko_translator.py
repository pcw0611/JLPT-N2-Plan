"""Compare the English-source QA translator on known difficult examples."""
from pathlib import Path

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "tmp" / "voca-translation-work" / "opus-en-ko-model"
SAMPLES = [
    "Remember that oversleeping is no excuse for being late.",
    "To make a web, it starts by making a frame of this silk and fastening it to hard objects, such as trees or fences.",
    "That dog has been barking 'Ruff-ruff-ruff-ruff!' all day long.",
    "Though living next door, he doesn't even say hello to us.",
    "This road will take you down to the edge of Lake Biwa.",
    "I welcome any corrections or additions to these minutes.",
]

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_DIR)
model.float()
model.eval()
inputs = tokenizer(SAMPLES, padding=True, truncation=True, return_tensors="pt")
with torch.inference_mode():
    outputs = model.generate(**inputs, max_new_tokens=96, num_beams=4)
for source, target in zip(SAMPLES, tokenizer.batch_decode(outputs, skip_special_tokens=True)):
    print(f"EN\t{source}")
    print(f"KO\t{target}")
