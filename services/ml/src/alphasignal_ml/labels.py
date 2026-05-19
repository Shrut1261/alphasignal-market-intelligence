import pandas as pd


def directional_label(close: pd.Series, *, horizon_days: int, threshold: float = 0.0) -> pd.Series:
    """Create leakage-safe forward directional labels from close prices."""

    forward_return = close.shift(-horizon_days) / close - 1.0
    labels = pd.Series("flat", index=close.index, name=f"direction_{horizon_days}d")
    labels[forward_return > threshold] = "up"
    labels[forward_return < -threshold] = "down"
    return labels
