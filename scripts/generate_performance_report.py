from __future__ import annotations

from pathlib import Path
import sys
import json


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import PERFORMANCE_SNAPSHOT_FILE
from config import AUXILIARY_RECOVERY_STATUS_FILE
from src.analytics.auxiliary_recovery_status import (
    build_auxiliary_recovery_status,
    save_auxiliary_recovery_status,
)
from src.analytics.performance_report import generate_performance_report
from src.analytics.performance_snapshot import generate_and_save_performance_snapshot
from src.analytics.strategy_metrics import load_strategy_metrics
from src.state.state_manager import load_portfolio_state
from src.validation.live_gate_evaluator import evaluate_live_gate, save_live_gate_decision


def main() -> None:
    project_root = PROJECT_ROOT
    snapshot = generate_and_save_performance_snapshot(
        metrics_file=project_root / "data/strategy_metrics.json",
        portfolio_log_file=project_root / "logs/portfolio.log",
        snapshot_file=project_root / PERFORMANCE_SNAPSHOT_FILE,
    )
    generate_performance_report(
        project_root / "docs/CNT v2 TESTNET PERFORMANCE REPORT.md",
        snapshot,
    )
    live_gate_decision = evaluate_live_gate(snapshot)
    save_live_gate_decision(
        project_root / "data/live_gate_decision.json",
        live_gate_decision,
    )
    state_file = project_root / "data/state.json"
    state = {}
    if state_file.exists():
        state = json.loads(state_file.read_text(encoding="utf-8"))
    save_auxiliary_recovery_status(
        project_root / AUXILIARY_RECOVERY_STATUS_FILE,
        build_auxiliary_recovery_status(
            snapshot=snapshot,
            strategy_metrics=load_strategy_metrics(project_root / "data/strategy_metrics.json"),
            state=state,
            portfolio_state=load_portfolio_state(project_root / "data/portfolio_state.json"),
            live_gate_decision=live_gate_decision,
        ),
    )


if __name__ == "__main__":
    main()
