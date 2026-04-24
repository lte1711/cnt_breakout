---
aliases:
  - EXTRA ITEMS REGISTER
---

﻿CNT EXTRA ITEMS REGISTER

목적:
- 구현 작업지시서 범위를 벗어나지만 현재 저장소에 존재하는 항목을 기록한다.
- 즉시 제거하지 않고, 나중에 유지/제거/문서화 여부를 다시 판단할 수 있도록 남긴다.
- 앞으로 새로 발견되는 초과 항목도 이 문서에 계속 누적한다.

운영 규칙:
- 새 초과 항목은 기존 내용을 지우지 않고 아래에 추가한다.
- 각 항목은 날짜, 구분, 경로, 이유, 현재 판단을 함께 기록한다.
- 제거 결정이 나도 기존 기록은 남기고 상태만 갱신한다.

기록 형식:
- DATE=YYYY-MM-DD
- TYPE=code|config|editor|doc|runtime|compat
- PATH=...
- SUMMARY=...
- REASON=...
- CURRENT_DECISION=keep|optional|review_later|remove_later
- NOTE=...

CHANGE LOG

- DATE=2026-04-19
- TYPE=config
- PATH=config.py
- SUMMARY=repo-root .env 자동 로드 지원
- REASON=실행 편의성과 환경변수 관리 단순화를 위해 추가됨. 구현 작업지시서 v1의 직접 요구 사항은 아님.
- CURRENT_DECISION=review_later
- NOTE=운영 진행에는 유용하지만 전략 아키텍처 구현의 필수 항목은 아님.

- DATE=2026-04-19
- TYPE=editor
- PATH=.vscode/settings.json
- SUMMARY=VS Code 터미널 .env 자동 주입 설정
- REASON=개발 편의성 향상 목적. 구현 작업지시서 v1 범위 밖의 편의 설정임.
- CURRENT_DECISION=review_later
- NOTE=에디터 종속 설정이라 배포/운영 필수 요소는 아님.

- DATE=2026-04-19
- TYPE=config
- PATH=.env.example
- SUMMARY=.env 예시 파일 추가
- REASON=환경변수 입력 형식 안내 목적. 구현 작업지시서 v1의 직접 요구 사항은 아님.
- CURRENT_DECISION=review_later
- NOTE=신규 작업자 온보딩에는 유용함.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/engine_runtime_validation_checklist_v1.md
- SUMMARY=읽기 전용 및 1회 실행 검증 체크리스트
- REASON=검증 절차 표준화를 위해 추가됨. 구현 작업지시서 v1의 직접 구현 요구는 아님.
- CURRENT_DECISION=review_later
- NOTE=운영 전 점검 문서로는 가치가 있으나 필수 코드는 아님.

- DATE=2026-04-19
- TYPE=compat
- PATH=src/strategy_signal.py
- SUMMARY=신규 strategy_manager 구조를 감싸는 호환 래퍼 유지
- REASON=구조 전환 중 기존 호출부와의 호환성 확보 목적. 구현 작업지시서 v1의 핵심 산출물은 아님.
- CURRENT_DECISION=review_later
- NOTE=새 구조가 완전히 안정화되면 deprecated 또는 제거 후보가 될 수 있음.

- DATE=2026-04-19
- TYPE=code
- PATH=src/engine.py
- SUMMARY=청산 응답 상태를 FILLED/SUBMITTED로 구분하는 보수적 해석 보강
- REASON=실주문 응답 처리 안정성 향상을 위해 추가됨. 구현 작업지시서 v1의 직접 항목은 아니지만 운영 안전성에 도움이 됨.
- CURRENT_DECISION=keep
- NOTE=현재 운영 기준에서는 유지 가치가 큼.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/DESIGN SUMMARY.md
- SUMMARY=작업 설계 요약 문서
- REASON=작업 기록 목적. 구현 작업지시서 v1의 직접 구현 범위는 아님.
- CURRENT_DECISION=review_later
- NOTE=기록성 문서.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/RECORD TEXT.md
- SUMMARY=작업 결과 기록 문서
- REASON=작업 기록 목적. 구현 작업지시서 v1의 직접 구현 범위는 아님.
- CURRENT_DECISION=review_later
- NOTE=기록성 문서.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/VALIDATION RESULT.md
- SUMMARY=검증 결과 기록 문서
- REASON=검증 기록 목적. 구현 작업지시서 v1의 직접 구현 범위는 아님.
- CURRENT_DECISION=review_later
- NOTE=기록성 문서.

