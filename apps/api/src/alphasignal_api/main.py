from alphasignal_shared import get_settings
from alphasignal_shared.logging import configure_logging
from fastapi import FastAPI

from alphasignal_api.routes import backtests, health, portfolio, sentiment, signals

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(
    title="AlphaSignal API",
    version="0.1.0",
    description="Typed API for algorithmic trading signals, sentiment, and backtests.",
)

app.include_router(health.router, tags=["health"])
app.include_router(signals.router, prefix="/signals", tags=["signals"])
app.include_router(backtests.router, prefix="/backtests", tags=["backtests"])
app.include_router(sentiment.router, prefix="/sentiment", tags=["sentiment"])
app.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
