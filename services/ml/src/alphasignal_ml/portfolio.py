from pydantic import BaseModel, Field


class PortfolioWeight(BaseModel):
    ticker: str = Field(min_length=1, max_length=20)
    weight: float = Field(ge=0, le=1)


class PortfolioOptimizationResult(BaseModel):
    method: str
    weights: list[PortfolioWeight] = Field(min_length=1)
    expected_portfolio_return: float
    expected_portfolio_volatility: float = Field(ge=0)


def inverse_volatility_weights(
    tickers: list[str],
    expected_returns: list[float],
    volatilities: list[float],
) -> PortfolioOptimizationResult:
    """Create a simple long-only inverse-volatility portfolio."""

    if not (len(tickers) == len(expected_returns) == len(volatilities)):
        msg = "tickers, expected_returns, and volatilities must have the same length"
        raise ValueError(msg)
    if not tickers:
        msg = "tickers must not be empty"
        raise ValueError(msg)
    if any(volatility <= 0 for volatility in volatilities):
        msg = "volatilities must be positive"
        raise ValueError(msg)

    inverse_vols = [1 / volatility for volatility in volatilities]
    total_inverse_vol = sum(inverse_vols)
    raw_weights = [inverse_vol / total_inverse_vol for inverse_vol in inverse_vols]
    normalized_tickers = [ticker.strip().upper() for ticker in tickers]
    portfolio_return = sum(
        weight * expected_return
        for weight, expected_return in zip(raw_weights, expected_returns, strict=True)
    )
    portfolio_volatility = sum(
        weight * volatility for weight, volatility in zip(raw_weights, volatilities, strict=True)
    )

    return PortfolioOptimizationResult(
        method="inverse_volatility",
        weights=[
            PortfolioWeight(ticker=ticker, weight=weight)
            for ticker, weight in zip(normalized_tickers, raw_weights, strict=True)
        ],
        expected_portfolio_return=portfolio_return,
        expected_portfolio_volatility=portfolio_volatility,
    )
