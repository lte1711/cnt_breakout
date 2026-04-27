from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import BINANCE_BASE_URL, REQUEST_TIMEOUT
from tools.post_logging_partial_validation import (
    parse_kv,
    parse_market_features,
    parse_timestamp,
    summarize as summarize_basic,
)


RUNTIME_LOG = ROOT / "logs" / "runtime.log"
PORTFOLIO_LOG = ROOT / "logs" / "portfolio.log"
OUTPUT_JSON = ROOT / "reports" / "cnt_full_filter_rerun_20260427.json"
OUTPUT_MD = ROOT / "docs" / "CNT_FULL_FILTER_RERUN_20260427.md"
READY_DOC = ROOT / "docs" / "CNT_FULL_FILTER_RERUN_READY_PREP_20260427.md"

SYMBOL = "ETHUSDT"
INTERVAL = "1m"
LOCAL_TZ = ZoneInfo("Asia/Seoul")

DECISION_ID_RE = re.compile(r"decision_id['\"]?: ['\"](?P<decision_id>[^'\"]+)['\"]")
ENTRY_PRICE_RE = re.compile(r"entry_price['\"]?: (?P<entry_price>[0-9.]+)")
ENTRY_TIME_RE = re.compile(r"entry_time['\"]?: ['\"](?P<entry_time>[^'\"]+)['\"]")


def dt_from_log(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").replace(tzinfo=LOCAL_TZ)


def ms(value: datetime) -> int:
    return int(value.timestamp() * 1000)


def load_entry_lookup() -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for line in RUNTIME_LOG.read_text(encoding="utf-8-sig").splitlines():
        if "decision_id" not in line:
            continue
        if "action=BUY_FILLED" not in line and "action=PROMOTE_TO_OPEN_TRADE" not in line:
            continue
        decision_match = DECISION_ID_RE.search(line)
        if not decision_match:
            continue
        decision_id = decision_match.group("decision_id")
        price_match = ENTRY_PRICE_RE.search(line)
        time_match = ENTRY_TIME_RE.search(line)
        timestamp = parse_timestamp(line)
        entry_time_text = time_match.group("entry_time") if time_match else timestamp
        entry_price = float(price_match.group("entry_price")) if price_match else None
        lookup[decision_id] = {
            "decision_id": decision_id,
            "entry_time": entry_time_text,
            "entry_price": entry_price,
        }
    return lookup


def load_closed_rows() -> list[dict[str, Any]]:
    entry_lookup = load_entry_lookup()
    rows: list[dict[str, Any]] = []
    for line in PORTFOLIO_LOG.read_text(encoding="utf-8-sig").splitlines():
        if "close_action=" not in line or "decision_id=" not in line or "market_features=" not in line:
            continue
        values = parse_kv(line)
        decision_id = values.get("decision_id")
        if not decision_id:
            continue
        features = parse_market_features(line)
        entry_data = entry_lookup.get(decision_id, {})
        try:
            pnl = float(values.get("close_pnl_estimate", "0"))
        except ValueError:
            pnl = 0.0
        entry_price = entry_data.get("entry_price")
        if entry_price is None:
            entry_price = float(features.get("last_price", 0.0) or 0.0)
        rows.append(
            {
                "decision_id": decision_id,
                "strategy": values.get("selected_strategy", "UNKNOWN"),
                "entry_time": entry_data.get("entry_time", "UNKNOWN"),
                "close_time": parse_timestamp(line),
                "entry_price": entry_price,
                "pnl": pnl,
                "win": pnl > 0,
                "close_action": values.get("close_action", "UNKNOWN"),
                "market_context": values.get("market_context", features.get("multi_timeframe_trend", "UNKNOWN")),
                "market_features": features,
            }
        )
    return rows


def fetch_klines(symbol: str, start_time: datetime, end_time: datetime) -> list[dict[str, Any]]:
    url = f"{BINANCE_BASE_URL}/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": INTERVAL,
        "startTime": ms(start_time),
        "endTime": ms(end_time),
        "limit": 1000,
    }
    response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    raw = response.json()
    if not isinstance(raw, list):
        raise ValueError("invalid klines response")
    result = []
    for item in raw:
        if not isinstance(item, list) or len(item) < 11:
            raise ValueError("invalid kline item")
        result.append(
            {
                "open_time": int(item[0]),
                "open": float(item[1]),
                "high": float(item[2]),
                "low": float(item[3]),
                "close": float(item[4]),
                "volume": float(item[5]),
                "close_time": int(item[6]),
            }
        )
    return result


