import pandas as pd


def simple_returns(close: pd.Series) -> pd.Series:
    """Compute simple percentage returns from a close-price series."""

    return close.pct_change().rename("return")


def relative_strength_index(close: pd.Series, *, window: int = 14) -> pd.Series:
    """Compute Wilder-style RSI from close prices."""

    delta = close.diff()
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)

    average_gain = gains.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    average_loss = losses.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    relative_strength = average_gain / average_loss
    rsi = 100 - (100 / (1 + relative_strength))
    return rsi.rename(f"rsi_{window}")


def macd(
    close: pd.Series,
    *,
    fast_window: int = 12,
    slow_window: int = 26,
    signal_window: int = 9,
) -> pd.DataFrame:
    """Compute MACD line, signal line, and histogram."""

    fast_ema = close.ewm(span=fast_window, adjust=False).mean()
    slow_ema = close.ewm(span=slow_window, adjust=False).mean()
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
    histogram = macd_line - signal_line
    return pd.DataFrame(
        {
            "macd": macd_line,
            "macd_signal": signal_line,
            "macd_histogram": histogram,
        },
        index=close.index,
    )


def bollinger_bands(
    close: pd.Series,
    *,
    window: int = 20,
    standard_deviations: float = 2.0,
) -> pd.DataFrame:
    """Compute Bollinger middle, upper, lower, and percent-b features."""

    middle = close.rolling(window=window, min_periods=window).mean()
    rolling_std = close.rolling(window=window, min_periods=window).std()
    upper = middle + standard_deviations * rolling_std
    lower = middle - standard_deviations * rolling_std
    percent_b = (close - lower) / (upper - lower)
    return pd.DataFrame(
        {
            "bb_middle": middle,
            "bb_upper": upper,
            "bb_lower": lower,
            "bb_percent_b": percent_b,
        },
        index=close.index,
    )


def average_true_range(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    *,
    window: int = 14,
) -> pd.Series:
    """Compute average true range from high, low, and close prices."""

    previous_close = close.shift(1)
    true_range = pd.concat(
        [
            high - low,
            (high - previous_close).abs(),
            (low - previous_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return (
        true_range.ewm(alpha=1 / window, adjust=False, min_periods=window)
        .mean()
        .rename(f"atr_{window}")
    )


def on_balance_volume(close: pd.Series, volume: pd.Series) -> pd.Series:
    """Compute on-balance volume using close-to-close direction."""

    direction = close.diff().apply(lambda value: 1 if value > 0 else -1 if value < 0 else 0)
    return (direction * volume).fillna(0).cumsum().rename("obv")
