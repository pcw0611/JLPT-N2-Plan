"""Translate the unique Voca example sentences from Japanese to Korean locally."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import torch
from transformers import BertJapaneseTokenizer, EncoderDecoderModel, PreTrainedTokenizerFast


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs" / "anki" / "voca-examples-20260901"
CANDIDATES_PATH = OUTPUT_DIR / "candidates.json"
TRANSLATIONS_PATH = OUTPUT_DIR / "translations-ko.json"
MODEL_DIR = ROOT / "tmp" / "voca-translation-work" / "aihub-ja-ko-model"
MODEL_ID = "sappho192/aihub-ja-ko-translator"
MODEL_REVISION = "68c1d2703c8f2c3c05be2da32a1559759b6b08b0"

# Directly reviewed corrections for known model errors.
OVERRIDES = {
    "順調だった交渉は、担当者の発言をきっかけに一転して厳しい状況になった。":
        "순조롭던 협상은 담당자의 발언을 계기로 상황이 돌변해 어려워졌다.",
}


def load_cache() -> dict[str, str]:
    if not TRANSLATIONS_PATH.exists():
        return {}
    payload = json.loads(TRANSLATIONS_PATH.read_text(encoding="utf-8"))
    return payload.get("translations", {})


def save_cache(translations: dict[str, str]) -> None:
    payload = {
        "model": MODEL_ID,
        "revision": MODEL_REVISION,
        "direction": "ja-ko",
        "unique_sentence_count": len(translations),
        "translations": translations,
    }
    TRANSLATIONS_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=24)
    parser.add_argument("--num-beams", type=int, default=2)
    parser.add_argument("--max-new-tokens", type=int, default=64)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    candidates = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
    sentences = list(dict.fromkeys(row["japanese"] for row in candidates))
    if args.limit:
        sentences = sentences[: args.limit]

    translations = load_cache()
    translations.update({k: v for k, v in OVERRIDES.items() if k in sentences})
    pending = [sentence for sentence in sentences if sentence not in translations]

    print(f"unique={len(sentences)} cached={len(sentences) - len(pending)} pending={len(pending)}")
    if not pending:
        save_cache(translations)
        return

    torch.set_num_threads(max(1, torch.get_num_threads()))
    source_tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_DIR / "src_tokenizer")
    target_tokenizer = PreTrainedTokenizerFast.from_pretrained(MODEL_DIR / "trg_tokenizer")
    model = EncoderDecoderModel.from_pretrained(MODEL_DIR)
    model.eval()

    for start in range(0, len(pending), args.batch_size):
        batch = pending[start : start + args.batch_size]
        inputs = source_tokenizer(
            batch,
            padding=True,
            truncation=True,
            max_length=192,
            return_attention_mask=True,
            return_token_type_ids=False,
            return_tensors="pt",
        )
        with torch.inference_mode():
            outputs = model.generate(
                **inputs,
                max_new_tokens=args.max_new_tokens,
                num_beams=args.num_beams,
                early_stopping=True,
            )
        decoded = target_tokenizer.batch_decode(outputs, skip_special_tokens=True)
        for source, target in zip(batch, decoded):
            target = re.sub(r"\s+", " ", target).strip()
            translations[source] = target
        save_cache(translations)
        print(f"translated={min(start + len(batch), len(pending))}/{len(pending)}")


if __name__ == "__main__":
    main()
