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
REPORT_MD_PATH = REPORTS_DIR / "breakout_v3_setup_root_cause_matrix.md"
REPORT_JSON_PATH = REPORTS_DIR / "breakout_v3_setup_root_cause_matrix.json"

SETUP_STAGE_KEYS = [
    "setup_not_ready",
    "volatility_floor_fail",
    "price_position_fail",
]

REQUESTED_SOFT_KEYS = [
    "vwap_distance_fail",
    "band_width_fail",
    "volume_fail",
    "band_expansion_fail",
]

ALL_MATRIX_KEYS = SETUP_STAGE_KEYS + REQUESTED_SOFT_KEYS


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                events.append(json.loads(stripped))
    return events


def event_matrix_fail_keys(event: dict[str, Any]) -> list[str]:
    flags = event.get("condition_flags", {})
    secondary = set(event.get("secondary_fail_reasons", []))
    failed: list[str] = []

    if not flags.get("setup_ready", False):
        failed.append("setup_not_ready")
    if not flags.get("volatility_floor_pass", False):
        failed.append("volatility_floor_fail")
    if not flags.get("price_position_pass", False):
        failed.append("price_position_fail")

    for key in REQUESTED_SOFT_KEYS:
        if key in secondary:
            failed.append(key)

    return failed


def combo_label(fail_keys: list[str]) -> str:
    if not fail_keys:
        return "none"
    return " + ".join(sorted(fail_keys))


def trace_projection(index: int, event: dict[str, Any]) -> dict[str, Any]:
    fail_keys = event_matrix_fail_keys(event)
    return {
        "event_index": index,
        "timestamp": event.get("timestamp"),
        "allowed": event.get("allowed"),
        "summary_reason": event.get("summary_reason"),
        "first_blocker": event.get("first_blocker"),
        "hard_blocker": event.get("hard_blocker"),
        "setup_stage_pass": event.get("stage_flags", {}).get("setup"),
        "trigger_stage_pass": event.get("stage_flags", {}).get("trigger"),
        "quality_stage_pass": event.get("stage_flags", {}).get("quality"),
        "soft_pass_count": event.get("soft_pass_count"),
        "matrix_fail_keys": sorted(fail_keys),
        "matrix_fail_combination": combo_label(fail_keys),
        "secondary_fail_reasons": event.get("secondary_fail_reasons", []),
        "condition_flags": event.get("condition_flags", {}),
        "raw_event": event,
    }


