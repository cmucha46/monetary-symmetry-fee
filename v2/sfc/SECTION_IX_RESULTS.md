# Section IX Results — The Interest-Income Channel, Tested

**Status: qualitative-quantitative SFC experiment.** One period, first-round demand effects only, computed on the Godley-Lavoie accounting core in this directory (`behavior.py`). This is **not a forecasting model** and its magnitudes are **not FRB/US-comparable estimates**; they measure the sign, the channel decomposition, and the approximate scale of the Section IX mechanism relative to the interest flows it reroutes. Full grid output: `section_ix_results.csv` (243 regime pairs; every pair closes under the full stock-flow identities).

## Sponsor amendment recorded (Nov 22, 2026)

The fee base is **not** the memo's loan-only base. By sponsor decision, **bonds are included, grandfathered identically to loans**: the fee is paid by lenders on covered loans and by **borrowing issuers** on covered bonds — nonfinancial businesses on post-effective-date bond issuance, state & local governments on theirs. Coverage follows the borrower's obligation through sale or securitization; each obligation is taxed exactly once (no separate charge on MBS or intermediary funding instruments). At the illustrative synchronized rates (f = 2%), the fee take of +200B splits: banks +80B, nonbanks +30B, NFC issuers +56B, SLG issuers +34B. The household creditor/debtor split is unchanged by the amendment.

## The comparison

Regime A (conventional): IORB 4%, no fee. Regime B (synchronized): IORB 2%, fee 2% — **equal combined policy-sensitive charge of 4%**. Covered-loan rate in B is spread + IORB + theta x fee. Both regimes run through the identical builder on the identical opening balance sheet; consumption intercepts are calibrated so Regime A reproduces baseline consumption at every grid point, so every reported difference is behavioural, not accounting.

The **net demand impulse** is Regime B minus Regime A first-round demand: household consumption (both groups) + federal purchases + loan-financed spending (change in new covered lending). It is expressed in $B and as a % of the **interest-flow magnitude** — Regime A's total loan interest paid by private borrowers (+1,045B on the illustrative stocks). A **negative** impulse means the fee regime is the more contractionary / disinflationary one at equal borrower charge — the Section IX hypothesis.

## Headline result by recycling scenario (81 grid points each)

| Recycling of fee revenue | Impulse negative at | Range (% of interest flows) | Median |
|---|---|---|---|
| (a) Deficit reduction (receipts not spent) | 32/81 grid points | -4.6% to +6.2% | +0.8% |
| (b) Lump-sum transfers to debtor households | 0/81 grid points | +6.2% to +25.3% | +14.9% |
| (c) Government purchases | 0/81 grid points | +14.5% to +25.3% | +20.0% |

Composition matters more than the deficit row's total: under deficit recycling, **all 27 grid points at full pass-through (theta = 1) are in the negative set**, while the positive points concentrate at theta < 1, where the comparison is no longer at equal borrower cost. See the flip analysis below.

## Channel decomposition at the central grid point

Central point: deposit beta 0.55, pass-through theta = 1.0, creditor MPC 0.125, debtor MPC 0.75, deficit recycling. $B, Regime B minus Regime A.

| Channel | $B | Mechanism |
|---|---|---|
| Creditor interest income | -12 | Deposit rate halves with IORB (beta < 1); creditors lose interest receipts and cut spending at MPC 0.05-0.20 |
| Creditor dividends | -1 | Banks recapture part of the halving as deposit spread, but nonbank fee costs and NFC issuer fees cut payouts by more at the central point |
| Debtor cash flow | -17 | At theta = 1 the loan side is exactly neutral; debtors still lose the deposit interest on their own small deposit holdings when IORB halves |
| Credit volume | +0 | Zero at theta = 1 by construction (equal all-in rate) |
| **Net demand impulse** | **-30** | **-2.9% of interest flows** |

