# RESULTS V1 — First deterministic fiscal score, FY2027–36

**Status: sensitivity calculation, NOT an estimate.** Deterministic only; no
Monte Carlo; no Fed-discretion dial; no FRB/US integration yet. All figures
$T over FY2027–36 unless stated. Machine-readable version:
`results/deterministic_score_v1.csv`; annual detail (incl. fee by category,
IORB/fee paths, remittance and deferred-asset paths):
`results/deterministic_annual_v1.csv`.

## The score

| s | β | Gross fee | Net fee (×0.87) | Public-yield saving | IORB/remit. saving | **Consolidated interest saving** | **Combined total** |
|---|---|---|---|---|---|---|---|
| 50% | 0.70 | 4.34 | 3.77 | 0.74 | 0.30 | 1.05 | **4.82** |
| 50% | 0.88 | 3.98 | 3.46 | 0.85 | 0.35 | 1.20 | **4.66** |
| 50% | 1.00 | 3.77 | 3.28 | 0.91 | 0.37 | 1.28 | **4.56** |
| 75% | 0.70 | 6.71 | 5.84 | 1.24 | 0.51 | 1.75 | **7.59** |
| 75% | 0.88 | 5.89 | 5.13 | 1.34 | 0.55 | 1.89 | **7.02** |
| 75% | 1.00 | 5.45 | 4.74 | 1.39 | 0.57 | 1.96 | **6.70** |
| 90% | 0.70 | 8.20 | 7.14 | 1.62 | 0.66 | 2.28 | **9.41** |
| 90% | 0.88 | 7.03 | 6.12 | 1.67 | 0.68 | 2.35 | **8.47** |
| 90% | 1.00 | 6.41 | 5.58 | 1.70 | 0.69 | 2.39 | **7.97** |

Range across the grid: **combined $4.56T – $9.41T**. Centre cell
(s=75%, β=0.88): **$7.02T** = $5.13T net fee + $1.89T consolidated interest.

## Every line, explained

- **Gross fee** — cohort ledger, by category. Centre cell split:
  mortgage $1.97T, consumer $0.88T, business $2.81T, other $0.24T.
  Collections start 2028 (2028 itself is tiny, $0.01–0.02T, because only the
  0.15 pp intro rate on one year's new cohorts is collected); the taxable
  book is still phasing in at the end of the window ($37.4T of ~$47T
  eligible at the centre in 2036) — as with the prototype, the 10-year fee
  total is materially a phase-in artefact and a second decade would collect
  more on the same settings.
- **Net fee** — gross × 0.87. The 13% haircut is the prototype's
  `net_receipts_factor` prior mean, retained as a labelled **placeholder**
  for tax interactions/administration. It is unestimated; a JCT interaction
  score for this instrument does not exist.
- **Public-yield saving** — interest saved on **public-held** debt only,
  from an explicit repricing schedule: 18% of the public stock reprices each
  year at a new-issue yield reduced by τ × (IORB drop), τ = 0.32
  (**placeholder**, prototype prior mean). Year-1 effect is therefore small
  and grows as the stock rolls over — the opposite profile from the
  prototype's back-loaded CBO ramp, and not a plug-in: **comparison line
  only** — the prototype's CBO-plug-in method produced $1.79T of "Treasury
  interest savings" (gross of Fed-held debt) at its discretion dial; the
  comparable consolidated public-yield line here is $0.85–1.70T depending on
  dial/β, *plus* the IORB line below.
- **IORB/remittance saving** — the Fed pays less interest on the $2.93T
  reserve stock (H.4.1-anchored) because IORB is solved down. In the
  **consolidated** view this is the whole remittance channel: lower IORB
  expense raises Fed net income dollar-for-dollar. The prototype's separate
  "lost Fed Treasury income" claw-back is an *internal* transfer in the
  consolidated view (Treasury pays the Fed less coupon; the Fed remits less)
  and correctly nets to zero here — it still appears, explicitly, in the
  gross view in the annual CSV (gross interest saving at the centre is
  $1.44T and scenario cash remittances rise by $0.44T over the window; adding
  gross interest saving + remittance change + fee would double-count, which
  is why the headline uses the consolidated lines only).
- **Combined total** — net fee + consolidated interest saving. Nothing else
  is added. In particular the reserve drain from fee settlement is **not**
  in the total (it is a stock movement, tested in `sfc.settlement_flows`).

## Deferred asset in the runs (a real mechanism, visible here)

The Fed starts 2027 with a ~$0.235T deferred asset. On the **baseline**
(no-fee) path, low Fed net income pays it down only slowly — cash
remittances are $0 in 2027–29 and total just $0.47T over the window. On the
centre fee scenario, IORB expense falls enough that the deferred asset is
extinguished during 2030 and cash remittances total $0.92T. This timing
effect is exactly what the prototype's flat 0.50 haircut could not represent.

## Sensitivity switches (centre scenario, from `results/sensitivity_v1.csv`)

| Switch | Gross fee | Combined |
|---|---|---|
| Centre (lock_phase, refi η=0) | 5.89 | 7.02 |
| `phase_lock_mode="no_phase_lock"` (2029 vintages lock full-formula rate) | 6.01 | 7.12 |
| `refi_elasticity=1.5` (turnover responds to falling stance) | 6.46 | 7.51 |

## Why this differs from the prototype — and why neither is a verdict on $6T

- Prototype (fixed 75%, means): combined ≈ $7.3T on its (gross/plug-in)
  accounting; its discretion headline was $5.60T. V1 centre combined is
  $7.02T on consolidated accounting. The similarity of magnitude is
  coincidental composition: v1's fee is larger (category turnover mix;
  business category — see warning below) and its interest line is smaller
  and slower (explicit repricing instead of the CBO plug-in).
- **β direction:** at fixed s, *lower* β gives a *higher* combined total in
  v1 — lower pass-through leaves IORB (and hence the fee f = k·IORB) higher,
  and the fee gain outweighs the smaller interest saving. Any presentation
  of the grid must carry this, because β is unestimated.
- **⚠ Largest unverified assumption:** the business category starts from
  *total* nonfinancial business debt ($23.29T, Z.1) with a placeholder
  covered share of 0.70 standing in for "the loan portion". If the statutory
  covered base is bank/nonbank *loans only*, the business stock — and
  roughly $2.8T of centre-case gross fee — is overstated. Pinning the
  covered base to Z.1 loan instruments (L.214) is the top data priority
  for v2.
- Other placeholders that move the answer materially: IORB_BASE path
  (SEP-anchored illustrative, not FRB/US), τ = 0.32, the 13% haircut,
  per-category turnover/avoidance, the public-debt path, and the exclusion
  of debt-stock feedback (D5, conservative).
- **ZLB warning (from `policy.py`, tested):** the fee is a multiple of
  IORB, so at IORB ≈ 0 the fee ≈ 0 at any dial — including 90%. At s=90%
  the centre-β runs already solve IORB down to ~0.35–0.45% in the 2030s:
  the instrument operates near the region where it degenerates, and no
  recession/ZLB scenario has been run in v1.

**Bottom line for the $6T hypothesis:** v1's grid straddles $6T
($4.56T–$9.41T) — it survives at high dials and fails at the 50% floor
for every β. Since the dial itself is not identified by anything in this
module (that is the FRB/US / reaction-function question), v1 neither
confirms nor refutes $6T; it replaces the prototype's single distribution
with an honest grid whose width is the finding.
