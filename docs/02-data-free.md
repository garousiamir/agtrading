# 02 Data Sources (Zero Budget)

Rule: **only free and public sources.** Record each source's licence and terms in `data_sources`. Never assume coverage; query it.

## Market data (OHLCV, trades)

| Source | Free? | What it gives | Limits to plan for |
|---|---|---|---|
| **Kraken public OHLCVT archives** | Yes | Long spot history per pair, includes trade counts | Confirm exact pair and interval availability; archive format may change |
| **Binance public data archives** (`github.com/binance/binance-public-data`) | Yes | Spot klines and trades from ~2017 | Cannot provide 10 years of Binance history; spot timestamps switched to microseconds in Jan 2025 |
| **Coinbase Exchange public candles API** | Yes | Recent and historical candles | Max 300 candles per request; history may be incomplete; rate limited |
| **Kraken and Binance public REST APIs** | Yes | Incremental and recent candles | Rate limits; fill gaps with archives |

**Expected reality:** Free sources will likely give **8–10+ years for BTC and ETH on at least one venue**, but this must be verified by the coverage catalog, not assumed. Pre-2017 history on a single venue may not exist for free. Do not stitch venues into one tradable series.

## Fundamental and on-chain data

| Source | Free tier | Use | Limits |
|---|---|---|---|
| **CoinGecko public API** | Yes, limited | Market cap, supply, dominance | Free history limited in time range and granularity; store every snapshot with `retrieved_at` |
| **Coin Metrics Community data** | Yes, limited | Some network metrics and reference rates | Coverage of metrics and years is limited; check per metric |
| **Blockchain.com / Mempool / block explorers** | Yes, limited | Network activity, hash rate, fees | Rate limits; history may be partial |
| **Public protocol data** (block rewards, issuance schedules) | Yes | Supply schedule features | Computed, not fetched; very reliable |

**Important:** Free on-chain history for 10 years may be incomplete for many metrics. Fundamental features are used only where coverage is verified for the whole test period. Otherwise the feature is excluded and the report says so.

## Rules

1. Store every raw download unchanged with URL, retrieval time, and SHA-256.
2. Respect each provider's terms and rate limits. Use a token bucket and exponential backoff.
3. For any revised metric, store each revision with `available_at`. Do not backdate revisions.
4. Mark legacy data without receive timestamps as `availability_basis = assumed` with a conservative delay (for example, one full day for daily metrics).
5. Treat BTC/USD and BTC/USDT as different markets.
6. Do not assume stablecoins equal one dollar; include a depeg check.
7. Record survivorship bias if delisted-asset records are missing. For BTC and ETH this is minor, but the flag must still be shown.

## Free data check (phase 1 exit test)
The coverage report must list, for BTC and ETH and each source:
- first and last available timestamp,
- missing intervals (outages, unknown gaps),
- whether each fundamental feature covers the full validation period.
