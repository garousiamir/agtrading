# Assumptions and open questions

Every OPEN item from `docs/01-decisions.md`, plus assumptions made while
building. Nothing here is resolved until the owner says so.

## Open items (unresolved)

| # | Item | Source | Needed by | Status |
|---|---|---|---|---|
| 1 | Which exchange accounts the owner can open as an Irish resident | 01 Residence and access; 03 | Phase 7 (testnet), phase 9 (live) | **Unresolved** |
| 2 | Monthly Claude API spend cap (suggested €20) | 01 Budget | Phase 6 | **Unresolved** |
| 3 | Pilot capital amount (an amount the owner can lose entirely) | 01 Capital | Phase 9; must be typed by the owner | **Unresolved** |
| 4 | Host provider (any Linux VPS) | 01 Hosting | Phase 6 | **Unresolved** |
| 5 | Which exchange testnet adapter to build (Binance Spot Testnet preferred, else OKX demo or Bybit testnet) | 03; 06 Phase 7 prompt | Phase 7 | **Unresolved** |
| 6 | Promotion thresholds (max drawdown limit, paper-vs-backtest tolerance) must be fixed before any evaluation | 05 section 5 | Phase 5 | **Unresolved** |

## Assumptions made in phase 0

- **Repo layout.** The spec pack was moved to the repo root: `CLAUDE.md` at the
  root, spec files in `docs/`, and the pack's own README kept as
  `docs/00-spec-pack-readme.md`. Code lives in this repo (`agtrading`) rather
  than a new repo named `crypto-platform`.
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
