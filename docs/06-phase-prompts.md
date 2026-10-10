# 06 Phase Prompts for Claude Code

Paste one prompt at a time. Review the result and the exit test before moving on.

## Phase 0: Skeleton

> Read `CLAUDE.md` and everything in `docs/`. Do not write application code yet.
> 1. Create the repository skeleton from `docs/04-architecture.md`, with empty packages.
> 2. Create `docs/assumptions.md` listing every OPEN item from `docs/01-decisions.md` as unresolved.
> 3. Create a `Makefile` with `test`, `lint`, and `migrate` targets that run without error on an empty project.
> 4. Add a test that fails if a file in the repo contains a pattern resembling an API key or secret.
> 5. Stop and report: the file tree, the test output, and any questions. Do not start Phase 1.

## Phase 1: Free data foundation

> Confirm phase 0 passed. Now implement phase 1 from `docs/04-architecture.md` using only free sources in `docs/02-data-free.md`.
> - Ingest BTC and ETH from at least one free archive source and one API source.
> - Store raw files unchanged with URL, retrieval time, and SHA-256.
> - Normalise to UTC `Decimal` prices and `timezone`-aware timestamps.
> - Quarantine suspect rows; never delete them.
> - Publish an immutable manifest atomically.
> - Produce a coverage report: first and last timestamps, gaps, outages, and fundamental-feature coverage per period.
> Exit test: re-running ingestion on identical inputs gives identical manifest hashes. Show me the coverage report and stop.

## Phase 2: Simulator and accounting

> Implement phase 2. Event-driven simulator with Decimal ledger and the cost model in `docs/05-validation-and-risk.md` section 4.
> - Implement the candle execution rules exactly as written.
> - Add cash, buy-and-hold BTC and ETH, and 200-day trend baselines.
> - Write 20 hand-calculated fixtures in `tests/fixtures/` with expected fees, fills, cash, and positions, and test that the engine matches them.
> Exit test: all 20 fixtures pass. Stop and report.

## Phase 3: Strategy language and search

> Implement phase 3. Restricted YAML DSL with a JSON Schema, validator, and compiler.
> - Reject future-index access, centred windows, unknown operators, and excessive complexity.
> - Implement the runtime interface so strategy code receives only an as-of view.
> - Implement template search with Optuna (PostgreSQL storage) inside nested chronological splits.
> - Enforce trial and compute budgets; record every trial, including rejected ones.
> Exit test: an adversarial strategy that reads future data is rejected; budgets hold after forced retries. Stop and report.

## Phase 4: Fundamental features

> Implement phase 4. Add free on-chain and market-structure features with `available_at` and revision tracking.
> Exit test: changing future on-chain data leaves all earlier features unchanged. Stop and report.

## Phase 5: Evaluation and reports

> Implement phase 5. Walk-forward evaluation, holdout guard with access audit and consumed-holdout flag, block bootstrap, Deflated Sharpe, cost stress, and the report template in `docs/05-validation-and-risk.md` section 5.
> Exit test: discovery identities cannot read holdout files; reports list all trials and show "insufficient evidence" where appropriate. Stop and report.

## Phase 6: Dashboard, auth, and Claude review

> Implement phase 6.
> - FastAPI endpoints for research and signals.
> - React dashboard with the screens needed for MANUAL mode: signal, size, stop, reason, and a log of what the owner actually did.
> - Argon2id login and mandatory TOTP.
> - Claude review module: read-only summaries of development results and operational data. No order, risk, holdout, or key access. Enforce a monthly token cap.
> Exit test: Playwright tests pass; Claude summaries cite only the data they were given. Stop and report.

## Phase 7: Paper trading, SEMI mode, and risk

> Implement phase 7.
> - Paper execution using the phase 2 simulator, with restart reconciliation.
> - SEMI mode: order preview, owner approval with password and TOTP, then submission.
> - Independent risk service with the limits in `docs/05-validation-and-risk.md` section 6.
> - Three emergency controls.
> - One exchange testnet adapter from `docs/03-exchanges.md` (confirm which one with me first).
> Exit test: failure injection passes; restart reconciles; emergency controls work. Stop and report.

## Phase 8: Prospective paper run

> No coding. Run approved strategies on paper for 60–90 days. Produce a weekly report comparing paper results with backtests. At the end, produce the promotion verdict using the policy in section 5. If nothing qualifies, say so.

## Phase 9: Live unlock (only if phase 8 passes)

> Check all eight conditions in `docs/05-validation-and-risk.md` section 9. Show each as true or false with evidence. Do not enable live trading unless every condition is true and the owner has typed the pilot amount and approved the exact package hash.
