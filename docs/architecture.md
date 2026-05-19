# AlphaSignal Architecture

```mermaid
flowchart LR
    Providers["Market, macro, news, and social providers"] --> Ingest["services/ingest"]
    Ingest --> RawStore["TimescaleDB raw facts"]
    RawStore --> Features["services/features"]
    Providers --> Sentiment["services/sentiment"]
    Sentiment --> FeatureStore["Feature and sentiment tables"]
    Features --> FeatureStore
    FeatureStore --> ML["services/ml"]
    ML --> Signals["fact_signal"]
    Signals --> Backtest["services/backtest"]
    Backtest --> API["apps/api FastAPI"]
    Signals --> API
    API --> Web["apps/web Next.js dashboard"]
```

## Bias Controls

- Time-series splits only move forward in time.
- Feature tables must use data available at or before each signal timestamp.
- Backtests consume prior close or next open fills depending on strategy configuration.
- The ticker universe will be versioned to discuss survivorship bias explicitly.
