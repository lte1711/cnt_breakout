---
tags:
  - cnt
  - docs
  - v2
aliases:
  - CNT v2 ENGINE DECOMPOSITION DESIGN KO
---

# CNT v2 엔진 분해 설계

```text
DOCUMENT_NAME = cnt_v2_engine_decomposition_design_ko
PROJECT       = CNT
VERSION       = 2.0
DATE          = 2026-04-19
STATUS        = DESIGN_READY
GOAL          = REDUCE_ENGINE_SIZE_WITHOUT_BREAKING_RUNTIME_RULES
```

---

# 1. 설계 목표

현재 문제:

* `src/engine.py`가 너무 많은 책임을 가지고 있음
* 이 때문에 회귀 위험이 커지고 런타임 reasoning 비용도 높아짐

설계 목표:

* 기존 entry chain과 runtime truth rule 유지
* orchestration 세부사항을 더 작은 서비스로 이동
* one-shot scheduler execution model 유지
* `engine.py`를 coordinator-only 책임에 가깝게 축소

목표 해석:

```text
engine.py = cycle coordinator
services  = domain behavior owners
```

---

# 2. 제안 분리

## 2.1 Pending Reconciliation Service

제안 파일:

* `src/services/pending_reconciliation_service.py`

책임:

* pending order state normalization
* exchange-side order lookup
* buy fill promotion
* sell fill resolution
* stale / invalid pending cleanup
* pending status classification

입력:

* symbol
* pending order
* open trade

출력:

* action
* pending_after
* open_trade_after
* fill_order

## 2.2 Trade Lifecycle Service

제안 파일:

* `src/services/trade_lifecycle_service.py`

책임:

* open-trade normalization
* runtime field updates
* `highest_price_since_entry`
* `entry_time`
* close pnl estimation
* strategy metrics updates
* risk metrics updates

입력:

* open trade
* fill price
* timestamp
* strategy metrics
* risk metrics

출력:

* updated open trade
* updated strategy metrics
* updated risk metrics
* close summary payload

## 2.3 Execution Service

제안 파일:

* `src/services/execution_service.py`

책임:

* entry order submit
* target/time/partial limit submit
* protective market submit
* pending cancel before protective override
* order response normalization

입력:

* signal / exit signal
* validated order values
* filters
* current open trade

출력:

* action
* pending_after
* open_trade_after
* reason

## 2.4 State Persistence Service

제안 파일:

* `src/services/cycle_persistence_service.py`

책임:

* state object normalization
* runtime log append
* portfolio state update
* snapshot generation
* report generation
* live gate save

메모:

이 서비스는 business logic이 아니라 cycle writeout layer다.

---

# 3. 분해 후 엔진

분해 후 `src/engine.py`의 기대 책임:

1. load current state
2. run prechecks
3. call pending reconciliation service
4. call open-trade reconciliation service
5. call exit evaluation / execution service
6. call signal orchestration / entry decision
7. call persistence service
8. handle top-level exceptions

즉 engine은 coordinator로 남되, reconciliation과 execution 세부 내부 로직을 직접 소유하지 않게 된다.

---

# 4. 제안 마이그레이션 순서

권장 순서:

```text
Step 1. extract pending reconciliation service
Step 2. extract trade lifecycle service
Step 3. extract execution service
Step 4. extract persistence/update service
Step 5. shrink engine.py to coordinator form
```

이유:

* pending reconciliation은 경계가 가장 분명함
* trade lifecycle math와 metrics는 분리 가능
* execution logic은 가장 민감하므로 helper가 준비된 뒤에 옮기는 것이 맞음
* persistence는 runtime side effect를 안정적으로 유지하기 위해 마지막에 분리하는 것이 좋음

---

# 5. 리팩터 안전 규칙

분해 과정에서 바뀌면 안 되는 것:

* entry chain: `run.ps1 -> main.py -> src.engine.start_engine`
* one-shot scheduler model
* exchange-truth-over-local-state rule
* single-position current operating rule
* live gate thresholds
* existing strategy contracts

분해 후에도 유지해야 하는 런타임 산출물:

* `state.json`
* `portfolio_state.json`
* `strategy_metrics.json`
* `performance_snapshot.json`
* `live_gate_decision.json`
* `runtime.log`
* `portfolio.log`

---

# 6. 상태 의미 후속 과제

분해 후에 일정 잡을 만한 후속 설계 과제:

`state.status`의 의미를 더 명확히 하는 것

후보 값:

* `cycle_completed`
* `waiting_next_schedule`
* `error`
* `pending_reconcile`
* `open_trade_active`

이건 1차 분해에서 꼭 필요한 것은 아니지만, 책임 분리 뒤에 이어가기 좋은 과제다.

---

# 7. 현재 결정

```text
DECOMPOSITION = DESIGN_READY
IMPLEMENTATION = NOT_STARTED
PREREQUISITE  = KEEP COLLECTING TESTNET EVIDENCE WHILE REFACTORING CAREFULLY
```

## Obsidian Links

- [[00 CNT Vault Home|Vault Home]]
- [[00 Docs Index|Docs Index]]

### Related
- [[00 Docs Index|Docs Index]]