- DATE=2026-04-19
- TYPE=runtime
- PATH=archive/legacy_root_files
- SUMMARY=루트 구버전 state.json 및 runtime.log 보존 디렉터리
- REASON=루트 정리(T10) 과정에서 삭제 대신 보존 이동을 선택하며 추가됨. 구현 작업지시서 v1의 직접 산출물은 아님.
- CURRENT_DECISION=review_later
- NOTE=증적 보존 목적의 아카이브 경로.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/SHARING CHECKLIST.md
- SUMMARY=외부 공유 전 점검 체크리스트
- REASON=배포 위생(T16) 정리를 위해 추가됨. 구현 작업지시서 v1의 직접 구현 항목은 아님.
- CURRENT_DECISION=review_later
- NOTE=공유/배포 절차 표준화 목적.

- DATE=2026-04-19
- TYPE=doc
- PATH=scripts/export_shareable_zip.ps1
- SUMMARY=.env와 .git 등을 제외한 공유용 ZIP 생성 스크립트
- REASON=배포 위생(T16) 정리를 위해 추가됨. 구현 작업지시서 v1의 직접 구현 항목은 아님.
- CURRENT_DECISION=review_later
- NOTE=외부 제출용 산출물 생성 보조 스크립트.
- DATE=2026-04-19
- TYPE=doc
- PATH=docs/cnt_v1_closure_validation_report.md
- SUMMARY=v1 마감 검증 최종 보고서
- REASON=v1 마감 판정을 재검토 가능하게 남기기 위한 독립 산출물. 구현 작업지시서 v1의 직접 코드 요구사항은 아니며 검증/인수 목적의 추가 문서.
- CURRENT_DECISION=review_later
- NOTE=마감 판정 근거와 PASS/FAIL 결과를 한곳에 고정하는 문서.
- DATE=2026-04-19
- TYPE=code
- PATH=src/models/execution_decision.py
- SUMMARY=ExecutionDecision dataclass 추가
- REASON=v1.1에서 신호와 실행 결정을 분리하기 위한 신규 모델. v1 직접 범위 밖의 확장 항목.
- CURRENT_DECISION=keep
- NOTE=engine가 주문 실행 여부를 구조화해서 받는 기준 모델.

- DATE=2026-04-19
- TYPE=code
- PATH=src/models/risk_result.py
- SUMMARY=RiskCheckResult dataclass 추가
- REASON=v1.1 risk_guard 결과를 표준화하기 위한 신규 모델. 확장용 항목.
- CURRENT_DECISION=keep
- NOTE=risk_guard의 passed/reason 계약을 고정.

- DATE=2026-04-19
- TYPE=code
- PATH=src/execution_decider.py
- SUMMARY=ExecutionDecision 생성 레이어 추가
- REASON=StrategySignal과 실제 실행 가능 여부를 분리하는 v1.1 핵심 확장.
- CURRENT_DECISION=keep
- NOTE=gate 이후 validator/executor 이전에 위치.

- DATE=2026-04-19
- TYPE=code
- PATH=src/risk/risk_guard.py
- SUMMARY=state 기반 risk guard 추가
- REASON=로그 파싱 없이 daily loss limit과 cooldown 차단을 수행하기 위한 v1.1 확장.
- CURRENT_DECISION=keep
- NOTE=signal, state, balance를 입력으로 사용.

- DATE=2026-04-19
- TYPE=code
- PATH=src/signal_logger.py
- SUMMARY=signal observability 레이어 추가
- REASON=진입 허용/차단 사유를 signal.log에 별도 기록하기 위한 v1.1 확장.
- CURRENT_DECISION=keep
- NOTE=runtime.log와 분리된 전략 신호 관측 로그.

- DATE=2026-04-19
- TYPE=runtime
- PATH=logs/signal.log
- SUMMARY=전략 신호 기록 로그 파일
- REASON=signal_logger 연결로 생성되는 신규 운영 로그 대상.
- CURRENT_DECISION=keep
- NOTE=entry_allowed, trigger, reason, confidence 등의 관측 기록용.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v1.1 IMPLEMENTATION VALIDATION REPORT.md
- SUMMARY=v1.1 Stage 1 구현 검증 보고서
- REASON=Stage 1 구현 결과를 체크리스트 기준으로 재검토 가능하게 남기기 위한 문서.
- CURRENT_DECISION=keep
- NOTE=Stage 1 완료, Stage 2 미구현 상태를 명시하는 기준 보고서.

- DATE=2026-04-19
- TYPE=compat
- PATH=src/strategy_signal.py
- SUMMARY=legacy compatibility wrapper 제거 완료
- REASON=v1.1 Stage 1에서 내부 참조 0건 확인 후 wrapper 제거가 완료됨.
- CURRENT_DECISION=removed
- NOTE=기존 compat 항목은 이력 보존용이며, 현재 파일은 저장소에 존재하지 않음.

