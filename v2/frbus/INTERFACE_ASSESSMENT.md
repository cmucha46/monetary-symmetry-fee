# FRB/US Interface Assessment — Monetary Symmetry Fee v2

**Project:** Monetary Symmetry Fee v2 (memo of 2026-11-22) · **Date:** 2026-11-22 · **Lane:** FRB/US interface assessment
**Scope:** precisely how the v2 Federal Credit Fee (permanent 50/50, f = IORB after a ≤24-month transition, initial fee 0.15%) can and cannot be represented in FRB/US. Builds on v1 Lane B (`upstream/TOOLING_VERIFICATION.md` §5–6), Lane D discipline (as recorded in `validation/VALIDATION_AND_WEDGE_POC.md`), and Lane G (`integration/FRBUS_SCENARIOS.md`). Nothing from v1 is re-derived except where v2 changes the question or v1 was incomplete — two such cases are flagged in §1.1 and §2.2.

**Environment (verified this session, same as v1):**

| Item | Value |
|---|---|
| Working solver | PolicyEngine `frbus` 0.1.0, venv `upstream/us-frb-model/.venv`, Python 3.12.3 |
| Cross-check solver | Official PyFRB/US **1.1.1** (`upstream/official/`), public domain |
| Equations | Official `model.xml`, SHA-256 `3227f4d2a1d48d6c59e055b11c719a2c40f29e2dfd5094601ec16c24fdd4f24b` — byte-identical in both packages |
| Data | Official Oct 2026 LONGBASE, SHA-256 `c023c739f4179a70ca0ede84996539f8d2bf72170b9cc301afc89b95d2271a9e` |
| Model size | 933 variables; 284 endogenous. All equations quoted below are verbatim from this `model.xml` |

**Bottom line.** The fee enters FRB/US in exactly three places, all imposed from outside: (1) a **level wedge** on the three private lending rates the model actually carries — `rme`, `rcar`, `rbbb` — scaled by pass-through β and by a cohort-supplied covered share κ_t; (2) a **receipts path** added to the fiscal residual `ugfsrp` under the non-recycling closure `dfpex=1, dfpdbt=0, dfpsrp=0` (re-confirmed against this `model.xml`, §2.1); (3) **nothing else** — the lower funds path should be *found by the model's own rule*, not imposed (§3), and the in-model Treasury interest saving then arises endogenously through `rgw → rgfint → gfintn`. Everything balance-sheet — reserves, IORB expense, remittances, cohorts, pass-through, offshore substitution, and the distributional interest-income channel that is the memo's §IX hypothesis — is outside the model and must be carried by the SFC/cohort layer (§4). A smoke test of the recommended design (endogenous `rff` + constant wedge) was run this session and solves; results in §5.

---

## 1. Where borrowing costs are set, and where the wedge enters

FRB/US has no bank, loan-stock, or lending-spread sector (v1, verified by name search over all 933 names). What it has is a small set of *price-of-credit* variables. The complete wedge-entry map:

### 1.1 The map

| Credit category | Rate variable | Equation (verbatim, condensed) | Wedge entry | Downstream demand channel |
|---|---|---|---|---|
| **Mortgages** | `rme` — interest rate on conventional mortgages [Behavioral] | Δ`rme` = y₁ + y₂·Δ`rg10` + y₃·d87·Δ`rg10` + y₄·(`rg10`₋₁ − `rme`₋₁) + y₅·d87·(`rg10`₋₁ − `rme`₋₁) | Exogenise `rme` at baseline level + wedge_t | `eh` (residential investment, responds to lagged Δ`rme`); `rcch` (housing cost of capital, uses `rme` level) |
| **Consumer (auto proxy)** | `rcar` — new car loan rate at finance companies [Behavioral] | `rcar` = y₁ + y₂·d79a + y₃·(1−d79a)·t47 + **0.6967·`rcar`₋₁** + y₅·`rg5` + y₆·`rg5`₋₁ | Exogenise `rcar` at baseline level + wedge_t | `rccd` (identity, below) → `qecd` (durables target, log `rccd`) |
| **Consumer durables cost of capital** | `rccd` [Identity] | `rccd` = max(100·jrcd + `rcar` − zpi5, 0.01) | **Never wedge directly** — inherits the full `rcar` wedge by identity (v1 Lane D rule; re-verified in §5 smoke test: +0.50 on `rcar` ⇒ +0.517 mean on `rccd`) | `qecd` |
| **Business / corporate bonds** | `rbbb` — S&P BBB corporate bond rate [Identity] | `rbbb` = `rbbbp` + `rg10`; `rbbbp` [Behavioral premium] = AR around y₁ + y₂·zgap10 | Exogenise `rbbb` at baseline level + wedge_t (equivalently: shift the `rbbbp` path; do **not** wedge `rg10`) | `rbfi` = 0.5·(7.2 + (1−trfcim)·(`rg5` + `rbbb` − `rg10`) − zpib5) + 0.5·`req` → `rtbfi`/`rtinv` (business investment). Note the leverage: a 1pp `rbbb` wedge enters `rbfi` at 0.5·(1−trfcim), and a *fall* in `rg10` widens the (`rbbb`−`rg10`) spread term, amplifying it |
| **Treasury curve (NOT covered)** | `rg5`, `rg10`, `rg30` [Identities] | `rgX` = `zrffX` (expected-funds VAR) + `rgXp` (term premium) | **Never wedge.** These must stay endogenous so the lower `rff` path transmits into yields — that transmission *is* the in-model interest-saving channel (§2.3) | `rgw` (federal borrowing rate), `req` = `rg30` − zpic30 + `reqp` (equity cost), `rcch`, housing |
| **Policy rate** | `rff` [Behavioral] | `rff` = max(`rffrule`, `rffmin`); rule block in §3 | Not wedged; endogenous in the recommended design (§3) | Everything via `zrff*`, `rtb` |