def nearest_index(klines: list[dict[str, Any]], target_ms: int) -> int:
    if not klines:
        raise ValueError("no klines")
    return min(range(len(klines)), key=lambda index: abs(int(klines[index]["open_time"]) - target_ms))


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def derive_features(row: dict[str, Any], klines: list[dict[str, Any]]) -> dict[str, Any]:
    entry_dt = dt_from_log(str(row["entry_time"]))
    close_dt = dt_from_log(str(row["close_time"]))
    entry_index = nearest_index(klines, ms(entry_dt))
    close_index = nearest_index(klines, ms(close_dt))
    if close_index < entry_index:
        close_index = entry_index

    entry_price = float(row["entry_price"] or klines[entry_index]["close"])
    pre_30_start = max(0, entry_index - 30)
    pre_60_start = max(0, entry_index - 60)
    pre_5_start = max(0, entry_index - 5)
    pre_10_start = max(0, entry_index - 10)
    after_3_end = min(len(klines), entry_index + 4)

    pre30_open = float(klines[pre_30_start]["open"])
    pre60_open = float(klines[pre_60_start]["open"])
    pre5_open = float(klines[pre_5_start]["open"])
    recent_30 = klines[pre_30_start : entry_index + 1]
    pre_10 = klines[pre_10_start:entry_index]
    pre_5 = klines[pre_5_start:entry_index]
    path = klines[entry_index : close_index + 1]
    early_path = klines[entry_index:after_3_end]

    recent_high_30 = max(float(item["high"]) for item in recent_30) if recent_30 else entry_price
    recent_low_30 = min(float(item["low"]) for item in recent_30) if recent_30 else entry_price
    high_distance_pct = (recent_high_30 - entry_price) / entry_price if entry_price else 0.0
    range_position = (
        (entry_price - recent_low_30) / (recent_high_30 - recent_low_30)
        if recent_high_30 > recent_low_30
        else 0.0
    )

    max_high = max(float(item["high"]) for item in path) if path else entry_price
    min_low = min(float(item["low"]) for item in path) if path else entry_price
    early_low = min(float(item["low"]) for item in early_path) if early_path else entry_price
    volume_10 = mean([float(item["volume"]) for item in pre_10])
    volume_5 = mean([float(item["volume"]) for item in pre_5])

    ret30 = (entry_price - pre30_open) / pre30_open if pre30_open else 0.0
    ret60 = (entry_price - pre60_open) / pre60_open if pre60_open else 0.0
    ret5 = (entry_price - pre5_open) / pre5_open if pre5_open else 0.0
    mfe = (max_high - entry_price) / entry_price if entry_price else 0.0
    mae = (min_low - entry_price) / entry_price if entry_price else 0.0
    early_mae = (early_low - entry_price) / entry_price if entry_price else 0.0
    vol5v5 = volume_5 / volume_10 if volume_10 else 0.0

    issues = []
    market_context = str(row.get("market_context") or "UNKNOWN")
    if ret30 >= 0.0015:
        issues.append("PRE_RUNUP_30M")
    if ret5 >= 0.0010:
        issues.append("SHORT_TERM_CHASE")
    if market_context.endswith("ENTRY_UP"):
        issues.append("ENTRY_UP_CONTEXT")
    if high_distance_pct <= 0.0005 or range_position >= 0.8:
        issues.append("ENTRY_NEAR_HIGH")
    if early_mae <= -0.0015:
        issues.append("FAST_ADVERSE_MOVE")
    if vol5v5 < 0.5:
        issues.append("VOLUME_CONTRACTION")

    return {
        "ret5": ret5,
        "ret30": ret30,
        "ret60": ret60,
        "recent_high_distance_pct": high_distance_pct,
        "recent_range_position": range_position,
        "mfe": mfe,
        "mae": mae,
        "early_mae_3m": early_mae,
        "vol5v5": vol5v5,
        "issues": issues,
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary = summarize_basic(rows)
    count = len(rows)
    summary["avg_ret30"] = mean([float(row.get("ret30", 0.0)) for row in rows]) if count else 0.0
    summary["avg_mfe"] = mean([float(row.get("mfe", 0.0)) for row in rows]) if count else 0.0
    summary["avg_mae"] = mean([float(row.get("mae", 0.0)) for row in rows]) if count else 0.0
    summary["avg_high_distance"] = mean([float(row.get("recent_high_distance_pct", 0.0)) for row in rows]) if count else 0.0
    return summary


def grouped(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        buckets[str(row.get(key) or "UNKNOWN")].append(row)
    return {name: summarize(items) for name, items in sorted(buckets.items())}


def grouped_issue(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        for issue in row.get("issues", []) or ["NO_ISSUE"]:
            buckets[issue].append(row)
    return {name: summarize(items) for name, items in sorted(buckets.items())}


def evaluate_filter(rows: list[dict[str, Any]], name: str, issues: set[str]) -> dict[str, Any]:
    blocked = [row for row in rows if issues.intersection(set(row.get("issues", [])))]
    retained = [row for row in rows if row not in blocked]
    return {
        "name": name,
        "retained": summarize(retained),
        "blocked": summarize(blocked),
        "missed_winners": sum(1 for row in blocked if row.get("win")),
        "blocked_losers": sum(1 for row in blocked if not row.get("win")),
    }


def evaluate_candidates(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    specs = [
        ("block_PRE_RUNUP_30M", {"PRE_RUNUP_30M"}),
        ("block_ENTRY_NEAR_HIGH", {"ENTRY_NEAR_HIGH"}),
        ("block_ENTRY_UP_CONTEXT", {"ENTRY_UP_CONTEXT"}),
        ("block_FAST_ADVERSE_MOVE", {"FAST_ADVERSE_MOVE"}),
        ("block_PRE_RUNUP_OR_ENTRY_NEAR_HIGH", {"PRE_RUNUP_30M", "ENTRY_NEAR_HIGH"}),
        ("block_LATE_CHASE_SET", {"PRE_RUNUP_30M", "ENTRY_NEAR_HIGH", "ENTRY_UP_CONTEXT"}),
        ("block_FULL_RISK_SET", {"PRE_RUNUP_30M", "ENTRY_NEAR_HIGH", "ENTRY_UP_CONTEXT", "FAST_ADVERSE_MOVE"}),
    ]
    return [evaluate_filter(rows, name, issues) for name, issues in specs]


def fmt(value: Any) -> str:
    if value is None:
        return "NA"
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)


def group_table(groups: dict[str, dict[str, Any]]) -> str:
    lines = [
        "| Group | Trades | Wins | Losses | Expectancy | PF | Avg ret30 | Avg MFE | Avg MAE |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, item in sorted(groups.items(), key=lambda pair: (-pair[1]["trades"], pair[0])):
        lines.append(
            f"| {name} | {item['trades']} | {item['wins']} | {item['losses']} | "
            f"{fmt(item['expectancy'])} | {fmt(item['profit_factor'])} | "
            f"{fmt(item['avg_ret30'])} | {fmt(item['avg_mfe'])} | {fmt(item['avg_mae'])} |"
        )
    return "\n".join(lines)


def candidate_table(results: list[dict[str, Any]]) -> str:
    lines = [
        "| Filter | Retained | Missed Winners | Blocked Losers | Retained Expectancy | Retained PF |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for item in results:
        retained = item["retained"]
        lines.append(
            f"| {item['name']} | {retained['trades']} | {item['missed_winners']} | "
            f"{item['blocked_losers']} | {fmt(retained['expectancy'])} | {fmt(retained['profit_factor'])} |"
        )
    return "\n".join(lines)


def row_table(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Entry | Close | Result | PnL | Context | ret30 | High Dist | MFE | MAE | Issues |",
        "| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['entry_time']} | {row['close_time']} | {'WIN' if row['win'] else 'LOSS'} | "
            f"{fmt(row['pnl'])} | {row['market_context']} | {fmt(row['ret30'])} | "
            f"{fmt(row['recent_high_distance_pct'])} | {fmt(row['mfe'])} | {fmt(row['mae'])} | "
            f"{', '.join(row.get('issues', [])) or 'NONE'} |"
        )
    return "\n".join(lines)


def render_report(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    return f"""---
tags:
  - cnt
  - full-filter-rerun
  - exchange-replay
created: 2026-04-27
---

# CNT Full Filter Rerun 20260427

## Verdict

```text
REPORT_STATUS = VERIFIED_WITH_BINANCE_SPOT_TESTNET_1M_KLINES
RUNTIME_CHANGE = NO
CONFIG_CHANGE = NO
STRATEGY_CHANGE = NO
POST_LOGGING_CLOSED_TRADES = {summary['trades']}
```

## Aggregate

| Metric | Value |
| --- | ---: |
| Trades | {summary['trades']} |
| Wins | {summary['wins']} |
| Losses | {summary['losses']} |
| Win rate | {fmt(summary['win_rate'])} |
| Net PnL | {fmt(summary['net_pnl'])} |
| Expectancy | {fmt(summary['expectancy'])} |
| Profit factor | {fmt(summary['profit_factor'])} |
| Avg ret30 | {fmt(summary['avg_ret30'])} |
| Avg MFE | {fmt(summary['avg_mfe'])} |
| Avg MAE | {fmt(summary['avg_mae'])} |

## Context Split

{group_table(payload['by_context'])}

## Issue Split

{group_table(payload['by_issue'])}

## Candidate Filters

{candidate_table(payload['candidates'])}

## Trade Rows

{row_table(payload['rows'])}

## Decision

```text
FILTER_PROMOTION = NO
RUNTIME_STRATEGY_TUNING = HOLD
CONFIG_CHANGE = HOLD
LIVE_TRANSITION = HOLD
```

## Record Text

2026-04-27: Full filter rerun was executed on post-logging closed trades using Binance Spot Testnet 1m klines. This report is an offline validation artifact only.

Related:
- [[CNT_POST_LOGGING_PARTIAL_VALIDATION_20260427]]
- [[CNT_PRE_RUNUP_THRESHOLD_ANALYSIS_20260427]]
"""


def render_ready(rows: list[dict[str, Any]], minimum: int) -> str:
    return f"""---
tags:
  - cnt
  - full-filter-rerun
  - readiness
created: 2026-04-27
---

# CNT Full Filter Rerun Ready Prep 20260427

## Verdict

```text
FULL_FILTER_RERUN_READY_PREP = COMPLETE
RUNTIME_CHANGE = NO
CONFIG_CHANGE = NO
STRATEGY_CHANGE = NO
POST_LOGGING_CLOSED_TRADES = {len(rows)}
MIN_REQUIRED = {minimum}
STATUS = {'READY' if len(rows) >= minimum else 'WAIT'}
```

## Prepared Tool

```text
TOOL = tools/full_filter_rerun_exchange_replay.py
OUTPUT_JSON = reports/cnt_full_filter_rerun_20260427.json
OUTPUT_DOC = docs/CNT_FULL_FILTER_RERUN_20260427.md
```

## Execution Rule

```text
IF post_logging_closed_trades >= 10:
  python tools/full_filter_rerun_exchange_replay.py
ELSE:
  wait
```

## Feature Coverage

```text
PRE_RUNUP_30M = prepared
ENTRY_NEAR_HIGH = prepared
MFE = prepared
MAE = prepared
FAST_ADVERSE_MOVE = prepared
PRIMARY_UP_ENTRY_UP = prepared through market_context split
```

## Current Decision

```text
FILTER_PROMOTION = NO
CONFIG_CHANGE = HOLD
LIVE_TRANSITION = HOLD
```

## Record Text

2026-04-27: Full filter rerun preparation was completed. The replay tool is ready, but actual full rerun remains gated until one more post-logging closed trade is available.

Related:
- [[CNT_POST_LOGGING_PARTIAL_VALIDATION_20260427]]
- [[CNT_PRE_RUNUP_THRESHOLD_ANALYSIS_20260427]]
"""


def run(minimum: int, dry_run: bool) -> int:
    rows = load_closed_rows()
    READY_DOC.write_text(render_ready(rows, minimum), encoding="utf-8", newline="\n")
    if dry_run or len(rows) < minimum:
        print(f"post_logging_closed_trades={len(rows)}")
        print(f"min_required={minimum}")
        print(f"ready_doc={READY_DOC.relative_to(ROOT)}")
        print("status=READY" if len(rows) >= minimum else "status=WAIT")
        return 0

    enriched = []
    for row in rows:
        entry_dt = dt_from_log(str(row["entry_time"]))
        close_dt = dt_from_log(str(row["close_time"]))
        klines = fetch_klines(SYMBOL, entry_dt - timedelta(minutes=70), close_dt + timedelta(minutes=5))
        enriched_row = dict(row)
        enriched_row.update(derive_features(row, klines))
        enriched.append(enriched_row)

    payload = {
        "source": "logs/portfolio.log + Binance Spot Testnet /api/v3/klines",
        "summary": summarize(enriched),
        "by_context": grouped(enriched, "market_context"),
        "by_issue": grouped_issue(enriched),
        "candidates": evaluate_candidates(enriched),
        "rows": enriched,
    }
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    OUTPUT_MD.write_text(render_report(payload), encoding="utf-8", newline="\n")
    print(f"post_logging_closed_trades={len(enriched)}")
    print(f"output_json={OUTPUT_JSON.relative_to(ROOT)}")
    print(f"output_doc={OUTPUT_MD.relative_to(ROOT)}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-trades", type=int, default=10)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    raise SystemExit(run(minimum=args.min_trades, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