Under transfers recycling at the same grid point the impulse is +120B (+11.5%); under purchases, +170B (+16.2%). The recycling term is larger than every monetary channel combined, in both cases.

## Where it flips: pass-through under deficit recycling

| theta (fee pass-through) | Impulse negative at | Min | Median | Max |
|---|---|---|---|---|
| 0.50 | 0/27 | +3.1% | +4.5% | +6.2% |
| 0.75 | 5/27 | -0.5% | +0.8% | +2.0% |
| 1.00 | 27/27 | -4.6% | -3.0% | -1.4% |

Read this table carefully — it contains two different experiments. At **theta = 1** the comparison is the clean Section IX test (equal all-in borrower cost), and the impulse is negative at **27 of 27** grid points. At **theta < 1** the regimes no longer impose equal borrower cost: the un-passed share of the fee makes loans cheaper in Regime B, so a *price* channel (cheaper credit, more borrowing) enters alongside the *income* channel Section IX is about. The next table separates them by switching the credit-volume response (eps) off and on:

| eps (credit-volume semi-elasticity, ASSUMED) | theta | Impulse negative at | Median |
|---|---|---|---|
| 0.00 | 0.50 | 18/27 | -0.7% |
| 0.00 | 0.75 | 27/27 | -1.8% |
| 0.00 | 1.00 | 27/27 | -3.0% |
| 0.03 | 0.50 | 0/27 | +4.5% |
| 0.03 | 0.75 | 5/27 | +0.8% |
| 0.03 | 1.00 | 27/27 | -3.0% |
| 0.06 | 0.50 | 0/27 | +9.6% |
| 0.06 | 0.75 | 0/27 | +3.4% |
| 0.06 | 1.00 | 27/27 | -3.0% |

With the volume response switched **off** (eps = 0), the pure income-redistribution channels favor the hypothesis at every theta — medians -0.7% (theta = 0.5), -1.8% (theta = 0.75), -3.0% (theta = 1) of interest flows. The flips at theta < 1 in the headline grid are produced by the **assumed** credit-volume elasticity acting on a borrower-cost gap that only exists because pass-through is incomplete. That is a real policy finding — incomplete pass-through breaks cost equivalence, and the Fed would have to run a higher IORB (and hence a higher fee) to restore equal restraint — but it is a finding about equivalence (memo Questions 4-5), not a refutation of the Section IX income mechanism. Note also that theta = 1 is the configuration the levy literature (LITERATURE.md section 2) finds most likely at fee scale, since absorption of a 200 bp charge is arithmetically impossible for the average bank.

## Sensitivities at the central grid point (deficit recycling)

| Variant | Impulse ($B) | % of interest flows |
|---|---|---|
| Headline (grd book locked, coupons unrepriced, eps=0.03, salience=1) | -30 | -2.9% |
| Grandfathered book reprices with IORB (all-adjustable sensitivity) | +79 | +7.6% |
| Covered bond coupons reprice down by f (issuer cost fully offset) | -34 | -3.2% |
| Interest-income salience 0.75 (Lit. 1.4 grid) | -27 | -2.6% |
| Interest-income salience 0.50 (Lit. 1.4 grid) | -24 | -2.3% |

The grandfathered-repricing sensitivity is the dangerous one: if the pre-enactment book repriced down with IORB (an all-adjustable world), debtors would receive a cash-flow windfall on the $13T grandfathered stock at MPC 0.50-1.00 and the impulse reverses sign outright. The headline treatment (book locked) rests on the evidence that ~92% of US mortgages are fixed-rate (LITERATURE.md section 1.3) — the hypothesis is, in part, a bet on the US fixed-rate mortgage stock.

## Verdict

**The hypothesis survives — conditionally, and smaller than its framing suggests.**

