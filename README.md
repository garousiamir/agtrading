# crypto-platform

Personal research and trading platform for BTC and ETH spot markets.
Built in phases; see `CLAUDE.md` for the standing rules and `docs/` for the spec.

**Current phase: 0 (skeleton).** No application code yet.

## Quick start

Requires [uv](https://docs.astral.sh/uv/).

```sh
make install   # uv sync --frozen (installs Python 3.12 deps from uv.lock)
make test
make lint
make migrate
```

## Layout

See `docs/04-architecture.md`. Open questions and assumptions are tracked in
`docs/assumptions.md`.

This is not financial advice, and no part of this platform guarantees profit.
