from pathlib import Path
import re
from datetime import date

ROOT = Path("C:/cnt/docs")

DEFAULT_TAGS = [
    "cnt",
    "type/documentation",
    "status/active",
]

RULES = [
    ("market", "market-context"),
    ("context", "market-context"),
    ("logging", "post-logging"),
    ("post_logging", "post-logging"),
    ("pre_runup", "pre-runup"),
    ("runup", "pre-runup"),
    ("filter", "context-filter"),
    ("offline", "offline-experiment"),
    ("validation", "type/validation"),
    ("experiment", "offline-experiment"),
    ("runtime", "type/operation"),
    ("risk", "risk"),
    ("breakout", "strategy/breakout_v3"),
    ("graph", "graph-view"),
    ("obsidian", "obsidian"),
]

def unique_keep_order(items):
    out = []
    for x in items:
        x = x.strip()
        if x and x not in out:
            out.append(x)
    return out

def infer_tags(path: Path, body: str):
    text = (path.name + "\n" + body[:2000]).lower()
    tags = list(DEFAULT_TAGS)

    for key, tag in RULES:
        if key in text:
            tags.append(tag)

    if "report" in text:
        tags.append("type/analysis")
    if "validation" in text or "검증" in text:
        tags.append("type/validation")
    if "completed" in text or "complete" in text or "완료" in text:
        tags.append("status/completed")

    return unique_keep_order(tags)

def parse_existing_tags(frontmatter: str):
    tags = []

    block = re.search(r"(?ms)^tags:\s*\n((?:\s*-\s*.+\n?)+)", frontmatter)
    if block:
        for line in block.group(1).splitlines():
            item = re.sub(r"^\s*-\s*", "", line).strip().strip('"').strip("'")
            if item:
                tags.append(item)

    inline = re.search(r"(?m)^tags:\s*\[(.*?)\]", frontmatter)
    if inline:
        for item in inline.group(1).split(","):
            item = item.strip().strip('"').strip("'")
            if item:
                tags.append(item)

    return unique_keep_order(tags)

def normalize_tag(tag: str):
    tag = tag.strip().strip('"').strip("'")
    tag = tag.replace(" ", "-")
    tag = tag.replace("status:", "status/")
    tag = tag.replace("ACTIVE", "active")
    tag = tag.replace("verified", "status/verified") if tag == "verified" else tag
    tag = tag.replace("validated", "status/validated") if tag == "validated" else tag
    return tag.lower()

changed = 0
processed = 0

for path in ROOT.rglob("*.md"):
    processed += 1
    text = path.read_text(encoding="utf-8", errors="replace")

    fm_match = re.match(r"(?s)^---\s*\n(.*?)\n---\s*\n?", text)

    if fm_match:
        fm = fm_match.group(1)
        body = text[fm_match.end():]
        existing_tags = [normalize_tag(t) for t in parse_existing_tags(fm)]

        inferred = infer_tags(path, body)
        final_tags = unique_keep_order(existing_tags + inferred)

        # remove existing tags block / inline tags
        fm2 = re.sub(r"(?ms)^tags:\s*\n(?:\s*-\s*.+\n?)+", "", fm)
        fm2 = re.sub(r"(?m)^tags:\s*\[.*?\]\s*\n?", "", fm2)
        fm2 = fm2.strip()

        tag_block = "tags:\n" + "\n".join(f"  - {t}" for t in final_tags)

        new_fm = tag_block + ("\n" + fm2 if fm2 else "")
        new_text = f"---\n{new_fm}\n---\n\n{body.lstrip()}"

    else:
        body = text
        final_tags = infer_tags(path, body)
        today = date.today().isoformat()
        tag_block = "tags:\n" + "\n".join(f"  - {t}" for t in final_tags)
        new_text = f"---\n{tag_block}\ncreated: {today}\n---\n\n{text.lstrip()}"

    if new_text != text:
        path.write_text(new_text, encoding="utf-8", newline="\n")
        changed += 1

print(f"PROCESSED={processed}")
print(f"CHANGED={changed}")