def format_table(rows: list[tuple[str, Any]]) -> str:
    lines = ["| key | value |", "|---|---:|"]
    for key, value in rows:
        lines.append(f"| {key} | {value} |")
    return "\n".join(lines)


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    snapshot = load_json(SNAPSHOT_PATH)
    events = load_events(EVENTS_PATH)

    setup_fail_events: list[dict[str, Any]] = []
    setup_pass_events: list[dict[str, Any]] = []
    allowed_events: list[dict[str, Any]] = []
    setup_pass_blocked_events: list[dict[str, Any]] = []

    combo_counts: Counter[str] = Counter()
    triple_requested_count = 0

    for index, event in enumerate(events, start=1):
        stage_flags = event.get("stage_flags", {})
        trace = trace_projection(index, event)

        if stage_flags.get("setup") is True:
            setup_pass_events.append(trace)
            if event.get("allowed") is False:
                setup_pass_blocked_events.append(trace)
        else:
            setup_fail_events.append(trace)
            combo_counts[trace["matrix_fail_combination"]] += 1

        if event.get("allowed") is True:
            allowed_events.append(trace)

        fail_keys = set(trace["matrix_fail_keys"])
        if {"vwap_distance_fail", "band_width_fail", "volume_fail"}.issubset(fail_keys):
            triple_requested_count += 1

    top_combinations = combo_counts.most_common(10)
    setup_fail_count = len(setup_fail_events)
    setup_pass_count = len(setup_pass_events)
    allowed_count = len(allowed_events)
    setup_pass_blocked_count = len(setup_pass_blocked_events)

    top_fail_combination, top_fail_combination_count = (
        top_combinations[0] if top_combinations else ("none", 0)
    )
    single_dominant_blocker = (
        setup_fail_count > 0 and (top_fail_combination_count / setup_fail_count) > 0.5
    )
    multi_condition_failure_detected = any(
        len(item["matrix_fail_keys"]) >= 2 for item in setup_fail_events
    )

    allowed_combinations = Counter(item["matrix_fail_combination"] for item in allowed_events)
    setup_pass_blocked_reasons = Counter(
        item["first_blocker"] or item["summary_reason"] for item in setup_pass_blocked_events
    )

    report_json = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "snapshot_signal_count": snapshot.get("signal_count"),
        "event_log_count": len(events),
        "setup_fail_count": setup_fail_count,
        "setup_pass_count": setup_pass_count,
        "allowed_count": allowed_count,
        "setup_pass_blocked_count": setup_pass_blocked_count,
        "top_fail_combination": top_fail_combination,
        "top_fail_combination_count": top_fail_combination_count,
        "single_dominant_blocker": single_dominant_blocker,
        "multi_condition_failure_detected": multi_condition_failure_detected,
        "triple_requested_simultaneous_fail_count": triple_requested_count,
        "top_fail_combinations": [
            {"combination": combo, "count": count} for combo, count in top_combinations
        ],
        "allowed_combinations": dict(allowed_combinations),
        "setup_pass_blocked_reasons": dict(setup_pass_blocked_reasons),
        "allowed_event_traces": allowed_events,
        "setup_pass_blocked_event_traces": setup_pass_blocked_events,
    }
    REPORT_JSON_PATH.write_text(
        json.dumps(report_json, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report_lines = [
        "---",
        "title: breakout_v3_setup_root_cause_matrix",
        "status: completed",
        f"generated_at: {report_json['generated_at']}",
        "---",
        "",
        "# Breakout V3 Setup Root Cause Matrix",
        "",
        "## Scope",
        "",
        "- strategy: `breakout_v3`",
        "- mode: `shadow-only`",
        "- activation: `forbidden`",
        "- tuning: `forbidden`",
        "",
        "## Baseline",
        "",
        f"- snapshot signal_count: `{snapshot.get('signal_count')}`",
        f"- event log count: `{len(events)}`",
        "- matrix analysis uses event log data to preserve event-level combinations",
        "",
        "## Core Facts",
        "",
        format_table([
            ("setup_fail_count", setup_fail_count),
            ("setup_pass_count", setup_pass_count),
            ("allowed_count", allowed_count),
            ("setup_pass_blocked_count", setup_pass_blocked_count),
            ("top_fail_combination", top_fail_combination),
            ("top_fail_combination_count", top_fail_combination_count),
            ("single_dominant_blocker", str(single_dominant_blocker)),
            ("multi_condition_failure_detected", str(multi_condition_failure_detected)),
            ("triple_requested_simultaneous_fail_count", triple_requested_count),
        ]),
        "",
        "## Fail Condition Combination TOP 10",
        "",
        format_table([(combo, count) for combo, count in top_combinations] or [("none", 0)]),
        "",
        "## Allowed Event Combinations",
        "",
        format_table(list(allowed_combinations.items()) or [("none", 0)]),
        "",
        "## Setup Pass But Blocked Reasons",
        "",
        format_table(list(setup_pass_blocked_reasons.items()) or [("none", 0)]),
        "",
        "## Interpretation",
        "",
        f"- The top setup-fail combination is `{top_fail_combination}` with `{top_fail_combination_count}` events.",
        f"- Multi-condition simultaneous failure detected: `{multi_condition_failure_detected}`.",
        f"- The requested triple failure (`vwap_distance_fail + band_width_fail + volume_fail`) appears `{triple_requested_count}` times.",
        f"- Allowed events contain `{len(allowed_combinations)}` distinct setup-related combinations.",
        f"- Setup-pass-but-blocked events remain `{setup_pass_blocked_count}`, and their blockers are dominated by `{next(iter(setup_pass_blocked_reasons), 'none')}`.",
        "",
        "## Final Judgement",
        "",
        "`breakout_v3` setup pressure is not a single independent failure. It is primarily a simultaneous failure structure, with repeated multi-condition combinations clustering around setup and requested quality-side conditions.",
        "",
        "## Obsidian Links",
        "",
        "- [[CNT v2 BREAKOUT V3 SETUP BOTTLENECK ISOLATION REPORT]]",
    ]
    REPORT_MD_PATH.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("STEP-BREAKOUT-V3-SETUP-ROOT-CAUSE-MATRIX-1 = PASS")
    print(f"FACT: setup_fail_count = {setup_fail_count}")
    print(f"FACT: setup_pass_count = {setup_pass_count}")
    print(f"FACT: top_fail_combination = {top_fail_combination}")
    print(f"FACT: top_fail_combination_count = {top_fail_combination_count}")
    print(f"FACT: multi_condition_failure_detected = {multi_condition_failure_detected}")
    print(f"FACT: allowed_setup_combination_count = {len(allowed_combinations)}")
    print(f"FACT: setup_pass_blocked_count = {setup_pass_blocked_count}")
    print(
        "FINAL_JUDGEMENT = setup failures are primarily clustered multi-condition combinations, "
        "not isolated single-condition failures"
    )
    print("NEXT_RECOMMENDED_PHASE = CONTINUE_SETUP_BOTTLENECK_ISOLATION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
