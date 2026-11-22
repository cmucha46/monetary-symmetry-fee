# T-Bill Variant — Debt-Maturity Migration under a Frozen Debt Ceiling

**Prepared:** November 22, 2026 · **Assignment:** sponsor's T-bill
variant authorization of November 22, 2026, extending the Combined
Study (Monetary Symmetry Fee v2 + Medicare for America under a
spending closure). **Plan context:** the combined plan on the
combined study's consolidation basis — growing CBO-style debt path,
central case headline, corrected maturity-dependent τ. This study
changes **only the Treasury's maturity structure**; the fee, MFA,
receipts, drag and remittance lines are the combined study's,
unchanged.

> **Standing caveats — read before citing any number.**
> (1) Every figure is a **simulation under stated assumptions** from
> this project's models — not a Federal Reserve, CBO, or JCT
> forecast. (2) **τ_long is UNESTIMATED** (combined study, caveat 3);
> results are a τ_long surface. (3) **The bill spread at scale has
> NO empirical basis** — the spread scenarios are ASSUMED, and the
> break-even spread (§4) is the robustness object, not any scenario.
> (4) The **term-premium saving from shortening is reported on a
> separate line (§6) and is never added to the coverage margins** —
> it exists with or without the fee. (5) One-ledger rule: the
> variant's increment is added once, to the interest line only.

---

## Executive summary

**The variant.** T-bills are excluded from the debt-ceiling
calculation and the ceiling is never raised again. Note and bond
auctions are on hold: maturing note/bond principal is refunded into
bills, and all net new borrowing is bills. The bill complex is the
existing seven tenors (4, 6, 8, 13, 17, 26, 52 weeks) on the current
schedule and issuance mix.

**What the machinery gives:**

1. **Migration is fast.** On the combined central debt path, the
   bill stock (average balances) rises from $7.1T (22% of marketable
   debt, FY2026) to **$42.6T — 83% of the stock — by FY2036**; the
   stock's weighted-average maturity falls from 70 months to
   **8 months**. The legacy curve does not need to be retired by
   policy; it matures out from under the frozen ceiling.

2. **The interest line rises at every τ_long, and its
   τ_long-dependence is abolished, not reduced.** Variant interest
   savings (central, FY27–36) are **$3,765B at Δspread = 0 —
   identical at τ_long = 0, 0.25, 0.5 and 0.75**, because legacy
   survivors are never refinanced in kind: there is no long
   new-issue rate left for τ_long to act on. Against the combined
   study's corrected basis ($909B at τ_long = 0), the gain at
   τ_long = 0 is **+$2,455B** before any spread toll. The remaining
   τ_long-gradient in the *gain* (+$2,455B → +$1,405B across the
   surface) is entirely the counterfactual's: it measures what the
   current structure would have captured, not any uncertainty
   inside the variant.

3. **The spread toll is real but second-order across the whole
   scenario grid.** Charging the bill spread an ASSUMED schedule
   asymptoting to +25 / +50 / +100bp as the bill share rises costs
   $326B / $656B / $1,328B of the gain (τ_long = 0). **Break-even:
   bills could trade at a constant average spread ≈ +96bp over
   IORB (τ_long = 0) to +50bp (τ_long = 0.75) across the whole
   window — against a 2008–26 median of −14bp and a worst recent
   print of +26bp — before the variant's gain is exhausted.** The
   variant does not need the spread to behave; it needs it not to
   explode by an order of magnitude beyond anything observed.

4. **Coverage: the central case's thin margin becomes comfortable;
   high-stress remains unfinanced.** Restated central margins
   (combined-study margin + variant gain): at the headline spread
   scenario (S∞ = +50bp), **+$1,977B at τ_long = 0** (from +$179B),
   rising to +$2,280B at τ_long = 0.75; the central case is financed
   in **every** cell of the τ_long × spread grid (worst cell
   +$1,305B). High-stress improves by $0.1–2.7T depending on cell
   (the gain collapses toward zero where a high τ_long meets the
   widest spread) and remains **unfinanced in every cell** (best
   −$4,925B at τ_long = 0.75, Δspread = 0). The variant is a margin-widener for
   the central case, not a rescue for the stress case.

