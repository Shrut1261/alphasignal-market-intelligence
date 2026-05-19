import pytest
from alphasignal_backtest.metrics import calculate_performance_metrics


def test_calculate_performance_metrics_returns_core_kpis() -> None:
    metrics = calculate_performance_metrics([0.01, -0.005, 0.002, 0.004])

    assert metrics.cumulative_return > 0
    assert metrics.annualized_volatility >= 0
    assert metrics.max_drawdown <= 0


def test_calculate_performance_metrics_rejects_empty_returns() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        calculate_performance_metrics([])
