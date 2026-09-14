"""Download the direct Japanese-to-Korean fallback translator for evaluation."""
from pathlib import Path

from huggingface_hub import snapshot_download


ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "tmp" / "voca-translation-work" / "aihub-ja-ko-model"

snapshot_download(
    repo_id="sappho192/aihub-ja-ko-translator",
    revision="68c1d2703c8f2c3c05be2da32a1559759b6b08b0",
    local_dir=MODEL_DIR,
    allow_patterns=[
        "config.json",
        "generation_config.json",
        "model.safetensors",
        "src_tokenizer/*",
        "trg_tokenizer/*",
    ],
)

print(MODEL_DIR)
