# Personal Crypto Research and Trading Platform: Spec Pack

This folder replaces the long master specification with shorter files you can hand to Claude Code one at a time.

## Files

| File | Purpose | Give to Claude Code? |
|---|---|---|
| `CLAUDE.md` | Permanent rules Claude Code must follow in every session | Yes, place in repo root |
| `docs/01-decisions.md` | Your answers: Ireland, zero data budget, manual/semi/auto modes, Claude's role, hosting | Yes |
| `docs/02-data-free.md` | Data sources that cost nothing, and their limits | Yes |
| `docs/03-exchanges.md` | Exchange and testnet suggestions for an Irish resident (verify before opening accounts) | Yes |
| `docs/04-architecture.md` | Components, modes, and build phases | Yes |
| `docs/05-validation-and-risk.md` | Validation rules, cost model, risk limits, live-unlock conditions | Yes |
| `docs/06-phase-prompts.md` | Exact prompts to paste into Claude Code, one phase at a time | Yes |

## How to use

1. Create an empty git repository named `crypto-platform`.
2. Copy `CLAUDE.md` into its root and the `docs/` folder alongside it.
3. Open Claude Code in that folder.
4. Paste the Phase 0 prompt from `docs/06-phase-prompts.md`.
5. Review the output before continuing. Do not paste several phases at once.

## Honest limits

- **No platform can guarantee profit.** Most retail strategies that look good in backtests lose money live. This pack is designed to find out honestly, including when the answer is "nothing qualifies."
- **Zero loss is not achievable.** Risk limits reduce and bound losses, and paper trading tests the system before real money is involved. Choose a pilot amount you can lose entirely.
- **Ten years of tested history is not guaranteed.** Free sources may not cover ten years of every asset. The platform reports the real span and refuses claims it cannot support.
- **Claude is an advisor, not a trader.** It reviews, explains, and proposes. It cannot place orders or change risk limits.
- **Check legal access before opening any account.** Exchange availability for Irish residents changes; see `docs/03-exchanges.md`.
- **This is not financial advice.** Consider a regulated Irish or EU financial adviser before committing meaningful capital, and keep records for tax purposes (Revenue treats crypto gains as taxable).
