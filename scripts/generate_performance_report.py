from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import PERFORMANCE_SNAPSHOT_FILE
from src.analytics.performance_report import generate_performance_report
from src.analytics.performance_snapshot import generate_and_save_performance_snapshot
from src.validation.live_gate_evaluator import evaluate_live_gate, save_live_gate_decision


def main() -> None:
    project_root = PROJECT_ROOT
    snapshot = generate_and_save_performance_snapshot(
        metrics_file=project_root / "data/strategy_metrics.json",
        portfolio_log_file=project_root / "logs/portfolio.log",
        snapshot_file=project_root / PERFORMANCE_SNAPSHOT_FILE,
    )
    generate_performance_report(
        project_root / "docs/CNT v2 TESTNET PERFORMANCE REPORT.txt",
        snapshot,
    )
    save_live_gate_decision(
        project_root / "data/live_gate_decision.json",
        evaluate_live_gate(snapshot),
    )


if __name__ == "__main__":
    main()
