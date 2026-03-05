# Memo — Obscicron X post (Poisson+Kelly quant story)

## What we captured
- Primary post: `output/x/x-2029125852873801796-2026-03-04.md`
- Linked context tweet: `output/x/x-2028904166895112617-2026-03-05.md`

The linked tweet points to an X Article:
- **Title:** "How I'd Become a Quant If I Had to Start Over Tomorrow"
- **URL:** http://x.com/i/article/2028762672343257088

## Attempted retrieval
- `scripts/article-capture.sh` failed due to X returning **HTTP 500** at capture time (Playwright saw “This page isn’t working”).
- OCR of the article preview images only yielded the header, not body text.

## Extracted, testable kernel (ignoring the hype)
The story implies a recipe:
1) Model short-horizon BTC market moves as an event-rate process (Poisson-ish framing).
2) Convert that to an edge estimate (probability distribution of outcomes).
3) Size bets using Kelly (or fractional Kelly) to maximize log-growth.

### Reality check
- A weekend Poisson+Kelly model is **not** sufficient for durable profitability in 15-min crypto markets without:
  - fees/spread/slippage model
  - liquidation/funding effects (if perps)
  - regime detection (volatility clustering, fat tails)
  - strong uncertainty control (Kelly is brittle under model error)

## 2–3 falsifiable tests we can run (relevant to our work)
Even without the full article, we can test the core claim structure.

### Test 1 — “Poisson-ish” assumption validity
**Question:** Are 15-min return magnitudes/directions consistent with a simple constant-rate arrival model?
**How:** Fit a baseline (Poisson/event-rate or simple diffusion) to historical 15-min BTC returns and check:
- overdispersion vs Poisson
- tail behavior vs assumed distribution
- stationarity across regimes
**Pass condition:** model error is small enough that Kelly sizing wouldn’t blow up.

### Test 2 — Kelly brittleness under model error
**Question:** How much edge estimation error can you tolerate before fractional Kelly dominates / full Kelly ruins you?
**How:** simulate repeated betting with mis-specified probabilities; sweep fractional Kelly factor.
**Output:** recommended “max fractional Kelly” given plausible calibration error.

### Test 3 — Transfer to Polymarket (our actual sandbox)
**Question:** Do Polymarket markets show predictable short-horizon mean reversion / event-rate patterns that could be sized with a Kelly-like rule?
**How:** on Polymarket price series, evaluate whether a simple probabilistic model produces stable positive log-growth under realistic fees + fill assumptions.

## Next action
- Re-try capturing the X Article body later (X 500 may be transient), OR open it via headed browser session.
- If we can capture it, extract concrete assumptions + any specific model details (features, data, risk controls) and re-run the above tests targeted to those claims.