- DATE=2026-04-19
- TYPE=code
- PATH=src/models/exit_signal.py
- SUMMARY=Stage 2 ExitSignal dataclass 추가
- REASON=Stage 2에서 exit 판단과 실행 경로를 분리하기 위한 신규 모델.
- CURRENT_DECISION=keep
- NOTE=should_exit, exit_type, reason, partial_qty 등을 구조화하는 기준 모델.

- DATE=2026-04-19
- TYPE=code
- PATH=src/risk/enhanced_exit_manager.py
- SUMMARY=Stage 2 exit evaluation 레이어 추가
- REASON=trailing stop, time exit, partial exit를 기존 엔진 실행 경로 위에 확장하기 위한 신규 모듈.
- CURRENT_DECISION=keep
- NOTE=판단만 수행하고 실제 주문 실행은 engine의 기존 SELL 경로를 사용.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v1.1 STAGE 2 IMPLEMENTATION VALIDATION REPORT.md
- SUMMARY=Stage 2 구현 검증 보고서
- REASON=Stage 2 구현 결과를 체크리스트 기준으로 재검토 가능하게 남기기 위한 문서.
- CURRENT_DECISION=keep
- NOTE=Stage 2 완료 및 승인 상태를 고정하는 기준 보고서.

- DATE=2026-04-19
- TYPE=code
- PATH=src/portfolio/strategy_orchestrator.py
- SUMMARY=v2 multi-strategy orchestrator 추가
- REASON=다중 전략 신호 수집과 선택을 상위 레이어로 분리하기 위한 v2 확장.
- CURRENT_DECISION=keep
- NOTE=engine가 직접 단일 strategy_manager 결과만 보지 않도록 연결.

- DATE=2026-04-19
- TYPE=code
- PATH=src/portfolio/signal_ranker.py
- SUMMARY=v2 signal ranking 레이어 추가
- REASON=복수 전략 신호 중 선택 정책을 독립 레이어로 분리하기 위한 v2 확장.
- CURRENT_DECISION=keep
- NOTE=초기 정책은 confidence 최고값 1개 선택.

- DATE=2026-04-19
- TYPE=code
- PATH=src/models/position_state.py
- SUMMARY=v2 PositionState dataclass 추가
- REASON=단일 open_trade를 넘어 포지션 단위 상태 모델을 도입하기 위한 v2 확장.
- CURRENT_DECISION=keep
- NOTE=portfolio_state의 open_positions 구성 요소.

- DATE=2026-04-19
- TYPE=code
- PATH=src/models/portfolio_state.py
- SUMMARY=v2 PortfolioState dataclass 추가
- REASON=포트폴리오 단위 노출과 포지션 상태를 별도 schema로 관리하기 위한 v2 확장.
- CURRENT_DECISION=keep
- NOTE=기존 state.json과 분리된 2.0 schema 사이드카 상태.

- DATE=2026-04-19
- TYPE=code
- PATH=src/state/state_manager.py
- SUMMARY=v2 portfolio state manager 추가
- REASON=portfolio_state load/save와 runtime state 변환을 분리하기 위한 v2 확장.
- CURRENT_DECISION=keep
- NOTE=data/portfolio_state.json 관리 담당.

- DATE=2026-04-19
- TYPE=code
- PATH=src/risk/portfolio_risk_manager.py
- SUMMARY=v2 portfolio risk manager 추가
- REASON=계정 전체 노출과 one-per-symbol 정책을 execution_decider 상위에서 차단하기 위한 v2 확장.
- CURRENT_DECISION=keep
- NOTE=MAX_PORTFOLIO_EXPOSURE와 ONE_PER_SYMBOL_POLICY 반영.

- DATE=2026-04-19
- TYPE=code
- PATH=src/market/spot_adapter.py
- SUMMARY=spot adapter 추가
- REASON=시장 타입별 실행 차이를 adapter 레이어로 분리하기 위한 v2 확장.
- CURRENT_DECISION=keep
- NOTE=현재는 dry path 중심 구조 제공.

- DATE=2026-04-19
- TYPE=code
- PATH=src/market/futures_adapter.py
- SUMMARY=futures adapter 추가
- REASON=leverage, margin_mode, reduce_only 등 futures 전용 파라미터를 분리하기 위한 v2 확장.
- CURRENT_DECISION=keep
- NOTE=현재는 dry path 중심 구조 제공.

