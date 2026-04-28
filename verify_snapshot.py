from pathlib import Path
from src.analytics.performance_snapshot import generate_and_save_performance_snapshot
import json

metrics_file = Path('data/strategy_metrics.json')
portfolio_log = Path('logs/portfolio.log')
snapshot_file = Path('data/performance_snapshot.json')
portfolio_state = Path('data/portfolio_state.json')

snapshot = generate_and_save_performance_snapshot(
    metrics_file=metrics_file,
    portfolio_log_file=portfolio_log,
    snapshot_file=snapshot_file,
    portfolio_state_file=portfolio_state
)

print('=== PERFORMANCE SNAPSHOT (BREAKOUT_V1 EXCLUDED) ===')
print(f'Expectancy: {snapshot["expectancy"]:.6f}')
print(f'Net PnL: {snapshot["net_pnl"]:.8f}')
print(f'Profit Factor: {snapshot["profit_factor"]:.4f}')
print(f'Win Rate: {snapshot["win_rate"]:.4f}')
print(f'Closed Trades: {snapshot["closed_trades"]}')
print(f'Wins: {snapshot["wins"]} / Losses: {snapshot["losses"]}')
print()
print('=== STRATEGY BREAKDOWN ===')
for strat, data in snapshot['strategy_breakdown'].items():
    print(f'{strat}:')
    print(f'  Trades: {data["trades_closed"]}')
    print(f'  Win Rate: {data["win_rate"]:.4f}')
    print(f'  Expectancy: {data["expectancy"]:.6f}')
    print(f'  PF: {data["profit_factor"]:.4f}')
