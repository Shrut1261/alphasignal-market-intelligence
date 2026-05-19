# AlphaSignal Roadmap

This roadmap is intentionally honest: the repository will only mark a phase complete when runnable code, tests, and documentation exist.

| Phase | Status | Evidence |
| --- | --- | --- |
| Phase 0 - Foundation | Complete | Monorepo, FastAPI, TimescaleDB/Redis Compose, CI, typed shared package, quality gate |
| Phase 1 - Data Layer | In progress | Yahoo and FRED async adapters, SQL schema, repository write layer, mocked provider tests |
| Phase 2 - Features and Sentiment | In progress | Technical indicators and lexical sentiment baseline with tests |
| Phase 3 - ML Models | In progress | Leakage-safe labels and classification metrics baseline |
| Phase 4 - Backtesting | In progress | Weight-lagged vector backtest, transaction costs, metrics, strategy adapter |
| Phase 5 - API | In progress | Health, signals, and backtest endpoints |
| Phase 6 - Frontend | Planned | Next.js dashboard scaffold next |
| Phase 7 - Deploy and Polish | Planned | Deployment configs and demo assets after API/frontend stabilize |

## Near-Term Build Order

1. Expand database migrations and provider loaders.
2. Add Prefect ingestion flows and local seed scripts.
3. Build portfolio/backtest trade ledger with alpha and beta vs SPY.
4. Add LightGBM training baseline with time-series CV.
5. Replace lexical sentiment baseline with FinBERT batch scoring.
6. Scaffold the Next.js dashboard with real API contract fixtures.