- DATE=2026-04-19
- TYPE=code
- PATH=src/execution/order_router.py
- SUMMARY=v2 market order router 추가
- REASON=spot/futures adapter 분기를 실행 레이어에서 분리하기 위한 v2 확장.
- CURRENT_DECISION=keep
- NOTE=현재는 dry routing 검증용 구조 포함.

- DATE=2026-04-19
- TYPE=code
- PATH=src/logging/portfolio_logger.py
- SUMMARY=v2 portfolio logger 추가
- REASON=선택된 전략과 포트폴리오 수준 의사결정을 별도 로그로 남기기 위한 v2 확장.
- CURRENT_DECISION=keep
- NOTE=logs/portfolio.log 기록 담당.

- DATE=2026-04-19
- TYPE=runtime
- PATH=data/portfolio_state.json
- SUMMARY=v2 portfolio sidecar state 파일
- REASON=기존 state.json과 분리된 portfolio schema 2.0 상태 저장 대상.
- CURRENT_DECISION=keep
- NOTE=단일 런타임 state와 별개로 portfolio 관점 상태를 저장.

- DATE=2026-04-19
- TYPE=runtime
- PATH=logs/portfolio.log
- SUMMARY=v2 portfolio decision 로그 파일
- REASON=selected strategy 및 portfolio-level decision을 관측하기 위한 신규 로그 대상.
- CURRENT_DECISION=keep
- NOTE=no_ranked_signal 등 포트폴리오 관점 의사결정 기록용.
- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 VALIDATION REPORT.md
- SUMMARY=v2 initial validation wording downgraded to patch-pending baseline
- REASON=initial report overstated routing and operating-readiness versus actual runtime connection and policy enforcement state.
- CURRENT_DECISION=keep
- NOTE=Treat this as structural baseline evidence until the patch validation pass is completed.
- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 POST-OPERATIONAL PATCH VALIDATION REPORT.md
- SUMMARY=v2 post-operational patch validation report added
- REASON=post-operational consistency patch was validated and recorded as a separate report for traceability.
- CURRENT_DECISION=keep
- NOTE=Captures P3-level cleanup and consistency verification after the operational patch baseline.
- DATE=2026-04-19
- TYPE=code
- PATH=src/analytics/strategy_metrics.py
- SUMMARY=v2 performance metrics analytics layer added
- REASON=performance tuning stage requires persistent strategy-level statistics and expectancy calculation.
- CURRENT_DECISION=keep
- NOTE=Owns save/load/update helpers for strategy performance metrics.

- DATE=2026-04-19
- TYPE=code
- PATH=src/models/strategy_performance.py
- SUMMARY=strategy performance dataclass added
- REASON=performance tuning stage needs a typed metrics structure per strategy.
- CURRENT_DECISION=keep
- NOTE=Stores win/loss and expectancy-related aggregate fields.

- DATE=2026-04-19
- TYPE=code
- PATH=src/models/ranked_signal_selection.py
- SUMMARY=ranked signal selection dataclass added
- REASON=performance-aware ranker now returns selected signal with score metadata.
- CURRENT_DECISION=keep
- NOTE=Used to log rank score and score component evidence.

- DATE=2026-04-19
- TYPE=runtime
- PATH=data/strategy_metrics.json
- SUMMARY=persistent strategy performance metrics snapshot
- REASON=performance tuning stage requires strategy-level cumulative metrics across restarts.
- CURRENT_DECISION=keep
- NOTE=Runtime artifact, not Git-synced.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 PERFORMANCE TUNING LOG.md
- SUMMARY=performance tuning evidence log initialized
- REASON=parameter changes must be recorded with sample-based rationale.
- CURRENT_DECISION=keep
- NOTE=Use for before/after tuning decisions.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 TESTNET PERFORMANCE REPORT.md
- SUMMARY=testnet performance reporting template initialized
- REASON=performance stage requires numeric operating evidence, not qualitative summaries.
- CURRENT_DECISION=keep
- NOTE=Initialized with a single safe runtime observation; still insufficient for tuning decisions.
- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 PERFORMANCE TUNING VALIDATION REPORT.md
- SUMMARY=performance tuning foundation validation report added
- REASON=performance stage implementation needs a formal evidence record before broader tuning and testnet observation.
- CURRENT_DECISION=keep
- NOTE=Captures metrics persistence, ranking fallback, and expectancy-based selection validation.
- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 PERFORMANCE VALIDATION REPORT.md
- SUMMARY=performance validation checklist result documented
- REASON=current testnet evidence was reviewed against the checklist and formally classified as insufficient sample.
- CURRENT_DECISION=keep
- NOTE=Use this report to prevent premature tuning decisions before minimum observation thresholds are met.
- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 TESTNET DATA COLLECTION STATUS REPORT.md
- SUMMARY=testnet data collection stage status report added
- REASON=data collection instruction was executed and current state had to be fixed as in-progress rather than concluded.
- CURRENT_DECISION=keep
- NOTE=Documents that tuning and deployment decisions remain blocked by sample size.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 LIVE READINESS REPORT.md
- SUMMARY=live readiness gate report added
- REASON=live gate was evaluated and formally concluded as not ready under current evidence.
- CURRENT_DECISION=keep
- NOTE=Use this to prevent premature live deployment.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 DATA COLLECTION AND LIVE GATE VALIDATION REPORT.md
- SUMMARY=combined data collection and live gate validation report added
- REASON=the two sequential gate documents were reviewed together and finalized as a single formal decision record.
- CURRENT_DECISION=keep
- NOTE=Use this as the top-level decision summary for the current testnet phase.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 NEXT PHASE PLAN.md
- SUMMARY=next phase data-accumulation and automation plan added
- REASON=after validation hold state, the project needed an explicit execution plan for what to automate while waiting for sufficient data.
- CURRENT_DECISION=keep
- NOTE=Defines Track A/B/C and the milestone sequence up to live gate re-evaluation.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 NEXT PHASE PLANNING REPORT.md
- SUMMARY=next phase planning decision report added
- REASON=the proposed next-phase plan was accepted and needed a formal report mirroring earlier validation-report style.
- CURRENT_DECISION=keep
- NOTE=Use this as the official bridge from validation hold state into automation-prep execution.