> **Correction to v1 (flagged, not silent).** v1's name search concluded FRB/US has "no mortgage variable" because no variable *name* contains `mort`. That is wrong in substance: **`rme` is the conventional mortgage rate** (its *definition* says so; the name is an abbreviation). Lane G accordingly wedged only `rcar`/`rbbb`, leaving the single largest covered category — mortgages — to move only through `rg10`. Under a fee regime `rg10` *falls* (lower `rff`), so the v1 setup implicitly *cut* mortgage rates while raising auto and corporate rates. **v2 must wedge `rme` as a first-class entry** (done in the §5 smoke test; it exogenises cleanly). The v1 non-equivalence factors (0.61/0.46/0.36 at s = 50/75/90%) are therefore, if anything, *overstated* for a mortgage-inclusive fee — one more reason they must not be carried into v2 as results.

### 1.2 How the wedge is imposed (implementation discipline, from v1 Lane D, still binding)

- **Exogenised level paths, never constant `*_aerr`.** `rcar`'s own-lag coefficient is 0.6967 and `rme`'s equation is in differences with an error-correction term; a constant add-factor on either compounds (Lane D measured a ~3× ramp on `rcar` by quarter 8). The correct procedure, used by Lane G and by §5: solve a baseline, then exogenise the rate at *baseline level + wedge_t* for every quarter of the solve.
- **One wedge per rate, one rate per category.** Never wedge both `rcar` and `rccd`, nor both `rbbbp`/`rbbb` and `rg10` — each pair double-counts by identity.
- **Two model instances** if any run exogenises `rff` (v1 method): baselines from the two instances agree exactly, so deviations are comparable. In the recommended v2 design (§3) `rff` is never exogenised and one instance suffices.

### 1.3 Scaling the wedge: pass-through × covered share (the phase-in)

The imposed wedge on category *c* in quarter *t* is

```
wedge_{c,t} = β_c · f_t · κ_{c,t}
```

- `f_t` — the statutory fee rate path: 0.15% at enactment, rising to f = IORB by the synchronization date (≤ 24 months; scenario B vs C in the memo = early vs full-length transition). Supplied by the scenario builder; **nothing in FRB/US enforces f = i** — the 50/50 link is an input, always.
- `β_c` — pass-through of the fee into the category's new-loan rate. **Assumed, not estimated** (v1 central 0.88, sensitivity 0.70; nothing in FRB/US identifies it). Category-specific β is defensible (prime mortgages vs subprime consumer vs BBB credit will not pass through identically) but each added β is another uncalibrated parameter — report sensitivity, per memo §VII.
- `κ_{c,t}` — covered share of the *flow that the rate prices*. This is where grandfathering enters, and it is category-specific because `rcar`/`rme`/`rbbb` are **new-origination / new-issue rates**, not stock-average rates:
  - *Adjustable-rate and revolving credit* reprice on the outstanding stock almost immediately: κ → covered share of stock within a few quarters.
  - *New fixed-rate loans* bear the fee only as they are originated: κ_{c,t} = covered share of originations in category c — near the statutory coverage share from day one for the *rate*, even while the *stock* (and hence revenue) is still mostly grandfathered. **Do not conflate the two κ's**: the rate wedge keys off origination coverage; revenue (cohort model) keys off stock coverage. Using the stock share for the wedge would badly understate early transmission; using the origination share for revenue would overstate early collections.
  - *Refinancing waves* accelerate stock turnover (and revenue) when rates fall — an endogenous feedback the cohort model sees and FRB/US does not; κ paths must be precomputed per scenario, including the refi response to the scenario's own `rme` path. This circularity is handled by iteration between the cohort model and FRB/US, not inside either.
