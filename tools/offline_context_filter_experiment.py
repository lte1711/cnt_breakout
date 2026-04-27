from __future__ import annotations

import json
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = ROOT / "reports" / "cnt_all_trade_exchange_feature_analysis_20260426.json"
OUTPUT_JSON_PATH = ROOT / "reports" / "cnt_context_filter_experiment_20260426.json"
OUTPUT_MD_PATH = ROOT / "docs" / "CNT_CONTEXT_FILTER_EXPERIMENT_20260426.md"


Trade = dict
Predicate = Callable[[Trade], bool]


def has_issue(issue: str) -> Predicate:
    return lambda trade: issue in trade.get("issues", [])


def any_issue(*issues: str) -> Predicate:
    issue_set = set(issues)
    return lambda trade: bool(issue_set.intersection(trade.get("issues", [])))


def issue_and(*issues: str) -> Predicate:
    issue_set = set(issues)
    return lambda trade: issue_set.issubset(set(trade.get("issues", [])))


def feature_value(trade: Trade, key: str) -> float | None:
    value = trade.get(key)
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def load_trades() -> list[Trade]:
    payload = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    return list(payload.get("rows", []))


def summarize(trades: list[Trade]) -> dict:
    total = len(trades)
    wins = sum(1 for trade in trades if trade.get("win"))
    losses = total - wins
    net_pnl = sum(float(trade.get("pnl", 0.0)) for trade in trades)
    gross_profit = sum(float(trade.get("pnl", 0.0)) for trade in trades if float(trade.get("pnl", 0.0)) > 0)
    gross_loss = abs(sum(float(trade.get("pnl", 0.0)) for trade in trades if float(trade.get("pnl", 0.0)) <= 0))

    max_consecutive_losses = 0
    current_losses = 0
    for trade in trades:
        if trade.get("win"):
            current_losses = 0
        else:
            current_losses += 1
            max_consecutive_losses = max(max_consecutive_losses, current_losses)

    return {
        "trades": total,
        "wins": wins,
        "losses": losses,
        "win_rate": wins / total if total else 0.0,
        "net_pnl": net_pnl,
        "expectancy": net_pnl / total if total else 0.0,
        "profit_factor": gross_profit / gross_loss if gross_loss else None,
        "max_consecutive_losses": max_consecutive_losses,
    }


def evaluate_filter(name: str, predicate: Predicate, trades: list[Trade]) -> dict:
    blocked = [trade for trade in trades if predicate(trade)]
    retained = [trade for trade in trades if not predicate(trade)]
    blocked_winners = [trade for trade in blocked if trade.get("win")]
    blocked_losers = [trade for trade in blocked if not trade.get("win")]

    return {
        "name": name,
        "retained": summarize(retained),
        "blocked": summarize(blocked),
        "missed_winners": len(blocked_winners),
        "blocked_losers": len(blocked_losers),
        "missed_winner_pnl": sum(float(trade.get("pnl", 0.0)) for trade in blocked_winners),
        "blocked_loser_loss": abs(sum(float(trade.get("pnl", 0.0)) for trade in blocked_losers)),
        "retained_trades": retained,
        "blocked_trades": blocked,
    }


def format_float(value: float | None) -> str:
    if value is None:
        return "NA"
    return f"{value:.6f}"


