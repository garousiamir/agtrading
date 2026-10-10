# 05 Validation, Costs, Risk, and Unlock

## 1. Time boundaries

Use boundaries shifted to match verified coverage. Illustrative, if data starts in 2014:

| Stage | Period | Use |
|---|---|---|
| Development | 2014–2016 | Design and inner-fold tuning |
| Walk-forward | 2017–2024 | Quarterly out-of-sample folds with frozen procedure |
| Holdout | 2025 | Evaluated once |
| Prospective | After freezing | Forward paper test |

The report must show the valid feature interval, evaluated interval, and holdout interval separately. Eight years of walk-forward results are not ten years of tested performance.

## 2. Walk-forward procedure (per quarter)

1. Admit only data with `available_at` before the decision cutoff.
2. Run inner chronological splits in the trailing three-year window.
3. Fit scalers, imputers, selectors, and calibrators **inside each training split only**.
4. Select parameters using inner validation only.
5. Refit on eligible pre-test data.
6. Freeze the artifact and store its hash.
7. Evaluate the next three months.
8. Advance using the predefined rule.

If outer results change the procedure, mark the procedure "revised after outer results" and lose the claim of untouched evaluation.

## 3. Label isolation
- Each label stores `information_start`, `decision_time`, `label_end`.
- Exclude training labels whose `label_end` is after the training cutoff.
- Purge a gap equal to the label horizon before each test block; embargo one horizon after.

## 4. Cost model (net returns only)

Net P&L = trading P&L − fees − spread and impact − borrow + funding − other.
Never count spread or impact twice.

Candle-level approximation:
`cost_bps = fee_bps + 0.5 × spread_bps + k × sigma_bps × sqrt(Q / V)`

- Use the fee schedule in effect on each historical date. Do not use today's discounted tier for history.
- Illustration only: 20 bps per side ≈ 40 bps round trip.

Required stress tests: base costs, double variable costs, lower liquidity, longer delay, partial fills, no maker rebate, exchange outage during rebalance, stablecoin depeg.

Execution rules:
- No fill on the candle close that produced the signal.
- Stops gapped through fill at the first executable modeled price.
- A limit order does not fill just because a candle touched its price.
- If stop and target both fall in one candle, assume the stop filled first.

## 5. Statistics and promotion

Reports must include:
- All trials tested (including rejected ones) and the total count.
- Net return, CAGR, max drawdown, Sharpe, Sortino.
- Block bootstrap uncertainty on daily portfolio returns (not on individual trades).
- Deflated Sharpe Ratio with the trial count stated.
- Comparison with cash, buy-and-hold BTC and ETH, simple 200-day trend, and volatility-matched exposure.
- Verdict: **promote**, **reject**, or **insufficient evidence**.

Suggested promotion policy (set numbers before evaluation):
- All integrity and leakage tests pass.
- Positive net performance in walk-forward and holdout.
- Maximum drawdown within a limit you set in advance.
- Beats simple baselines on a risk-adjusted basis.
- Still positive with doubled variable costs.
- At least 60 days of paper trading within tolerance of the backtest.

## 6. Risk limits (engineering defaults, configurable)

| Control | Default |
|---|---|
| Gross exposure | ≤ 100% of allocated equity |
| Per-asset concentration | ≤ 25% |
| Leverage and borrowing | Disabled (hard-coded off) |
| Expected loss per entry at stop | ≤ 0.25% of equity |
| Single order size | ≤ 0.5% of equity |
| Participation in market volume | ≤ 1% of recent traded notional |
| Daily loss (UTC) | −2%: disable new risk |
| Drawdown from peak | −10%: suspend until owner reviews |
| Stale price | Reject orders if quote is older than 10 seconds |
| Reconciliation mismatch | Block new risk until resolved |
| Risk service down or unknown | Block new risk |

Emergency commands (three separate buttons):
1. Disable new orders.
2. Cancel open orders.
3. Reduce or flatten exposure (not guaranteed; depends on liquidity and exchange availability).

## 7. Order handling
- Write the order intent to the database before sending it.
- Use unique client order IDs; reuse them on retry.
- On timeout, check the exchange by client ID before resubmitting.
- Assume exactly-once delivery cannot be guaranteed; deduplicate fills by exchange fill ID.
- Reconcile balances, positions, and open orders on startup, after reconnects, and every 5 minutes.

## 8. Claude review scope
Claude receives read-only summaries of:
- Research results (development period only, plus holdout only after evaluation).
- Paper and live P&L, orders, fills, reconciliation status, and risk events.
- Data quality reports.

Claude's outputs are stored as notes. Claude never receives exchange keys, holdout data before evaluation, or write access to risk or orders.

## 9. Live unlock conditions (all must be true)

1. Integrity and leakage tests pass.
2. Holdout or prospective evaluation completed under the promotion policy.
3. At least 60 consecutive days of paper trading with no unexplained ledger differences.
4. Paper results within tolerance of backtest.
5. Risk limits tested with a simulated breach.
6. Emergency controls tested on a testnet or paper account.
7. Owner types the pilot amount to confirm it.
8. Owner approves the exact package hash with password and TOTP.

The execution process checks all eight before sending any live order. The UI check alone is not enough.

**Honest note:** Passing these conditions does not guarantee profit. They reduce the chance of avoidable failures.
