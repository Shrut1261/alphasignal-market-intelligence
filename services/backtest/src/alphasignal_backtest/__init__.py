"""Backtesting engine package."""

from alphasignal_backtest.engine import BacktestResult, run_vector_backtest
from alphasignal_backtest.events import Fill, Order, OrderSide, OrderType
from alphasignal_backtest.metrics import PerformanceMetrics, calculate_performance_metrics
from alphasignal_backtest.portfolio import PortfolioState, Position

__all__ = [
    "BacktestResult",
    "Fill",
    "Order",
    "OrderSide",
    "OrderType",
    "PerformanceMetrics",
    "PortfolioState",
    "Position",
    "calculate_performance_metrics",
    "run_vector_backtest",
]