5. **The rollover exposure is a peak, not a window loss — on this
   rate path.** Under Lane B's Regime D inflation shock, the
   migrated stock's average rate peaks at **4.72% (FY2029) vs
   4.28%** for the current structure, and the shock-window
   (FY28–30) interest cost is **+$687B vs +$474B** above the
   no-shock path (+45%). Over the full window the migrated
   structure's D-minus-C cost is actually *smaller* (+$476B vs
   +$539B), because Lane B's shocked path undershoots the no-shock
   path in FY31–33 and the migrated stock captures the undershoot
   instantly. The exposure to fear is therefore the **spike during
   the inflation fight itself** — the interest bill rising fastest
   exactly when tightening is politically hardest — not a
   cumulative penalty on this path. A shock path that stayed high
   (no undershoot) would not repay it; see §7's caveat.

6. **The recession side is symmetric and favorable.** Under Regime
   E's collapsing rate path, the migrated structure's interest bill
   falls **$806B more** than the current structure's over the
   window (E-minus-C: −$2,358B vs −$1,552B) — the financing-side
   automatic stabilizer the sponsor identified, priced.

7. **Versus the sponsor's envelope** (~$2.5–3.2T interest line;
   central τ_long = 0 margin ~+$1.5–2T — given in the main chat as
   scaffolding, not targets): the machinery's variant interest line
   is **$3,765B at Δspread = 0 — above the envelope** — and
   $3,109B at S∞ = +50bp (inside it); the τ_long = 0 margin is
   +$2,634B at Δspread = 0 (above) and +$1,977B at S∞ = +50bp (top
   of the envelope). §9 identifies the failed envelope assumption:
   it priced realization off the combined study's CBO-reconciliation
   basis, whose front segment inherits the 70-month recursion lag;
   the literal bucket engine reprices bills within their actual
   maturity year.

---

## 1. The spec as modeled

