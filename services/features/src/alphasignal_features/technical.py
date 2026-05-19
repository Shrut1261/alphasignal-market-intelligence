import pandas as pd


def simple_returns(close: pd.Series) -> pd.Series:
    """Compute simple percentage returns from a close-price series."""

    return close.pct_change().rename("return")
