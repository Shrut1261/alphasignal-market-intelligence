# AlphaSignal

AlphaSignal is a production-shaped algorithmic trading intelligence platform for market data ingestion, feature engineering, sentiment scoring, ML signal generation, backtesting, and dashboard delivery.

## Current Status

AlphaSignal is under active development. The public repository currently contains a tested backend foundation plus early vertical slices for ingestion, feature engineering, sentiment scoring, ML metrics, backtesting, and API endpoints. See [docs/roadmap.md](docs/roadmap.md) for the phase-by-phase status.

## Phase 0 Decisions

| Decision | Options | Recommendation |
| --- | --- | --- |
| Frontend | Streamlit for speed, Next.js for portfolio polish, both with Streamlit internal prototype | Next.js + TypeScript for public demo credibility |
| Orchestration | Cron, Airflow, Prefect | Prefect because it is lighter than Airflow and still production-readable |
| Database | SQLite, Postgres, TimescaleDB | TimescaleDB locally via Docker with Postgres compatibility |
| API | Flask, FastAPI, Django Ninja | FastAPI for typed schemas, async endpoints, and OpenAPI docs |
| ML path | scikit baseline, LightGBM, LSTM/TFT | Start with leakage-safe LightGBM, add deep forecasting after backtesting is stable |

## Repository Layout

```text
apps/api                 FastAPI service
apps/web                 Next.js dashboard placeholder
services/ingest          Market/news/macro ingestion flows
services/features        Technical and statistical features
services/sentiment       FinBERT/news sentiment pipeline
services/ml              Model training and signal generation
services/backtest        Event-driven backtesting engine
packages/shared          Shared settings, schemas, and logging
infra/sql                Database bootstrap SQL
docs                     Architecture and interview notes
tests                    Cross-package tests
```

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
docker compose up -d
pytest
uvicorn alphasignal_api.main:app --reload --app-dir apps/api/src
```

Open `http://localhost:8000/docs` for the API documentation.

## API Surface

- `GET /health`
- `GET /signals/{ticker}`
- `POST /backtests`
- `POST /sentiment/{ticker}`
- `POST /portfolio/optimize`

## Test Plan

- Unit tests validate shared settings, Pydantic schemas, API health, ingestion provider parsing, technical indicators, sentiment scoring, ML metrics, and backtest behavior.
- CI runs `ruff`, `black --check`, `mypy`, and `pytest`.
- Later phases add loader integration tests with mocked providers and database contract tests.

## Phase 0 Resume Bullet

Built the production foundation for AlphaSignal, a quantitative trading intelligence platform, using FastAPI, TimescaleDB, Redis, typed Pydantic schemas, pytest, ruff, black, mypy, and CI-ready monorepo architecture.

## LinkedIn Snippet

Started building AlphaSignal, a real-time algorithmic trading intelligence platform combining market data, sentiment, ML signals, and backtesting. Phase 0 is complete: typed Python monorepo, FastAPI service, TimescaleDB/Redis infrastructure, shared schemas, quality tooling, and test coverage.

## Phase 1-2 Resume Bullet

Implemented tested AlphaSignal ingestion and feature-engineering slices, including async Yahoo/FRED provider adapters, TimescaleDB-ready persistence contracts, RSI/MACD/Bollinger/ATR/OBV indicators, sentiment baseline scoring, and API-accessible backtest metrics.
