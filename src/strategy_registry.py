from __future__ import annotations

# breakout_v1 deactivated for data purity and validation accuracy
# from src.strategies.breakout_v1 import BreakoutV1Strategy
from src.strategies.breakout_v2 import BreakoutV2Strategy
from src.strategies.breakout_v3 import BreakoutV3Strategy
from src.strategies.mean_reversion_v1 import MeanReversionV1Strategy


STRATEGY_REGISTRY = {
    # "breakout_v1": BreakoutV1Strategy,  # DEACTIVATED - noise source affecting data purity
    "breakout_v2": BreakoutV2Strategy,
    "breakout_v3": BreakoutV3Strategy,
    "mean_reversion_v1": MeanReversionV1Strategy,
}
