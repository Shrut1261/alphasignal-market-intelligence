CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS dim_ticker (
    ticker TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    asset_class TEXT NOT NULL,
    sector TEXT,
    exchange TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS fact_ohlcv (
    ticker TEXT NOT NULL REFERENCES dim_ticker(ticker),
    ts TIMESTAMPTZ NOT NULL,
    open NUMERIC(18, 6) NOT NULL,
    high NUMERIC(18, 6) NOT NULL,
    low NUMERIC(18, 6) NOT NULL,
    close NUMERIC(18, 6) NOT NULL,
    adjusted_close NUMERIC(18, 6),
    volume BIGINT NOT NULL,
    source TEXT NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (ticker, ts, source)
);

SELECT create_hypertable('fact_ohlcv', 'ts', if_not_exists => TRUE);

CREATE TABLE IF NOT EXISTS fact_sentiment (
    ticker TEXT NOT NULL REFERENCES dim_ticker(ticker),
    published_at TIMESTAMPTZ NOT NULL,
    source TEXT NOT NULL,
    headline TEXT NOT NULL,
    url TEXT,
    sentiment_label TEXT NOT NULL,
    sentiment_score DOUBLE PRECISION NOT NULL,
    model_name TEXT NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (ticker, published_at, source, headline)
);

SELECT create_hypertable('fact_sentiment', 'published_at', if_not_exists => TRUE);

CREATE TABLE IF NOT EXISTS fact_macro_observation (
    series_id TEXT NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    source TEXT NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (series_id, observed_at, source)
);

SELECT create_hypertable('fact_macro_observation', 'observed_at', if_not_exists => TRUE);

CREATE TABLE IF NOT EXISTS fact_signal (
    ticker TEXT NOT NULL REFERENCES dim_ticker(ticker),
    as_of_date DATE NOT NULL,
    horizon_days INTEGER NOT NULL,
    signal TEXT NOT NULL,
    confidence DOUBLE PRECISION NOT NULL,
    model_name TEXT NOT NULL,
    features JSONB NOT NULL DEFAULT '{}'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (ticker, as_of_date, horizon_days, model_name)
);
