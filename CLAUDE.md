# CLAUDE.md: Standing rules for this repository

These rules are mandatory. If a request conflicts with them, stop and explain the conflict.

## Purpose
Personal research and trading platform for BTC and ETH spot markets. Single owner. Research, paper trading, and manual-or-automatic execution with strict risk controls.

## Non-negotiable rules

1. **Build one phase at a time.** Do not start a phase until the owner confirms the previous phase's exit tests pass.
2. **Time order is sacred.** No feature may use data with `available_at` after its decision time. No shuffled train/test splits.
3. **Holdout is consumed once.** Once holdout results influence any change, mark it consumed and require a new prospective test.
4. **Count every trial.** Record every parameter combination tested. Report the Deflated Sharpe Ratio.
5. **Net returns only** for all ranking and promotion (after fees, spread, slippage, funding).
6. **Benchmarks and cost stress are mandatory** in every strategy report: cash, buy-and-hold, a simple trend rule, and doubled costs.
7. **"Insufficient evidence" is a valid verdict** and must be shown when evidence is weak.
8. **Never display a score as a probability of profit** unless it has been calibrated out of sample.
9. **No floating point for money.** Use `Decimal` everywhere money or quantity is computed.
10. **All timestamps are UTC and timezone-aware.**
11. **Research code never has exchange trading credentials.** Only the execution service may hold them, in a separate process.
12. **Live trading is locked by default.** The execution service must refuse live orders unless every unlock condition in `docs/05-validation-and-risk.md` section 5 is true. Check this in the execution process, not only in the UI.
13. **No secret in code, logs, database rows, JSON columns, or git.** Add a test that fails if a secret pattern appears in these places.
14. **Exchange keys must have withdrawal permission disabled.** Reject any key that reports withdrawal permission.
15. **LLM output is untrusted.** It may propose strategies in the restricted DSL. It cannot read holdout data, change risk limits, approve deployments, or submit orders.
16. **No `eval`, `exec`, or dynamic imports** of user-supplied or LLM-supplied content.
17. **Every money-affecting change needs a test.** Changes to accounting, risk, order handling, or validation require a new or updated test in the same commit.
18. **Pin dependencies** with a committed lockfile.
19. **Ask before adding a paid service or paid data source.** The data budget is zero.
20. **Never fabricate data.** If a source lacks coverage, return an explicit error. Do not fill gaps silently.

## Working style
- Write small, reviewable commits.
- Show the owner the exit test results at the end of each phase.
- When unsure about a financial or legal assumption, record it in `docs/assumptions.md` and ask.
