from __future__ import annotations

from pathlib import Path


def append_log(log_file: Path, message: str) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)

    with log_file.open("a", encoding="utf-8") as f:
        f.write(message + "\n")