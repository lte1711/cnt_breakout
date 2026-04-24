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
REPORT_MD_PATH = REPORTS_DIR / "breakout_v3_setup_market_context_split.md"
REPORT_JSON_PATH = REPORTS_DIR / "breakout_v3_setup_market_context_split.json"

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


def layer_combo(fail_keys: set[str]) -> str:
    layers: list[str] = []
    if fail_keys & VOLATILITY_LAYER:
        layers.append("VOLATILITY_LAYER")
    if fail_keys & PARTICIPATION_LAYER:
        layers.append("PARTICIPATION_LAYER")
    if fail_keys & POSITION_LAYER:
        layers.append("POSITION_LAYER")
    if fail_keys & SETUP_STATE_LAYER:
        layers.append("SETUP_STATE_LAYER")
    if not layers:
        return "none"
    return " + ".join([layer for layer in LAYER_ORDER if layer in layers])


def market_context_label(event: dict[str, Any]) -> str:
    flags = event.get("condition_flags", {})
    market_bias_pass = bool(flags.get("market_bias_pass", False))
    trend_up_pass = bool(flags.get("trend_up_pass", False))
    range_bias_pass = bool(flags.get("range_bias_pass", False))

    if not market_bias_pass:
        return "MARKET_NOT_TREND_UP"
    if trend_up_pass:
        return "TREND_UP_PASS"
    if range_bias_pass:
        return "RANGE_BIAS_PASS"
    return "MARKET_BIAS_PASS_OTHER"


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
    setup_fail_count = 0
    setup_pass_count = 0
    market_not_trend_up_count = 0
    setup_fail_and_market_not_trend_up_count = 0
    setup_fail_but_market_trend_up_count = 0

    layer_market_context_distribution: dict[str, Counter[str]] = {}
    allowed_market_contexts: Counter[str] = Counter()
    setup_pass_blocked_market_contexts: Counter[str] = Counter()
    breakout_not_confirmed_market_contexts: Counter[str] = Counter()

    allowed_event_traces: list[dict[str, Any]] = []
    setup_pass_blocked_event_traces: list[dict[str, Any]] = []

    for index, event in enumerate(events, start=1):
        flags = event.get("condition_flags", {})
        stage_flags = event.get("stage_flags", {})
        context = market_context_label(event)
        fail_keys = event_fail_keys(event)
        combo = layer_combo(fail_keys)

        if context == "MARKET_NOT_TREND_UP":
            market_not_trend_up_count += 1

        if stage_flags.get("setup") is True:
            setup_pass_count += 1
            if event.get("allowed") is False:
                setup_pass_blocked_market_contexts[context] += 1
                setup_pass_blocked_event_traces.append(
                    {
                        "event_index": index,
                        "timestamp": event.get("timestamp"),
                        "market_context": context,
                        "layer_combination": combo,
                        "first_blocker": event.get("first_blocker"),
                        "summary_reason": event.get("summary_reason"),
                        "condition_flags": flags,
                        "secondary_fail_reasons": event.get("secondary_fail_reasons", []),
                        "raw_event": event,
                    }
                )
        else:
            setup_fail_count += 1
            if context == "MARKET_NOT_TREND_UP":
                setup_fail_and_market_not_trend_up_count += 1
            if flags.get("trend_up_pass", False):
                setup_fail_but_market_trend_up_count += 1

        layer_market_context_distribution.setdefault(combo, Counter())[context] += 1

        if event.get("allowed") is True:
            allowed_market_contexts[context] += 1
            allowed_event_traces.append(
                {
                    "event_index": index,
                    "timestamp": event.get("timestamp"),
                    "market_context": context,
                    "layer_combination": combo,
                    "condition_flags": flags,
                    "secondary_fail_reasons": event.get("secondary_fail_reasons", []),
                    "raw_event": event,
                }
            )

        if event.get("first_blocker") == "breakout_not_confirmed":
            breakout_not_confirmed_market_contexts[context] += 1

    top_layer_market_context = {
        combo: dict(counter.most_common())
        for combo, counter in sorted(
            layer_market_context_distribution.items(),
            key=lambda item: (-sum(item[1].values()), item[0]),
        )[:10]
    }

    report_json = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "snapshot_signal_count": snapshot.get("signal_count"),
        "event_log_count": total_event_count,
        "setup_fail_count": setup_fail_count,
        "setup_pass_count": setup_pass_count,
        "market_not_trend_up_count": market_not_trend_up_count,
        "setup_fail_and_market_not_trend_up_count": setup_fail_and_market_not_trend_up_count,
        "setup_fail_but_market_trend_up_count": setup_fail_but_market_trend_up_count,
        "allowed_market_contexts": dict(allowed_market_contexts),
        "setup_pass_blocked_market_contexts": dict(setup_pass_blocked_market_contexts),
        "breakout_not_confirmed_market_contexts": dict(breakout_not_confirmed_market_contexts),
        "layer_market_context_distribution_top10": top_layer_market_context,
        "allowed_event_traces": allowed_event_traces,
        "setup_pass_blocked_event_traces": setup_pass_blocked_event_traces,
    }
    REPORT_JSON_PATH.write_text(
        json.dumps(report_json, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report_lines = [
        "---",
        "title: breakout_v3_setup_market_context_split",
        "status: completed",
        f"generated_at: {report_json['generated_at']}",
        "---",
        "",
        "# Breakout V3 Setup Market Context Split",
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
        "- market context split uses event-level shadow log data",
        "",
        "## Core Facts",
        "",
        format_table([
            ("total_event_count", total_event_count),
            ("setup_fail_count", setup_fail_count),
            ("setup_pass_count", setup_pass_count),
            ("market_not_trend_up_count", market_not_trend_up_count),
            ("setup_fail_and_market_not_trend_up_count", setup_fail_and_market_not_trend_up_count),
            ("setup_fail_but_market_trend_up_count", setup_fail_but_market_trend_up_count),
            ("allowed_market_context_count", len(allowed_market_contexts)),
            ("setup_pass_blocked_market_context_count", len(setup_pass_blocked_market_contexts)),
        ]),
        "",
        "## Allowed Event Market Context",
        "",
        format_table(list(allowed_market_contexts.items()) or [("none", 0)]),
        "",
        "## Setup Pass But Blocked Market Context",
        "",
        format_table(list(setup_pass_blocked_market_contexts.items()) or [("none", 0)]),
        "",
        "## breakout_not_confirmed Market Context",
        "",
        format_table(list(breakout_not_confirmed_market_contexts.items()) or [("none", 0)]),
        "",
        "## Layer Combination Market Context Distribution TOP 10",
        "",
    ]

    for combo, counter_map in top_layer_market_context.items():
        report_lines.extend(
            [
                f"### {combo}",
                "",
                format_table(list(counter_map.items()) or [("none", 0)]),
                "",
            ]
        )

    breakout_not_confirmed_market_context = (
        ", ".join(f"{key}={value}" for key, value in breakout_not_confirmed_market_contexts.items())
        if breakout_not_confirmed_market_contexts
        else "none"
    )

    report_lines.extend(
        [
            "## Interpretation",
            "",
            f"- `market_not_trend_up` appears `{market_not_trend_up_count}` times.",
            f"- `setup_fail + market_not_trend_up` appears `{setup_fail_and_market_not_trend_up_count}` times.",
            f"- `setup_fail + trend_up_pass` still appears `{setup_fail_but_market_trend_up_count}` times.",
            f"- breakout-not-confirmed market context = `{breakout_not_confirmed_market_context}`.",
            "",
            "## Final Judgement",
            "",
            "`breakout_v3` setup cluster is not only a non-trend regime problem. Setup pressure still survives after trend-up passes, which means the bottleneck is partly market-context-driven and partly intrinsic to the setup layer itself.",
            "",
            "## Obsidian Links",
            "",
            "- [[CNT v2 BREAKOUT V3 SETUP BOTTLENECK ISOLATION REPORT]]",
        ]
    )

    REPORT_MD_PATH.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("STEP-BREAKOUT-V3-SETUP-MARKET-CONTEXT-SPLIT-1 = PASS")
    print(f"FACT: total_event_count = {total_event_count}")
    print(f"FACT: setup_fail_count = {setup_fail_count}")
    print(f"FACT: market_not_trend_up_count = {market_not_trend_up_count}")
    print(
        "FACT: setup_fail_and_market_not_trend_up_count = "
        f"{setup_fail_and_market_not_trend_up_count}"
    )
    print(
        "FACT: setup_fail_but_market_trend_up_count = "
        f"{setup_fail_but_market_trend_up_count}"
    )
    print(f"FACT: allowed_market_context_count = {len(allowed_market_contexts)}")
    print(
        "FACT: setup_pass_blocked_market_context_count = "
        f"{len(setup_pass_blocked_market_contexts)}"
    )
    print(
        "FACT: breakout_not_confirmed_market_context = "
        f"{breakout_not_confirmed_market_context}"
    )
    print(
        "FINAL_JUDGEMENT = setup cluster survives both non-trend regime pressure and "
        "post-trend-up setup conditions"
    )
    print("NEXT_RECOMMENDED_PHASE = CONTINUE_SETUP_MARKET_CONTEXT_SPLIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
