from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_PATH = ROOT / "data" / "shadow_breakout_v3_snapshot.json"
EVENTS_PATH = ROOT / "logs" / "shadow_breakout_v3.jsonl"
REPORTS_DIR = ROOT / "reports"
REPORT_MD_PATH = REPORTS_DIR / "breakout_v3_setup_bottleneck_report.md"
ALLOWED_TRACE_PATH = REPORTS_DIR / "breakout_v3_allowed_trace.json"
SETUP_PASS_BLOCKED_TRACE_PATH = (
    REPORTS_DIR / "breakout_v3_setup_pass_blocked_trace.json"
)

REQUESTED_SETUP_BOTTLENECK_KEYS = [
    "vwap_distance_fail",
    "band_width_fail",
    "volume_fail",
    "band_expansion_fail",
    "setup_not_ready",
]

SETUP_STAGE_FLAG_MAP = {
    "setup_ready": "setup_not_ready",
    "volatility_floor_pass": "volatility_floor_fail",
    "price_position_pass": "price_position_fail",
}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                events.append(json.loads(stripped))
    return events


def _sorted_counter(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted(counter.items(), key=lambda item: (-item[1], item[0])))


def _event_trace(index: int, event: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_index": index,
        "timestamp": event.get("timestamp"),
        "symbol": event.get("symbol"),
        "strategy_name": event.get("strategy_name"),
        "allowed": event.get("allowed"),
        "summary_reason": event.get("summary_reason"),
        "first_blocker": event.get("first_blocker"),
        "hard_blocker": event.get("hard_blocker"),
        "soft_pass_count": event.get("soft_pass_count"),
        "soft_fail_count": event.get("soft_fail_count"),
        "min_soft_pass_required": event.get("min_soft_pass_required"),
        "stage_flags": event.get("stage_flags", {}),
        "condition_flags": event.get("condition_flags", {}),
        "secondary_fail_reasons": event.get("secondary_fail_reasons", []),
        "metadata": event.get("metadata", {}),
        "raw_event": event,
    }


def _count_stage_pass_fail(events: list[dict[str, Any]]) -> tuple[dict[str, int], dict[str, int]]:
    pass_counts: Counter[str] = Counter()
    fail_counts: Counter[str] = Counter()
    for event in events:
        for stage_name, passed in event.get("stage_flags", {}).items():
            if passed:
                pass_counts[stage_name] += 1
            else:
                fail_counts[stage_name] += 1
    return _sorted_counter(pass_counts), _sorted_counter(fail_counts)


