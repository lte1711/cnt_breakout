#!/usr/bin/env python3
"""Compatibility wrapper for simplify_graph_links.py."""

from pathlib import Path
import runpy


if __name__ == "__main__":
    script = Path(__file__).with_name("simplify_graph_links.py")
    runpy.run_path(str(script), run_name="__main__")
