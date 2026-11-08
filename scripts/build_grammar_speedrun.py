"""Synchronize data into the maintained, original-feature Speedrun UI."""
from pathlib import Path
import runpy
ROOT = Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT / 'scripts/sync_grammar_speedrun_html.py'), run_name='__main__')
