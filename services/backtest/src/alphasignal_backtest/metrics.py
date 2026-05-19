import math

from pydantic import BaseModel, Field


class PerformanceMetrics(BaseModel):
    cumulative_return: float
    annualized_return: float
    annualized_volatility: float = Field(ge=0)
    sharpe_ratio: float
    max_drawdown: float


def calculate_performance_metrics(
    daily_returns: list[float],
    *,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> PerformanceMetrics:
    """Calculate core strategy metrics from daily simple returns."""

    if not daily_returns:
        msg = "daily_returns must not be empty"
        raise ValueError(msg)

    equity_curve: list[float] = []
    equity = 1.0
    for daily_return in daily_returns:
        equity *= 1.0 + daily_return
        equity_curve.append(equity)

    cumulative_return = equity_curve[-1] - 1.0
    annualized_return = equity_curve[-1] ** (periods_per_year / len(daily_returns)) - 1.0

    mean_return = sum(daily_returns) / len(daily_returns)
    variance = (
        sum((daily_return - mean_return) ** 2 for daily_return in daily_returns)
        / (len(daily_returns) - 1)
        if len(daily_returns) > 1
        else 0.0
    )
    daily_volatility = math.sqrt(variance)
    annualized_volatility = daily_volatility * math.sqrt(periods_per_year)

    excess_daily_return = mean_return - (risk_free_rate / periods_per_year)
    sharpe_ratio = (
        excess_daily_return / daily_volatility * math.sqrt(periods_per_year)
        if daily_volatility > 0
        else 0.0
    )

    running_max = equity_curve[0]
    max_drawdown = 0.0
    for equity_value in equity_curve:
        running_max = max(running_max, equity_value)
        max_drawdown = min(max_drawdown, equity_value / running_max - 1.0)

    return PerformanceMetrics(
        cumulative_return=cumulative_return,
        annualized_return=annualized_return,
        annualized_volatility=annualized_volatility,
        sharpe_ratio=sharpe_ratio,
        max_drawdown=max_drawdown,
    )
