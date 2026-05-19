# Interview Talking Points

## Why FinBERT?

FinBERT is trained for financial language, so it handles market-specific phrasing better than generic sentiment models. AlphaSignal will use it for headline-level classification and aggregate scores by ticker-day before joining to returns.

## Avoiding Look-Ahead Bias

Signals are generated from features available at the decision timestamp. Forward returns are used only as labels during training, and backtests apply fills after the signal time rather than at the same close used to compute the signal.

## Scaling to 10k Tickers

The platform separates ingestion, feature computation, ML scoring, and API reads. TimescaleDB hypertables support time-series writes, Prefect orchestrates chunked jobs, and the API reads precomputed signal tables rather than recalculating indicators per request.
