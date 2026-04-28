from pathlib import Path
from src.validation.live_gate_evaluator import evaluate_live_gate, save_live_gate_decision
import json

snapshot_file = Path('data/performance_snapshot.json')
decision_file = Path('data/live_gate_decision.json')

snapshot = json.loads(snapshot_file.read_text(encoding="utf-8"))
decision = evaluate_live_gate(snapshot)
save_live_gate_decision(decision_file, decision)

print("=== LIVE_GATE DECISION SAVED ===")
print(f"Status: {decision['status']}")
print(f"Reason: {decision['reason']}")
print(f"File: {decision_file.absolute()}")
