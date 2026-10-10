# 04 Architecture and Build Phases

## Components

```
crypto-platform/
  apps/
    api/            FastAPI: REST + server-sent events
    web/            React + TypeScript dashboard
    worker-research/  Celery worker: ingestion, features, backtests, search
    worker-eval/      Holdout evaluation; separate identity; no exchange access
    execution/        Paper/live order manager and risk service; only process with exchange keys
  packages/
    core/           Decimal math, time utilities, domain types
    ingest/         Source adapters (free sources only)
    catalog/        Coverage, quality, immutable dataset manifests
    features/       Point-in-time features
    strategy/       Restricted DSL: parser, validator, compiler, runtime
    sim/            Vectorised screen + event-driven simulator
    validation/     Walk-forward splits, purging, embargo, holdout guard
    stats/          Metrics, block bootstrap, Deflated Sharpe
    risk/           Pre-trade limits (isolated module)
    oms/            Order state machine, reconciliation
    llm/            Claude client, prompt templates, budget guard
    signals/        Signal generation for MANUAL and SEMI modes
  infra/            Docker Compose (local and host profiles)
  tests/
```

## Stack (keep it boring)

| Layer | Choice |
|---|---|
| Backend | Python 3.12, FastAPI, Pydantic v2 |
| Data | Polars, DuckDB, PyArrow, Parquet files on local disk (or any S3-compatible storage later) |
| Metadata | PostgreSQL 16 |
| Queue | Redis or PostgreSQL-backed queue (simpler than RabbitMQ for one user) |
| ML | scikit-learn; LightGBM later |
| Search | Optuna with PostgreSQL storage |
| Frontend | React, TypeScript, Vite |
| Secrets | `age`-encrypted file; master key in OS keychain (local) or host secret store (host) |
| Auth | Argon2id passwords, TOTP mandatory |
| Tests | pytest, Hypothesis, Playwright |
| Deployment | Docker Compose with `local` and `host` profiles |

Use a simpler queue than the original spec: one user does not need RabbitMQ.

## Modes (per strategy)

- **MANUAL:** signal + sizing + stop + reason shown; owner executes on their own account; owner marks each action done (or the platform imports it via read-only sync later).
- **SEMI:** platform prepares orders; owner approves with password + TOTP; platform submits.
- **AUTO:** platform submits within risk limits; blocked until unlock conditions pass.

Every mode runs the same strategy code. Only the last step differs.

## Build phases

Each phase has an exit test. Do not start the next phase until it passes.

| Phase | Build | Exit test |
|---|---|---|
| 0 | Repo skeleton, `CLAUDE.md`, `docs/assumptions.md`, protocol | Repo runs `make test` (empty suite passes) |
| 1 | Free data ingestion, catalog, manifests, quality report | Coverage report for BTC and ETH; re-run gives identical manifest hashes |
| 2 | Event simulator, Decimal ledger, costs, baselines, 20 hand-checked fixtures | All fixtures match; baselines reproduce expected results |
| 3 | DSL, validator, compiler, template search with Optuna, trial counter | Future-peeking strategy is rejected; budget limits hold after forced retries |
| 4 | Fundamental features with `available_at` | Changing future on-chain data leaves past features unchanged |
| 5 | Walk-forward evaluation, holdout guard, statistics, reports | Discovery identity cannot read holdout; reports show all trials |
| 6 | Dashboard, auth, TOTP, manual-signal view, Claude review integration | Playwright end-to-end tests pass; Claude summaries cite real data only |
| 7 | Paper trading with restart reconciliation; SEMI mode; risk service; emergency controls; exchange testnet adapter | Failure injection passes; restart reconciles; emergency stop works |
| 8 | Prospective paper run (60–90 days, real time) | Section 5 of `05` evaluated honestly; report says whether anything qualifies |
| 9 | Live unlock (only if phase 8 passes and owner confirms pilot amount) | All eight unlock conditions shown as true |

## Local and host hosting

- `APP_ENV=local`: runs on the owner's machine; secrets from OS keychain; web UI on localhost only.
- `APP_ENV=host`: runs on a Linux VPS; TLS via reverse proxy; secrets from host store; firewall allows only HTTPS and SSH from the owner's IP; execution container isolated.
- Same images, same migrations, same tests in both.
- Backup: nightly encrypted PostgreSQL dump and Parquet folder copy, with a monthly restore test.
