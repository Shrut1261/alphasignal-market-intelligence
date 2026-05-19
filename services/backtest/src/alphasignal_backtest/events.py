from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class OrderSide(StrEnum):
    BUY = "buy"
    SELL = "sell"


class OrderType(StrEnum):
    MARKET = "market"


class Order(BaseModel):
    ticker: str = Field(min_length=1, max_length=20)
    side: OrderSide
    quantity: int = Field(gt=0)
    order_type: OrderType = OrderType.MARKET
    created_at: datetime


class Fill(BaseModel):
    ticker: str = Field(min_length=1, max_length=20)
    side: OrderSide
    quantity: int = Field(gt=0)
    fill_price: float = Field(gt=0)
    commission: float = Field(ge=0)
    filled_at: datetime

    @property
    def signed_quantity(self) -> int:
        return self.quantity if self.side == OrderSide.BUY else -self.quantity
