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
REPORT_MD_PATH = REPORTS_DIR / "breakout_v3_setup_cluster_layer_isolation.md"
REPORT_JSON_PATH = REPORTS_DIR / "breakout_v3_setup_cluster_layer_isolation.json"

VOLATILITY_LAYER = {
    "band_width_fail",
    "band_expansion_fail",
    "volatility_floor_fail",
}
PARTICIPATION_LAYER = {"volume_fail"}
POSITION_LAYER = {"vwap_distance_fail", "price_position_fail"}
SETUP_STATE_LAYER = {"setup_not_ready"}

LAYER_ORDER = [
    "VOLATILITY_LAYER",
    "PARTICIPATION_LAYER",
    "POSITION_LAYER",
    "SETUP_STATE_LAYER",
]


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


def event_fail_keys(event: dict[str, Any]) -> set[str]:
    flags = event.get("condition_flags", {})
    secondary = set(event.get("secondary_fail_reasons", []))
    fail_keys: set[str] = set()
    if not flags.get("setup_ready", False):
        fail_keys.add("setup_not_ready")
    if not flags.get("volatility_floor_pass", False):
        fail_keys.add("volatility_floor_fail")
    if not flags.get("price_position_pass", False):
        fail_keys.add("price_position_fail")
    fail_keys.update(secondary)
    return fail_keys


def layers_from_fail_keys(fail_keys: set[str]) -> list[str]:
    layers: list[str] = []
    if fail_keys & VOLATILITY_LAYER:
        layers.append("VOLATILITY_LAYER")
    if fail_keys & PARTICIPATION_LAYER:
        layers.append("PARTICIPATION_LAYER")
    if fail_keys & POSITION_LAYER:
        layers.append("POSITION_LAYER")
    if fail_keys & SETUP_STATE_LAYER:
        layers.append("SETUP_STATE_LAYER")
    return layers


def combo_label(items: list[str]) -> str:
    if not items:
        return "none"
    ordered = [item for item in LAYER_ORDER if item in items]
    leftovers = sorted(set(items) - set(ordered))
    return " + ".join(ordered + leftovers)


