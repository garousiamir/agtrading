# 01 Decisions

Answers to the owner's questions. Items marked **OPEN** must be confirmed before the relevant phase.

## Residence and access
- Owner lives in **Ireland**. Platform must be **international in design** (multiple venues, configurable jurisdiction, no hard-coded country).
- Exchange choice must respect Irish and EU regulation (see `03-exchanges.md`). **OPEN:** owner confirms which exchange accounts they can open.

## Budget
- **Data licence budget: €0.** Use only free and public sources (see `02-data-free.md`).
- Infrastructure budget: owner's own machine first. Cloud hosting optional later.
- Claude API spend: **OPEN**. Set a hard monthly cap (suggested €20) in configuration.

## Capital and loss tolerance
- Pilot capital: **OPEN**. Rule: an amount the owner can lose entirely without changing their life.
- The platform cannot eliminate losses. It bounds them with the limits in `05-validation-and-risk.md`.
- Phase 7 (live) does not start until the owner types the pilot amount to confirm it.

## Operating modes
The platform has three modes. The owner selects one per strategy, changeable at any time.

| Mode | What the platform does | Who places orders |
|---|---|---|
| **MANUAL** | Shows signals, position sizes, stop levels, and reasons. Logs what the owner did. | Owner, on their own exchange account |
| **SEMI** | Prepares each order and waits for owner approval in the UI (with TOTP). | Platform, after approval |
| **AUTO** | Places orders automatically within risk limits. | Platform |

- Default mode for every new strategy: **MANUAL**.
- Switching to SEMI or AUTO requires paper-trading evidence (see `05`) and a confirmation step.
- AUTO requires the live unlock conditions in `05` section 5.

## Claude's role
- Claude **reviews everything**, including live operations: it reads dashboards, logs, reconciliation reports, and risk events, and writes plain-language summaries and alerts.
- Claude **proposes** strategies in the restricted DSL. Proposals are validated like any other input.
- Claude **cannot**: place or cancel orders, change risk limits, approve deployments, read holdout data, or read exchange keys.
- Claude's access is **read-only to operational data** plus write access to its own proposals and notes.
- Implementation: Claude API with a server-side key. This is not a consumer login. Claude Code builds this integration; the owner's Anthropic account provides the key.

## Hosting
- Must run **both locally and on a host**.
- Same Docker Compose files for both. Configuration selects `APP_ENV=local` or `APP_ENV=host`.
- Local: owner's machine. Host: any Linux VPS the owner chooses. Keep the execution service on a separate container with its own network policy in both cases.
- Choice of host provider: **OPEN** (decide in phase 6).

## Exchange for first testnet
See `03-exchanges.md`. Recommendation: use a paper simulator built in-house for phases 2–6, and use an exchange testnet only in phase 7 to test order plumbing.

## Scope
- Assets: BTC and ETH spot only.
- Timeframes: 1h, 4h, 1d.
- No leverage, borrowing, futures, options, market making, or sub-minute trading.
- Fundamental features: free on-chain and market data only (see `02-data-free.md`).
