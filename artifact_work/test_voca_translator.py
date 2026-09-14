"""Smoke-test the approved local JA->KO ONNX translation model."""
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "tmp" / "voca-translation-work" / "model"
sys.path.insert(0, str(MODEL_DIR))

from torch_free.inference import TranslatorInferencer


SAMPLES = [
    "順調だった交渉は、担当者の発言をきっかけに一転して厳しい状況になった。",
    "厚い雲に覆われているものの、午後には晴れる見込みだ。",
    "景気の回復にもかかわらず、若者の就職率は思ったほど上がっていない。",
    "締め切り直前になってじたばたしても、状況が改善するとは限らない。",
    "この制度を利用するには、所定の手続きを済ませる必要がある。",
]

translator = TranslatorInferencer(str(MODEL_DIR), precision="q4", verbose=False)
for source in SAMPLES:
    target = translator.translate(source, src_lang="ja", tgt_lang="ko", max_new_tokens=96)
    print(f"JA\t{source}")
    print(f"KO\t{target}")
