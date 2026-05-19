from pydantic import BaseModel, Field

from alphasignal_backtest.events import Fill


class Position(BaseModel):
    ticker: str
    quantity: int = 0
    average_cost: float = 0.0


class PortfolioState(BaseModel):
    cash: float
    positions: dict[str, Position] = Field(default_factory=dict)
    realized_commissions: float = 0.0

    def apply_fill(self, fill: Fill) -> None:
        position = self.positions.get(fill.ticker, Position(ticker=fill.ticker))
        signed_quantity = fill.signed_quantity
        trade_value = fill.quantity * fill.fill_price

        if signed_quantity > 0:
            new_quantity = position.quantity + signed_quantity
            total_cost = position.average_cost * position.quantity + trade_value
            position.average_cost = total_cost / new_quantity
            position.quantity = new_quantity
            self.cash -= trade_value + fill.commission
        else:
            position.quantity += signed_quantity
            self.cash += trade_value - fill.commission

        self.realized_commissions += fill.commission
        self.positions[fill.ticker] = position

    def equity(self, marks: dict[str, float]) -> float:
        marked_value = sum(
            position.quantity * marks.get(ticker, position.average_cost)
            for ticker, position in self.positions.items()
        )
        return self.cash + marked_value