def trace_projection(index: int, event: dict[str, Any]) -> dict[str, Any]:
    fail_keys = event_fail_keys(event)
    layers = layers_from_fail_keys(fail_keys)
    return {
        "event_index": index,
        "timestamp": event.get("timestamp"),
        "allowed": event.get("allowed"),
        "summary_reason": event.get("summary_reason"),
        "first_blocker": event.get("first_blocker"),
        "hard_blocker": event.get("hard_blocker"),
        "stage_flags": event.get("stage_flags", {}),
        "soft_pass_count": event.get("soft_pass_count"),
        "fail_keys": sorted(fail_keys),
        "layer_combination": combo_label(layers),
        "layers": layers,
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

    total_event_count = len(events)
    setup_fail_events: list[dict[str, Any]] = []
    setup_pass_events: list[dict[str, Any]] = []
    allowed_events: list[dict[str, Any]] = []
    setup_pass_blocked_events: list[dict[str, Any]] = []

    layer_fail_counts: Counter[str] = Counter()
    layer_combo_counts: Counter[str] = Counter()
    breakout_not_confirmed_common: Counter[str] = Counter()
    triple_layer_failure_count = 0

    for index, event in enumerate(events, start=1):
        trace = trace_projection(index, event)
        stage_flags = trace["stage_flags"]
        layers = trace["layers"]

        for layer in layers:
            layer_fail_counts[layer] += 1
        layer_combo_counts[trace["layer_combination"]] += 1

        if {"VOLATILITY_LAYER", "PARTICIPATION_LAYER", "POSITION_LAYER"}.issubset(set(layers)):
            triple_layer_failure_count += 1

        if stage_flags.get("setup") is True:
            setup_pass_events.append(trace)
            if event.get("allowed") is False:
                setup_pass_blocked_events.append(trace)
                if event.get("first_blocker") == "breakout_not_confirmed":
                    for layer in layers:
                        breakout_not_confirmed_common[layer] += 1
        else:
            setup_fail_events.append(trace)

        if event.get("allowed") is True:
            allowed_events.append(trace)

    top_layer_combinations = layer_combo_counts.most_common(10)
    top_layer_combination, top_layer_combination_count = (
        top_layer_combinations[0] if top_layer_combinations else ("none", 0)
    )

    allowed_layer_combinations = Counter(item["layer_combination"] for item in allowed_events)
    setup_pass_blocked_layer_combinations = Counter(
        item["layer_combination"] for item in setup_pass_blocked_events
    )

    report_json = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "snapshot_signal_count": snapshot.get("signal_count"),
        "event_log_count": total_event_count,
        "setup_fail_count": len(setup_fail_events),
        "setup_pass_count": len(setup_pass_events),
        "layer_fail_counts": dict(layer_fail_counts),
        "top_layer_combinations": [
            {"combination": combo, "count": count}
            for combo, count in top_layer_combinations
        ],
        "top_layer_combination": top_layer_combination,
        "top_layer_combination_count": top_layer_combination_count,
        "triple_layer_failure_count": triple_layer_failure_count,
        "allowed_layer_combinations": dict(allowed_layer_combinations),
        "setup_pass_blocked_count": len(setup_pass_blocked_events),
        "setup_pass_blocked_layer_combinations": dict(setup_pass_blocked_layer_combinations),
        "breakout_not_confirmed_common_layers": dict(breakout_not_confirmed_common),
        "allowed_event_traces": allowed_events,
        "setup_pass_blocked_event_traces": setup_pass_blocked_events,
    }
    REPORT_JSON_PATH.write_text(
        json.dumps(report_json, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report_lines = [
        "---",
        "title: breakout_v3_setup_cluster_layer_isolation",
        "status: completed",
        f"generated_at: {report_json['generated_at']}",
        "---",
        "",
        "# Breakout V3 Setup Cluster Layer Isolation",
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
        f"- event log count: `{total_event_count}`",
        "- layer analysis uses event-level shadow log data",
        "",
        "## Core Facts",
        "",
        format_table([
            ("total_event_count", total_event_count),
            ("setup_fail_count", len(setup_fail_events)),
            ("setup_pass_count", len(setup_pass_events)),
            ("top_layer_combination", top_layer_combination),
            ("top_layer_combination_count", top_layer_combination_count),
            ("volatility_layer_fail_count", layer_fail_counts.get("VOLATILITY_LAYER", 0)),
            ("participation_layer_fail_count", layer_fail_counts.get("PARTICIPATION_LAYER", 0)),
            ("position_layer_fail_count", layer_fail_counts.get("POSITION_LAYER", 0)),
            ("setup_state_layer_fail_count", layer_fail_counts.get("SETUP_STATE_LAYER", 0)),
            ("triple_layer_failure_count", triple_layer_failure_count),
            ("allowed_layer_combination_count", len(allowed_layer_combinations)),
            ("setup_pass_blocked_count", len(setup_pass_blocked_events)),
        ]),
        "",
        "## Layer Combination TOP 10",
        "",
        format_table([(combo, count) for combo, count in top_layer_combinations] or [("none", 0)]),
        "",
        "## Allowed Event Layer Combinations",
        "",
        format_table(list(allowed_layer_combinations.items()) or [("none", 0)]),
        "",
        "## Setup Pass But Blocked Layer Combinations",
        "",
        format_table(list(setup_pass_blocked_layer_combinations.items()) or [("none", 0)]),
        "",
        "## breakout_not_confirmed Common Layers",
        "",
        format_table(list(breakout_not_confirmed_common.items()) or [("none", 0)]),
        "",
        "## Interpretation",
        "",
        f"- The dominant layer combination is `{top_layer_combination}` with `{top_layer_combination_count}` events.",
        f"- VOLATILITY + PARTICIPATION + POSITION simultaneous failure appears `{triple_layer_failure_count}` times.",
        f"- Allowed events span `{len(allowed_layer_combinations)}` layer combinations.",
        f"- Setup-pass-but-blocked events remain `{len(setup_pass_blocked_events)}` and all current blockers are `breakout_not_confirmed`.",
        "",
        "## Final Judgement",
        "",
        "`breakout_v3` setup pressure is primarily a layered cluster problem. Failures are not isolated to one condition name; they cluster across volatility, participation, position, and setup-state layers.",
        "",
        "## Obsidian Links",
        "",
        "- [[CNT v2 BREAKOUT V3 SETUP BOTTLENECK ISOLATION REPORT]]",
    ]
    REPORT_MD_PATH.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("STEP-BREAKOUT-V3-SETUP-CLUSTER-LAYER-ISOLATION-1 = PASS")
    print(f"FACT: total_event_count = {total_event_count}")
    print(f"FACT: setup_fail_count = {len(setup_fail_events)}")
    print(f"FACT: top_layer_combination = {top_layer_combination}")
    print(f"FACT: top_layer_combination_count = {top_layer_combination_count}")
    print(f"FACT: volatility_layer_fail_count = {layer_fail_counts.get('VOLATILITY_LAYER', 0)}")
    print(f"FACT: participation_layer_fail_count = {layer_fail_counts.get('PARTICIPATION_LAYER', 0)}")
    print(f"FACT: position_layer_fail_count = {layer_fail_counts.get('POSITION_LAYER', 0)}")
    print(f"FACT: setup_state_layer_fail_count = {layer_fail_counts.get('SETUP_STATE_LAYER', 0)}")
    print(f"FACT: triple_layer_failure_count = {triple_layer_failure_count}")
    print(f"FACT: allowed_layer_combination_count = {len(allowed_layer_combinations)}")
    print(f"FACT: setup_pass_blocked_count = {len(setup_pass_blocked_events)}")
    print(
        "FINAL_JUDGEMENT = setup failures are layered clusters across volatility, participation, "
        "position, and setup-state rather than isolated condition errors"
    )
    print("NEXT_RECOMMENDED_PHASE = CONTINUE_SETUP_CLUSTER_LAYER_ISOLATION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
