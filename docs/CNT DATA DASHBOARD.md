---
tags:
  - cnt
  - obsidian
  - dashboard
aliases:
  - CNT DATA DASHBOARD
---

# CNT Data Dashboard

이 문서는 Obsidian에서 `Dataview` 플러그인을 사용할 때 CNT 런타임 데이터를 빠르게 확인하기 위한 대시보드다.

## Vault Assumption

이 대시보드는 **vault root가 CNT repository root**일 때를 기준으로 작성됐다.
즉, `C:\\cnt` 전체를 vault로 연 상태에서 `data/*.json`에 직접 접근하는 구성을 전제로 한다.

## Plugin Requirement

- Community plugin: `dataview`
- Optional plugin: `templater-obsidian`

## Strategy Metrics Table

```dataviewjs
const path = 'data/strategy_metrics.json';
let raw = null;
try {
  raw = await app.vault.adapter.read(path);
} catch (error) {
  dv.paragraph(`strategy_metrics.json read failed: ${error}`);
}

if (raw) {
  const metrics = JSON.parse(raw);
  dv.table(
    ["전략", "선택", "종결", "승률", "기대값", "PF"],
    Object.values(metrics).map((s) => [
      s.strategy_name,
      s.signals_selected,
      s.trades_closed,
      `${(s.win_rate * 100).toFixed(1)}%`,
      Number(s.expectancy).toFixed(6),
      Number(s.profit_factor).toFixed(3),
    ]),
  );
}
```

## Live Gate Snapshot

```dataviewjs
const path = 'data/live_gate_decision.json';
let raw = null;
try {
  raw = await app.vault.adapter.read(path);
} catch (error) {
  dv.paragraph(`live_gate_decision.json read failed: ${error}`);
}

if (raw) {
  const gate = JSON.parse(raw);
  dv.table(
    ["항목", "값"],
    [
      ["status", gate.status],
      ["reason", gate.reason],
      ["closed_trades", gate.metrics?.closed_trades ?? ""],
      ["expectancy", gate.metrics?.expectancy ?? ""],
      ["net_pnl", gate.metrics?.net_pnl ?? ""],
    ],
  );
}
```

## Performance Snapshot Summary

```dataviewjs
const path = 'data/performance_snapshot.json';
let raw = null;
try {
  raw = await app.vault.adapter.read(path);
} catch (error) {
  dv.paragraph(`performance_snapshot.json read failed: ${error}`);
}

if (raw) {
  const snap = JSON.parse(raw);
  dv.table(
    ["항목", "값"],
    [
      ["timestamp", snap.timestamp],
      ["total_signals", snap.total_signals],
      ["selected_signals", snap.selected_signals],
      ["executed_trades", snap.executed_trades],
      ["closed_trades", snap.closed_trades],
      ["win_rate", Number(snap.win_rate).toFixed(4)],
      ["expectancy", Number(snap.expectancy).toFixed(6)],
      ["profit_factor", Number(snap.profit_factor).toFixed(4)],
      ["net_pnl", Number(snap.net_pnl).toFixed(6)],
    ],
  );
}
```

## Usage Note

- 이 문서는 Obsidian 내부 확인용 대시보드다.
- 운영 판단은 항상 실제 `data/*.json`, `logs/*.log`, 그리고 [[AGENTS]] 규칙과 함께 읽어야 한다.

---

## Obsidian Links

- [[CNT v2 TESTNET PERFORMANCE REPORT]]
- [[CNT v2 CURRENT STATUS ASSESSMENT]]
- [[00 Docs Index|Docs Index]]
