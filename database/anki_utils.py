"""
Anki collection location and inspection helper for Windows and macOS.
"""
import os
import platform
from pathlib import Path

def get_anki_collection_path(profile_name="사용자 1"):
    """Find local collection.anki2 path automatically across Windows and macOS."""
    system = platform.system()
    if system == "Darwin":  # macOS
        base = Path.home() / "Library" / "Application Support" / "Anki2"
    elif system == "Windows":
        appdata = os.environ.get("APPDATA")
        base = Path(appdata) / "Anki2" if appdata else Path.home() / "AppData" / "Roaming" / "Anki2"
    else:
        base = Path.home() / ".local" / "share" / "Anki2"

    if not base.exists():
        return None

    preferred = base / profile_name / "collection.anki2"
    if preferred.exists():
        return preferred

    for item in base.iterdir():
        if item.is_dir() and (item / "collection.anki2").exists():
            return item / "collection.anki2"

    return None