- **The memo §II.D design fork** (fixed-rate cohorts keep the origination-date fee vs. bear an adjustable fee absorbed by lenders): the first design is exactly the wedge above. The second puts part of the burden on lender margins — **FRB/US has no lender margin to squeeze**. Its only in-model shadow is a widening of spread variables (`rbbbp`, `reqp`) imposed as an assumption. If that design is simulated, the split of the fee between borrower-rate wedge and spread-widening must be stated as an external assumption, and the macro difference between the two designs will be understated by construction (the margin squeeze's credit-supply effects have no channel).

---

## 2. Fiscal routing: receipts in, no recycling, one ledger for interest

### 2.1 The closure — v1 settings re-confirmed against the installed model.xml

The fiscal rule lives in exactly one equation, `trpt` (trend average personal tax rate):

```
trpt = dfpex·trptx
     + dfpdbt·( trpt(-1) + y1·(debt/GDP − target) + y2·Δ(debt/GDP − target) )
     + dfpsrp·( trpt(-1) + y3·( (surplus/GDP) − (target + 0.0075·xgap2) ) )
```

With **`dfpex=1, dfpdbt=0, dfpsrp=0`, `trpt ≡ trptx`** (the exogenous trend rate): no debt feedback, no surplus feedback, so a receipts windfall is neither taxed away nor spent by the rule — it flows to the surplus and the debt stock. **The v1 settings are correct for pyfrbus 1.1.1 / this model.xml.** (The package demo default is `dfpsrp=1, dfpdbt=0` — the recycling configuration. Any run not explicitly setting all three switches is not a fee run.) The §5 smoke test set all three in both runs.

### 2.2 Where receipts must enter: `ugfsrp` — and a trap in the obvious alternative

The federal accounts in-model:

```
gfrecn  = tpn + tcin + ugfsrp·xgdpn                    (receipts, identity)
gfsrpn  = tpn + tcin − egfln − egfen − gtn − gfintn + ugfsrp·xgdpn   (surplus, identity)
gfdbtnp = ugfdbtp·( gfdbtnp(-1) − 0.25·gfsrpn )        (debt held by public)
gfintn  = rgfint · gfdbtn(-1)                          (net interest)
```

`ugfsrp` ("federal government budget surplus, residual") is the model's residual receipts/surplus ratio, and it is the **only clean entry point** for fee revenue: an imposed path `ugfsrp_t = ugfsrp_base,t + FeeReceipts_t / xgdpn_t` raises receipts *and* the surplus *and* reduces the debt path, consistently, in one move. Two implementation notes:

- `ugfsrp`'s own equation is mean-reverting (`ugfsrp = y₁(1−y₂) + y₂·ugfsrp(−1)`), so — same lesson as the rates — impose the **full path** (exogenise `ugfsrp`, or set a time-varying `ugfsrp_aerr` path), never a constant add-factor.
- **Trap (corrects a v1 Lane B suggestion):** adding the revenue to `gfrecn` via `gfrecn_aerr` is a *silent no-op* for everything that matters. Verified by name search of this model.xml: **no other equation consumes `gfrecn`** — it is a terminal reporting identity. Receipts entered there would appear in a receipts printout while the surplus, debt, and interest paths never move. Worse than recycling, because it looks like success. Do not use it. Entering via `tpn`/`tcin` add-factors is also wrong: those are income-tax accruals, and `trp`'s equation carries an output-gap term that would contaminate the experiment.

### 2.3 Interest savings and remittances — one ledger, chosen in advance

FRB/US *does* contain a federal interest block, and it is the in-model counterpart of the memo's Q3:

```
rgw    = y1·rtb + y2·rg5 + y3·rg10 + y4·rg30            (avg rate on NEW federal debt)
rgfint = AR pass-through of rgw into the avg rate on EXISTING debt
         (weights involve lagged rgfint, lagged rgw, and debt-stock growth —
          a crude one-parameter maturity/rollover proxy, not a maturity structure)
gfintn = rgfint · gfdbtn(-1)
```

So if `rff` falls endogenously (§3), `rtb/rg5/rg10/rg30` fall, `rgw` falls, `rgfint` follows with a lag, and `gfintn` declines — **inside the model, consistently with the debt path that the `ugfsrp` receipts are simultaneously reducing**. That is the correct consolidated in-model fiscal statement: Δ`gfsrpn` and the `gfdbtnp` path, baseline vs fee run.

What is **not** in the model: the Federal Reserve itself. There is no remittance variable, no IORB expense, no deferred asset (see §4). The v2 fiscal identity the memo demands —

```
Δ consolidated deficit = fee receipts + Δ Treasury interest (gfintn)
                       + Δ Fed remittances (lower IORB expense net of lower Fed earnings)
```

— therefore spans two ledgers, and the seam is exactly where double-counting will happen if it is not policed:

- **Rule:** if fee receipts are routed through `ugfsrp` and `gfintn` is taken from the model, then the SFC layer may add *only* the remittance term (computed from the cohort/SFC Fed balance sheet, driven by the model's `rff` path). It must not recompute Treasury interest from the `rff` path — that number already lives in `gfintn`.
- The `rgfint` rollover proxy is crude: it cannot distinguish a bills-heavy from a coupons-heavy maturity structure (memo §VI, Component 3 wants actual maturities). Where the SFC cohort model's maturity detail and `rgfint` disagree, report both and treat the difference as model uncertainty — do not average them silently.

---

## 3. The policy rule: let the model find the lower funds path

### 3.1 The rule block as installed

```
rffrule = dmpex·rfffix + dmprr·(real-rate rule) + dmptay·rfftay
        + dmptlr·rfftlr + dmpintay·rffintay + dmpalt·rffalt
rff     = max(rffrule, rffmin)        (plus threshold-rule variants via dmptrsh)
rffintay = ρ·rff(-1) + (1−ρ)·( rstar + π̄4 + y1·(π̄4 − pitarg) + y2·xgap2 )
```

**LONGBASE default (read from the data in the §5 smoke test): `dmpintay=1`, `dmptay=dmptlr=dmpalt=dmprr=dmpex=0`, `rffmin=0.125`** — i.e. the inertial Taylor rule is the active rule, responding to the 4-quarter average of core PCE inflation (`picxfe`), its gap to `pitarg`, and the output gap `xgap2`. The memo §V's requested Taylor variants are one-line data changes (`dmptay`/`dmptlr` switches, or `rfftlr`'s unemployment-gap form), and `stochsim` is available for the stochastic runs.

### 3.2 Two ways to run the fee — and which is defensible

**Design E (endogenous — recommended, and smoke-tested in §5).** Exogenise *only* the private rates (wedge paths from §1.3); leave `rff` to the rule. The rule then responds to the wedge's *consequences* — output and inflation gaps — not to the wedge itself. Any lower `rff` path is a model output: the Fed eases because the fee is doing measurable restraint work in the model's economy. This is the only design in which "the Fed can achieve the same mandate outcomes at roughly half the funds rate" is a *finding* rather than an assumption, and it is the design the memo's §V asks for ("the Fed's response must be endogenous… rather than instructing the simulated Fed to generate a particular amount of revenue").

**Design I (imposed — v1 Lane G).** Exogenise `rff` at an algebraically split path (Δrff = q/(1+βk)) alongside the wedge. Legitimate uses: exact accounting decompositions, equal-effect rescaling, and rff-path handoffs to the fiscal module. **Not defensible as evidence about the equilibrium rate path**: it assumes the split it purports to test, and with the rule switched off, any failure of the wedge to restrain demand shows up as unopposed inflation — an artefact of the design, not of the policy. v2 should use Design I only for decomposition exhibits, labelled as such.

**The honest limitation of Design E** (state it in every write-up): FRB/US's rule reacts to *outcomes with lags and inertia*; a real FOMC operating the v2 regime would react to the *combined stance* p = i + f directly. Design E therefore **understates** how far and how fast `rff` would fall, within any finite window (§5 quantifies this: a +0.50pp wedge bought only −0.06pp of mean `rff` offset inside the wedge window, −0.15pp at peak). A closer approximation — offered as a documented variant, not the default — is to feed the rule an effective-stance argument via a negative `rffintay_aerr` path equal to the wedge's estimated funds-equivalent. That variant reintroduces an assumed equivalence (β again) through the back door; if it is run, it must be bracketed by Design E (conservative) and labelled as assuming the transmission it measures. Reporting both bounds is the defensible presentation.

**Expectations.** All v1 runs and the §5 smoke test use the default VAR (backward-looking) expectations. Under model-consistent expectations (`mce="mcap"`, `"wp"`, `"mcap+wp"`, `"all"` — supported by the installed solver), an anticipated permanently-lower `rff` path moves `zrff10/zrff30` and hence the whole curve more strongly, enlarging the interest-saving channel and shrinking the measured non-equivalence. Regime-permanence questions (the memo's regimes B–E are *regimes*, not episodes) should be run under MCE as the headline and VAR as the robustness check — the reverse of v1's episode logic.

---

## 4. What FRB/US cannot represent — the explicit externally-assumed list

Per memo §VI ("if full integration cannot be achieved, report precisely which behavioral relationships remain externally assumed"). Each item below was verified against this `model.xml` / variable list, not asserted from the model's reputation.

1. **Reserves, IORB as such, TGA, settlement.** No reserve quantity, no administered-rate distinct from `rff`, no Treasury General Account, no ON RRP. The memo §III.A reserve drain — fee payment drains reserves, Treasury spending restores them — has *no in-model counterpart whatsoever*. `rff` is a single policy rate; "IORB" in any FRB/US run is a proxy label for `rff`, and the Fed's interest expense on reserves does not exist as a flow.
2. **Federal Reserve earnings, remittances, deferred asset.** No variables. The remittance term of the consolidated fiscal identity (§2.3) is 100% external (SFC layer), driven by the model's `rff`/yield paths.
3. **Lenders.** No bank or nonbank balance sheet, margin, funding cost, underwriting standard, or credit-supply function. Consequences: pass-through β is an input (§1.3); credit *rationing* (as opposed to credit *price*) cannot occur; the lender-borne adjustable-fee design (§1.3) has no channel; fee-induced changes in loan ownership/securitisation are invisible.
4. **Loan cohorts and the fee base.** No loan stocks by any category — hence no grandfathering, fixed/adjustable split, refi/prepay dynamics, or revenue base inside the model. All κ_t paths and all collections come from the cohort model (Component 3). FRB/US consumes their *price* implication only.
5. **The interest-income distribution — the memo §IX hypothesis itself.** FRB/US consumption is aggregate (with a durables/housing split); interest income enters national income in aggregate (`ynirn`, which does use `rbbb`). Who *receives* the policy-sensitive interest — depositors, bondholders, banks, foreigners — and their differing propensities to spend are not in the model. The fee's core claim (redirecting interest-type income from private creditors to Treasury reduces inflationary income feedback at equal credit restraint) can therefore be **bounded** in FRB/US (aggregate fiscal leg via `ugfsrp`, aggregate price legs via the wedge) but **not tested** in it. The test belongs to the SFC layer (sectoral balances with distinct household/creditor behaviour) and, if it is ever installed, a HANK cross-check. Any FRB/US-only claim to have confirmed or refuted §IX is overreach.
6. **Offshore and untaxed-credit substitution.** The foreign block prices trade and the exchange rate (which does respond to the rate path), but there is no cross-border *lending* margin and no shadow-credit sector. Substitution enters only as an exogenous haircut to κ_t, imposed by the scenario builder — a sensitivity dial, not a result.
7. **Treasury-market microstructure and debt-supply effects on term premia.** `rg5p/rg10p/rg30p` are behavioural AR-type equations driven by model gaps; a structurally lower debt path does not compress term premia in-model except through those gaps. Any debt-supply → term-premium effect must be imposed via `rg*p_aerr` paths and labelled an assumption.
8. **Mortgage-market detail.** `rme` keys off `rg10` alone: no agency-MBS spread, no GSE channel, no mortgage credit box. The wedge on `rme` is a spread over that single anchor.
9. **State & local governments as borrowers.** S&L appears as spending/employment trends (`egse`, `egsl`), not as a muni-borrowing sector whose costs move with the fee or the curve.
10. **The f = i synchronization constraint and the transition itself.** Nothing in the model links the fee to `rff`; the ≤24-month transition path of (i_t, f_t), the Board's independent adjustment during transition, and the mandatory terminal equality are all scenario inputs. Likewise the 0.15% initial fee is an input. FRB/US can evaluate *consequences* of a stated (i, f) path pair; it cannot validate the path's feasibility against the dual mandate except through Design E's outcome-based reaction (§3.2).

---

## 5. Smoke test (actually run this session)

**Script:** `v2/frbus/smoke_test.py` · **Output:** `v2/frbus/smoke_test_deviations.csv` · **Solver:** PolicyEngine `frbus` 0.1.0, official Oct 2026 LONGBASE + official `model.xml` (hashes in header). **Window:** 2027Q1–2031Q4 (20 quarters). **Closure in both runs:** `dfpex=1, dfpdbt=0, dfpsrp=0`.

**Design.** Baseline: nothing exogenised — `rff` set entirely by the LONGBASE-default inertial Taylor rule (confirmed from data: `dmpintay=1`, all other rule switches 0, `rffmin=0.125`). Wedge run: `rcar`, `rbbb`, **`rme`** exogenised at baseline level **+0.50pp for 2027Q1–2028Q4** (8 quarters), baseline level thereafter; `rff` left endogenous; **no fee revenue fed in** (`ugfsrp` untouched) — this tests the credit-pricing leg and the rule's response only.

**Outcome: both solves converge** (baseline 2.1 s, wedge 3.7 s wall including load). Deviations of the wedge run from baseline:

| Measure | Value |
|---|---|
| `rff` deviation, mean over the 8 wedge quarters | **−0.056 pp** |
| `rff` deviation, peak (2029Q2) | **−0.147 pp** |
| `xgdp` trough (2029Q1) | −0.264 % |
| `lur` peak (2029Q1) | +0.130 pp |
| `picxfe` minimum (window-censored, 2031Q2) | −0.007 pp |
| `rg10` deviation, mean over wedge quarters | −0.020 pp |
| `rccd` deviation, mean over wedge quarters | +0.517 pp (identity inheritance from `rcar`, as designed) |

**Reading.** The design works mechanically exactly as §3.2 predicts: the wedge restrains demand (output trough −0.26%, unemployment +0.13pp), and the model's rule *does* find a lower funds path on its own — but only a partial, lagged offset (≈11% of the wedge contemporaneously on average, ≈29% at peak, and still growing after the wedge ends, because the rule is inertial and reacts to realised slack). Two cautions against misreading this as "the" answer: (i) it is the *outcome-reactive* bound — a stance-targeting FOMC would offset more, sooner (§3.2); (ii) a 0.50pp/8-quarter wedge on three rates is a probe, not a v2 regime — no revenue, no κ phase-in, no permanence, VAR expectations. Its purpose was to prove the interface, and it does: endogenous-`rff` + multi-rate wedge (including `rme`, never before exogenised in this project) solves cleanly and produces the qualitatively required sign pattern on every margin.

**Errors/failures:** none in the solves. One diagnostic dead end, reported for completeness: the `y_*` equation coefficients are not exposed as data columns by `load_data` in this package version, so coefficient values other than Lane D's verified `rcar` own-lag (0.6967) are cited structurally, not numerically, in §1.

---

## 6. Recommended v2 run protocol (summary for the integration lane)

1. Solver: PolicyEngine `frbus` 0.1.0; official 1.1.1 for spot cross-checks on identical files. Pin the Oct 2026 LONGBASE + `model.xml` hashes above.
2. Every run: `dfpex=1, dfpdbt=0, dfpsrp=0`, set explicitly, baseline included.
3. Wedges: exogenised **level** paths on `rme`, `rcar`, `rbbb` only; wedge_{c,t} = β_c·f_t·κ_{c,t} with κ from the cohort model (origination-coverage for rates). Never wedge `rccd`, `rbbbp` separately, or any `rg*`.
4. Receipts: imposed `ugfsrp` path = baseline + receipts/xgdpn. Never `gfrecn`. Fiscal results read from Δ`gfsrpn` / `gfdbtnp` / `gfintn`; remittance term added once, in the SFC layer only.
5. Policy: Design E (endogenous `rff`, LONGBASE inertial-Taylor default; `dmptay`/`dmptlr` variants as sensitivity) as headline; Design I (imposed split) only for labelled decompositions; stance-targeting variant (§3.2) as the upper bound on the `rff` offset.
6. Expectations: MCE (`mcap+wp`) headline for permanent-regime questions, VAR as robustness — reversed from v1's episode practice, deliberately.
7. Regimes B–E (memo §VII) differ only in the (i_t, f_t, κ_t, receipts_t) input paths and the shock set; the interface above is regime-invariant.
