from pathlib import Path
import re

ROOT = Path("C:/cnt/docs")

def clean_tag(tag):
    tag = tag.strip().lower()

    # 제거 조건
    if any(tag.startswith(x) for x in [
        "aliases", "created:", "updated:", "generated_at", "title:"
    ]):
        return None

    if "??" in tag:
        return None

    # 정규화
    tag = tag.replace("status/-", "status/")
    tag = tag.replace("status:", "status/")

    return tag

changed = 0

for path in ROOT.rglob("*.md"):
    text = path.read_text(encoding="utf-8", errors="replace")

    m = re.match(r"(?s)^---\n(.*?)\n---\n?", text)
    if not m:
        continue

    fm = m.group(1)
    body = text[m.end():]

    tags_block = re.search(r"(?ms)^tags:\n((?:\s*-\s*.+\n?)+)", fm)
    if not tags_block:
        continue

    tags = []
    for line in tags_block.group(1).splitlines():
        tag = re.sub(r"^\s*-\s*", "", line)
        tag = clean_tag(tag)
        if tag:
            tags.append(tag)

    tags = list(dict.fromkeys(tags))

    new_tags = "tags:\n" + "\n".join(f"  - {t}" for t in tags)

    fm2 = re.sub(r"(?ms)^tags:\n(?:\s*-\s*.+\n?)+", "", fm).strip()
    new_fm = new_tags + ("\n" + fm2 if fm2 else "")

    new_text = f"---\n{new_fm}\n---\n\n{body.lstrip()}"

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        changed += 1

print("CLEANED =", changed)
