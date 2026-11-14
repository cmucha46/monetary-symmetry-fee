# Lane H — The Interest-Income / Reserve-Flow Channel FRB/US Omits

**Question.** Lane D/G found that in FRB/US a fee-split tightening delivers
only 36–61% of a conventional tightening's macro effect at equal all-in
borrower cost. Carlos objected (2026-11-13): *"That's insane to assume
conventional is more disinflationary — higher rates [mean] more net
interest payments injected into bank reserves; higher fees means more
bank reserves drained."*

This lane quantifies that objection instead of rebutting or endorsing
it. Code: `src/monetary_symmetry/flow_channel.py` (runner:
`python3 run_flow_channel.py`); data: `results/flow_channel_v1.csv`;
tests: `tests/test_flow_channel.py` (16 tests; full suite 50 passed).

**Method in one paragraph.** FRB/US has no reserves, no IORB, no bank
balance sheet and no government-interest-income flow among its 933
variables (Lane B), so the channel is measured where it can be: the
repo's stock-flow-consistent Treasury/Fed ledger (`sfc.py`) plus the
cohort fee model, at β = 0.88 on the central covered base
(`loans_plus_securitized`). Two scalings are kept strictly separate:
the **regime** (a permanent fee system operating at the baseline desired
stance, FY2027–36 — the fiscal module's own comparison) and the
**episode** (Lane G's +100 bp for 8 quarters). All regime figures are
deltas, fee scenario minus conventional, with the all-in borrower cost
held at the desired stance in both regimes by construction
(`policy.policy_for`).

---

## 1. The flow table — every dollar once, zero-sum

Three things happen to private-sector income when the conventional
regime is replaced by the fee regime at the same desired stance:

1. **The fee redirects creditor income to the Treasury.** Borrowers pay
   the same all-in policy-sensitive charge in both regimes (that is the
   regime definition). Of each borrower dollar, the share that used to
   be creditor net income is now remitted as the fee. Lenders' net loss
   on the lending channel is therefore *exactly* the net fee
   (gross fee × 0.87; the 13% haircut is a tax interaction attributed to
   lenders as lower income tax on smaller profits — Assumption A1,
   labelled, inherited from the fiscal module).
2. **The government pays less interest into the private sector.**
   Lower IORB → less interest on reserves paid to banks (**E_i**).
   Lower new-issue Treasury yields → less coupon income to public
   holders as the stock reprices at 18%/yr (**E_p**). This is the
   fiscal score's "consolidated interest saving" seen from the other
   side: *the government's saving is the private sector's lost
   injection, dollar for dollar* (identity, tested).
3. **Interest on Fed-held Treasuries falls too — and counts for
   nothing.** The Treasury pays the Fed less; the Fed earns less; the
   two cancel inside consolidated government (E_f, memo only, never
   added anywhere: $0.13T over 10 yr at s = 75%).

Sector net-income deltas (Treasury +E, Fed 0 on accrual — its income
gain is passed to Treasury as ultimate remittances, with the deferred
asset absorbing the improvement in *cash* first; banks/lenders −;
borrowers 0 by construction; other private −E_p) sum to zero in every
year and scenario (tested).

### 1a. Levels first: how big is the conventional injection?

Consolidated government→private net interest injection in the
conventional baseline (interest to public holders + IORB + Fed opex
− Fed MBS income):

| Year | Injection ($T/yr) | of which IORB to banks | of which coupons to public |
|---|---|---|---|
| 2027 | 1.162 | 0.120 | 1.084 |
| 2030 | 1.382 | 0.100 | 1.324 |
| 2033 | 1.520 | 0.094 | 1.469 |
| 2036 | 1.645 | 0.094 | 1.594 |

Carlos's direction is right and the aggregate flow is large — over a
trillion dollars a year. But note the composition: **the IORB-into-
reserves leg is the small part (~$0.09–0.12T/yr)**; coupons to public
holders are ~10× larger. What the fee regime removes is not the whole
injection but the slice driven by the *stance difference*: all of the
IORB difference (IORB falls a lot — to 0.88% at s = 75%) and only the
repricing slice of coupons, scaled by the placeholder yield
transmission τ = 0.32 (see §5 — this term is exactly linear in τ).

### 1b. Annual deltas by scenario ($T/yr; fee − conventional)

**s = 50%** (β = 0.88)

| Year | Gross fee | Net fee | E_i (IORB removed) | E_p (coupon removed) | Injection removed | Private income removed, variant (i) |
|---|---|---|---|---|---|---|
| 2029 | 0.213 | 0.185 | 0.032 | 0.024 | 0.056 | 0.241 |
| 2030 | 0.333 | 0.290 | 0.047 | 0.054 | 0.101 | 0.391 |
| 2033 | 0.509 | 0.443 | 0.044 | 0.122 | 0.166 | 0.609 |
| 2036 | 0.643 | 0.560 | 0.044 | 0.170 | 0.214 | 0.774 |
| **10-yr** | **3.730** | **3.245** | **0.348** | **0.848** | **1.196** | **4.442** |

**s = 75%** (β = 0.88) — centre case

| Year | Gross fee | Net fee | E_i | E_p | Injection removed | Private removed (i) |
|---|---|---|---|---|---|---|
| 2029 | 0.357 | 0.311 | 0.060 | 0.043 | 0.103 | 0.414 |
| 2030 | 0.504 | 0.439 | 0.072 | 0.088 | 0.160 | 0.599 |
| 2033 | 0.750 | 0.653 | 0.068 | 0.192 | 0.260 | 0.913 |
| 2036 | 0.941 | 0.819 | 0.068 | 0.265 | 0.333 | 1.152 |
| **10-yr** | **5.544** | **4.823** | **0.547** | **1.341** | **1.888** | **6.711** |

**s = 90%** (β = 0.88)

| Year | Gross fee | Net fee | E_i | E_p | Injection removed | Private removed (i) |
|---|---|---|---|---|---|---|
| 2029 | 0.463 | 0.403 | 0.084 | 0.059 | 0.143 | 0.546 |
| 2030 | 0.609 | 0.530 | 0.088 | 0.113 | 0.201 | 0.731 |
| 2033 | 0.891 | 0.775 | 0.083 | 0.238 | 0.321 | 1.096 |
| 2036 | 1.112 | 0.968 | 0.083 | 0.327 | 0.410 | 1.378 |
| **10-yr** | **6.625** | **5.764** | **0.680** | **1.674** | **2.354** | **8.118** |

(Full annual series for all years in `results/flow_channel_v1.csv`,
including the sector table, the Fed-held memo, and cash remittance /
deferred-asset timing. 2027 is zero throughout — no fee in force;
2028 is the introductory year, ~$0.02T.)

Three observations:

- **The 10-year variant-(i) private income removed is exactly the
  fiscal score's combined total** ($4.44T / $6.71T / $8.12T). That is
  not a coincidence or a second result: a fiscal "benefit" scored as
  deficit reduction *is* private income withdrawn. The $6T debate and
  the potency debate are the same dollars.
- **Cash ≠ accrual at the Fed.** At s = 75% the Fed's accrual position
  improves from 2029, but cash remittances to Treasury are unchanged in
  2029 (delta $0.000) because the improvement first pays down the
  deferred asset (baseline $0.094T vs scenario $0.034T at end-2029);
  scenario remittances resume a year earlier than baseline and run
  +$0.05–0.10T/yr higher thereafter. Anyone timing the "injection" in
  cash will misdate it by ~a year.
- **Variant (iii), TGA accumulation, is timing only.** A collected,
  unspent fee drains reserves into the TGA one-for-one; spending
  reverses it (tested in `sfc.settlement_flows`). And in the
  ample-reserves floor system the Fed supplies reserves elastically at
  IORB — a settlement drain does not mechanically tighten bank
  lending, as it would have in the pre-2008 corridor system. The
  demand-relevant object is the *income* flow above, not the reserve
  stock. This qualifies the reserve-drain half of the critique while
  leaving the income half intact — and the income half is the bigger
  number anyway.

### 1c. Treasury's use decides what the fee flow means (variants)

- **(i) Deficit reduction / reduced issuance** (the fiscal score's
  assumption): §2's demand translation applies as stated.
- **(ii) Spent on Medicare for America benefits:** the net fee returns
  to private recipients — providers and beneficiary households — with
  (labelled) MPC 0.60–0.90 instead of creditors' 0.10–0.40. The fee
  term flips from a withdrawal to a *redistribution gain*; only
  E_i + E_p remain removed. See §2.
- **(iii) TGA:** no demand term (above).

---

## 2. Demand translation — ranges, not a point claim

Labelled assumptions (in code): MPC of interest/creditor-income
recipients **0.10–0.40**; healthcare recipients under (ii)
**0.60–0.90**; simple multiplier **1.0–1.5** on top of first-round MPC
effects (the top of every range therefore stacks the highest MPC with
the highest multiplier — read tops as bounds, not centrals); foreign
holders (~30% of public Treasuries, anchored approximation) excluded
from the coupon term's US demand effect. GDP: $30.9T in
...[truncated 8180 chars]