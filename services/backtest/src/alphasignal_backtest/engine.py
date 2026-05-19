from pydantic import BaseModel, Field

from alphasignal_backtest.metrics import PerformanceMetrics, calculate_performance_metrics


class BacktestResult(BaseModel):
    """Result object returned by the backtesting engine."""

    strategy_name: str
    initial_cash: float = Field(gt=0)
    final_equity: float = Field(gt=0)
    equity_curve: list[float] = Field(min_length=1)
    strategy_returns: list[float] = Field(min_length=1)
    metrics: PerformanceMetrics


def run_vector_backtest(
    *,
    strategy_name: str,
    asset_returns: list[float],
    target_weights: list[float],
    initial_cash: float = 100_000.0,
    transaction_cost_bps: float = 1.0,
) -> BacktestResult:
    """Run a daily close-to-close backtest from returns and target weights.

    This is intentionally simple but production-shaped: weights are lagged one period
    to avoid look-ahead bias, and turnover-based transaction costs are applied.
    """

    if len(asset_returns) != len(target_weights):
        msg = "asset_returns and target_weights must have the same length"
        raise ValueError(msg)
    if not asset_returns:
        msg = "asset_returns must not be empty"
        raise ValueError(msg)

    cost_rate = transaction_cost_bps / 10_000
    previous_weight = 0.0
    equity = initial_cash
    equity_curve: list[float] = []
    strategy_returns: list[float] = []

    for daily_return, target_weight in zip(asset_returns, target_weights, strict=True):
        turnover = abs(target_weight - previous_weight)
        net_return = previous_weight * daily_return - turnover * cost_rate
        equity *= 1 + net_return
        equity_curve.append(equity)
        strategy_returns.append(net_return)
        previous_weight = target_weight

    return BacktestResult(
        strategy_name=strategy_name,
        initial_cash=initial_cash,
        final_equity=equity_curve[-1],
        equity_curve=equity_curve,
        strategy_returns=strategy_returns,
        metrics=calculate_performance_metrics(strategy_returns),
    )
