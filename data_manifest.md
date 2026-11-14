# Data manifest — Monetary Symmetry Fee model v2 (Lane E)

Every input is labelled **SOURCED** (published figure, cited below),
**ANCHORED** (built from sourced figures by stated arithmetic), or
**PLACEHOLDER** (judgmental, not estimated — must not be quoted as data).

## Starting private-loan stocks (end-2026 levels, $T)

| Category | Stock | Status | Source |
|---|---|---|---|
| Mortgage (household 1–4 family residential) | 13.788 | SOURCED | Fed Financial Accounts Z.1, Table D.3 (debt outstanding by sector), 2025 annual: one-to-four-family residential mortgages $13,788.3B. Series LA153165105. Retrieved 2026-11-13 via federalreserve.gov Z.1 D.3 page. |
| Consumer credit | 5.099 | SOURCED | Z.1 Table D.3, 2025 annual: consumer credit $5,098.8B. Series LA153166000. Same retrieval. |
| Business (C&I + CRE + all nonfinancial business debt) | 23.292 | SOURCED (with caveat) | Z.1 Table D.3, 2025 annual: nonfinancial business debt $23,291.5B (corporate $15,169.4B). Series LA144104005. **Caveat:** this total includes corporate bonds and other non-loan debt; the model's `covered_share = 0.70` for this category is the (placeholder) device that converts it toward a loan base. This is the single largest unverified assumption in v1 — see RESULTS_V1.md. |
| Other household | 2.045 | ANCHORED | Residual: household debt total $20,931.8B (Z.1 D.3, 2025, LA154104005) − mortgages 13,788.3 − consumer 5,098.8 = 2,044.7B. |
| **Total** | **44.224** | ANCHORED | vs prototype's $45.4T aggregate (its own Z.1 reading, different vintage/category mix). The $1.2T difference is vintage + the prototype's inclusion choices; v2 prefers the itemised D.3 split because categories must not overlap (business mortgages sit inside `business`, not in `mortgage`). |

Z.1 cross-checks retrieved the same day: Q3-2025 Z.1 release (release dated
2026-01-09, data through 2025-09-30): household debt $20.7T, nonfinancial
business debt $22.1T, total domestic nonfinancial debt $79.7T; L.214 total
mortgages (all sectors) $21.56T in 2025 — consistent with household mortgages
being only part of all mortgages, the rest sitting in the business category.

## Federal Reserve / Treasury stocks

| Input | Value | Status | Source |
|---|---|---|---|
| Fed-held Treasury securities | $4.196T | SOURCED | Fed H.4.1, week ended Oct 22, 2025: U.S. Treasury securities held outright $4,196,467M. |
| Fed-held MBS | $2.085T | SOURCED | H.4.1, same week: mortgage-backed securities $2,084,542M. |
| Reserve balances | $2.933T | SOURCED | H.4.1, same week: reserve balances $2,933,037M (avg) / $2,929,637M (Wed). |
| Fed deferred asset (start) | ~$0.235T | SOURCED approx. | Fed remittances have been negative since Sep 2022; shortfalls accrue as a "deferred asset" that must be paid down from future earnings before remittances resume (Federal Reserve Bank of St. Louis, "The Fed's Remittances to the Treasury: Explaining the 'Deferred Asset'", Nov 2023; Bipartisan Policy Center explainer: deferred assets "over $230 billion", peaked >$245B in Jan 2026; H.4.1 weekly series). v1 uses $0.235T as the end-2026 starting value — PLACEHOLDER within a sourced range. |
| Debt held by public (start) | $31.0T | PLACEHOLDER | CBO-scale round number for end-2026; NOT yet tied to a specific CBO baseline table. Pending Lane integration with the CBO Feb 2026 baseline (cf. Lane C file §3: net interest $1,108B in 2027 → $2,144B in 2036). |
| Public-debt growth path, yields, repricing shares, Fed book yields, opex, term premium, yield transmission (0.32) | — | PLACEHOLDER | See `src/monetary_symmetry/sfc.py LedgerParams` docstrings. Yield transmission 0.32 is the prototype's invented prior mean, retained ONLY as a labelled placeholder so v1 is comparable to the prototype; it is not estimated. |

## Policy / cohort parameters

| Input | Status |
|---|---|
| IORB_BASE path [4.10 … 3.20] | PLACEHOLDER input file from the prototype ("approximation to September 2026 SEP through 2029; illustrative convergence thereafter"). NOT a forecast, NOT FRB/US output. |
| Per-category covered share, fixed share, turnover, maturity, avoidance | PLACEHOLDER (prototype had aggregate invented priors: covered 0.80, turnover 0.225, fixed 0.64, avoidance 0.065 — v2 splits them by category around similar centres; none is estimated). |
| Debt growth 3.8%/yr | PLACEHOLDER (prototype prior mean). |
| Net receipts factor 0.87 (13% haircut) | PLACEHOLDER (prototype prior mean for "tax interactions and admin"; unestimated — a JCT-style interaction score does not exist for this fee). |
| Phase-in (2028 flat 0.15 pp; 2029 half; 2030 full) | DESIGN INPUT from the project brief / prototype scenario; the prototype README calls it "one possible reconciliation… not a legal forecast". |
| Dial range s ∈ [0.50, 0.90], fee f = IORB·s/(1−s) | DESIGN INPUT from the project brief (statutory design as specified by Carlos). |

## What is NOT in v1 (by design)
- No FRB/US paths (Lane B integration pending) — hence no inflation/employment effects in this score.
- No Fed-discretion dial — requires an identified reaction function.
- No Monte Carlo — deterministic only, per Lane E brief.
- Medicare for America financing test — this module produces only the fee +
  interest side; the financing identity it must feed is in
  `../research/MEDICARE_FOR_AMERICA_SOURCES.md` §4 (note: state MOE = $0 in
  FY2027–36 under H.R.10924 §2209; displacement phases 2030/2033/2035).
