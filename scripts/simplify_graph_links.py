#!/usr/bin/env python3
"""Simplify CNT Obsidian links so leaf docs point only to their immediate parent."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


class ParentLinkNormalizer:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.docs_dir = repo_root / "docs"
        self.ko_docs_dir = self.docs_dir / "ko"
        self.index_name = "00 Docs Index"
        self.ko_index_name = "00 Docs Index KO"
        self.vault_home_name = "00 CNT Vault Home"
        self.parent_rules = [
            (r"^CNT v2 BREAKOUT V3", "CNT v2 BREAKOUT V3 DESIGN DRAFT"),
            (r"^CNT v2 BREAKOUT V2", "CNT v2 BREAKOUT V2 DESIGN"),
            (r"^CNT v2 BREAKOUT ", "CNT v2 BREAKOUT QUALITY EVALUATION REPORT"),
            (r"^CNT v2 DASHBOARD|^CNT DATA DASHBOARD|^CNT OPERATIONS DASHBOARD", "CNT DATA DASHBOARD"),
            (r"^CNT OBSIDIAN|^CNT DOCS |^CNT TOOLCHAIN|^CNT AUTO DASHBOARD|^CNT AUTOMATION TOOLS|^CNT GRAPH |^CNT VERSION ", "CNT TOOLCHAIN INTEGRATION REPORT"),
            (r"^CNT v2 OBSERVABILITY", "CNT v2 OBSERVABILITY PRIORITY PLAN"),
            (r"^CNT v2 LIVE|^CNT v2 OFFICIAL LIVE GATE|^CNT v2 CURRENT STATUS ASSESSMENT", "CNT v2 LIVE READINESS GATE"),
            (r"^CNT v2 TESTNET|^CNT v2 DATA COLLECTION|^CNT v2 SCHEDULED|^CNT v2 TASK", "CNT v2 TESTNET PERFORMANCE REPORT"),
            (r"^CNT v2 VALIDATION|^CNT v2 PERFORMANCE|^CNT v2 IMPLEMENTATION|^CNT v2 PATCH|^CNT v2 EXIT FAILSAFE|^CNT v2 PHASE 1|^CNT v2 ENGINE|^CNT v2 RANKER|^CNT v2 STAGE 3|^CNT v2 METRICS|^CNT v2 CANDIDATE|^CNT v2 SHADOW SEMANTICS", "CNT v2 VALIDATION REPORT"),
            (r"^CNT v1\.1 ", "CNT v1.1 ARCHITECTURE DESIGN DOCUMENT"),
            (r"^DESIGN SUMMARY|^RECORD TEXT|^SHARING CHECKLIST|^VALIDATION RESULT|^cnt_v1_", "CNT v2 ARCHITECTURE DESIGN DOCUMENT"),
        ]
        self.top_level_docs = self._extract_top_level_links(self.docs_dir / f"{self.index_name}.md")
        self.top_level_ko_docs = self._extract_top_level_links(self.ko_docs_dir / f"{self.ko_index_name}.md")

    def _extract_top_level_links(self, path: Path) -> set[str]:
        if not path.exists():
            return set()
        content = path.read_text(encoding="utf-8")
        links = set()
        for target, _label in WIKILINK_RE.findall(content):
            if target in {self.index_name, self.ko_index_name, self.vault_home_name}:
                continue
            links.add(target)
        return links

    def _iter_markdown_files(self):
        for root in (self.docs_dir, self.ko_docs_dir):
            if not root.exists():
                continue
            for path in root.rglob("*.md"):
                yield path

    def _is_korean(self, path: Path) -> bool:
        return "ko" in path.parts

    def _korean_target(self, target: str) -> str:
        if target.endswith(" KO"):
            return target
        ko_candidate = self.ko_docs_dir / f"{target} KO.md"
        if ko_candidate.exists():
            return f"{target} KO"
        return target

    def _get_links_section_bounds(self, lines: list[str]) -> tuple[int, int] | None:
        start = None
        for idx, line in enumerate(lines):
            if line.strip() in {"## Obsidian Links", "## Links"}:
                start = idx
                break
        if start is None:
            return None
        end = len(lines)
        for idx in range(start + 1, len(lines)):
            if lines[idx].startswith("## "):
                end = idx
                break
        return start, end

    def _replace_wikilinks_with_text(self, line: str) -> str:
        def repl(match: re.Match[str]) -> str:
            target = match.group(1)
            label = match.group(2) or target
            return label

        return WIKILINK_RE.sub(repl, line)

    def _simplify_frontmatter_tags(self, lines: list[str], current_name: str) -> list[str]:
        if not lines or lines[0].strip() != "---":
            return lines

        try:
            end = lines.index("---", 1)
        except ValueError:
            return lines

        keep_tags = current_name in {self.index_name, self.ko_index_name}
        frontmatter = lines[1:end]
        new_frontmatter: list[str] = []
        in_tags = False

        for line in frontmatter:
            if line.strip() == "tags:":
                in_tags = True
                if keep_tags:
                    new_frontmatter.append("tags:")
                    new_frontmatter.append("  - cnt")
                    if current_name == self.ko_index_name:
                        new_frontmatter.append("  - ko")
                continue

            if in_tags:
                if re.match(r"^\s*-\s+", line):
                    continue
                if line.startswith(" ") or line.startswith("\t"):
                    continue
                in_tags = False

            if not in_tags:
                new_frontmatter.append(line)

        return ["---", *new_frontmatter, "---", *lines[end + 1 :]]

    def _extract_section_targets(self, lines: list[str], start: int, end: int) -> list[str]:
        targets: list[str] = []
        for line in lines[start + 1 : end]:
            match = WIKILINK_RE.search(line)
            if match:
                targets.append(match.group(1))
        return targets

    def _pick_parent(self, path: Path, current_name: str, section_targets: list[str]) -> str:
        is_ko = self._is_korean(path)

        if current_name == self.index_name:
            return self.vault_home_name
        if current_name == self.ko_index_name:
            return self.index_name

        if is_ko and current_name in self.top_level_ko_docs:
            return self.ko_index_name
        if (not is_ko) and current_name in self.top_level_docs:
            return self.index_name

        base_name = current_name[:-3] if current_name.endswith(" KO") else current_name
        for pattern, parent in self.parent_rules:
            if re.search(pattern, base_name):
                return self._korean_target(parent) if is_ko else parent

        excluded = {current_name, self.vault_home_name, self.index_name, self.ko_index_name}
        for target in section_targets:
            if target in excluded:
                continue
            return self._korean_target(target) if is_ko else target

        return self.ko_index_name if is_ko else self.index_name

    def normalize_file(self, path: Path) -> bool:
        original = path.read_text(encoding="utf-8")
        lines = original.splitlines()
        current_name = path.stem
        lines = self._simplify_frontmatter_tags(lines, current_name)
        bounds = self._get_links_section_bounds(lines)
        is_index_doc = current_name in {self.index_name, self.ko_index_name}

        if bounds is None:
            start = len(lines)
            end = len(lines)
            section_targets: list[str] = []
        else:
            start, end = bounds
            section_targets = self._extract_section_targets(lines, start, end)

        parent = self._pick_parent(path, current_name, section_targets)
        updated_lines: list[str] = []

        for line in lines[:start]:
            if is_index_doc:
                updated_lines.append(line)
                continue
            updated_lines.append(self._replace_wikilinks_with_text(line))

        if not is_index_doc:
            if updated_lines and updated_lines[-1].strip() != "":
                updated_lines.append("")
            updated_lines.extend(["## Obsidian Links", "", f"- [[{parent}]]"])
        elif bounds is not None:
            updated_lines.extend(["## Obsidian Links", "", f"- [[{parent}]]"])

        for line in lines[end:]:
            if is_index_doc:
                updated_lines.append(line)
                continue
            updated_lines.append(self._replace_wikilinks_with_text(line))

        updated = "\n".join(updated_lines) + ("\n" if original.endswith("\n") else "")
        if updated == original:
            return False
        path.write_text(updated, encoding="utf-8")
        return True

    def normalize_all(self) -> int:
        changed = 0
        for path in self._iter_markdown_files():
            if self.normalize_file(path):
                changed += 1
        return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", nargs="?", default=".")
    args = parser.parse_args()
    normalizer = ParentLinkNormalizer(Path(args.repo_root).resolve())
    changed = normalizer.normalize_all()
    print(f"changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
