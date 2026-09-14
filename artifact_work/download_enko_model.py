"""Download the English-to-Korean QA translator."""
from pathlib import Path

from huggingface_hub import snapshot_download


ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "tmp" / "voca-translation-work" / "opus-en-ko-model"

snapshot_download(
    repo_id="Helsinki-NLP/opus-mt-tc-big-en-ko",
    revision="ae8606b7b29a495f31ce679cee2007f536a3a5ce",
    local_dir=MODEL_DIR,
    allow_patterns=[
        "config.json",
        "generation_config.json",
        "model.safetensors",
        "source.spm",
        "target.spm",
        "special_tokens_map.json",
        "tokenizer_config.json",
        "vocab.json",
    ],
)

print(MODEL_DIR)
