# Assumptions and open questions

Every OPEN item from `docs/01-decisions.md`, the owner's answers, and
assumptions made while building.

## Owner answers (2026-10-10)

| # | Item | Owner's answer | Status / consequence |
|---|---|---|---|
| 1 | Exchange accounts the owner can open | "All" | **Recorded, with a legal caveat.** The MiCA transitional period ended on 1 July 2026, so a provider serving Irish residents must be MiCA-authorised. Before any live use, the chosen venue must appear in the ESMA CASP register. Being able to open an account is not the same as the provider being authorised. Reported as authorised by the Central Bank of Ireland: Kraken (to verify). Reported as having lost EU access: Binance (unverified, third-party source). |
| 2 | Claude API monthly cap | Can buy the Max plan (€100) | **Conflict, needs an answer.** The Claude Max plan is a consumer subscription for claude.ai and Claude Code. It does not provide an API key for the platform's server-side Claude review module (`01-decisions.md`, Claude's role). That module needs a separate pay-as-you-go Anthropic API key from console.anthropic.com. Max is still useful for building with Claude Code. Assumption until answered: a hard cap in config, default **€20/month**, owner-configurable up to **€100/month**. |
| 3 | Pilot capital | Not given | **Unresolved.** Only needed in phase 9, where the owner must type it in themselves. |
| 4 | Host provider | Shared PHP hosting | **Conflict, needs an answer.** The architecture needs Docker, long-running Python 3.12 processes, PostgreSQL 16, Redis and an isolated execution container. Shared PHP hosting cannot run any of these. Options: (a) run locally only (`APP_ENV=local`, free), (b) a small Linux VPS (typically a few € per month; a paid service, so it needs the owner's approval under rule 19). Assumption until answered: **local only**. Phases 1–5 do not need a host. |
| 5 | Phase 7 testnet | Binance Spot Testnet, plus others such as CoinEx if possible | **Partly resolved.** Primary: Binance Spot Testnet (order plumbing only; a testnet uses fake funds, so its EU status does not matter). CoinEx: no public spot testnet or sandbox was found, and its MiCA status is unconfirmed. Without a sandbox, testing a CoinEx adapter would mean real orders, which the live lock forbids before phase 9. The adapter interface will be venue-agnostic so CoinEx can be added if a sandbox exists. Re-check in phase 7. Fallback testnets: OKX demo, Bybit testnet. |
| 6 | Promotion thresholds | "Do whatever you think is better" | **Resolved.** Set in `docs/promotion-policy.md` (v1), fixed now, before any evaluation. |
| 7 | Repo name | `agtrading` is OK | **Resolved.** |

## Assumptions made in phase 0

- **Repo layout.** The spec pack was moved to the repo root: `CLAUDE.md` at the
  root, spec files in `docs/`, and the pack's own README kept as
  `docs/00-spec-pack-readme.md`.
- **Python tooling.** Python 3.12 (per `04-architecture.md`), managed with `uv`;
  `uv.lock` is the committed lockfile (rule 18). Dev tools so far: pytest, ruff.
- **Package naming.** Each package is an importable module prefixed `cp_`
  (for example `packages/core/src/cp_core`) to avoid clashing with PyPI names.
- **Execution isolation.** `cp_execution` is excluded from the main Python
  distribution so research code cannot import it (rule 11). A test enforces
  this. It will get its own packaging and container.
- **`make migrate`.** No database exists yet; the target lists `migrations/*.sql`
  and succeeds when there are none. The PostgreSQL migration runner is added
  with the first migration.
- **Secret scanning.** The phase 0 test scans committed files only. Scanning
  logs, database rows and JSON columns (also required by rule 13) is added
  when those exist.
