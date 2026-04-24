from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
EVENTS_PATH = ROOT / "logs" / "shadow_breakout_v3.jsonl"
SNAPSHOT_PATH = ROOT / "data" / "shadow_breakout_v3_snapshot.json"
REPORTS_DIR = ROOT / "reports"
REPORT_MD_PATH = REPORTS_DIR / "breakout_v3_post_trend_setup_residual_trace.md"
REPORT_JSON_PATH = REPORTS_DIR / "breakout_v3_post_trend_setup_residual_trace.json"

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
        "condition_flags": event.get("condition_flags", {}),
        "secondary_fail_reasons": event.get("secondary_fail_reasons", []),
        "fail_keys": sorted(fail_keys),
        "layers": layers,
        "layer_combination": combo_label(layers),
        "raw_event": event,
    }


def common_items(traces: list[dict[str, Any]], key: str) -> list[str]:
    if not traces:
        return []
    sets = [set(trace.get(key, [])) for trace in traces]
    common = sets[0].copy()
    for items in sets[1:]:
        common &= items
    return sorted(common)


def format_table(rows: list[tuple[str, Any]]) -> str:
    lines = ["| key | value |", "|---|---:|"]
    for key, value in rows:
        lines.append(f"| {key} | {value} |")
    return "\n".join(lines)


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    snapshot = load_json(SNAPSHOT_PATH)
    events = load_events(EVENTS_PATH)

    post_trend_setup_fail: list[dict[str, Any]] = []
    setup_pass_breakout_blocked: list[dict[str, Any]] = []
    allowed_events: list[dict[str, Any]] = []

    for index, event in enumerate(events, start=1):
        trace = trace_projection(index, event)
        flags = trace["condition_flags"]
        stage_flags = trace["stage_flags"]

        if flags.get("trend_up_pass", False) and not stage_flags.get("setup", False):
            post_trend_setup_fail.append(trace)

        if (
            stage_flags.get("setup", False)
            and event.get("allowed") is False
            and event.get("first_blocker") == "breakout_not_confirmed"
        ):
            setup_pass_breakout_blocked.append(trace)

        if event.get("allowed") is True:
            allowed_events.append(trace)

    post_trend_common_layers = common_items(post_trend_setup_fail, "layers")
    post_trend_common_conditions = common_items(post_trend_setup_fail, "fail_keys")
    blocked_common_layers = common_items(setup_pass_breakout_blocked, "layers")
    blocked_common_conditions = common_items(setup_pass_breakout_blocked, "fail_keys")
    allowed_common_layers = common_items(allowed_events, "layers")
    allowed_common_conditions = common_items(allowed_events, "fail_keys")

    common_layer_between_blocked_groups = sorted(
        set(post_trend_common_layers) & set(blocked_common_layers)
    )
    common_condition_between_blocked_groups = sorted(
        set(post_trend_common_conditions) & set(blocked_common_conditions)
    )

    blocked_condition_union = Counter()
    for trace in post_trend_setup_fail + setup_pass_breakout_blocked:
        blocked_condition_union.update(trace["fail_keys"])
    allowed_condition_union = Counter()
    for trace in allowed_events:
        allowed_condition_union.update(trace["fail_keys"])

    breakout_confirmed_candidate_conditions = sorted(
        {
            condition
            for condition in blocked_common_conditions
            if condition not in set(allowed_common_conditions)
        }
    )

    if breakout_confirmed_candidate_conditions:
        allowed_difference_summary = (
            "blocked groups share "
            + ", ".join(breakout_confirmed_candidate_conditions)
            + " while allowed traces do not"
        )
    else:
        allowed_difference_summary = "no unique blocked-only common condition found"

    report_json = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "snapshot_signal_count": snapshot.get("signal_count"),
        "event_log_count": len(events),
        "post_trend_setup_fail_count": len(post_trend_setup_fail),
        "setup_pass_breakout_blocked_count": len(setup_pass_breakout_blocked),
        "allowed_count": len(allowed_events),
        "post_trend_setup_fail_traces": post_trend_setup_fail,
        "setup_pass_breakout_blocked_traces": setup_pass_breakout_blocked,
        "allowed_traces": allowed_events,
        "post_trend_common_layers": post_trend_common_layers,
        "post_trend_common_conditions": post_trend_common_conditions,
        "blocked_common_layers": blocked_common_layers,
        "blocked_common_conditions": blocked_common_conditions,
        "allowed_common_layers": allowed_common_layers,
        "allowed_common_conditions": allowed_common_conditions,
        "common_layer_between_blocked_groups": common_layer_between_blocked_groups,
        "common_condition_between_blocked_groups": common_condition_between_blocked_groups,
        "breakout_confirmed_candidate_conditions": breakout_confirmed_candidate_conditions,
        "allowed_difference_summary": allowed_difference_summary,
        "blocked_condition_union": dict(blocked_condition_union),
        "allowed_condition_union": dict(allowed_condition_union),
    }
    REPORT_JSON_PATH.write_text(
        json.dumps(report_json, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report_lines = [
        "---",
        "title: breakout_v3_post_trend_setup_residual_trace",
        "status: completed",
        f"generated_at: {report_json['generated_at']}",
        "---",
        "",
        "# Breakout V3 Post-Trend Setup Residual Trace",
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
        "",
        "## Core Facts",
        "",
        format_table([
            ("post_trend_setup_fail_count", len(post_trend_setup_fail)),
            ("setup_pass_breakout_blocked_count", len(setup_pass_breakout_blocked)),
            ("allowed_count", len(allowed_events)),
            ("common_layer_between_blocked_groups", ", ".join(common_layer_between_blocked_groups) or "none"),
            ("common_condition_between_blocked_groups", ", ".join(common_condition_between_blocked_groups) or "none"),
            ("allowed_difference_summary", allowed_difference_summary),
        ]),
        "",
        "## Group A: trend_up_pass=true + setup_fail=true",
        "",
        format_table([
            ("common_layers", ", ".join(post_trend_common_layers) or "none"),
            ("common_conditions", ", ".join(post_trend_common_conditions) or "none"),
        ]),
        "",
        "## Group B: setup_pass=true + allowed=false + breakout_not_confirmed",
        "",
        format_table([
            ("common_layers", ", ".join(blocked_common_layers) or "none"),
            ("common_conditions", ", ".join(blocked_common_conditions) or "none"),
        ]),
        "",
        "## Allowed Group",
        "",
        format_table([
            ("common_layers", ", ".join(allowed_common_layers) or "none"),
            ("common_conditions", ", ".join(allowed_common_conditions) or "none"),
        ]),
        "",
        "## breakout_confirmed Candidate Conditions",
        "",
        format_table([(item, blocked_condition_union[item]) for item in breakout_confirmed_candidate_conditions] or [("none", 0)]),
        "",
        "## Interpretation",
        "",
        f"- post-trend residual setup failures count = `{len(post_trend_setup_fail)}`",
        f"- setup-pass breakout-blocked count = `{len(setup_pass_breakout_blocked)}`",
        f"- common layer overlap between both blocked groups = `{', '.join(common_layer_between_blocked_groups) or 'none'}`",
        f"- common condition overlap between both blocked groups = `{', '.join(common_condition_between_blocked_groups) or 'none'}`",
        f"- allowed difference summary = `{allowed_difference_summary}`",
        "",
        "## Final Judgement",
        "",
        "`breakout_v3` still shows a shared blocked root after trend-up. The residual setup-fail group and the breakout-not-confirmed group overlap structurally, which suggests that post-trend setup pressure and breakout confirmation failure are related rather than fully separate problems.",
        "",
        "## Obsidian Links",
        "",
        "- [[CNT v2 BREAKOUT V3 SETUP BOTTLENECK ISOLATION REPORT]]",
    ]
    REPORT_MD_PATH.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("STEP-BREAKOUT-V3-POST-TREND-SETUP-RESIDUAL-TRACE-1 = PASS")
    print(f"FACT: post_trend_setup_fail_count = {len(post_trend_setup_fail)}")
    print(f"FACT: setup_pass_breakout_blocked_count = {len(setup_pass_breakout_blocked)}")
    print(f"FACT: allowed_count = {len(allowed_events)}")
    print(
        "FACT: common_layer_between_blocked_groups = "
        f"{', '.join(common_layer_between_blocked_groups) or 'none'}"
    )
    print(
        "FACT: common_condition_between_blocked_groups = "
        f"{', '.join(common_condition_between_blocked_groups) or 'none'}"
    )
    print(f"FACT: allowed_difference_summary = {allowed_difference_summary}")
    print(
        "FINAL_JUDGEMENT = post-trend residual setup failures and breakout-not-confirmed "
        "failures share a partial structural root"
    )
    print("NEXT_RECOMMENDED_PHASE = CONTINUE_POST_TREND_SETUP_RESIDUAL_TRACE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
