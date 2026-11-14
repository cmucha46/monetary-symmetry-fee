# RESULTS V2 — Covered-base correction (Lane F)

**Question:** how much of the v1 centre case (combined $7.02T at s=75%,
β=0.88) was an artefact of defining the business covered base as *total
nonfinancial business debt × 0.70* — a proxy that counts corporate bonds
and commercial paper as if they were fee-bearing loans?

**Answer, in one line:** less than Lane E feared. On the recommended
central interpretation the centre combined total falls from $7.02T to
**$6.71T** (−$0.30T, −4.3%) and the $6T hypothesis **survives at s=75%**.
On the strict loans-only interpretation it falls to **$5.60T** and $6T
**fails at s=75%** (it still survives at s=90%). Lane E's "~$2.8T of gross
fee overstated" is **not reproduced**: $2.885T is the *eligible-principal
stock* gap for business, not the fee gap — the computed 10-year business
gross-fee gap is $0.50T (central). A $2.8T fee gap arises only if business
mortgages ($7.20T of loans) are removed from *every* category — an
accounting error, because they are covered mortgage loans that sit in the
business bucket in this repo's mutually exclusive bucketing.

Machine-readable: `results/deterministic_score_v2.csv` (27 rows: 3
covered-base variants × s ∈ {50,75,90}% × β ∈ {0.70, 0.88, 1.00});
annual detail `results/deterministic_annual_v2.csv`. All other model
inputs are identical to v1; the consolidated interest line is unchanged
by the base definition (the IORB path is solved from the desired stance),
so every difference below is a fee-line difference.

## Interpretation adopted (brief, "Statutory counterfactual")

The fee falls on **outstanding principal of newly originated covered
private loans; the lender remits**. Therefore:

- **Debt securities are not covered.** Corporate bonds ($7,924.1B),
  business commercial paper ($215.0B) and business-issued municipal
  securities ($651.7B) are marketable securities, not loans. This is the
  core v1 error: the ×0.70 proxy effectively fee'd ~30% of them.
- **Securitised loans are covered once** (central variant). Securitisation
  transfers the loan; it does not extinguish the principal. The brief
  requires modelling securitisation and *preventing double taxation of
  the same principal* — so the originating/servicing lender remits once
  and the MBS/ABS holder is not charged again. The strict variant reads
  coverage as portfolio loans only and excludes securitised pools.
- **Federal-government-as-lender credit is not private credit.**
  G.19's federal-government holder line ($1,578.0B, mostly Direct student
  loans) is excluded from the consumer base in both corrected variants.
- Categories remain the repo's mutually exclusive **borrower buckets**:
  business mortgages live inside `business`, not `mortgage` (which is
  household-sector mortgages). H.8 "CRE loans" (~$3.00T, banks only) are a
  subset of Z.1 commercial + multifamily mortgages and must not be added
  on top of them.

## Covered base by category ($T, starting stocks)

| Category | lane_e_proxy stock × share = eligible | loans_plus_securitized (CENTRAL) stock × share = eligible | loans_only (STRICT) stock × share = eligible |
|---|---|---|---|
| mortgage | 13.788 × 0.90 = 12.409 | 14.356 × 1.000 = **14.356** | 14.356 × 0.776 = **11.147** |
| consumer | 5.099 × 0.85 = 4.334 | 5.099 × 0.691 = **3.521** | 5.099 × 0.691 = **3.521** |
| business | 23.292 × 0.70 = 16.304 | 13.419 × 1.000 = **13.419** | 13.419 × 0.669 = **8.973** |
| other | 2.045 × 0.60 = 1.227 | 1.247 × 1.000 = **1.247** | 1.247 × 1.000 = **1.247** |
| **Total eligible** | **34.275** | **32.543** | **24.888** |
| Total stock | 44.224 | 34.121 | 34.121 |

## Category findings