- DATE=2026-04-19
- TYPE=code
- PATH=src/analytics/performance_snapshot.py
- SUMMARY=performance snapshot generator added
- REASON=automation phase requires normalized snapshot data before report and gate evaluation.
- CURRENT_DECISION=keep
- NOTE=Builds conservative snapshot values from metrics and portfolio log.

- DATE=2026-04-19
- TYPE=code
- PATH=src/analytics/performance_report.py
- SUMMARY=performance report generator added
- REASON=automation phase requires report regeneration directly from snapshot data.
- CURRENT_DECISION=keep
- NOTE=Used by script and engine hook.

- DATE=2026-04-19
- TYPE=code
- PATH=src/validation/live_gate_evaluator.py
- SUMMARY=live gate evaluator added
- REASON=automation phase requires machine-readable GO/NO-GO output.
- CURRENT_DECISION=keep
- NOTE=Defaults to conservative NOT_READY or FAIL when evidence is insufficient.

- DATE=2026-04-19
- TYPE=code
- PATH=scripts/generate_performance_report.py
- SUMMARY=automation wrapper script added
- REASON=manual or scheduled regeneration path is required for scaling.
- CURRENT_DECISION=keep
- NOTE=Runs snapshot, report, and gate decision generation together.

- DATE=2026-04-19
- TYPE=runtime
- PATH=data/performance_snapshot.json
- SUMMARY=auto-generated performance snapshot
- REASON=automation phase persists normalized analysis data here.
- CURRENT_DECISION=keep
- NOTE=Runtime artifact, not Git-synced.

- DATE=2026-04-19
- TYPE=runtime
- PATH=data/live_gate_decision.json
- SUMMARY=auto-generated live gate decision
- REASON=automation phase persists machine-readable gate output here.
- CURRENT_DECISION=keep
- NOTE=Runtime artifact, not Git-synced.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 AUTO VALIDATION & DECISION SYSTEM WORK INSTRUCTION.md
- SUMMARY=automation phase work instruction added
- REASON=the automatic decision phase needed a formal instruction document in repository.
- CURRENT_DECISION=keep
- NOTE=Defines the snapshot-report-gate pipeline.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 AUTO VALIDATION & DECISION SYSTEM PROGRESS REPORT.md
- SUMMARY=automation phase progress report added
- REASON=implementation progress for the auto decision layer needed a formal report.
- CURRENT_DECISION=keep
- NOTE=Companion report for implementation and validation status.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 SCHEDULED DATA COLLECTION SETUP.md
- SUMMARY=scheduler setup instruction added
- REASON=the project now needs operational scheduling rather than only code-side readiness.
- CURRENT_DECISION=keep
- NOTE=Defines the task scheduler target, arguments, and operating rules.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 SCHEDULED DATA COLLECTION SETUP REPORT.md
- SUMMARY=scheduler setup progress report added
- REASON=scheduler attachment phase required its own formal progress record.
- CURRENT_DECISION=keep
- NOTE=Tracks manual validation, registration, and follow-up checks.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 TASK SCHEDULER REGISTRATION CHECKLIST.md
- SUMMARY=task scheduler registration checklist added
- REASON=scheduler phase needs an execution checklist that can be verified operationally.
- CURRENT_DECISION=keep
- NOTE=Use this before and after task registration.

