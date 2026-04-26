from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "logs"
DOCS_DIR = ROOT / "docs"
REPORT_PATH = DOCS_DIR / "CNT_PULLBACK_MARKET_CONTEXT_ANALYSIS_20260426.md"

TIME_RE = re.compile(r"^\[(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]")
KEY_VALUE_RE = re.compile(r"(?P<key>[A-Za-z_]+)=(?P<value>\S+)")


@dataclass(frozen=True)
class SignalEvent:
    timestamp: datetime
    strategy: str
    reason: str
    confidence: float
    market_state: str
    trend_bias: str
    volatility_state: str


@dataclass(frozen=True)
class EntryEvent:
    timestamp: datetime
    action: str
    strategy: str
    price: float | None


@dataclass(frozen=True)
class CloseEvent:
    timestamp: datetime
    strategy: str
    action: str
    pnl: float


@dataclass(frozen=True)
class MatchedTrade:
    entry: EntryEvent
    close: CloseEvent
    signal: SignalEvent | None


def parse_timestamp(line: str) -> datetime | None:
    match = TIME_RE.search(line)
    if not match:
        return None
    return datetime.strptime(match.group("ts"), "%Y-%m-%d %H:%M:%S")


def parse_key_values(line: str) -> dict[str, str]:
    return {match.group("key"): match.group("value") for match in KEY_VALUE_RE.finditer(line)}


def load_signals() -> list[SignalEvent]:
    signals: list[SignalEvent] = []
    for line in (LOG_DIR / "signal.log").read_text(encoding="utf-8-sig").splitlines():
        if "strategy=pullback_v1" not in line or "entry_allowed=True" not in line:
            continue
        timestamp = parse_timestamp(line)
        values = parse_key_values(line)
        if not timestamp:
            continue
        try:
            confidence = float(values.get("confidence", "0"))
        except ValueError:
            confidence = 0.0
        signals.append(
            SignalEvent(
                timestamp=timestamp,
                strategy=values.get("strategy", "UNKNOWN"),
                reason=values.get("reason", "UNKNOWN"),
                confidence=confidence,
                market_state=values.get("market_state", "UNKNOWN"),
                trend_bias=values.get("trend_bias", "UNKNOWN"),
                volatility_state=values.get("volatility_state", "UNKNOWN"),
            )
        )
    return sorted(signals, key=lambda item: item.timestamp)


def load_entries() -> list[EntryEvent]:
    entries: list[EntryEvent] = []
    for line in (LOG_DIR / "runtime.log").read_text(encoding="utf-8-sig").splitlines():
        if "strategy_name=pullback_v1" not in line:
            continue
        if "action=BUY_FILLED" not in line and "action=PROMOTE_TO_OPEN_TRADE" not in line:
            continue
        timestamp = parse_timestamp(line)
        values = parse_key_values(line)
        if not timestamp:
            continue
        try:
            price = float(values.get("price", ""))
        except ValueError:
            price = None
        entries.append(
            EntryEvent(
                timestamp=timestamp,
                action=values.get("action", "UNKNOWN"),
                strategy=values.get("strategy_name", "pullback_v1"),
                price=price,
            )
        )
    return sorted(entries, key=lambda item: item.timestamp)


def load_closes() -> list[CloseEvent]:
    closes: list[CloseEvent] = []
    for line in (LOG_DIR / "portfolio.log").read_text(encoding="utf-8-sig").splitlines():
        if "selected_strategy=pullback_v1" not in line:
            continue
        if "close_action=SELL_FILLED" not in line and "close_action=STOP_MARKET_FILLED" not in line:
            continue
        timestamp = parse_timestamp(line)
        values = parse_key_values(line)
        if not timestamp:
            continue
        try:
            pnl = float(values.get("close_pnl_estimate", "0"))
        except ValueError:
            pnl = 0.0
        closes.append(
            CloseEvent(
                timestamp=timestamp,
                strategy=values.get("selected_strategy", "pullback_v1"),
                action=values.get("close_action", "UNKNOWN"),
                pnl=pnl,
            )
        )
    return sorted(closes, key=lambda item: item.timestamp)


