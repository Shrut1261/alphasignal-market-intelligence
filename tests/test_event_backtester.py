from datetime import UTC, datetime

from alphasignal_backtest.events import Fill, OrderSide
from alphasignal_backtest.portfolio import PortfolioState


def test_portfolio_state_applies_buy_and_sell_fills() -> None:
    portfolio = PortfolioState(cash=10_000)
    portfolio.apply_fill(
        Fill(
            ticker="AAPL",
            side=OrderSide.BUY,
            quantity=10,
            fill_price=100,
            commission=1,
            filled_at=datetime.now(tz=UTC),
        )
    )

    assert portfolio.cash == 8_999
    assert portfolio.equity({"AAPL": 110}) == 10_099

    portfolio.apply_fill(
        Fill(
            ticker="AAPL",
            side=OrderSide.SELL,
            quantity=5,
            fill_price=110,
            commission=1,
            filled_at=datetime.now(tz=UTC),
        )
    )

    assert portfolio.positions["AAPL"].quantity == 5
    assert portfolio.realized_commissions == 2