- **Ceiling mechanics.** Bills (the `bills` bucket, $7,120B at
  FY2026) are outside the ceiling calculation; the ceiling is never
  raised. Note, bond, TIPS and FRN auctions are on hold: no
  refunding in kind. Every dollar of maturing non-bill principal is
  refunded into bills; every dollar of net new borrowing (the
  combined path's deficits net of plan flows) is bills. Migration
  begins FY2027 (variant enacted with the plan; ASSUMED timing).
- **Bill complex.** The existing seven tenors on the current
  schedule and issuance mix — the model carries bills as one bucket
  repricing within the year (the skeleton's construction), so tenor
  composition enters only through the cadence arithmetic (§8) and
  the average-maturity reporting calibration.
- **Rate treatment** (combined study, Sponsor Correction #2,
  extended): bills reprice at the administered path plus the spread
  scenario: dy_bill = −A_t + Δspread_t, transmission 1 by
  arbitrage, where A_t is the skeleton's administered decline
  (0 before FY2030; 1.95pp from FY2030). FRNs, while alive, are
  indexed to the 13-week bill rate and take the bill rate. Legacy
  notes/TIPS/bonds are **never repriced**: survivors keep the
  legacy average rate (BASE_RATE, 3.57%, in the skeleton's
  construct) until their principal matures into bills.
- **Debt path.** The combined study's growing baseline (marketable
  $31,830B → $56,029B) with the combined fixed point iterated
  (savings ↔ combined path) exactly as in Lane 3/4. Fee receipts
  ($4,050B net), the Regime C drag (−$2,667B) and Δ remittances
  (+$410B) are imported unchanged; the MFA residuals are Lane 1's
  verified paths. **No new FRB/US solves**: the debt-structure
  channel is a consolidation-layer object — FRB/US carries no
  maturity-structure state for the Treasury's own issuance — so
  the combined study's rate paths are inputs here, as they were
  to Lane 3/4. (FRB/US's own interest line would also move under
  the variant; the combined study's §5.4 basis divergence applies
  unchanged and is not re-litigated here.)
- **Savings definition.** Rate effect only, consolidated
  (× 0.8559 non-Fed-held share), as in Lane 3/4:
  savings_t = (BASE_RATE − avg_rate_t) × avg_debt_t × 0.8559.
  The debt-*level* effect of the flows is already in the path.

## 2. Migration machinery

The fiscal skeleton's buckets become state variables. Each year,
for each non-bill bucket, the maturing principal (the skeleton's
annual maturity fractions — notes 0.135, TIPS 0.10, bonds 0.035;
FRN principal 0.5/yr **ASSUMED** — the skeleton's 1.0 for FRN is a
repricing fraction for a 2-year floater, not a maturity fraction)
is moved to the bill bucket; the bill bucket also absorbs the
year's net new borrowing. Bucket conservation is test-asserted to
machine precision. Average remaining maturities per bucket are
**ASSUMED**, calibrated so the FY2026 balance-weighted mean
reproduces the published 70-month WAM (bills 0.17yr, FRN 1.0,
notes 4.6, TIPS 7.0, bonds 16.5); legacy buckets age one year per
year without new issuance. WAM is a reporting metric only — it is
not an input to savings.

**Reconciliation to Lane 4 (read before comparing bases).** The
variant's *increment* is measured inside one engine against that
engine's own current-structure base, then added to Lane 4's
published margins. The engine's base differs from Lane 4's base:
Lane 4 runs a 33% "front segment" through the *full* bucket
recursion, so its front end inherits the 70-month realization lag;
the engine assigns segment dy by actual bucket — bills + FRN are
24.7% of the stock repricing at fraction 1.0. The engine base is
therefore higher: **$1,310B vs Lane 4's $909B at τ_long = 0
(+44%)**, converging to +4% at τ_long = 0.75 ($2,361B vs $2,263B),
where the long segment dominates and both constructions treat it
alike. Restating coverage as *Lane 4 margin + engine gain* is the
conservative combination (it pairs the lower published base with
the engine's increment); the engine-consistent restatement would
be larger by the base gap. The gap is a characterization,
regression-guarded in the test suite — and it cuts both ways for
the reader: Lane 4's front-end line is, on the engine's more
literal construction, itself understated, for the same reason
v2's was (combined study §6).

## 3. The migration path (combined central path)

Average balances during the year; variant at Δspread = 0 (the path
is insensitive to the spread scenario to <1% — savings feed back
into the debt path only at the margin).

| FY | Bill stock ($B) | Bill share | Stock WAM (mo) | Avg rate (%) |
|---|---:|---:|---:|---:|
| 2026 (start) | 7,120 | 22.4% | 70 | 3.57 |
| 2027 | 9,538 | 29.1% | 56 | 3.57 |
| 2028 | 14,051 | 40.7% | 42 | 3.57 |
| 2029 | 18,090 | 49.8% | 32 | 3.57 |
| 2030 | 21,925 | 57.4% | 24 | 2.43 |
| 2031 | 25,513 | 63.6% | 19 | 2.31 |
| 2032 | 28,882 | 68.7% | 16 | 2.21 |
| 2033 | 32,187 | 73.1% | 13 | 2.12 |
| 2034 | 35,420 | 76.8% | 11 | 2.05 |
| 2035 | 38,885 | 80.0% | 10 | 1.99 |
| 2036 | 42,646 | 82.8% | 8 | 1.94 |

Legacy stock remaining at FY2036 (average balances): notes
$4,116B, bonds $3,957B, TIPS $788B, FRN ~$0B — the long tail is the
bond bucket, whose 3.5%/yr runoff is the migration's binding
constraint. Half the stock is bills by FY2029; the average rate
reaches 1.94% by FY2036 against the current structure's slower
glide (the combined study's τ_long = 0.5 average rate path reaches
only ~2.8% on the same basis — §7's stress table).

Note what the path implies for the ceiling itself: counted
(notes/bonds/TIPS/FRN) debt falls every year from FY2027 — the
frozen ceiling binds less each year, and the last constraint it
ever imposes is the FY2027 refunding calendar. The ceiling's
operative content after enactment is entirely the maturity
mandate, exactly as the sponsor framed it.

## 4. The bill spread — scenarios and break-even

**Evidence in hand (and its limit).** The combined study's exhibit
(4,529 trading days, 2008–2026): bill − IORB spread mean −10.8bp,
median −14.0bp at today's ~$7T bill stock; +26bp print on
2026-11-19 during an issuance surge; era means from −40bp (2021
scarcity) to +2.8bp (2022–24 hikes, SD 27.5bp). **There is no
observation anywhere near a $20–45T bill stock.** The schedule
below is therefore an ASSUMED pricing of an unobserved object,
and the break-even is the result that does not depend on it.

**Scenario grid (ASSUMED).** Δspread_t = S∞ × clip((share_t −
0.2237)/(1 − 0.2237), 0, 1), linear in the excess bill share
(γ = 1), S∞ ∈ {+25, +50, +100}bp. (A convex γ = 2 form at
S∞ = +50 yields a *larger* gain, $1,324B vs $1,096B at
τ_long = 0.5 — the linear form is the conservative one in-window,
since share^γ < share along the path.) Migration pays a small
toll before the fee era: at S∞ = +50, variant savings are
−$4B / −$14B / −$28B in FY27–29 (the share rises while A_t is
still 0), −$46B cumulative, recovered in FY2030 alone.

**Break-even (headline robustness number).** The constant Δspread,
applied every year, at which the variant's cumulative gain over
the current structure is exactly zero (bisection on the full
fixed-point machinery):

| τ_long | Break-even Δspread | As a level vs IORB* |
|---|---:|---:|
| 0 | +1.10pp | ≈ +96bp |
| 0.25 | +0.95pp | ≈ +80bp |
| 0.5 | +0.79pp | ≈ +65bp |
| 0.75 | +0.64pp | ≈ +50bp |

*Level = break-even Δspread plus the exhibit's −14bp median
baseline spread. Interpretation: bills would have to trade, on
average across the entire decade and across a bill stock rising
to $43T, at **+50 to +96bp over IORB** — roughly 2–4× the worst
sustained spread in the 2008–26 record, and the opposite sign
from the full-sample median — before maturity migration stops
paying for itself on the interest line. This does not prove the
spread will behave; it prices how badly it would have to behave.

## 5. Interest line and coverage restatement

**Interest savings, central case, FY27–36 ($B):**

| τ_long | Lane 4 base | Engine base | Variant Δspread=0 | S∞=+25 | S∞=+50 | S∞=+100 |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 909 | 1,310 | **3,765** | 3,439 | 3,109 | 2,437 |
| 0.25 | 1,365 | 1,663 | **3,765** | 3,439 | 3,109 | 2,437 |
| 0.5 | 1,816 | 2,013 | **3,765** | 3,439 | 3,109 | 2,437 |
| 0.75 | 2,263 | 2,361 | **3,765** | 3,439 | 3,109 | 2,437 |

The variant column is constant across τ_long **exactly** (test-
asserted): with no refunding in kind, τ_long has no long new-issue
rate to act on. What survives of τ_long is in the *gain*
(variant − engine base): +2,455 / +2,102 / +1,752 / +1,405 at
Δspread = 0 — a statement about the counterfactual, not about
the variant. The front/long split question the combined study
posed (front $901B / long $915B at τ_long = 0.5) is dissolved by
the variant: by FY2036, 83% of the stock *is* the front end.

**Coverage margins restated ($B; Lane 4 margin + variant gain):**

Central — financed in **all 16 cells**:

| τ_long | S∞=0 | +25 | +50 | +100 |
|---|---:|---:|---:|---:|
| 0 | +2,634 | +2,307 | **+1,977** | +1,305 |
| 0.25 | +2,736 | +2,410 | +2,080 | +1,408 |
| 0.5 | +2,837 | +2,511 | +2,181 | +1,509 |
| 0.75 | +2,937 | +2,610 | +2,280 | +1,608 |

High-stress — financed in **no cell** (shown at the same grid):

| τ_long | S∞=0 | +25 | +50 | +100 |
|---|---:|---:|---:|---:|
| 0 | −5,243 | −5,611 | −5,982 | −6,738 |
| 0.25 | −5,135 | −5,503 | −5,874 | −6,630 |
| 0.5 | −5,029 | −5,396 | −5,768 | −6,524 |
| 0.75 | −4,925 | −5,292 | −5,664 | −6,420 |

The variant's high-stress gain (up to +$2,717B at τ_long = 0,
Δspread = 0 — larger than central's because the stress debt path
is bigger — but shrinking to +$83B at τ_long = 0.75, S∞ = +100)
closes at most a quarter of the $10,730B residual's shortfall. **The high-stress verdict
of the combined study is unchanged**: no maturity policy finances
a residual of that size; it remains a general-revenue problem.

Timing (§5.3 of the combined study) improves but is not the
headline restated here: the variant's savings are *more*
back-loaded than the base's in level but start from a higher
FY2030 base (FY2030 variant savings $326B at S∞ = +50, τ_long = 0,
vs $140B Lane 4 at τ_long = 0.5); the annual pay-go shortfall
years (2030, 2035–36) should be re-read against the restated
annual table in `coverage_restated.csv`'s companion outputs
rather than assumed away — the banked-ledger closure remains the
plan's stated mechanism.

## 6. Term-premium channel — SEPARATE line, never in coverage

Shortening the stock saves the term premium **whether or not the
fee exists**: migrated principal pays the bill rate instead of a
long rate carrying a term premium. Priced as its own exhibit —
excess bill stock (variant minus current-structure bill stock on
the variant's combined path) × TP × 0.8559, TP an **ASSUMED**
scenario parameter:

| TP (ASSUMED) | Cumulative FY27–36 saving |
|---|---:|
| 50bp | $747B |
| 100bp | $1,493B |

This is **not** added to any margin in §5, and the coverage
machinery has no term-premium input (test-asserted). It is
reported because a reader comparing the variant against history
will notice that bill financing has usually been cheaper for
reasons unrelated to this plan — and because the same shortening
that earns the term premium in normal times is what concentrates
the rollover exposure in §7. Crediting it to the fee design
would be the mirror image of the v1 plug-in error.

## 7. Regime D — the rollover exposure, priced

Method: Lane B's Regime D fee run supplies the *increment* to the
plan's own administered path (FY-average L_rff, D minus C:
**+1.76pp FY28, +2.26pp FY29, +0.56pp FY30**, then −0.62 / −0.70 /
−0.33pp FY31–33 — the shocked economy's rule path undershoots the
no-shock path once the shock passes). The increment shifts the
skeleton's A_t; both structures are run on the common baseline
growing debt path at Δspread = 0, τ_long = 0.5 (pure rate
channel). No new FRB/US solves.

**Average rate on the stock under D (%):**

| FY | Current structure | Migrated |
|---|---:|---:|
| 2028 | 4.08 | 4.30 |
| 2029 | 4.28 | **4.72** |
| 2030 | 3.31 | 2.76 |
| 2031 | 2.90 | 1.91 |
| 2036 | 2.83 | 2.19 |

**Interest bill, consolidated ($B):**

| | FY28–30 under C | FY28–30 under D | Shock-window cost | Full-window D − C |
|---|---:|---:|---:|---:|
| Current | 3,181 | 3,655 | +474 | +539 |
| Migrated | 2,990 | 3,677 | **+687** | +476 |

Reading: the migrated structure's interest bill in the shock's
peak year (FY2029: $1,482B vs $1,346B) and across the shock window
is **~45% more exposed** — pass-through is effectively complete
within the year the shock lands, against the current structure's
multi-year glide (its average rate is still 3.31% in FY2030, a
year after the shock's peak). That is the rollover exposure,
priced: **≈ +$213B of additional interest across FY28–30**
(+687 − +474), concentrated in the two years when the tightening
is doing its work. The full-window figure runs the other way
(+476 < +539) only because Lane B's D path *undershoots* C in
FY31–33 — an easing the migrated stock captures instantly and
the current structure mostly misses. **Caveat, load-bearing:** on
a counterfactual shock path that rises and *stays* high (a
1979–82-style plateau rather than Lane B's spike-and-undershoot),
there is no undershoot to capture, and the migrated structure's
full-window exposure would exceed the current structure's by
roughly the shock-window margin, compounding with the bill
share. The variant converts interest-rate risk from a slow leak
into a marked-to-market position in the administered rate — in
both directions (§8).

## 8. Regime E — the symmetric side (one paragraph)

Under Lane B's recession path (increment to the plan's rate path:
−1.09pp FY29, −2.26pp FY30, −2.16pp FY31, decaying thereafter;
the fee itself collapses toward 0.11% at the trough in Lane B),
the migrated structure's interest bill falls **$806B further**
than the current structure's across the window (E-minus-C:
−$2,358B migrated vs −$1,552B current; FY28–30 interest $2,360B
vs $2,837B). The relief arrives with the trough, not years after
it: the same ≤1-year pass-through that exposes the Treasury in
Regime D makes the interest bill collapse in Regime E exactly
when deficits peak — a financing-side automatic stabilizer worth
roughly $0.8T on this path, and the honest mirror of §7: the
variant does not buy insurance in one direction; it removes the
lag in both.

## 9. The 52-week cadence option, and the envelope check

**52-week weekly (bracketed sponsor option).** Under continuous
issuance, a tenor-τ stock's mean remaining maturity is τ/2
regardless of auction frequency; cadence changes only the
lumpiness of the maturity profile. On ASSUMED tenor weights
approximating the current mix (4wk 13%, 6wk 7%, 8wk 13%, 13wk
28%, 17wk 9%, 26wk 20%, 52wk 10%), the bill stock's mean
remaining maturity is **8.8 weeks (2.0 months) with or without**
the change — **the effect on effective maturity is exactly zero**.
What weekly auctioning does change: the largest single-date
maturity concentration of the 52-week component falls from
~7.7% of the component (13 four-weekly towers) to ~1.9% (52
weekly dates). Verdict: **immaterial to the interest arithmetic;
mildly valuable for rollover smoothness** — adopt or not on
operational grounds; it does not move any number in this study.

**Envelope check (honesty requirement).** The main chat's
envelope — interest line ~$2.5–3.2T, central τ_long = 0 margin
~+$1.5–2T — was labeled scaffolding. The machinery contradicts
its top end at Δspread = 0 (interest $3,765B; margin +$2,634B)
and its bottom end at S∞ = +100 (interest $2,437B; margin
+$1,305B); the envelope brackets the mid-spread outcomes
(S∞ = +50: $3,109B; +$1,977B). The failed envelope assumption is
identified: it scaled savings from the combined study's
CBO-reconciliation price ($191B per 0.1pp), which embeds Lane
4's construction of the front segment through the full
70-month recursion — a ~35% realization factor applied to debt
that in fact reprices within the year. The literal bucket
engine realizes the front end at its actual maturity, raising
both the base (§2) and the variant. The envelope's bill-stock
range ($15–35T) also understated the FY36 stock ($42.6T average
balances): full refunding of *all* maturing notes/bonds — the
spec as given — migrates the stock faster than the envelope's
implicit pace.

## 10. Critical assessment and limitations

1. **The result is only as good as the spread's behavior at
   unprecedented scale — and the study's answer is a bound, not
   a prediction.** $43T of bills is ~6× today's stock and a
   larger share of GDP than bills have ever carried. Money-fund
   capacity, dealer balance sheets, deposit disintermediation
   (the fee's β channel in reverse: bills competing with the
   deposit base), and foreign official demand all bind somewhere
   between $7T and $43T; the model prices none of them except
   through the ASSUMED spread schedule. The break-even framing
   (+50 to +96bp sustained, against a −14bp median) is the
   strongest statement the evidence supports.
2. **The skeleton's constructs are inherited, not cured.**
   Legacy coupons are frozen at BASE_RATE (the flat-curve
   fiction); bucket runoff is geometric, not the actual maturity
   calendar; the FY2027 migration start is assumed. A
   security-level MSPD maturity ladder would refine the path's
   first three years; it would not change the direction of any
   result, because the binding runoff (bonds at 3.5%/yr) is a
   stock fact, not a calibration.
3. **The variant abolishes τ_long by construction — inside this
   machinery.** The invariance is exact because the skeleton has
   no other channel for the long segment to matter once issuance
   stops. In the world, ceasing long issuance for a decade would
   itself move the term premium and the long rate (scarcity of
   duration; pension/insurance demand for long assets) — effects
   that live in the §6 exhibit's parameter and in market
   functioning, not in the interest identity computed here.
4. **Debt-ceiling law and market plumbing are outside the
   model.** Intra-year refunding room during the transition,
   cash-management around maturity towers, and the legal form of
   the bills exclusion (an amendment to 31 U.S.C. §3101's face-
   amount definition) are drafting and operations questions; the
   annual model sees none of them.
5. **Interaction with the fee's own politics is noted, not
   modeled.** Under the variant, an FOMC tightening raises the
   Treasury's interest bill within the year on ~83% of the stock
   by FY36 — the fiscal-dominance pressure channel the combined
   study flagged qualitatively is mechanically amplified. The
   model's Taylor rule does not hear Treasury's complaints;
   a real one might. This is the variant's deepest unpriced
   risk, and it is institutional, not arithmetical.

## 11. All-in presentation (sponsor-requested)

*Added at the sponsor's request. This section re-presents
figures computed in §4–§6 and in the combined study; it adds
no new modeling and displaces no headline figure. All figures:
combined plan, central case, FY2027–36, τ_long = 0, $B, unless
stated.*

**The fee swing on the study basis.** The swing — the fee
side's all-in contribution, stated as the §5 restated coverage
margin plus the MFA central residual that margin is measured
against ($2,524B):

| Spread scenario | Restated margin (§5) | + MFA residual | = Fee swing |
|---|---:|---:|---:|
| Δspread = 0 | +2,634 | 2,524 | **5,158** |
| S∞ = +25bp | +2,307 | 2,524 | **4,831** |
| S∞ = +50bp (headline) | +1,977 | 2,524 | **4,501** |
| S∞ = +100bp | +1,305 | 2,524 | **3,829** |

**Customary spread.** The grid above stresses the spread
upward from the Δspread = 0 case. The §4 spread schedule also
evaluates in the other direction: at an asymptote of
S∞ = −14bp — the full-sample median bill–IORB spread in the
combined study's exhibit (2008–2026) — the variant engine
computes a gain of $2,636B and a fee swing of **$5,338B**
(COMPUTED by direct evaluation of the spread machinery at the
−14bp asymptote, not interpolated; a linear interpolation of
the §5 toll schedule, ≈$326B per 25bp, gives $5,341B — the two
bases differ by $3B).

**Term premium, added only here (ASSUMED grid, §6).** The §6
exhibit prices the maturity policy's own saving at **+$747B
(TP = 50bp)** and **+$1,493B (TP = 100bp)**. The standing note
of §6 applies with full force: this saving is attributable to
the maturity policy, not the fee — bill financing has usually
been cheaper for reasons unrelated to this plan — and it is
excluded from every coverage margin elsewhere in this report.
It is added in this section only because an all-in presentation
of the combined legislation's total fiscal effect is what was
requested.

**All-in totals (fee swing + term premium):**

| Basis | + TP 50bp | + TP 100bp |
|---|---:|---:|
| Customary spread (S∞ = −14bp, computed) | 6,085 | 6,831 |
| Δspread = 0 | 5,905 | 6,651 |
| Headline spread (S∞ = +50bp) | 5,248 | 5,994 |

**Without the variant.** On the same consolidation basis, with
no maturity migration, the fee swing is **$2,703B–$4,056B**
across τ_long (combined-study margins of +$179B / +$634B /
+$1,085B / +$1,532B, each plus the $2,524B residual), and there
is no term-premium line: the §6 saving exists only on the
excess bill stock the variant creates.

**Reading.** The $6–7T figures in the first row are the all-in
BOUND, not an estimate: reaching them requires the customary
(negative) spread to hold at an unprecedented bill stock, the
term premium counted in, and the favorable end of its ASSUMED
grid, simultaneously — the joint-corner construction the §9
envelope check warns against. The headline of this report is
unchanged: **$4,501B** at the stress spread (S∞ = +50bp) with
the term premium excluded. A reader who disputes any layer of
the stack can remove it from the tables above and land on a
figure stated elsewhere in this report. The FRB/US basis
(combined margin ≈ +$7.5T, unified-scaled) is NOT used anywhere
in this section: Title II enters that basis as demand-neutral
receipts with no incidence carrier, and the combined study
carries it as an upper bound only.

## Appendix — files, code, tests

Code: `v2/tbill_variant/tbill_variant.py` (engine, spread
schedule, break-even solver, term-premium exhibit, stress,
cadence), `run_tbill.py`. Outputs: `migration_path.csv`,
`interest_lines.csv`, `spread_grid.csv`, `coverage_restated.csv`,
`term_premium.csv`, `stress.csv`, `tbill_summary.json`. Lane 3/4
code is imported unmodified; v1, v2 and combined-study originals
are unmodified by this study. Tests: `tests_tbill.py` — bucket
conservation, share monotonicity, τ_long-invariance of the
variant, gain monotonicity in the spread, break-even bracketing,
engine↔Lane 4 reconciliation bounds, term-premium separateness,
CBO guard, spread-schedule endpoints, cadence arithmetic,
shock-increment signs. **ASSUMED parameters (collected):** FRN
principal runoff 0.5/yr; bucket average maturities (WAM
reporting only); spread schedule form and asymptotes; migration
start FY2027; term-premium grid {50, 100}bp (exhibit only);
bill tenor weights (cadence arithmetic only); the combined
study's inherited assumptions (13% haircut, erosion, drag
import) unchanged.