- **Mortgages — all of them are loans, so all are covered (central).**
  Z.1 L.217 (2025): total mortgages $21,559.6B = 1–4 family $14,770.1B +
  multifamily $2,446.7B + commercial $3,957.0B + farm $385.9B. In borrower
  buckets: household sector $14,356.4B (`mortgage` category — v1 used only
  the D.3 household 1–4-family line, $13,788.3B, and so *understated* this
  category) and nonfinancial business $7,203.2B (inside `business`).
  Securitised holdings: agency- & GSE-backed pools $3,209.9B + ABS issuers
  $1,099.3B; portfolio holdings include depositories $7,228.6B and GSE
  retained portfolios $7,668.2B. Strict variant removes the pools.
- **Consumer — G.19 loans, minus the federal government as lender.**
  G.19 total $5,098.8B (2025; revolving $1,324.3B + nonrevolving
  $3,774.5B) is already "owned and securitised" — counted once. Holders
  (NSA): depositories $2,074.2B, finance companies $713.6B, credit unions
  $721.3B, nonprofit $11.8B → private $3,520.9B; federal government
  $1,578.0B excluded. G.19 footnote 1: securitised pools mostly remain on
  originators' balance sheets, so no further strict-variant removal is
  applied (gap labelled below).
- **Business — loans are $13,418.5B, not $23,291.5B of total debt.**
  Z.1 L.102 (2025): business loans = depository institution loans n.e.c.
  $2,869.4B (the C&I proxy; H.8 cross-check: bank C&I $2,769.3B, Aug 2025 —
  banks are a subset of all lenders, so H.8 can cross-check but cannot
  size the base) + other loans and advances $3,345.9B (nonbank, finance
  company, GSE and federal-programme loans) + business mortgages
  $7,203.2B. NOT loans, excluded: debt securities $8,790.8B and FDI
  intercompany debt $316.6B.
- **Farm / other residuals.** Farm mortgages ($385.9B) are inside the
  L.217 mortgage instrument total; their borrowers are farm (noncorporate)
  businesses, so in borrower buckets they sit inside `business`.
  `other` = household loans not in mortgages or consumer credit:
  $20,702.1B (L.214 household loans) − $14,356.4B − $5,098.8B = $1,246.9B
  (ANCHORED residual). v1's $2,045B "other household" residual was an
  artefact of the D.3 household total minus the narrower mortgage line.

## Revised score — combined totals, $T (net fee + consolidated interest)

| Variant | s=50% (β .70/.88/1.0) | s=75% (β .70/.88/1.0) | s=90% (β .70/.88/1.0) |
|---|---|---|---|
| lane_e_proxy (v1) | 4.82 / 4.66 / 4.56 | 7.59 / **7.02** / 6.70 | 9.41 / 8.47 / 7.97 |
| loans_plus_securitized | 4.59 / 4.44 / 4.36 | 7.25 / **6.71** / 6.42 | 9.01 / 8.12 / 7.65 |
| loans_only | 3.77 / 3.70 / 3.65 | 5.98 / **5.60** / 5.39 | 7.46 / 6.79 / 6.44 |

## Centre-case decomposition (s=75%, β=0.88, gross fee by category, $T)

| Category | v1 | central | Δ central | strict | Δ strict |
|---|---|---|---|---|---|
| mortgage | 1.968 | 2.277 | +0.309 | 1.768 | −0.200 |
| consumer | 0.875 | 0.711 | −0.164 | 0.711 | −0.164 |
| business | 2.814 | 2.316 | **−0.498** | 1.549 | **−1.265** |
| other | 0.236 | 0.240 | +0.004 | 0.240 | +0.004 |
| **Gross fee** | **5.893** | **5.544** | **−0.349** | **4.268** | **−1.625** |
| Net fee (×0.87) | 5.127 | 4.823 | −0.304 | 3.713 | −1.414 |
| Interest saving | 1.888 | 1.888 | 0 | 1.888 | 0 |
| **Combined** | **7.015** | **6.711** | **−0.304** | **5.601** | **−1.414** |

So: of the v1 centre $7.02T, **$0.30T (4.3%) was base definition** on the
central interpretation and **$1.41T (20.1%)** on the strict one. The
business correction alone is −$0.50T of gross fee (central), partly offset
by +$0.31T from correcting the mortgage category *upward* (v1 had omitted
household multifamily/commercial/farm mortgages).

