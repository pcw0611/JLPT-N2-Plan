"""Smoke-test the direct Japanese-to-Korean fallback translator."""
from pathlib import Path

import torch
from transformers import BertJapaneseTokenizer, EncoderDecoderModel, PreTrainedTokenizerFast


ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "tmp" / "voca-translation-work" / "aihub-ja-ko-model"
SAMPLES = [
    "順調だった交渉は、担当者の発言をきっかけに一転して厳しい状況になった。",
    "厚い雲に覆われているものの、午後には晴れる見込みだ。",
    "景気の回復にもかかわらず、若者の就職率は思ったほど上がっていない。",
    "締め切り直前になってじたばたしても、状況が改善するとは限らない。",
    "この制度を利用するには、所定の手続きを済ませる必要がある。",
]

torch.set_num_threads(max(1, (torch.get_num_threads() // 2)))
source_tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_DIR / "src_tokenizer")
target_tokenizer = PreTrainedTokenizerFast.from_pretrained(MODEL_DIR / "trg_tokenizer")
model = EncoderDecoderModel.from_pretrained(MODEL_DIR)
model.eval()

inputs = source_tokenizer(
    SAMPLES,
    padding=True,
    truncation=True,
    return_attention_mask=True,
    return_token_type_ids=False,
    return_tensors="pt",
)
with torch.inference_mode():
    outputs = model.generate(**inputs, max_new_tokens=96, num_beams=4)

for source, output in zip(SAMPLES, outputs):
    target = target_tokenizer.decode(output[1:-1], skip_special_tokens=True).strip()
    print(f"JA\t{source}")
    print(f"KO\t{target}")
