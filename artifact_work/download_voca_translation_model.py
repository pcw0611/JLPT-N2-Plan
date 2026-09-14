"""Download only the files needed for q4 ONNX Japanese-to-Korean translation."""
from pathlib import Path

from huggingface_hub import snapshot_download


ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "tmp" / "voca-translation-work" / "model"

snapshot_download(
    repo_id="sappho192/gemma3-multilingual-translator-270m",
    revision="512b5b5",
    local_dir=MODEL_DIR,
    allow_patterns=[
        "config.json",
        "generation_config.json",
        "tokenizer.json",
        "tokenizer.model",
        "tokenizer_config.json",
        "special_tokens_map.json",
        "onnx/model_q4.onnx",
        "onnx/model_q4.onnx_data",
        "torch_free/*.py",
        "torch_free/inference/*.py",
    ],
)

print(MODEL_DIR)