- DATE=2026-04-19
- TYPE=runtime
- PATH=logs/scheduler_stdout.log
- SUMMARY=scheduler stdout runtime log
- REASON=scheduler phase separates execution telemetry from portfolio log.
- CURRENT_DECISION=keep
- NOTE=Runtime artifact under ignored logs path.

- DATE=2026-04-19
- TYPE=runtime
- PATH=logs/scheduler_stderr.log
- SUMMARY=scheduler stderr runtime log
- REASON=scheduler phase requires separate exception visibility for unattended runs.
- CURRENT_DECISION=keep
- NOTE=Runtime artifact under ignored logs path.

- DATE=2026-04-19
- TYPE=code
- PATH=src/order_cancel.py
- SUMMARY=explicit signed cancel-order helper added
- REASON=exit failsafe patch requires canceling pending target/time-exit orders before protective override.
- CURRENT_DECISION=keep
- NOTE=Used only through shared signing path; added to prevent stuck exit orders from blocking stop protection.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 EXIT FAILSAFE PATCH REPORT.md
- SUMMARY=exit failsafe patch report added
- REASON=runtime issue and protective override patch needed a formal validation record.
- CURRENT_DECISION=keep
- NOTE=Documents the target-limit stuck scenario and the pending-cancel plus protective-exit override fix.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 EXIT FAILSAFE OPERATION CHECKLIST.md
- SUMMARY=short operational checklist for exit failsafe runtime confirmation
- REASON=patched code now needs real runtime evidence, so a minimal pass/fail checklist was required.
- CURRENT_DECISION=keep
- NOTE=Use this when the next pending target exit reverses into stop or trailing-stop territory.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 EXIT FAILSAFE OPERATION REPORT.md
- SUMMARY=operational observation report for exit failsafe follow-up added
- REASON=the patch was synthetically validated, but runtime proof still needs a dedicated report stage.
- CURRENT_DECISION=keep
- NOTE=Tracks the move from patch-applied status to operationally observed proof.

- DATE=2026-04-19
- TYPE=code
- PATH=scripts/monitor_runtime.py
- SUMMARY=phase 1 runtime monitoring script added
- REASON=phase 1 monitoring instruction was accepted and implemented as a conservative monitoring layer.
- CURRENT_DECISION=keep
- NOTE=Produces runtime monitor output from snapshot, gate, portfolio log, and runtime log evidence.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 PHASE 1 MONITORING IMPLEMENTATION REPORT.md
- SUMMARY=phase 1 monitoring implementation and suitability review report added
- REASON=two new CNT v2 documents were reviewed and the accepted monitoring instruction needed a formal implementation report.
- CURRENT_DECISION=keep
- NOTE=Records that the operational analysis report is partially stale while the monitoring instruction was implemented.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 STRATEGIC ANALYSIS PLAN.md
- SUMMARY=strategic analysis and user-referenced PDF plan saved as planning reference
- REASON=the latest broad project analysis needed to be preserved without being mistaken for runtime truth.
- CURRENT_DECISION=keep
- NOTE=Treat this as planning guidance layered on top of repository and runtime facts.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 ENGINE DECOMPOSITION DESIGN.md
- SUMMARY=engine decomposition design added
- REASON=the next requested step after the strategic analysis was a concrete engine split design.
- CURRENT_DECISION=keep
- NOTE=Defines proposed service boundaries and migration order without changing runtime behavior yet.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 ENGINEERING PHASE PLAN.md
- SUMMARY=engineering-phase priority plan added
- REASON=the project moved from structure-definition mode into engineering execution mode and needed an explicit safe-path plan.
- CURRENT_DECISION=keep
- NOTE=Sets tests-first as the approved execution order before deeper refactoring.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 TEST HARNESS IMPLEMENTATION REPORT.md
- SUMMARY=test harness implementation report added
- REASON=the first engineering-phase step needed a formal implementation record.
- CURRENT_DECISION=keep
- NOTE=Documents the minimum regression barrier added before engine decomposition work.

- DATE=2026-04-19
- TYPE=code
- PATH=tests/test_signal_ranker.py
- SUMMARY=signal ranker unit tests added
- REASON=ranker behavior must be fixed before tuning and refactoring proceed.
- CURRENT_DECISION=keep
- NOTE=Locks fallback and expectancy-weighted selection behavior.

