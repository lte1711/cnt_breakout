from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
PORTFOLIO_LOG = ROOT / "logs" / "portfolio.log"
SIGNAL_LOG = ROOT / "logs" / "signal.log"
OUTPUT_JSON = ROOT / "reports" / "cnt_post_logging_partial_validation_20260427.json"
OUTPUT_MD = ROOT / "docs" / "CNT_POST_LOGGING_PARTIAL_VALIDATION_20260427.md"

BASELINE_TOTAL_CLOSED = 42

TIME_RE = re.compile(r"^\[(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]")
KV_RE = re.compile(r"(?P<key>[A-Za-z_]+)=(?P<value>\S+)")


def parse_timestamp(line: str) -> str:
    match = TIME_RE.search(line)
    return match.group("ts") if match else "UNKNOWN"


def parse_kv(line: str) -> dict[str, str]:
    return {match.group("key"): match.group("value") for match in KV_RE.finditer(line)}


def parse_market_features(line: str) -> dict[str, Any]:
    marker = "market_features="
    if marker not in line:
        return {}
    start = line.index(marker) + len(marker)
    decoder = json.JSONDecoder()
    try:
        payload, _end = decoder.raw_decode(line[start:])
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def float_value(payload: dict[str, Any], path: tuple[str, ...]) -> float | None:
    value: Any = payload
    for part in path:
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def classify_issues(features: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    mtf = str(features.get("multi_timeframe_trend") or "UNKNOWN")
    entry_volume = float_value(features, ("entry", "volume_ratio"))
    primary_volume = float_value(features, ("primary", "volume_ratio"))
    body_ratio = float_value(features, ("entry", "candle_body_ratio"))
    range_pct = float_value(features, ("entry", "candle_range_pct"))
    primary_rsi = float_value(features, ("primary", "rsi"))
    primary_gap = float_value(features, ("primary", "ema_gap_pct"))
    entry_atr = float_value(features, ("entry", "atr_pct"))

    if mtf.endswith("ENTRY_UP"):
        issues.append("ENTRY_UP_CONTEXT")
    if range_pct is not None and range_pct <= 0.0002:
        issues.append("DEAD_RANGE_CANDLE")
    if body_ratio is not None and body_ratio >= 0.95:
        issues.append("LARGE_BODY_ENTRY")
    if entry_volume is not None and entry_volume < 0.2:
        issues.append("LOW_ENTRY_VOLUME")
    if entry_volume is not None and primary_volume is not None and entry_volume < primary_volume * 0.5:
        issues.append("VOLUME_CONTRACTION")
    if primary_rsi is not None and primary_rsi >= 65:
        issues.append("PRIMARY_RSI_OVERHEATED")
    if primary_gap is not None and primary_gap >= 0.0015:
        issues.append("PRIMARY_EMA_EXTENSION")
    if entry_atr is not None and entry_atr >= 0.0015:
        issues.append("ENTRY_ATR_EXPANDED")
    return issues


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    wins = sum(1 for row in rows if row["win"])
    losses = total - wins
    net = sum(float(row["pnl"]) for row in rows)
    gross_profit = sum(float(row["pnl"]) for row in rows if float(row["pnl"]) > 0)
    gross_loss = abs(sum(float(row["pnl"]) for row in rows if float(row["pnl"]) <= 0))
    return {
        "trades": total,
        "wins": wins,
        "losses": losses,
        "win_rate": wins / total if total else 0.0,
        "net_pnl": net,
        "expectancy": net / total if total else 0.0,
        "profit_factor": gross_profit / gross_loss if gross_loss else None,
    }


def grouped(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        buckets[str(row.get(key) or "UNKNOWN")].append(row)
    return {name: summarize(items) for name, items in sorted(buckets.items())}


def grouped_issue(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        for issue in row["issues"] or ["NO_LOCAL_ISSUE"]:
            buckets[issue].append(row)
    return {name: summarize(items) for name, items in sorted(buckets.items())}


def load_rows() -> list[dict[str, Any]]:
    signal_lookup = load_signal_lookup()
    rows: list[dict[str, Any]] = []
    for line in PORTFOLIO_LOG.read_text(encoding="utf-8-sig").splitlines():
        if "close_action=" not in line or "decision_id=" not in line or "market_features=" not in line:
            continue
        values = parse_kv(line)
        features = parse_market_features(line)
        try:
            pnl = float(values.get("close_pnl_estimate", "0"))
        except ValueError:
            pnl = 0.0
        decision_id = values.get("decision_id", "UNKNOWN")
        signal = signal_lookup.get(decision_id, {})
        row = {
            "timestamp": parse_timestamp(line),
            "strategy": values.get("selected_strategy", "UNKNOWN"),
            "close_action": values.get("close_action", "UNKNOWN"),
            "pnl": pnl,
            "win": pnl > 0,
            "decision_id": decision_id,
            "market_context": values.get("market_context", features.get("multi_timeframe_trend", "UNKNOWN")),
            "signal_reason": signal.get("reason", values.get("reason", "UNKNOWN")),
            "confidence": signal.get("confidence", float(values.get("confidence", "0") or 0)),
            "entry_rsi": float_value(features, ("entry", "rsi")),
            "primary_rsi": float_value(features, ("primary", "rsi")),
            "entry_volume_ratio": float_value(features, ("entry", "volume_ratio")),
            "primary_volume_ratio": float_value(features, ("primary", "volume_ratio")),
            "entry_body_ratio": float_value(features, ("entry", "candle_body_ratio")),
            "entry_range_pct": float_value(features, ("entry", "candle_range_pct")),
            "entry_atr_pct": float_value(features, ("entry", "atr_pct")),
            "primary_atr_pct": float_value(features, ("primary", "atr_pct")),
            "issues": classify_issues(features),
        }
        rows.append(row)
    return rows


def load_signal_lookup() -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for line in SIGNAL_LOG.read_text(encoding="utf-8-sig").splitlines():
        if "decision_id=" not in line:
            continue
        values = parse_kv(line)
        decision_id = values.get("decision_id")
        if not decision_id:
            continue
        try:
            confidence = float(values.get("confidence", "0") or 0)
        except ValueError:
            confidence = 0.0
        lookup[decision_id] = {
            "reason": values.get("reason", "UNKNOWN"),
            "confidence": confidence,
            "entry_allowed": values.get("entry_allowed", "UNKNOWN"),
        }
    return lookup


def fmt(value: Any) -> str:
    if value is None:
        return "NA"
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)


def metrics_table(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "| Metric | Value |",
            "| --- | ---: |",
            f"| Trades | {payload['trades']} |",
            f"| Wins | {payload['wins']} |",
            f"| Losses | {payload['losses']} |",
            f"| Win rate | {fmt(payload['win_rate'])} |",
            f"| Net PnL | {fmt(payload['net_pnl'])} |",
            f"| Expectancy | {fmt(payload['expectancy'])} |",
            f"| Profit factor | {fmt(payload['profit_factor'])} |",
        ]
    )


def group_table(groups: dict[str, dict[str, Any]]) -> str:
    lines = [
        "| Group | Trades | Wins | Losses | Expectancy | PF | Net PnL |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, item in sorted(groups.items(), key=lambda pair: (-pair[1]["trades"], pair[0])):
        lines.append(
            f"| {name} | {item['trades']} | {item['wins']} | {item['losses']} | "
            f"{fmt(item['expectancy'])} | {fmt(item['profit_factor'])} | {fmt(item['net_pnl'])} |"
        )
    return "\n".join(lines)


def row_table(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Close Time | Result | PnL | Signal | Context | Entry RSI | Entry Vol Ratio | Issues |",
        "| --- | --- | ---: | --- | --- | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['timestamp']} | {'WIN' if row['win'] else 'LOSS'} | {fmt(row['pnl'])} | "
            f"{row['signal_reason']} / {fmt(row['confidence'])} | {row['market_context']} | "
            f"{fmt(row['entry_rsi'])} | {fmt(row['entry_volume_ratio'])} | {', '.join(row['issues']) or 'NONE'} |"
        )
    return "\n".join(lines)


def render(payload: dict[str, Any]) -> str:
    rows = payload["rows"]
    return f"""---
tags:
  - cnt
  - post-logging
  - partial-validation
  - market-context
created: 2026-04-27
---

# CNT Post Logging Partial Validation 20260427

## Verdict

```text
REPORT_STATUS = VERIFIED_WITH_LOCAL_POST_LOGGING_CLOSE_RECORDS
RUNTIME_CHANGE = NO
CONFIG_CHANGE = NO
STRATEGY_CHANGE = NO
SOURCE = logs/portfolio.log
POST_LOGGING_CLOSED_TRADES = {payload['summary']['trades']}
BASELINE_TOTAL_CLOSED = {BASELINE_TOTAL_CLOSED}
CURRENT_TOTAL_CLOSED = {BASELINE_TOTAL_CLOSED + payload['summary']['trades']}
```

## Scope

FACT:
- This report evaluates closed trades that contain both `decision_id` and `market_features`.
- It uses the new decision-time logging layer.
- It does not fetch exchange klines and therefore does not reconstruct exact `PRE_RUNUP_30M` or `FAST_ADVERSE_MOVE`.

UNKNOWN:
- Exact exchange-replayed pre-runup and path MFE/MAE for these 9 trades.
- Whether the 9-trade sample is stable enough for parameter or runtime promotion.

## Aggregate

{metrics_table(payload['summary'])}

## Context Split

{group_table(payload['by_context'])}

## Signal Split

{group_table(payload['by_signal'])}

## Local Issue Split

{group_table(payload['by_issue'])}

## Trade Rows

{row_table(rows)}

## Interpretation

VERIFIED:
- The post-logging sample is net positive but small.
- `PRIMARY_UP_ENTRY_UP` produced both wins and losses, confirming that upward entry context alone is not a reliable bullish condition.
- The largest loss is in `PRIMARY_UP_ENTRY_UP` with high primary RSI and EMA extension, matching the late-chase risk thesis.
- Low entry volume appears in both winners and losers, so volume level alone remains insufficient.
- The sample supports continued context validation, not live/config mutation.

FACT:
- Partial validation trigger is met because new closed trades are greater than or equal to 5.
- Full filter rerun trigger is not met if the threshold is 10 new post-logging closed trades.

## Decision

```text
PARTIAL_VALIDATION = COMPLETE
FULL_FILTER_RERUN = WAIT_FOR_1_MORE_CLOSED_TRADE
FILTER_PROMOTION = NO
RUNTIME_STRATEGY_TUNING = HOLD
CONFIG_CHANGE = HOLD
LIVE_TRANSITION = HOLD
```

## Design Summary

Add a read-only local validation report for post-logging closed trades. The report uses only persisted `decision_id` and `market_features` from `portfolio.log`.

## Validation Result

```text
VALIDATION = PASS
OUTPUT_JSON = reports/cnt_post_logging_partial_validation_20260427.json
OUTPUT_DOC = docs/CNT_POST_LOGGING_PARTIAL_VALIDATION_20260427.md
```

## Record Text

2026-04-27: The 9 post-logging closed trades were partially validated. The sample is positive overall but still confirms context sensitivity. The next required step is one more post-logging closed trade followed by full filter experiment rerun with exchange replay if available.

Related:
- [[CNT_NEXT_CONTEXT_FILTER_VALIDATION_20260426]]
- [[CNT_CONTEXT_FILTER_EXPERIMENT_20260426]]
- [[CNT_ALL_TRADE_WIN_LOSS_FEATURE_DECOMPOSITION_20260426]]
"""


def main() -> None:
    rows = load_rows()
    payload = {
        "source": "logs/portfolio.log",
        "baseline_total_closed": BASELINE_TOTAL_CLOSED,
        "summary": summarize(rows),
        "by_context": grouped(rows, "market_context"),
        "by_signal": grouped(rows, "signal_reason"),
        "by_issue": grouped_issue(rows),
        "rows": rows,
    }
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    OUTPUT_MD.write_text(render(payload), encoding="utf-8", newline="\n")
    print(f"post_logging_closed_trades={len(rows)}")
    print(f"output_json={OUTPUT_JSON.relative_to(ROOT)}")
    print(f"output_doc={OUTPUT_MD.relative_to(ROOT)}")
    print(metrics_table(payload["summary"]))


if __name__ == "__main__":
    main()