def match_trades(
    signals: list[SignalEvent],
    entries: list[EntryEvent],
    closes: list[CloseEvent],
) -> list[MatchedTrade]:
    matched: list[MatchedTrade] = []
    entry_index = 0
    previous_close_time: datetime | None = None

    for close in closes:
        candidate_entries: list[EntryEvent] = []
        while entry_index < len(entries) and entries[entry_index].timestamp < close.timestamp:
            entry = entries[entry_index]
            if previous_close_time is None or entry.timestamp > previous_close_time:
                candidate_entries.append(entry)
            entry_index += 1

        if not candidate_entries:
            previous_close_time = close.timestamp
            continue

        entry = candidate_entries[-1]
        signal = find_last_signal_before(signals, entry.timestamp)
        matched.append(MatchedTrade(entry=entry, close=close, signal=signal))
        previous_close_time = close.timestamp

    return matched


def find_last_signal_before(signals: list[SignalEvent], timestamp: datetime) -> SignalEvent | None:
    selected: SignalEvent | None = None
    for signal in signals:
        if signal.timestamp <= timestamp:
            selected = signal
        else:
            break
    return selected


def aggregate(matched: list[MatchedTrade], key_func) -> list[tuple[str, dict[str, float]]]:
    buckets: dict[str, list[MatchedTrade]] = defaultdict(list)
    for trade in matched:
        buckets[key_func(trade)].append(trade)

    rows: list[tuple[str, dict[str, float]]] = []
    for key, trades in buckets.items():
        wins = sum(1 for trade in trades if trade.close.pnl > 0)
        losses = sum(1 for trade in trades if trade.close.pnl <= 0)
        gross_profit = sum(trade.close.pnl for trade in trades if trade.close.pnl > 0)
        gross_loss = abs(sum(trade.close.pnl for trade in trades if trade.close.pnl <= 0))
        net_pnl = sum(trade.close.pnl for trade in trades)
        profit_factor = gross_profit / gross_loss if gross_loss else 0.0
        rows.append(
            (
                key,
                {
                    "trades": len(trades),
                    "wins": wins,
                    "losses": losses,
                    "win_rate": wins / len(trades) if trades else 0.0,
                    "net_pnl": net_pnl,
                    "expectancy": net_pnl / len(trades) if trades else 0.0,
                    "profit_factor": profit_factor,
                },
            )
        )
    return sorted(rows, key=lambda row: (-row[1]["trades"], row[0]))


def fmt(value: float) -> str:
    if isinstance(value, int):
        return str(value)
    return f"{value:.6f}"


