from __future__ import annotations

import json
from pathlib import Path


def write_state(state_file: Path, state_data: dict) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)

    with state_file.open("w", encoding="utf-8") as f:
        json.dump(state_data, f, indent=2, ensure_ascii=False)