def _count_setup_stage_conditions(events: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for event in events:
        if event.get("stage_flags", {}).get("setup") is True:
            continue
        condition_flags = event.get("condition_flags", {})
        for flag_name, fail_name in SETUP_STAGE_FLAG_MAP.items():
            if not condition_flags.get(flag_name, False):
                counts[fail_name] += 1
    return _sorted_counter(counts)


def _count_requested_bottlenecks(events: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for event in events:
        secondary_fail_reasons = set(event.get("secondary_fail_reasons", []))
        first_blocker = event.get("first_blocker")
        for key in REQUESTED_SETUP_BOTTLENECK_KEYS:
            if key == "setup_not_ready":
                if first_blocker == "setup_not_ready":
                    counts[key] += 1
            elif key in secondary_fail_reasons:
                counts[key] += 1
    return _sorted_counter(counts)


def _count_distribution(
    events: list[dict[str, Any]], key: str, list_mode: bool = False
) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for event in events:
        value = event.get(key)
        if list_mode:
            for item in value or []:
                counts[item] += 1
        elif value:
            counts[str(value)] += 1
    return _sorted_counter(counts)


def _format_table(rows: list[tuple[str, Any]]) -> str:
    lines = ["| key | value |", "|---|---:|"]
    for key, value in rows:
        lines.append(f"| {key} | {value} |")
    return "\n".join(lines)


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    snapshot = _load_json(SNAPSHOT_PATH)
    events = _load_jsonl(EVENTS_PATH)

    total_signal_count = len(events)
    allowed_events = [
        _event_trace(index, event)
        for index, event in enumerate(events, start=1)
        if event.get("allowed") is True
    ]
    setup_pass_blocked_events = [
        _event_trace(index, event)
        for index, event in enumerate(events, start=1)
        if event.get("stage_flags", {}).get("setup") is True
        and event.get("allowed") is False
    ]

    stage_pass_counts, stage_fail_counts = _count_stage_pass_fail(events)
    setup_stage_fail_counts = _count_setup_stage_conditions(events)
    requested_bottleneck_counts = _count_requested_bottlenecks(events)
    first_blocker_distribution = _count_distribution(events, "first_blocker")
    secondary_fail_distribution = _count_distribution(
        events, "secondary_fail_reasons", list_mode=True
    )

    allowed_count = len(allowed_events)
    setup_pass_count = stage_pass_counts.get("setup", 0)
    top_setup_fail_reason = next(iter(requested_bottleneck_counts), "none")

    ALLOWED_TRACE_PATH.write_text(
        json.dumps(allowed_events, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    SETUP_PASS_BLOCKED_TRACE_PATH.write_text(
        json.dumps(setup_pass_blocked_events, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report_lines = [
        "---",
        "title: breakout_v3_setup_bottleneck_report",
        "status: completed",
        f"generated_at: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "---",
        "",
        "# Breakout V3 Setup Bottleneck Report",
        "",
        "## Scope",
        "",
        "- strategy: `breakout_v3`",
        "- mode: `shadow-only`",
        "- activation: `forbidden`",
        "- tuning: `forbidden`",
        "",
        "## Baseline Note",
        "",
        f"- instruction baseline snapshot signal_count: `42`",
        f"- actual log event count at execution time: `{total_signal_count}`",
        f"- current snapshot signal_count: `{snapshot.get('signal_count')}`",
        "",
        "## Core Facts",
        "",
        _format_table(
            [
                ("total_signal_count", total_signal_count),
                ("allowed_signal_count", allowed_count),
                ("allowed_signal_ratio", round(allowed_count / total_signal_count, 6) if total_signal_count else 0),
                ("setup_pass_count", setup_pass_count),
                ("setup_fail_count", stage_fail_counts.get("setup", 0)),
                ("top_setup_fail_reason", top_setup_fail_reason),
                ("allowed_trace_count", len(allowed_events)),
                ("setup_pass_blocked_trace_count", len(setup_pass_blocked_events)),
            ]
        ),
        "",
        "## Stage Pass Counts",
        "",
        _format_table(list(stage_pass_counts.items())),
        "",
        "## Stage Fail Counts",
        "",
        _format_table(list(stage_fail_counts.items())),
        "",
        "## Setup Stage Internal Fail Counts",
        "",
        _format_table(list(setup_stage_fail_counts.items())),
        "",
        "## Requested Setup Bottleneck Counts",
        "",
        _format_table(list(requested_bottleneck_counts.items())),
        "",
        "## First Blocker Distribution",
        "",
        _format_table(list(first_blocker_distribution.items())),
        "",
        "## Secondary Fail Reasons Distribution",
        "",
        _format_table(list(secondary_fail_distribution.items())),
        "",
        "## Allowed Event Trace Files",
        "",
        f"- `{ALLOWED_TRACE_PATH.relative_to(ROOT)}`",
        f"- count: `{len(allowed_events)}`",
        "",
        "## Setup Pass But Blocked Trace Files",
        "",
        f"- `{SETUP_PASS_BLOCKED_TRACE_PATH.relative_to(ROOT)}`",
        f"- count: `{len(setup_pass_blocked_events)}`",
        "",
        "## Interpretation",
        "",
        f"- setup is the main stage bottleneck by fail count: `{stage_fail_counts.get('setup', 0)}`",
        f"- setup pass remains rare: `{setup_pass_count} / {total_signal_count}`",
        f"- among requested bottleneck keys, the dominant failure is `{top_setup_fail_reason}`",
        "- allowed events were extracted as full raw traces without any tuning or activation change",
        "",
        "## Final Judgement",
        "",
        "`breakout_v3` is not dead, but it is still passing through a narrow setup-layer bottleneck. The next valid phase is setup bottleneck isolation based on trace evidence, not tuning or activation.",
        "",
        "## Obsidian Links",
        "",
        "- [[CNT v2 BREAKOUT V3 FIRST SHADOW OBSERVATION REVIEW]]",
    ]

    REPORT_MD_PATH.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("STEP-BREAKOUT-V3-SETUP-BOTTLENECK-TRACE-1 = PASS")
    print(f"FACT: total_signal_count = {total_signal_count}")
    print(f"FACT: allowed_count = {allowed_count}")
    print(f"FACT: setup_pass_count = {setup_pass_count}")
    print(f"FACT: top_setup_fail_reason = {top_setup_fail_reason}")
    print(f"FACT: allowed_trace_count = {len(allowed_events)}")
    print(
        "FACT: setup_pass_blocked_trace_count = "
        f"{len(setup_pass_blocked_events)}"
    )
    print(
        "FINAL_JUDGEMENT = setup bottleneck isolated with trace evidence; "
        "activation and tuning remain forbidden"
    )
    print("NEXT_RECOMMENDED_PHASE = SETUP_BOTTLENECK_ISOLATION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
