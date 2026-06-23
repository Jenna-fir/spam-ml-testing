"""Compatibility entrypoint for running the SQL loader from project root.

Usage:
    python sql_practice/load_data.py
"""

from pathlib import Path
import runpy

TARGET_SCRIPT = Path(__file__).resolve().parent.parent / "model" / "sql_practice" / "load_data.py"
runpy.run_path(str(TARGET_SCRIPT), run_name="__main__")