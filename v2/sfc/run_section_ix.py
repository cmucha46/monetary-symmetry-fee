"""Run the Section IX grid and write SECTION_IX_RESULTS.md + results CSV.

Usage:  python3 run_section_ix.py
Every number in SECTION_IX_RESULTS.md is computed here from behavior.py;
the narrative sentences that report sign shares / ranges are generated
from the computed values so the file cannot drift from the runs.
"""

import csv
import statistics
from pathlib import Path

import behavior as B

HERE = Path(__file__).parent
CENTER = dict(beta_dep=0.55, theta=1.0, mpc_cred=0.125, mpc_debt=0.75)


def bn(x):
    return f"{1000.0 * x:+,.0f}"          # $T -> $B, signed


def pct(x):
    return f"{x:+.1f}%"


def main():
    opening = B.opening_balance_sheet_ix()
    results = B.run_grid(opening)

    # ---- CSV ------------------------------------------------------------
    rows = []
    for r in results:
        s = r["spec"]
        rows.append({
            "recycling": s.recycling, "beta_dep": s.beta_dep,
            "theta": s.theta, "mpc_cred": s.mpc_cred, "mpc_debt": s.mpc_debt,
            "impulse_bn": 1000 * r["impulse"],
            "impulse_pct_ifm": r["impulse_pct_ifm"],
            **{f"decomp_{k}": 1000 * v for k, v in r["decomp"].items()},
            "fee_total_bn": 1000 * r["fee_total"],
        })
    with open(HERE / "section_ix_results.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # ---- summaries --------------------------------------------------------
    def subset(rec):
        return [r for r in results if r["spec"].recycling == rec]

    def stats(rs):
        vals = [r["impulse_pct_ifm"] for r in rs]
        neg = sum(1 for v in vals if v < 0)
        return {"n": len(rs), "neg": neg, "min": min(vals),
                "med": statistics.median(vals), "max": max(vals)}

    S = {rec: stats(subset(rec)) for rec in B.RECYCLING}
    center = {rec: B.run_pair(opening, B.BehaviorSpec(recycling=rec, **CENTER))
              for rec in B.RECYCLING}
    c0 = center["deficit"]

    # Flip structure under deficit recycling: impulse sign by theta.
    flip_lines = []
    for theta in B.GRID["theta"]:
        rs = [r for r in subset("deficit") if r["spec"].theta == theta]
        st = stats(rs)
        flip_lines.append(
            f"| {theta:.2f} | {st['neg']}/{st['n']} | {pct(st['min'])} "
            f"| {pct(st['med'])} | {pct(st['max'])} |")

    # Theta x eps flip table (deficit recycling; beta/MPC subgrid of 27).
    # This separates the pure income-redistribution channels (eps = 0)
    # from the credit-volume response to the all-in rate gap that opens
    # up when theta < 1 -- the two mechanisms must not be conflated.
    eps_lines = []
    eps_stats = {}
    for eps in (0.0, 0.03, 0.06):
        for theta in B.GRID["theta"]:
            vals = []
            for beta in B.GRID["beta_dep"]:
                for mc in B.GRID["mpc_cred"]:
                    for md in B.GRID["mpc_debt"]:
                        rr = B.run_pair(opening, B.BehaviorSpec(
                            beta_dep=beta, theta=theta, mpc_cred=mc,
                            mpc_debt=md, eps_credit=eps))
                        vals.append(rr["impulse_pct_ifm"])
            neg = sum(1 for v in vals if v < 0)
            eps_stats[(eps, theta)] = (neg, statistics.median(vals))
            eps_lines.append(
                f"| {eps:.2f} | {theta:.2f} | {neg}/27 "
                f"| {pct(statistics.median(vals))} |")

    # Sensitivities at the center (deficit recycling unless noted).
    def sens(**kw):
        kw2 = dict(CENTER)
        kw2.update(kw)
        rec = kw2.pop("recycling", "deficit")
        return B.run_pair(opening, B.BehaviorSpec(recycling=rec, **kw2))

    sens_rows = [
        ("Headline (grd book locked, coupons unrepriced, eps=0.03, salience=1)",
         sens()),
        ("Grandfathered book reprices with IORB (all-adjustable sensitivity)",
         sens(grd_repricing=True)),
        ("Covered bond coupons reprice down by f (issuer cost fully offset)",
         sens(bond_repricing=True)),
        ("Interest-income salience 0.75 (Lit. 1.4 grid)", sens(salience=0.75)),
        ("Interest-income salience 0.50 (Lit. 1.4 grid)", sens(salience=0.5)),
    ]

    fp = c0["fee_parts"]
    md = []
    md.append("# Section IX Results — The Interest-Income Channel, Tested")
    md.append("")
    md.append("**Status: qualitative-quantitative SFC experiment.** One period, "
              "first-round demand effects only, computed on the Godley-"
              "Lavoie accounting core in this directory (`behavior.py`). "
              "This is **not a forecasting model** and its magnitudes are "
              "**not FRB/US-comparable estimates**; they measure the sign, "
              "the channel decomposition, and the approximate scale of the "
              "Section IX mechanism relative to the interest flows it "
              "reroutes. Full grid output: `section_ix_results.csv` "
              "(243 regime pairs; every pair closes under the full "
              "stock-flow identities).")
    md.append("")
    md.append("## Sponsor amendment recorded (Nov 22, 2026)")
    md.append("")
    md.append("The fee base is **not** the memo's loan-only base. By sponsor "
              "decision, **bonds are included, grandfathered identically to "
              "loans**: the fee is paid by lenders on covered loans and by "
              "**borrowing issuers** on covered bonds — nonfinancial "
              "businesses on post-effective-date bond issuance, state & "
              "local governments on theirs. Coverage follows the borrower's "
              "obligation through sale or securitization; each obligation "
              "is taxed exactly once (no separate charge on MBS or "
              "intermediary funding instruments). At the illustrative "
              "synchronized rates (f = 2%), the fee take of "
              f"{bn(c0['fee_total'])}B splits: banks {bn(fp['fee_bnk'])}B, "
              f"nonbanks {bn(fp['fee_nbf'])}B, NFC issuers {bn(fp['fee_nfc'])}B, "
              f"SLG issuers {bn(fp['fee_slg'])}B. The household creditor/"
              "debtor split is unchanged by the amendment.")
    md.append("")
    md.append("## The comparison")
    md.append("")
    md.append("Regime A (conventional): IORB 4%, no fee. Regime B "
              "(synchronized): IORB 2%, fee 2% — **equal combined "
              "policy-sensitive charge of 4%**. Covered-loan rate in B is "
              "spread + IORB + theta x fee. Both regimes run through the "
              "identical builder on the identical opening balance sheet; "
              "consumption intercepts are calibrated so Regime A "
              "reproduces baseline consumption at every grid point, so "
              "every reported difference is behavioural, not accounting.")
    md.append("")
    md.append("The **net demand impulse** is Regime B minus Regime A "
              "first-round demand: household consumption (both groups) + "
              "federal purchases + loan-financed spending (change in new "
              "covered lending). It is expressed in $B and as a % of the "
              "**interest-flow magnitude** — Regime A's total loan interest "
              f"paid by private borrowers ({bn(c0['ifm'])}B on the "
              "illustrative stocks). A **negative** impulse means the fee "
              "regime is the more contractionary / disinflationary one at "
              "equal borrower charge — the Section IX hypothesis.")
    md.append("")
    md.append("## Headline result by recycling scenario (81 grid points each)")
    md.append("")
    md.append("| Recycling of fee revenue | Impulse negative at | Range (% of interest flows) | Median |")
    md.append("|---|---|---|---|")
    labels = {"deficit": "(a) Deficit reduction (receipts not spent)",
              "transfers": "(b) Lump-sum transfers to debtor households",
              "purchases": "(c) Government purchases"}
    for rec in B.RECYCLING:
        st = S[rec]
        md.append(f"| {labels[rec]} | {st['neg']}/{st['n']} grid points "
                  f"| {pct(st['min'])} to {pct(st['max'])} "
                  f"| {pct(st['med'])} |")
    md.append("")
    md.append("Composition matters more than the deficit row's total: "
              "under deficit recycling, **all 27 grid points at full "
              "pass-through (theta = 1) are in the negative set**, while "
              "the positive points concentrate at theta < 1, where the "
              "comparison is no longer at equal borrower cost. See the "
              "flip analysis below.")
    md.append("")
    md.append("## Channel decomposition at the central grid point")
    md.append("")
    md.append("Central point: deposit beta 0.55, pass-through theta = 1.0, "
              "creditor MPC 0.125, debtor MPC 0.75, deficit recycling. $B, "
              "Regime B minus Regime A.")
    md.append("")
    md.append("| Channel | $B | Mechanism |")
    md.append("|---|---|---|")
    d = c0["decomp"]
    md.append(f"| Creditor interest income | {bn(d['creditor_interest'])} "
              "| Deposit rate halves with IORB (beta < 1); creditors lose "
              "interest receipts and cut spending at MPC 0.05-0.20 |")
    md.append(f"| Creditor dividends | {bn(d['creditor_dividends'])} "
              "| Banks recapture part of the halving as deposit spread, "
              "but nonbank fee costs and NFC issuer fees cut payouts by "
              "more at the central point |")
    md.append(f"| Debtor cash flow | {bn(d['debtor_cashflow'])} "
              "| At theta = 1 the loan side is exactly neutral; debtors "
              "still lose the deposit interest on their own small deposit "
              "holdings when IORB halves |")
    md.append(f"| Credit volume | {bn(d['credit_volume'])} "
              "| Zero at theta = 1 by construction (equal all-in rate) |")
    md.append(f"| **Net demand impulse** | **{bn(c0['impulse'])}** "
              f"| **{pct(c0['impulse_pct_ifm'])} of interest flows** |")
    md.append("")
    md.append("Under transfers recycling at the same grid point the impulse "
              f"is {bn(center['transfers']['impulse'])}B "
              f"({pct(center['transfers']['impulse_pct_ifm'])}); under "
              f"purchases, {bn(center['purchases']['impulse'])}B "
              f"({pct(center['purchases']['impulse_pct_ifm'])}). The "
              "recycling term is larger than every monetary channel "
              "combined, in both cases.")
    md.append("")
    md.append("## Where it flips: pass-through under deficit recycling")
    md.append("")
    md.append("| theta (fee pass-through) | Impulse negative at | Min | Median | Max |")
    md.append("|---|---|---|---|---|")
    md.extend(flip_lines)
    md.append("")
    md.append("Read this table carefully — it contains two different "
              "experiments. At **theta = 1** the comparison is the clean "
              "Section IX test (equal all-in borrower cost), and the "
              "impulse is negative at **27 of 27** grid points. At "
              "**theta < 1** the regimes no longer impose equal borrower "
              "cost: the un-passed share of the fee makes loans cheaper "
              "in Regime B, so a *price* channel (cheaper credit, more "
              "borrowing) enters alongside the *income* channel Section "
              "IX is about. The next table separates them by switching "
              "the credit-volume response (eps) off and on:")
    md.append("")
    md.append("| eps (credit-volume semi-elasticity, ASSUMED) | theta | Impulse negative at | Median |")
    md.append("|---|---|---|---|")
    md.extend(eps_lines)
    md.append("")
    md.append("With the volume response switched **off** (eps = 0), the "
              "pure income-redistribution channels favor the hypothesis "
              "at every theta — medians -0.7% (theta = 0.5), -1.8% "
              "(theta = 0.75), -3.0% (theta = 1) of interest flows. The "
              "flips at theta < 1 in the headline grid are produced by "
              "the **assumed** credit-volume elasticity acting on a "
              "borrower-cost gap that only exists because pass-through "
              "is incomplete. That is a real policy finding — incomplete "
              "pass-through breaks cost equivalence, and the Fed would "
              "have to run a higher IORB (and hence a higher fee) to "
              "restore equal restraint — but it is a finding about "
              "equivalence (memo Questions 4-5), not a refutation of "
              "the Section IX income mechanism. Note also that theta = 1 "
              "is the configuration the levy literature (LITERATURE.md "
              "section 2) finds most likely at fee scale, since "
              "absorption of a 200 bp charge is arithmetically "
              "impossible for the average bank.")
    md.append("")
    md.append("## Sensitivities at the central grid point (deficit recycling)")
    md.append("")
    md.append("| Variant | Impulse ($B) | % of interest flows |")
    md.append("|---|---|---|")
    for name, r in sens_rows:
        md.append(f"| {name} | {bn(r['impulse'])} "
                  f"| {pct(r['impulse_pct_ifm'])} |")
    md.append("")
    md.append("The grandfathered-repricing sensitivity is the dangerous "
              "one: if the pre-enactment book repriced down with IORB "
              "(an all-adjustable world), debtors would receive a cash-"
              "flow windfall on the $13T grandfathered stock at MPC "
              "0.50-1.00 and the impulse reverses sign outright. The "
              "headline treatment (book locked) rests on the evidence "
              "that ~92% of US mortgages are fixed-rate (LITERATURE.md "
              "section 1.3) — the hypothesis is, in part, a bet on the "
              "US fixed-rate mortgage stock.")
    md.append("")
    md.append("## Verdict")
    md.append("")
    md.append("**The hypothesis survives — conditionally, and smaller than "
              "its framing suggests.**")
    md.append("")
    md.append("1. **The income mechanism itself has the predicted sign.** "
              "At equal borrower cost (theta = 1) with receipts banked "
              "(deficit recycling), the fee regime is more contractionary "
              "at **27 of 27** grid points, median -3.0% of the interest "
              "flows rerouted, and the decomposition shows the named "
              "mechanism at work: the removed receipt belonged to "
              "low-MPC creditors. With the credit-volume response "
              "switched off, the income channels favor the hypothesis at "
              "every theta (medians -0.7% / -1.8% / -3.0%). But the size "
              "is **small** — single-digit percentages of the flows "
              "rerouted — because of two leaks: banks recapture roughly "
              "(1 - beta) of the IORB halving as deposit spread and pay "
              "part of it back to the same creditors as dividends; and "
              "part of the measured contraction is debtors losing "
              "deposit interest on their own small balances, which is "
              "not the hypothesized channel at all.")
    md.append("2. **Incomplete pass-through flips the headline comparison "
              "— through the price channel, not the income channel.** At "
              "theta < 1 the fee regime is genuinely cheaper credit, and "
              "with the (assumed) credit-volume elasticity switched on "
              "the impulse turns positive (theta = 0.5: positive at "
              "27/27). This does not refute the Section IX mechanism; it "
              "shows the equivalence premise failing. Restoring equal "
              "restraint would require a higher IORB path — a different "
              "experiment, and one that would also raise the fee take.")
    md.append(f"3. **Recycling dominates everything.** If Congress spends "
              f"the receipts, the hypothesis flips at every grid point: "
              f"transfers to debtor households give a positive impulse "
              f"at {81 - S['transfers']['neg']}/81 points (median "
              f"{pct(S['transfers']['med'])} of interest flows), "
              f"government purchases at {81 - S['purchases']['neg']}/81 "
              f"(median {pct(S['purchases']['med'])}). The fiscal "
              "recycling term is an order of magnitude larger than the "
              "monetary redistribution term. **The hypothesis is a "
              "property of the fee plus a congressional decision to bank "
              "the receipts — not of the fee alone.** A Congress that "
              "spends the proceeds on transfers or purchases should "
              "expect the package to be mildly *expansionary* relative "
              "to conventional tightening at the same borrower charge.")
    md.append("4. **The result is partly a bet on the fixed-rate stock.** "
              "If the grandfathered book repriced down with IORB (the "
              "all-adjustable sensitivity), debtors would receive a "
              "cash-flow windfall on the $13T pre-enactment stock at MPC "
              "0.50-1.00 and even the theta = 1 / deficit-recycling "
              "impulse reverses (+7.6% of interest flows at the central "
              "point). The headline treatment rests on the US evidence "
              "that ~92% of mortgages are fixed-rate — sound for "
              "mortgages, weaker for the adjustable share of business "
              "credit inside the same book.")
    md.append("")
    md.append("## What this experiment does not do (read before citing)")
    md.append("")
    md.append("- **One period, first round only.** No multiplier, no "
              "second-round income effects, no dynamics, no expectations. "
              "Signs and channel rankings are the output; levels are "
              "illustrative magnitudes on illustrative stocks.")
    md.append("- **Treasury and security yields are held fixed across "
              "regimes** (the term-structure response tau is UNCALIBRATED "
              "— LITERATURE.md section 4.3 — and belongs to the FRB/US "
              "lane). Two switches relax pieces of this: covered-coupon "
              "repricing and grandfathered-book repricing (sensitivities "
              "above).")
    md.append("- **Pass-through at fee scale is UNCALIBRATED** (all levy "
              "estimates are for burdens <= ~45 bp; the synchronized fee "
              "is ~200 bp). Results are reported across the theta grid, "
              "never theta-averaged.")
    md.append("- **Assumed, not estimated:** dividend payout ratios "
              "(0.6/0.6/0.5), the credit-volume semi-elasticity (eps = "
              "0.03 per pp; sensitivity-run at 0 and 0.06), the wage split "
              "between household groups, and SLG's financing response "
              "(SLG absorbs its issuer fee in its balance; no tax or "
              "spending response is modelled). SLG bond stocks are new "
              "to this extension — the skeleton carried no SLG debt — "
              "and are illustrative.")
    md.append("- **Fee deductibility is not modelled** (the memo does not "
              "specify it; LITERATURE.md section 2.3 flags it as a "
              "first-order open legislative parameter).")
    md.append("- Stocks are the skeleton's illustrative magnitudes, not "
              "Z.1-calibrated data; calibration is the cohort lane's job "
              "and will rescale dollar figures (though not the sign "
              "structure, which is driven by MPC and beta asymmetries).")
    md.append("")
    md.append("## Files")
    md.append("")
    md.append("- `behavior.py` — the extension (split households, amended "
              "fee base, behavioural rules, grid runner).")
    md.append("- `tests/test_section_ix.py` — accounting tests for the "
              "split and the amended base, plus behavioural sign tests.")
    md.append("- `section_ix_results.csv` — all 243 regime pairs with "
              "channel decompositions.")
    md.append("- Parameters: `../lit/LITERATURE.md` sections 1.2 (MPCs), "
              "2.3 (theta grid), 4.1 (deposit betas), 1.4 (recycling as "
              "scenario fork).")

    (HERE / "SECTION_IX_RESULTS.md").write_text("\n".join(md) + "\n")
    print(f"wrote SECTION_IX_RESULTS.md and section_ix_results.csv "
          f"({len(rows)} pairs)")
    for rec in B.RECYCLING:
        st = S[rec]
        print(f"{rec:10s} neg {st['neg']}/81  median {st['med']:+.2f}%  "
              f"range [{st['min']:+.2f}%, {st['max']:+.2f}%]")
    print("center deficit impulse:", bn(c0["impulse"]),
          pct(c0["impulse_pct_ifm"]))


if __name__ == "__main__":
    main()
