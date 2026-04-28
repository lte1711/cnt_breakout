from pathlib import Path
from src.validation.live_gate_evaluator import evaluate_live_gate
import json

snapshot_file = Path('data/performance_snapshot.json')
decision_file = Path('data/live_gate_decision.json')

snapshot = json.loads(snapshot_file.read_text(encoding="utf-8"))
decision = evaluate_live_gate(snapshot)

print("=== LIVE_GATE DECISION ===")
print(f"Status: {decision['status']}")
print(f"Reason: {decision['reason']}")
print()
print("=== METRICS ===")
for key, value in decision['metrics'].items():
    if isinstance(value, dict):
        print(f"{key}:")
        for k, v in value.items():
            print(f"  {k}: {v}")
    else:
        print(f"{key}: {value}")

if decision['status'] == 'LIVE_READY':
    print("\n[SUCCESS] GATE PASSED - SYSTEM READY FOR DEPLOYMENT")
else:
    print(f"\n[INFO] Gate Status: {decision['status']}")