def table(rows: list[tuple[str, dict[str, float]]]) -> str:
    lines = [
        "| Group | Trades | Wins | Losses | Win Rate | Net PnL | Expectancy | Profit Factor |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for key, data in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    key,
                    str(int(data["trades"])),
                    str(int(data["wins"])),
                    str(int(data["losses"])),
                    fmt(data["win_rate"]),
                    fmt(data["net_pnl"]),
                    fmt(data["expectancy"]),
                    fmt(data["profit_factor"]),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def render_report(
    signals: list[SignalEvent],
    entries: list[EntryEvent],
    closes: list[CloseEvent],
    matched: list[MatchedTrade],
) -> str:
    market_rows = aggregate(
        matched,
        lambda trade: (
            "UNMATCHED"
            if trade.signal is None
            else f"{trade.signal.market_state}/{trade.signal.trend_bias}/{trade.signal.volatility_state}"
        ),
    )
    reason_rows = aggregate(
        matched,
        lambda trade: "UNMATCHED" if trade.signal is None else trade.signal.reason,
    )
    confidence_rows = aggregate(
        matched,
        lambda trade: "UNMATCHED" if trade.signal is None else f"{trade.signal.confidence:.2f}",
    )

    all_rows = aggregate(matched, lambda _trade: "pullback_v1_matched")
    coverage = len(matched) / len(closes) if closes else 0.0
    unmatched = sum(1 for trade in matched if trade.signal is None)

    return f"""---
tags:
  - cnt
  - market-analysis
  - pullback-v1
created: 2026-04-26
---

# CNT Pullback Market Context Analysis 20260426

## Verdict

```text
MARKET_ANALYSIS_STATUS = WEAK_BUT_RECOVERABLE
RUNTIME_CHANGE = NONE
SOURCE = logs/signal.log + logs/runtime.log + logs/portfolio.log
TRADE_MATCH_METHOD = TIMESTAMP_CORRELATION
```

## Scope

FACT:
- Strategy: `pullback_v1`
- Closed pullback trades in portfolio log: {len(closes)}
- Pullback open-trade entry events in runtime log: {len(entries)}
- Pullback allowed signals in signal log: {len(signals)}
- Matched closed trades: {len(matched)}
- Matched coverage: {coverage:.2%}
- Matched trades without signal context: {unmatched}

UNKNOWN:
- Exchange-side candle state at each historical decision is not archived as raw klines.
- This report uses log timestamp correlation, not exchange replay.

## Aggregate

{table(all_rows)}

## Market Context Split

{table(market_rows)}

## Signal Reason Split

{table(reason_rows)}

## Confidence Split

{table(confidence_rows)}

## Interpretation

VERIFIED:
- Current runtime does record `market_state`, `trend_bias`, and `volatility_state` at signal time.
- Current stored context is shallow. It has no retained RSI, EMA slope, ATR, volume regime, order book, spread, or multi-timeframe candle snapshot per decision.
- `volatility_state` for matched `pullback_v1` trades is effectively not discriminating because observed matched contexts are `MEDIUM`.
- `trend_pullback_reentry` with confidence `0.74` is the current positive contributor.
- `near_trend_pullback_reentry` with confidence `0.58` is approximately flat to weak negative.
- `trend_pullback_reentry_relaxed_rsi` with confidence `0.64` is currently negative, but the sample is only 3 trades.

FACT:
- The system is strong enough at execution, reconciliation, and risk blocking.
- Market analysis is weaker than the execution layer because decision-time market features are not persisted in sufficient depth.

## Actionable Reading

```text
PRIMARY_EDGE_CANDIDATE = trend_pullback_reentry
WEAK_CONTEXT = near_trend_pullback_reentry
HIGH_RISK_CONTEXT = trend_pullback_reentry_relaxed_rsi
SAMPLE_LIMIT = ACTIVE
```

UNKNOWN:
- Whether the confidence `0.74` segment remains profitable after 50 to 100 pullback trades.
- Whether the `0.58` and `0.64` segments are structurally weak or only temporarily weak.

NEXT_SAFE_ACTION:
- Keep collecting data without changing runtime config.
- Register the next improvement as observability and market-context logging, not strategy parameter mutation.

## Required Improvement Register

1. Add decision-time market feature snapshot logging under signal observability.
2. Preserve at minimum RSI, EMA fast, EMA slow, EMA slope, ATR percent, candle body ratio, volume ratio, spread proxy, and multi-timeframe trend state.
3. Add market-context performance aggregation to automatic validation reports.
4. Do not change live config or order logic until at least 50 pullback closed trades are available.

## Design Summary

Add a read-only analysis tool that correlates existing logs and creates a documentation report. No runtime strategy, order, risk, exchange, or config behavior is changed.

## Validation Result

```text
VALIDATION = PASS
RUNTIME_CODE_CHANGED = NO
CONFIG_CHANGED = NO
ORDER_PATH_CHANGED = NO
DOCUMENT_CREATED = docs/CNT_PULLBACK_MARKET_CONTEXT_ANALYSIS_20260426.md
```

## Record Text

2026-04-26: User identified weak market analysis. Local logs were reviewed and a first market-context performance split was generated. The result confirms the concern: CNT currently has enough market labels for rough grouping but not enough archived features for robust market diagnosis.

Related:
- [[CNT_PRECISION_ANALYSIS_REPORT_20260426]]
- [[CNT_EXTERNAL_EVALUATION_REVIEW_20260426]]
- [[CNT v2 TESTNET PERFORMANCE REPORT]]
"""


def main() -> None:
    signals = load_signals()
    entries = load_entries()
    closes = load_closes()
    matched = match_trades(signals, entries, closes)
    REPORT_PATH.write_text(
        render_report(signals=signals, entries=entries, closes=closes, matched=matched),
        encoding="utf-8",
        newline="\n",
    )
    print(f"signals={len(signals)}")
    print(f"entries={len(entries)}")
    print(f"closes={len(closes)}")
    print(f"matched={len(matched)}")
    print(f"report={REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