- DATE=2026-04-19
- TYPE=code
- PATH=tests/test_live_gate.py
- SUMMARY=live gate evaluator tests added
- REASON=automatic live/no-live decision logic must be regression-protected.
- CURRENT_DECISION=keep
- NOTE=Locks insufficient-sample, fail, and pass branches.

- DATE=2026-04-19
- TYPE=code
- PATH=tests/test_exit_manager.py
- SUMMARY=exit manager tests added
- REASON=exit behavior is a core safety area and must be anchored before more changes.
- CURRENT_DECISION=keep
- NOTE=Locks stop and partial-exit path expectations.

- DATE=2026-04-19
- TYPE=code
- PATH=tests/test_engine_cycle_smoke.py
- SUMMARY=engine cycle smoke tests added
- REASON=engine semantics must be frozen before decomposition begins.
- CURRENT_DECISION=keep
- NOTE=Uses mocked side effects to lock current cycle-state and save orchestration behavior.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 OBSERVABILITY PRIORITY PLAN.md
- SUMMARY=observability-first priority plan added
- REASON=after the test harness landed, the next-step question shifted to choosing the highest-leverage engineering move.
- CURRENT_DECISION=keep
- NOTE=Records observability as the confirmed next implementation step.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 PRIORITY DECISION REPORT.md
- SUMMARY=priority decision report added
- REASON=the project needed a formal record of why observability was chosen ahead of breakout tuning and engine decomposition.
- CURRENT_DECISION=keep
- NOTE=Use this as the decision bridge into the next engineering task.

- DATE=2026-04-19
- TYPE=doc
- PATH=docs/CNT v2 OBSERVABILITY IMPLEMENTATION REPORT.md
- SUMMARY=observability implementation report added
- REASON=the observability-first priority was implemented and needed a formal completion record.
- CURRENT_DECISION=keep
- NOTE=Captures ranking metadata, richer log fields, and validation results for the observability step.
- DATE=2026-04-20
- TYPE=doc
- PATH=docs/CNT v2 OBSERVABILITY VALIDATION GATE.md
- SUMMARY=breakout experiment start gate after observability correction
- REASON=observability implementation was complete, but runtime interpretation needed a formal hold gate before breakout parameter changes.
- CURRENT_DECISION=keep
- NOTE=documents that fresh-cycle runtime evidence is required before breakout relaxation begins.

- DATE=2026-04-20
- TYPE=doc
- PATH=docs/CNT v2 OBSERVABILITY AGGREGATION PATCH REPORT.md
- SUMMARY=records selected-strategy aggregation fix and fresh-cycle validation hold state
- REASON=selection counting and mixed-log parsing needed a formal patch record before moving into breakout experimentation.
- CURRENT_DECISION=keep
- NOTE=captures that code/tests are fixed while runtime proof remains pending due active pending SELL state.

- DATE=2026-04-20
- TYPE=doc
- PATH=docs/CNT v2 FRESH CYCLE OBSERVABILITY VALIDATION PLAN.md
- SUMMARY=formal runtime validation plan for new observability fields before breakout experiment
- REASON=after aggregation/test fixes, a fresh-cycle proof step was required before breakout parameter relaxation.
- CURRENT_DECISION=keep
- NOTE=documents execution order and PASS rule for runtime observability validation.

- DATE=2026-04-20
- TYPE=doc
- PATH=docs/CNT v2 FRESH CYCLE OBSERVABILITY VALIDATION REPORT.md
- SUMMARY=records successful fresh-cycle runtime proof for new observability format
- REASON=the previous gate hold was cleared only after live runtime evidence was captured and reflected in snapshot output.
- CURRENT_DECISION=keep
- NOTE=confirms breakout experiment gate is now open.

- DATE=2026-04-20
- TYPE=doc
- PATH=docs/CNT v2 BREAKOUT V1 RELAXATION EXPERIMENT PLAN.md
- SUMMARY=documents the first controlled breakout_v1 threshold relaxation on testnet
- REASON=after observability validation passed, breakout activation testing required a formal experiment plan and fixed parameter scope.
- CURRENT_DECISION=keep
- NOTE=limits the first experiment to atr_expansion_multiplier and rsi_threshold only.

- DATE=2026-04-20
- TYPE=doc
- PATH=docs/CNT v2 BREAKOUT V1 RELAXATION EXPERIMENT REPORT.md
- SUMMARY=tracks initial breakout relaxation evidence, selected_strategy_counts note, and scheduler log collision note
- REASON=the experiment start required a report that preserves both the initial post-change evidence and the parallel operational issues being tracked.
- CURRENT_DECISION=keep
- NOTE=currently in progress with initial evidence recorded and continued observation required.