1. **The income mechanism itself has the predicted sign.** At equal borrower cost (theta = 1) with receipts banked (deficit recycling), the fee regime is more contractionary at **27 of 27** grid points, median -3.0% of the interest flows rerouted, and the decomposition shows the named mechanism at work: the removed receipt belonged to low-MPC creditors. With the credit-volume response switched off, the income channels favor the hypothesis at every theta (medians -0.7% / -1.8% / -3.0%). But the size is **small** — single-digit percentages of the flows rerouted — because of two leaks: banks recapture roughly (1 - beta) of the IORB halving as deposit spread and pay part of it back to the same creditors as dividends; and part of the measured contraction is debtors losing deposit interest on their own small balances, which is not the hypothesized channel at all.
2. **Incomplete pass-through flips the headline comparison — through the price channel, not the income channel.** At theta < 1 the fee regime is genuinely cheaper credit, and with the (assumed) credit-volume elasticity switched on the impulse turns positive (theta = 0.5: positive at 27/27). This does not refute the Section IX mechanism; it shows the equivalence premise failing. Restoring equal restraint would require a higher IORB path — a different experiment, and one that would also raise the fee take.
3. **Recycling dominates everything.** If Congress spends the receipts, the hypothesis flips at every grid point: transfers to debtor households give a positive impulse at 81/81 points (median +14.9% of interest flows), government purchases at 81/81 (median +20.0%). The fiscal recycling term is an order of magnitude larger than the monetary redistribution term. **The hypothesis is a property of the fee plus a congressional decision to bank the receipts — not of the fee alone.** A Congress that spends the proceeds on transfers or purchases should expect the package to be mildly *expansionary* relative to conventional tightening at the same borrower charge.
4. **The result is partly a bet on the fixed-rate stock.** If the grandfathered book repriced down with IORB (the all-adjustable sensitivity), debtors would receive a cash-flow windfall on the $13T pre-enactment stock at MPC 0.50-1.00 and even the theta = 1 / deficit-recycling impulse reverses (+7.6% of interest flows at the central point). The headline treatment rests on the US evidence that ~92% of mortgages are fixed-rate — sound for mortgages, weaker for the adjustable share of business credit inside the same book.

## What this experiment does not do (read before citing)

- **One period, first round only.** No multiplier, no second-round income effects, no dynamics, no expectations. Signs and channel rankings are the output; levels are illustrative magnitudes on illustrative stocks.
- **Treasury and security yields are held fixed across regimes** (the term-structure response tau is UNCALIBRATED — LITERATURE.md section 4.3 — and belongs to the FRB/US lane). Two switches relax pieces of this: covered-coupon repricing and grandfathered-book repricing (sensitivities above).
- **Pass-through at fee scale is UNCALIBRATED** (all levy estimates are for burdens <= ~45 bp; the synchronized fee is ~200 bp). Results are reported across the theta grid, never theta-averaged.
- **Assumed, not estimated:** dividend payout ratios (0.6/0.6/0.5), the credit-volume semi-elasticity (eps = 0.03 per pp; sensitivity-run at 0 and 0.06), the wage split between household groups, and SLG's financing response (SLG absorbs its issuer fee in its balance; no tax or spending response is modelled). SLG bond stocks are new to this extension — the skeleton carried no SLG debt — and are illustrative.
- **Fee deductibility is not modelled** (the memo does not specify it; LITERATURE.md section 2.3 flags it as a first-order open legislative parameter).
- Stocks are the skeleton's illustrative magnitudes, not Z.1-calibrated data; calibration is the cohort lane's job and will rescale dollar figures (though not the sign structure, which is driven by MPC and beta asymmetries).

## Files

- `behavior.py` — the extension (split households, amended fee base, behavioural rules, grid runner).
- `tests/test_section_ix.py` — accounting tests for the split and the amended base, plus behavioural sign tests.
- `section_ix_results.csv` — all 243 regime pairs with channel decompositions.
- Parameters: `../lit/LITERATURE.md` sections 1.2 (MPCs), 2.3 (theta grid), 4.1 (deposit betas), 1.4 (recycling as scenario fork).
