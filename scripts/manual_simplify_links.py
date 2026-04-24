#!/usr/bin/env python3
"""Manual CNT link simplifier using repo-relative paths only."""

from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def simplify_index(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines()
    updated_lines: list[str] = []
    link_count = 0

    for line in lines:
        if line.startswith("## "):
            link_count = 0
            updated_lines.append(line)
            continue
        if line.startswith("- [["):
            link_count += 1
            if link_count > 3:
                continue
        updated_lines.append(line)

    updated = "\n".join(updated_lines) + ("\n" if original.endswith("\n") else "")
    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    root = repo_root()
    changed = 0
    for relative in ("docs/00 Docs Index.md", "docs/ko/00 Docs Index KO.md"):
        if simplify_index(root / relative):
            changed += 1
    print(f"changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