- DATE=2026-04-20
- TYPE=doc
- PATH=docs/CNT v2 BREAKOUT V1 RELAXATION CONTINUATION NOTE.md
- SUMMARY=records that the current breakout experiment should continue without further parameter changes yet
- REASON=the latest review confirmed there is no new blocker, but also no evidence yet to justify another threshold change.
- CURRENT_DECISION=keep
- NOTE=keeps the experiment in observation mode and separates ongoing operational issues from blockers.

- DATE=2026-04-20
- TYPE=doc
- PATH=docs/CNT v2 BREAKOUT REVIEW TIMER PLAN.md
- SUMMARY=fixes the next breakout judgment point at +8 hours
- REASON=the user requested a timer-based next review point instead of an open-ended wait.
- CURRENT_DECISION=keep
- NOTE=documents exact review time and required judgment outputs.

- DATE=2026-04-20
- TYPE=doc
- PATH=docs/CNT v2 BREAKOUT REVIEW TIMER REPORT.md
- SUMMARY=records timer application and next review time for breakout experiment
- REASON=the 8-hour timer needed a formal implementation report tied to the current breakout observation phase.
- CURRENT_DECISION=keep
- NOTE=references the one-time scheduled task and repo-local timer script.

- DATE=2026-04-20
- TYPE=code
- PATH=scripts/breakout_review_timer.ps1
- SUMMARY=one-time review marker script for breakout experiment next judgment
- REASON=required to leave a repo-local timestamped signal when the 8-hour review point is reached.
- CURRENT_DECISION=keep
- NOTE=writes a due marker to data and logs without changing runtime strategy state.

- DATE=2026-04-20
- TYPE=doc
- PATH=docs/CNT v2 BREAKOUT TIMER JUDGMENT REPORT.md
- SUMMARY=records the timer-triggered breakout experiment judgment and next recommendation
- REASON=the 8-hour review window needed a final decision document that translates accumulated data into the next action.
- CURRENT_DECISION=keep
- NOTE=concludes that the next move is trend-filter review rather than further ATR/RSI relaxation.

- DATE=2026-04-20
- TYPE=doc
- PATH=docs/CNT v2 BREAKOUT TREND FILTER REVIEW INSTRUCTION.md
- SUMMARY=formal instruction for diagnosing breakout upper filter structure before any further threshold changes
- REASON=the timer judgment concluded that the next action should be trend-filter review, so the review scope needed to be fixed in writing.
- CURRENT_DECISION=keep
- NOTE=explicitly keeps ATR/RSI second relaxation out of scope for this phase.

- DATE=2026-04-20
- TYPE=doc
- PATH=docs/CNT v2 BREAKOUT TREND FILTER REVIEW REPORT.md
- SUMMARY=documents breakout filter chain, log-based blocker analysis, and two bounded design options
- REASON=the project needed a design-review artifact that explains why trend-filter review is next and selects one recommendation.
- CURRENT_DECISION=keep
- NOTE=recommends option A, trend-filter relaxation, as the next controlled change design.

- DATE=2026-04-20
- TYPE=doc
- PATH=docs/CNT v2 BREAKOUT TREND FILTER CHANGE PLAN.md
- SUMMARY=records the actual implementation scope for the recommended trend-filter relaxation
- REASON=after the review selected option A, the implementation scope needed to be fixed before code change.
- CURRENT_DECISION=keep
- NOTE=keeps the change narrowly limited to the upper trend gate.

- DATE=2026-04-20
- TYPE=doc
- PATH=docs/CNT v2 BREAKOUT TREND FILTER CHANGE REPORT.md
- SUMMARY=records the code change, new tests, and initial runtime check for the breakout trend-filter change
- REASON=the actual move from review to implementation needed a separate execution record.
- CURRENT_DECISION=keep
- NOTE=states that runtime effect is not yet fully judged after only one fresh cycle.

- DATE=2026-04-20
- TYPE=doc
- PATH=docs/CNT v2 BREAKOUT COMPLETION ALERT REPORT.md
- SUMMARY=documents the alert rule and implementation for breakout observation completion
- REASON=the user requested a completion alarm so the end of the observation window is not missed.
- CURRENT_DECISION=keep
- NOTE=uses a 30-cycle post-change threshold as the default completion condition.

- DATE=2026-04-20
- TYPE=code
- PATH=scripts/breakout_completion_alert.ps1
- SUMMARY=one-shot repeating checker for breakout post-change completion threshold
- REASON=needed to emit a local alert and marker when the configured observation window completes.
- CURRENT_DECISION=keep
- NOTE=counts breakout post-change cycles from signal.log and sends the alert only once.

---

## Obsidian Links

- [[AGENTS]]