## $6T verdict under the corrected base

- **s=75%, central (recommended): $6.71T — $6T survives** (and survives at
  every β: $6.42–7.25T).
- **s=75%, loans-only strict: $5.60T — $6T does NOT survive** (range
  $5.39–5.98T across β; the β=0.70 cell misses by only $0.02T).
- s=90%: survives under both corrected variants. s=50%: fails under both.
- As in v1, this says nothing about where the Fed would set the dial;
  it only re-prices the grid on a defensible base.

## Sources (every number retrieved live, 2026-11-13)

| Figure | Series / table | Value (2025) | Vintage |
|---|---|---|---|
| Total mortgages; 1–4 / multifamily / commercial / farm | Z.1 L.217 lines 1–5, FL893065005 etc. | $21,559.6B (14,770.1 / 2,446.7 / 3,957.0 / 385.9) | Z.1 release Mar 19, 2026 (data thru 2025-12-31) |
| Household-sector mortgages | Z.1 L.217 line 7, FL153165005 | $14,356.4B | same |
| Agency/GSE pools; ABS issuers (mortgage assets) | Z.1 L.217 lines 37, 43 | $3,209.9B; $1,099.3B | same |
| Business loans (total); depository n.e.c.; other loans; business mortgages | Z.1 L.102 lines 29–32, FL144123005 / FL143168005 / FL143169005 / FL143165005 | $13,418.5B; $2,869.4B; $3,345.9B; $7,203.2B | same |
| Business debt securities (bonds / CP / munis) | Z.1 L.102 lines 25–28 | $8,790.8B (7,924.1 / 215.0 / 651.7) | same |
| Total loans; household loans total | Z.1 L.214 lines 1, 12, FL894123005 / FL154123005 | $42,481.4B; $20,702.1B | same |
| Consumer credit total; revolving; nonrevolving | G.19, SA | $5,098.8B; $1,324.3B; $3,774.5B | G.19 release Nov 6, 2026 |
| Consumer holders (fed govt etc.) | G.19 levels, NSA | fed govt $1,578.0B; private $3,520.9B | same |
| Bank C&I; bank loans & leases; bank real-estate loans | H.8 Table 2, SA, Aug 2025 | C&I $2,769.3B; total $12,471.6B; RE $5,605.6B (residential $2,605.5B → CRE ≈ $3,000.1B, ANCHORED difference) | H.8 release Sep 19, 2025 (via FRASER) |

**Labelled gaps (fallbacks used, not hidden):**
1. G.19 *total* securitised consumer pools: the DTCNL series exists but
   its 2025 level was not retrieved; only the depository slice (~$15.4B,
   Aug 2026, FRED DTCNLHDNM) was. Impact bounded by that slice's scale;
   strict consumer = central consumer.
2. Holder split of business "other loans and advances" ($3,345.9B, Z.1
   L.216) into direct nonbank loans vs ABS/CLO vs federal programmes was
   not retrieved — the strict variant therefore excludes the whole bucket
   (a deliberate low bound, not a point estimate).
3. Borrower split of agency pools / ABS mortgage assets is not published
   in the retrieved tables; pools are allocated to `mortgage` and ABS
   mortgages to `business` as labelled approximations in the strict
   variant only. The central variant does not need the split.
4. FFIEC/FDIC Call Report aggregates were not retrieved directly; H.8 is
   benchmarked to Call Reports (H.8 release of Sep 26, 2025: benchmarked
   through the June 2025 Call Report), so the H.8 cross-check is the
   Call-Report-consistent figure available.
5. Vintage note: v1's D.3 business total ($23,291.5B) comes from a later
   D.3 vintage than the Mar 19, 2026 L.102 implied total ($22,525.9B);
   the corrected variants use loan *levels* directly, so the total-debt
   vintage gap does not enter v2. The Sept 2026 Z.1 private-credit
   integration (~$1.31T of private-credit loans inside business debt,
   FEDS Note, Oct 16, 2026) postdates the March vintage — the central
   business "other loans" bucket is, if anything, understated in later
   vintages.
