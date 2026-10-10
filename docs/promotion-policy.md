# Promotion policy v1

Fixed on 2026-10-10, before any strategy has been evaluated (`05-validation-and-risk.md`
section 5 requires the numbers to be set in advance). The owner delegated the
choice of values.

**Changing this file after any walk-forward or holdout result has been seen
creates a new version.** Every strategy evaluated under an earlier version
keeps that version's verdict, and any change prompted by results counts as
"revised after outer results".

A strategy is **promoted** only if every rule below holds. If any rule fails,
the verdict is **reject**. If any evidence minimum in section A is not met, the
verdict is **insufficient evidence**, whatever the other numbers show.

All figures are net of costs (rule 5). "Sharpe" means annualised Sharpe on
daily portfolio returns.

## A. Evidence minimums (otherwise: insufficient evidence)

| # | Rule | Threshold |
|---|---|---|
| A1 | Walk-forward span of out-of-sample quarters | ≥ 16 quarters (4 years) |
| A2 | Closed round-trip trades in walk-forward | ≥ 30 |
| A3 | Holdout or prospective period | ≥ 6 months, evaluated once |
| A4 | Trial count recorded and used in the Deflated Sharpe | Yes |

## B. Integrity

| # | Rule |
|---|---|
| B1 | All leakage, time-order and integrity tests pass |
| B2 | Holdout not consumed by a previous change to this strategy family |

## C. Performance (backtest)

| # | Rule | Threshold |
|---|---|---|
| C1 | Net return, walk-forward | > 0 |
| C2 | Net return, holdout | > 0 |
| C3 | Max drawdown, walk-forward and holdout | ≤ 20% each |
| C4 | Deflated Sharpe Ratio (probability the true Sharpe > 0, given all trials) | ≥ 0.95 |
| C5 | Block-bootstrap 5th percentile of walk-forward Sharpe | > 0 |
| C6 | Sharpe vs. cash, buy-and-hold BTC, buy-and-hold ETH, 200-day trend and volatility-matched exposure | Higher than each, walk-forward |
| C7 | Doubled variable costs | Walk-forward net return > 0 and Sharpe > 0 |
| C8 | No single calendar year contributes > 50% of total walk-forward net P&L | Yes |

## D. Paper trading (before SEMI, AUTO or live)

| # | Rule | Threshold |
|---|---|---|
| D1 | Consecutive paper-trading days | ≥ 60 |
| D2 | Unexplained ledger differences | 0 |
| D3 | Signal agreement: paper signals vs. a backtest replay on the same data | ≥ 99% identical |
| D4 | Paper cumulative net return | Inside the 5th–95th percentile band of block-bootstrapped backtest returns for a window of the same length |
| D5 | Median realised cost per fill vs. modelled cost | ≤ 1.5× |
| D6 | Paper max drawdown | ≤ 10% (the live suspend level in section 6) |

## Why these values

- **20% drawdown (C3)** is far below BTC and ETH buy-and-hold drawdowns (often
  more than 70%), but loose enough that a real trend strategy can pass. The
  stricter 10% (D6) matches the live drawdown suspend level, so a strategy that
  would trip the live circuit breaker never reaches live.
- **DSR ≥ 0.95 (C4)** penalises the number of trials, so wide parameter searches
  have to clear a higher bar.
- **The bootstrap band (D4)** asks whether paper results are plausible given
  the backtest, instead of using an arbitrary percentage, which would be too
  strict for volatile assets over 60 days.
- **The 50% one-year cap (C8)** rejects strategies whose result rests on a
  single year, such as one bull run.
