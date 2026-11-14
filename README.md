# Monetary Symmetry Fee — model v2 (Lane E: external fiscal / cohort / SFC module)

Deterministic, reproducible fiscal layer for the Monetary Symmetry Fee
project. This package replaces the prototype's fiscal arithmetic (audited in
`../audit/PROTOTYPE_AUDIT.md`) with:

1. a **loan-cohort model by category** (mortgage / consumer / business / other),
2. a **consolidated Treasury–Federal Reserve stock-flow-consistent ledger**
   with an explicit Fed income statement and deferred-asset mechanism, and
3. a **first deterministic fiscal score** for FY2027–36 over
   dial s ∈ {50%, 75%, 90%} × pass-through β ∈ {0.70, 0.88, 1.00}.

It is deliberately **not** a macroeconomic model: FRB/US (Lane B) supplies
macro dynamics in the integrated project. FRB/US has no loan stock, no IORB
and no fee variable, so fee revenue, reserves and remittances must live in
this external layer — that is what this package is.

## Run it

```bash
cd repo
python3 -m pytest            # 50 tests
python3 run_flow_channel.py  # Lane H: results/flow_channel_v1.csv (see FLOW_CHANNEL.md)
python3 run_score.py         # writes results/deterministic_score_v1.csv,
                             # results/deterministic_annual_v1.csv,
                             # results/sensitivity_v1.csv (lane_e_proxy
                             # variant, values identical to v1) plus the
                             # Lane F v2 files below
```

**Lane F (v2) covered-base variants** — `covered_base_variant` in
`config.py` / `score.run_scenario`: `lane_e_proxy` (v1: total business
debt × 0.70), `loans_plus_securitized` (**default, central**: loan
principal only, securitised loans counted once, federal-government-held
consumer credit excluded) and `loans_only` (strict low bound: portfolio
loans only). Outputs: `results/deterministic_score_v2.csv`,
`results/deterministic_annual_v2.csv`; write-up in `RESULTS_V2_BASE.md`.

No third-party dependencies (standard library only). Python ≥ 3.10.

## Layout

```
src/monetary_symmetry/
  config.py   years, IORB_BASE placeholder path, phase schedule, categories
  policy.py   fee/IORB algebra, ZLB behaviour
  cohort.py   vintage ledger by category
  sfc.py      Treasury/Fed ledger, settlement flows, deferred asset
  score.py    the 3x3 deterministic grid + sensitivity switches
  flow_channel.py  Lane H: interest-income / reserve-flow channel FRB/US
              omits -- zero-sum sector flow table, Treasury-use variants,
              MPC-range demand translation (FLOW_CHANNEL.md)
tests/        pytest suite (cohort conservation, SFC zero-sum, consolidated
              vs gross identity, fee formula, ZLB, deferred asset, ...)
data_manifest.md   every input labelled SOURCED / ANCHORED / PLACEHOLDER
RESULTS_V1.md      the score, line by line, with all caveats
results/           generated CSVs
```

## Modelling decisions (explicit, switchable)

- **D1 — the 2028 introductory fee is not locked for life.** The prototype
  locked the flat 0.15 pp introductory fee into 2028 fixed-rate vintages
  forever (audit §5.4). In v2 the intro rate is a *transitional collection
  rate*: a fixed loan originated in 2028 pays 0.15 pp during 2028 and locks
  the full-formula fee rate of its origination year thereafter.
- **D2 — 2029 phase factor.** Default `phase_lock_mode="lock_phase"`:
  a 2029 fixed vintage locks the half-phase rate (the phase schedule in
  force at its origination), following the brief's phase-in design.
  Switch `phase_lock_mode="no_phase_lock"` locks the full-formula rate
  instead. The difference is measured in `results/sensitivity_v1.csv`
  (+$0.12T gross at the centre scenario) — small because the 2029 vintage
  decays, but it is measured, not hidden.
- **D3 — fixed vs floating.** Fixed vintages lock the fee *rate* (%) at
  origination (s at origination is embedded in that rate, since the dial is
  held fixed within each scenario run); floating vintages pay the current
  year's fee rate. This matches the brief: "floating reset with current fee".
- **D4 — turnover/refinancing.** Default `refi_elasticity=0` (prototype
  behaviour: turnover independent of rates — an internal inconsistency the
  audit flagged in a model whose policy *is* a rate change). With
  `refi_elasticity=η>0`, turnover rises η× the pp fall in the desired stance.
  Sensitivity at η=1.5: +$0.57T gross at the centre scenario.
- **D5 — debt stocks are exogenous and identical across scenarios** in the
  SFC ledger v1, so the interest decomposition is exact. Debt-stock feedback
  (fee receipts reducing later borrowing and hence interest) is excluded —
  conservative in direction, listed as a pending refinement.
- **D6 — fiscal years** are approximated by calendar years (federal FY is
  Oct–Sep; the one-quarter offset is ignored, as in the prototype).

## Accounting rules enforced by tests

- Cohort book ≤ eligible stock, always (no double-assessment of refinanced
  taxable principal; partition identity as in audit §5.1).
- Settlement flows sum to zero across sectors; a fee collection moves
  reserves → TGA and Treasury spending reverses it. **The temporary reserve
  drain is never counted as revenue** — revenue is the fee transfer itself,
  once.
- Consolidated net interest = interest on **public-held** debt + IORB
  expense + Fed opex − Fed MBS income. Interest on Fed-held Treasuries is
  internal and nets against Fed asset income — shown in the gross view,
  excluded from the consolidated view, with the identity
  `consolidated == gross_interest_all_debt − fed_net_income` tested yearly.
- Treasury repricing is an explicit maturity schedule (18%/yr of the public
  stock reprices at the new-issue yield). **The CBO $379B/0.1 pp sensitivity
  is not used** except as a comparison line in RESULTS_V1.md.
- Fed remittances follow the real deferred-asset mechanism (post-Sep-2022
  practice): negative income → remittances stop, deferred asset accrues;
  positive income pays the asset down before any cash is remitted.

## Honesty box

The IORB baseline path, all behavioural elasticities, the yield-transmission
coefficient (0.32), the 13% haircut, and the public-debt path are
**placeholders** (see `data_manifest.md`). The score is a transparent
sensitivity calculation on sourced starting stocks — the same epistemic
status the audit assigned to the prototype's fee line — with the
prototype's consolidated-accounting defects (CBO plug-in, gross-of-Fed-held
interest, instant repricing claw-back, vacuous tests) removed. It is not a
CBO score, not an FRB/US result, and not evidence about where the Fed would
set the dial.
