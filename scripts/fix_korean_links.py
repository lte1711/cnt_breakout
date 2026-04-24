#!/usr/bin/env python3
"""Normalize CNT markdown wiki-links to plain Obsidian-compatible names."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


WIKILINK_WITH_ALIAS = re.compile(r"\[\[docs(?:/ko)?/([^\]|]+)\|([^\]]+)\]\]")
WIKILINK_PLAIN = re.compile(r"\[\[docs(?:/ko)?/([^\]]+)\]\]")


def normalize_links(text: str) -> str:
    text = WIKILINK_WITH_ALIAS.sub(r"[[\1|\2]]", text)
    text = WIKILINK_PLAIN.sub(r"[[\1]]", text)
    return text


def process_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = normalize_links(original)
    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def iter_markdown_files(repo_root: Path):
    for root in (repo_root / "docs", repo_root / "docs" / "ko"):
        if not root.exists():
            continue
        yield from root.rglob("*.md")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", nargs="?", default=".")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    fixed = 0
    scanned = 0
    for path in iter_markdown_files(repo_root):
        scanned += 1
        if process_file(path):
            fixed += 1

    print(f"scanned={scanned} fixed={fixed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
