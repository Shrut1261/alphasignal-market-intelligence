# AlphaSignal Roadmap

This roadmap is intentionally honest: the repository will only mark a phase complete when runnable code, tests, and documentation exist.

| Phase | Status | Evidence |
| --- | --- | --- |
| Phase 0 - Foundation | Complete | Monorepo, FastAPI, TimescaleDB/Redis Compose, CI, typed shared package, quality gate |
| Phase 1 - Data Layer | MVP Complete | Yahoo and FRED async adapters, SQL schema, repository write layer, daily ingestion orchestration |
| Phase 2 - Features and Sentiment | MVP Complete | Technical indicators, FinBERT-ready facade, lexical fallback with tests |
| Phase 3 - ML Models | MVP Complete | Leakage-safe labels, directional metrics, deterministic baseline model, portfolio optimizer |
| Phase 4 - Backtesting | MVP Complete | Weight-lagged vector backtest, event objects, portfolio state, transaction costs |
| Phase 5 - API | MVP Complete | Health, market overview, signals, sentiment, portfolio, and backtest endpoints |
| Phase 6 - Frontend | MVP Complete | Next.js dashboard with KPIs, equity curve, sentiment chart, and platform cards |
| Phase 7 - Deploy and Polish | In progress | Deployment configs and demo assets after API/frontend stabilize |

## Near-Term Build Order

1. Expand database migrations and provider loaders.
2. Add Prefect ingestion flows and local seed scripts.
3. Build portfolio/backtest trade ledger with alpha and beta vs SPY.
4. Add LightGBM training baseline with time-series CV.
5. Replace lexical sentiment baseline with FinBERT batch scoring.
6. Scaffold the Next.js dashboard with real API contract fixtures.