def format_result_table(results: list[dict]) -> str:
    lines = [
        "| Filter | Retained | Missed Winners | Blocked Losers | Retained Win Rate | Retained Expectancy | Retained PF | Max CL | Net PnL |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for result in results:
        retained = result["retained"]
        lines.append(
            "| "
            + " | ".join(
                [
                    result["name"],
                    str(retained["trades"]),
                    str(result["missed_winners"]),
                    str(result["blocked_losers"]),
                    format_float(retained["win_rate"]),
                    format_float(retained["expectancy"]),
                    format_float(retained["profit_factor"]),
                    str(retained["max_consecutive_losses"]),
                    format_float(retained["net_pnl"]),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def format_blocked_table(result: dict, limit: int = 10) -> str:
    blocked = result["blocked_trades"][:limit]
    if not blocked:
        return "No blocked trades."
    lines = [
        "| Entry | PnL | Win | Signal | Context | Issues |",
        "| --- | ---: | --- | --- | --- | --- |",
    ]
    for trade in blocked:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(trade.get("entry", "")),
                    format_float(float(trade.get("pnl", 0.0))),
                    str(trade.get("win", "")),
                    str(trade.get("signal", "")),
                    str(trade.get("ctx", "")),
                    ", ".join(trade.get("issues", [])),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def render_report(baseline: dict, results: list[dict]) -> str:
    best_by_expectancy = max(results, key=lambda item: item["retained"]["expectancy"])
    best_by_pf = max(
        results,
        key=lambda item: item["retained"]["profit_factor"]
        if item["retained"]["profit_factor"] is not None
        else -1.0,
    )

    return f"""---
tags:
  - cnt
  - offline-experiment
  - context-filter
  - pullback-v1
created: 2026-04-26
---

# CNT Context Filter Experiment 20260426

## Verdict

```text
RUNTIME_CHANGE = NO
LIVE_CHANGE = NO
CONFIG_CHANGE = NO
EXPERIMENT = YES
MODE = OFFLINE_REPLAY_ONLY
SOURCE = reports/cnt_all_trade_exchange_feature_analysis_20260426.json
```

## Baseline

| Metric | Value |
| --- | ---: |
| Trades | {baseline['trades']} |
| Wins | {baseline['wins']} |
| Losses | {baseline['losses']} |
| Win Rate | {format_float(baseline['win_rate'])} |
| Net PnL | {format_float(baseline['net_pnl'])} |
| Expectancy | {format_float(baseline['expectancy'])} |
| Profit Factor | {format_float(baseline['profit_factor'])} |
| Max Consecutive Losses | {baseline['max_consecutive_losses']} |

## Candidate Results

{format_result_table(results)}

## Best Candidates

```text
BEST_BY_EXPECTANCY = {best_by_expectancy['name']}
BEST_BY_PF = {best_by_pf['name']}
```

Interpretation:
- The experiment is a replay calculation only.
- A high retained result is not approval to change `config.py` or live runtime.
- Missed winners are as important as blocked losers.

## Blocked Trade Samples

### {best_by_expectancy['name']}

{format_blocked_table(best_by_expectancy)}

## Decision

```text
FILTER_PROMOTION = NO
RUNTIME_STRATEGY_TUNING = HOLD
NEXT_REQUIRED = validate on new post-logging trades
```

## Design Summary

This tool applies candidate context filters to the existing 42 matched closed trades. It computes retained trades, missed winners, blocked losers, win rate, expectancy, profit factor, net PnL, and max consecutive losses. It does not change runtime code, config, order logic, or strategy selection.

## Validation Result

```text
VALIDATION = PASS
INPUT_TRADES = {baseline['trades']}
OUTPUT_JSON = reports/cnt_context_filter_experiment_20260426.json
OUTPUT_DOC = docs/CNT_CONTEXT_FILTER_EXPERIMENT_20260426.md
RUNTIME_CODE_CHANGED = NO
CONFIG_CHANGED = NO
```

## Record Text

2026-04-26: Offline context filter experiment was run against the 42-trade exchange-feature dataset. Results are for hypothesis ranking only and must be validated on new post-logging trades before any runtime use.

Related:
- [[CNT_ALL_TRADE_WIN_LOSS_FEATURE_DECOMPOSITION_20260426]]
- [[CNT_EXCHANGE_REPLAY_MARKET_CONTEXT_REVIEW_20260426]]
- [[CNT_MARKET_CONTEXT_LOGGING_LAYER_IMPLEMENTATION_20260426]]
"""


def main() -> None:
    trades = load_trades()
    baseline = summarize(trades)
    candidates: list[tuple[str, Predicate]] = [
        ("block_PRE_RUNUP_30M", has_issue("PRE_RUNUP_30M")),
        ("block_ENTRY_UP_CONTEXT", has_issue("ENTRY_UP_CONTEXT")),
        ("block_DEAD_RANGE_CANDLE", has_issue("DEAD_RANGE_CANDLE")),
        ("mark_FAST_ADVERSE_MOVE_block", has_issue("FAST_ADVERSE_MOVE")),
        ("block_VOLUME_CONTRACTION", has_issue("VOLUME_CONTRACTION")),
        (
            "block_PRE_RUNUP_OR_ENTRY_UP",
            any_issue("PRE_RUNUP_30M", "ENTRY_UP_CONTEXT"),
        ),
        (
            "block_PRE_RUNUP_OR_DEAD_RANGE",
            any_issue("PRE_RUNUP_30M", "DEAD_RANGE_CANDLE"),
        ),
        (
            "block_ENTRY_UP_OR_DEAD_RANGE",
            any_issue("ENTRY_UP_CONTEXT", "DEAD_RANGE_CANDLE"),
        ),
        (
            "block_CORE_RISK_SET",
            any_issue("PRE_RUNUP_30M", "ENTRY_UP_CONTEXT", "DEAD_RANGE_CANDLE"),
        ),
        (
            "block_CORE_RISK_PLUS_VOLUME_CONTRACTION",
            any_issue("PRE_RUNUP_30M", "ENTRY_UP_CONTEXT", "DEAD_RANGE_CANDLE", "VOLUME_CONTRACTION"),
        ),
        (
            "block_PRE_RUNUP_AND_ENTRY_UP_ONLY",
            issue_and("PRE_RUNUP_30M", "ENTRY_UP_CONTEXT"),
        ),
    ]
    results = [evaluate_filter(name, predicate, trades) for name, predicate in candidates]

    json_payload = {
        "baseline": baseline,
        "results": [
            {key: value for key, value in result.items() if key not in {"retained_trades", "blocked_trades"}}
            for result in results
        ],
    }
    OUTPUT_JSON_PATH.write_text(json.dumps(json_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    OUTPUT_MD_PATH.write_text(render_report(baseline, results), encoding="utf-8", newline="\n")

    print(f"input_trades={baseline['trades']}")
    print(f"output_json={OUTPUT_JSON_PATH.relative_to(ROOT)}")
    print(f"output_doc={OUTPUT_MD_PATH.relative_to(ROOT)}")
    print(format_result_table(results))


if __name__ == "__main__":
    main()
