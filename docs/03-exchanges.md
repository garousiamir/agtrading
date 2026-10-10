# 03 Exchanges and Testnets (for an Irish resident)

**Warning:** Exchange availability, licences, and fees change often. Before opening any account, check the exchange's current terms for Ireland. Do not rely on this file for legal eligibility.

## Live trading candidates (Ireland)

| Exchange | Why consider it | Things to verify before use |
|---|---|---|
| **Kraken** | Available in Ireland; mature REST and WebSocket API; public historical archive (useful for research) | Confirm Irish account eligibility; confirm the API permissions model; check fee tiers |
| **Coinbase** (Coinbase Advanced API) | Regulated EU entity based in Ireland; well-documented API | Confirm the API covers your account type; check fee and candle limits |
| **Binance** | Deepest liquidity; best testnet documentation | Verify whether Irish residents can open accounts. Many EU residents cannot. Use the testnet for development regardless. |
| **OKX / Bybit** | Testnet or demo modes exist | Verify EU and Irish eligibility before opening accounts |

## Testnet and demo options

| Option | Use | Notes |
|---|---|---|
| **Binance Spot Testnet** | Integration testing of order placement, filters, and cancellations | Fake funds; separate keys; check current availability |
| **Bybit testnet** | Second option for adapter testing | Separate testnet keys |
| **OKX demo trading** | Third option | Requires a demo key with a simulated-trading header |
| **Built-in paper simulator** (recommended) | Phases 2–6 | Not a venue; a local engine that uses the same strategy code and real price feeds. Costs nothing and tests your system, not the exchange. |

## Recommendation

1. **Phases 2–6:** Use the built-in paper simulator. It is free, fully under your control, and tests the logic you actually care about.
2. **Phase 7 (plumbing test):** Use **Binance Spot Testnet** if available to you, because its documentation and filters are the most complete. If it is unavailable, use **OKX demo** or **Bybit testnet**.
3. **Live, if ever:** Choose between **Kraken** and **Coinbase** based on your eligibility, fees, and API limits. Test both adapters on testnet or with a tiny amount before choosing.

## Adapter requirements (all venues)

- Read-only key for data, separate trading key for orders.
- Withdrawal permission disabled. The adapter must reject keys that report withdrawal permission.
- IP allowlist where supported.
- Rate limit handling and reconnection for WebSocket feeds.
- Client order IDs unique per account; duplicate-submission protection.

## Tax note
Irish crypto gains are generally taxable (Capital Gains Tax; Revenue guidance applies). Keep a full trade ledger from day one. The platform's ledger export is designed for this; confirm treatment with an accountant.
