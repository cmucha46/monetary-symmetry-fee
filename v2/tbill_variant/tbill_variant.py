"""
T-Bill Variant -- debt-maturity migration extension of the combined study.

SPONSOR'S DESIGN (final spec, Nov 22 2026): T-bills are excluded from
the debt-ceiling calculation and the ceiling is never raised again.
T-note and T-bond auctions are ON HOLD -- no refunding in kind:
maturing note/bond principal is refunded into bills, and all net new
borrowing (deficits) is bills. The bill complex is the EXISTING seven
standard tenors (4, 6, 8, 13, 17, 26, 52 weeks) on the current auction
schedule and issuance mix -- no designed ladder. Bracketed option:
52-week auctioned weekly instead of every 4 weeks (priced in
cadence_52wk(); immaterial to effective maturity, see the report).

WHAT THIS MODULE DOES
---------------------
Extends the combined study's consolidation (Lane 3/4 machinery in
../mfa_combined/, imported UNMODIFIED) with a time-varying maturity
structure:

* A bucket engine tracks end-of-year balances and average rates for
  the five MSPD buckets (bills / FRN / notes / TIPS / bonds) along a
  total marketable-debt path. With migrate=False it reproduces the
  current structure (fixed bucket shares; each bucket reprices at the
  skeleton's annual maturity fraction at its segment dy) -- the
  engine's own base, used so the variant INCREMENT is measured inside
  one engine. With migrate=True, maturing principal of every non-bill
  bucket is refunded into bills and all net new borrowing is bills;
  legacy survivors are never refinanced in kind, so their average
  rate stays at the legacy level (BASE_RATE in the skeleton's
  construct) until the principal matures out into bills.
* Segment rate treatment is the combined study's (Sponsor Correction
  #2): bills (and FRNs while alive -- floaters indexed to the 13-week
  bill rate) reprice at the administered path: dy_bill = -A_t +
  dspread_t, transmission 1 by arbitrage. Legacy long buckets under
  the CURRENT structure reprice at dy_long = -tau_long * A_t.
  A_t is the administered-path decline from the fiscal skeleton
  (0 before FY2030, 1.95pp from FY2030).
* The bill spread is the variant's price. dspread is the CHANGE in
  the bill-IORB spread vs the baseline spread embedded in the
  skeleton, scenario-driven by the bill share of the marketable
  stock (see spread_schedule). A break-even solver finds the constant
  dspread that exactly exhausts the variant's cumulative gain.
* Savings are the RATE effect only, consolidated (x PUBLIC_SHARE),
  exactly as in Lane 3/4: savings_t = (BASE_RATE - avg_rate_t) *
  avg_debt_t * PUBLIC_SHARE. The combined fixed point (savings <->
  combined debt path) is iterated as in Lane 3/4. Fee receipts, the
  FRB/US Regime C drag and delta remittances are taken from the
  combined study unchanged -- the variant touches only the debt
  structure, so the coverage restatement is: combined-study margin +
  variant interest increment. One ledger throughout.
* The TERM-PREMIUM channel is computed in a separate exhibit
  (term_premium_exhibit) and is NEVER added to any coverage margin:
  shortening saves the term premium with or without the fee.
* Regime D/E stress applies Lane B's FRB/US administered-rate
  deviation paths (annual FY averages of D_rff) to both structures on
  a common debt path. No new FRB/US solves: the debt-structure
  channel is a consolidation-layer object and the FRB/US paths are
  inputs, exactly as in the v2 final pass.

ASSUMED parameters are labeled inline and collected in ASSUMPTIONS.
No CBO figure is used as an input anywhere (guard-tested).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "mfa_combined"))
sys.path.insert(0, str(HERE.parent / "integration"))
sys.path.insert(0, str(HERE.parent / "cohort"))

import consolidation_combined as CC   # noqa: E402  Lane 3, unmodified
import consolidation_tau_maturity as CT  # noqa: E402  Lane 4, unmodified
from data import TREASURY             # noqa: E402

YEARS = CC.YEARS                       # 2027..2036
TAU_LONGS = CC.TAUS                    # (0, 0.25, 0.5, 0.75)
PUBLIC_SHARE = CC.PUBLIC_SHARE         # 0.8559
BASE_RATE = CC.BASE_RATE               # 0.0357
MARKETABLE_2026 = CC.MARKETABLE_2026   # 31,830

BUCKETS = ("bills", "frn", "notes", "tips", "bonds")
FRONT = ("bills", "frn")               # reprice at the bill rate
LEGACY = ("notes", "tips", "bonds")    # long stock; runs off under variant

# Repricing fractions (skeleton, cohort/data.py): the share of a bucket's
# balance refinanced at the new-issue rate each year under the CURRENT
# structure. For bills and FRNs this is 1.0 (bills mature <=1yr; FRNs are
# floaters resetting off the 13-week bill rate).
REPRICE_FRAC = dict(TREASURY["bucket_annual_maturity"])

# Principal MATURITY (runoff) fractions under the variant. Identical to
# REPRICE_FRAC for bills/notes/TIPS/bonds (the skeleton's fractions were
# calibrated as annual maturity shares reproducing the published 33%
# maturing <=1yr). FRN differs: repricing is continuous (1.0) but
# principal matures over the 2-year FRN life -> 0.5/yr ASSUMED.
MATURITY_FRAC = dict(REPRICE_FRAC)
MATURITY_FRAC["frn"] = 0.5             # ASSUMED (2-yr FRN, uniform ages)

INITIAL_BALANCES = dict(TREASURY["buckets_bn"])   # MSPD Sep 30 2026
BILL_SHARE_0 = INITIAL_BALANCES["bills"] / MARKETABLE_2026   # 0.2237

# Average remaining maturity per bucket (years), ASSUMED, calibrated so
# the balance-weighted mean at FY2026 reproduces the published WAM of
# 70 months: .2237*.17 + .0232*1.0 + .5114*4.6 + .0672*7.0 + .1744*16.5
# = 5.76yr = 69 months. Reporting metric only; not an input to savings.
BUCKET_AVG_MATURITY_YRS = {"bills": 0.17, "frn": 1.0, "notes": 4.6,
                           "tips": 7.0, "bonds": 16.5}

ASSUMPTIONS = {
    "frn_maturity_frac": "0.5/yr ASSUMED (2-yr FRN principal life; the "
                         "skeleton's 1.0 is a repricing fraction)",
    "bucket_avg_maturities": "ASSUMED, calibrated to reproduce WAM "
                             "70 months at FY2026 (reporting only)",
    "spread_schedule_form": "ASSUMED: linear in excess bill share, "
                            "dspread = S_inf * clip((share-share_0)/"
                            "(1-share_0),0,1); S_inf in {+25,+50,+100}bp",
    "migration_start": "FY2027 (variant enacted with the plan)",
    "term_premium_grid": "TP in {50, 100}bp ASSUMED scenario parameters "
                         "(exhibit only; never in coverage)",
    "baseline_spread_reference": "bill-IORB median -14bp (combined-study "
                                 "exhibit, 2008-2026) -- used only to "
                                 "express the break-even as a level",
}


# ---------------------------------------------------------------------------
# Spread schedule
# ---------------------------------------------------------------------------
def spread_schedule(share: float, s_inf_bp: float, gamma: float = 1.0) -> float:
    """Change in the bill-IORB spread (decimal) at a given bill share of
    the marketable stock. Zero at today's share by construction (the
    baseline spread is embedded in the skeleton's BASE_RATE construct);
    asymptotes to S_inf (bp) as the share -> 1. ASSUMED functional form."""
    x = (share - BILL_SHARE_0) / (1.0 - BILL_SHARE_0)
    x = min(1.0, max(0.0, x))
    return (s_inf_bp / 10000.0) * x ** gamma


# ---------------------------------------------------------------------------
# Bucket engine
# ---------------------------------------------------------------------------
def run_structure(avg_debt_by_year: dict[int, float],
                  end_debt_by_year: dict[int, float],
                  A: dict[int, float], tau_long: float,
                  migrate: bool,
                  s_inf_bp: float = 0.0, gamma: float = 1.0,
                  const_spread_pp: float | None = None) -> pd.DataFrame:
    """Run one maturity structure along a debt path.

    avg_debt_by_year / end_debt_by_year: total marketable debt ($B);
    end_debt_by_year must include 2026 = MARKETABLE_2026.
    A: administered decline by FY (decimal; negative = rates ABOVE the
    baseline path, as under the Regime D shock).
    migrate=False: current structure (fixed shares, segment repricing).
    migrate=True: note/bond/FRN/TIPS principal refunds into bills; all
    net new borrowing is bills; legacy survivors never reprice.
    s_inf_bp / gamma: spread schedule (variant only). const_spread_pp,
    if given, replaces the schedule with a constant dspread (pp) --
    used by the break-even solver.
    Returns annual: avg_rate, interest (gross + consolidated),
    savings (consolidated, rate effect only), bill stock/share, WAM.
    """
    # --- state -------------------------------------------------------------
    if migrate:
        bal = dict(INITIAL_BALANCES)               # end-of-year balances
        rates = {b: BASE_RATE for b in BUCKETS}
    else:
        shares = {b: INITIAL_BALANCES[b] / MARKETABLE_2026 for b in BUCKETS}
        rates = {b: BASE_RATE for b in BUCKETS}
    mat_age = dict(BUCKET_AVG_MATURITY_YRS)        # for WAM reporting
    rows = {}
    prev_end = MARKETABLE_2026
    for t in YEARS:
        avg_total = avg_debt_by_year[t]
        end_total = end_debt_by_year[t]
        dD = end_total - prev_end
        A_t = A.get(t, 0.0)
        if migrate:
            # maturing principal (on beginning balances)
            mat = {b: MATURITY_FRAC[b] * bal[b] for b in BUCKETS}
            end = {}
            end["bills"] = bal["bills"] + sum(mat[b] for b in BUCKETS
                                              if b != "bills") + dD
            for b in BUCKETS:
                if b != "bills":
                    end[b] = bal[b] - mat[b]
            avg_bal = {b: (bal[b] + end[b]) / 2.0 for b in BUCKETS}
            bill_share = avg_bal["bills"] / avg_total
            if const_spread_pp is not None:
                ds = const_spread_pp / 100.0
            else:
                ds = spread_schedule(bill_share, s_inf_bp, gamma)
            bill_rate = BASE_RATE - A_t + ds
            rates["bills"] = bill_rate             # full repricing
            rates["frn"] = bill_rate               # floater: bill index
            # legacy survivors keep their average rate (no refunding
            # in kind); their balances simply run off.
            interest = sum(rates[b] * avg_bal[b] for b in BUCKETS)
            bal = end
        else:
            avg_bal = {b: shares[b] * avg_total for b in BUCKETS}
            bill_share = shares["bills"]
            ds = 0.0
            dy = {b: (-A_t if b in FRONT else -tau_long * A_t)
                  for b in BUCKETS}
            interest = 0.0
            for b in BUCKETS:
                m = REPRICE_FRAC[b] * avg_bal[b]
                if avg_bal[b] > 0:
                    rates[b] = (rates[b] * (avg_bal[b] - m)
                                + (BASE_RATE + dy[b]) * m) / avg_bal[b]
                interest += rates[b] * avg_bal[b]
        avg_rate = interest / avg_total if avg_total > 0 else BASE_RATE
        # WAM (reporting): legacy buckets age 1yr/yr without new issuance
        if migrate:
            for b in LEGACY:
                mat_age[b] = max(0.25, mat_age[b] - 1.0)
            # bills/frn: continuous reissuance -> constant avg maturity;
            # frn ages while it runs off only if not reissued -- FRN
            # auctions are on hold, so surviving FRNs age too:
            mat_age["frn"] = max(0.25, mat_age["frn"] - 1.0)
        wam_yrs = sum(avg_bal[b] * mat_age[b] for b in BUCKETS) / avg_total
        rows[t] = {
            "avg_total_bn": avg_total,
            "avg_rate": avg_rate,
            "interest_gross_bn": interest,
            "interest_consol_bn": interest * PUBLIC_SHARE,
            "savings_consol_bn": (BASE_RATE - avg_rate) * avg_total
                                 * PUBLIC_SHARE,
            "bill_stock_bn": avg_bal["bills"] if migrate else
                             shares["bills"] * avg_total,
            "bill_share": (avg_bal["bills"] / avg_total) if migrate
                          else shares["bills"],
            "dspread_pp": ds * 100.0,
            "wam_months": wam_yrs * 12.0,
            **{f"bal_{b}_bn": avg_bal[b] for b in BUCKETS},
        }
        prev_end = end_total
    return pd.DataFrame.from_dict(rows, orient="index")


# ---------------------------------------------------------------------------
# Combined fixed point with a structure (Lane 3/4 iteration, generalized)
# ---------------------------------------------------------------------------
def _avg_end_from_path(D_path: dict[int, float]):
    avg, prev = {}, MARKETABLE_2026
    for t in YEARS:
        avg[t] = (prev + D_path[t]) / 2.0
        prev = D_path[t]
    end = dict(D_path); end[2026] = MARKETABLE_2026
    return avg, end


def combined_structure(tau_long: float, residual: pd.Series,
                       fees: pd.DataFrame, base_path: pd.DataFrame,
                       migrate: bool, s_inf_bp: float = 0.0,
                       gamma: float = 1.0,
                       const_spread_pp: float | None = None,
                       A: dict[int, float] | None = None,
                       tol: float = 0.05, max_iter: int = 100) -> dict:
    """Iterate savings <-> combined debt path to consistency, exactly as
    Lane 3/4 (D_t = baseline_t - cum(net fee flows - residual) -
    cum(savings)), with the structure engine supplying savings."""
    A = A if A is not None else CT.administered_decline()
    base_debt = {t: float(base_path.loc[t, "baseline_marketable_debt_bn"])
                 for t in YEARS}
    net_flow = {t: float(fees.loc[t, "net_receipts_bn"]
                         + fees.loc[t, "frbus_drag_bn"]
                         + fees.loc[t, "delta_remittances_bn"]
                         - residual.get(t, 0.0)) for t in YEARS}
    avg, end = _avg_end_from_path(base_debt)
    run = run_structure(avg, end, A, tau_long, migrate, s_inf_bp, gamma,
                        const_spread_pp)
    savings = run["savings_consol_bn"]
    iters = 0
    for iters in range(1, max_iter + 1):
        cum_net, cum_sav, D_path = 0.0, 0.0, {}
        for t in YEARS:
            cum_net += net_flow[t]
            cum_sav += float(savings[t])
            D_path[t] = base_debt[t] - cum_net - cum_sav
        avg, end = _avg_end_from_path(D_path)
        run = run_structure(avg, end, A, tau_long, migrate, s_inf_bp,
                            gamma, const_spread_pp)
        new = run["savings_consol_bn"]
        delta = float((new - savings).abs().max())
        savings = new
        if delta < tol:
            break
    cum_net, cum_sav, D_path = 0.0, 0.0, {}
    for t in YEARS:
        cum_net += net_flow[t]
        cum_sav += float(savings[t])
        D_path[t] = base_debt[t] - cum_net - cum_sav
    return {"run": run, "savings": savings, "debt_path": pd.Series(D_path),
            "iterations": iters}


def variant_gain(tau_long: float, scen: str, ctx: dict,
                 s_inf_bp: float = 0.0, gamma: float = 1.0,
                 const_spread_pp: float | None = None) -> dict:
    """Variant interest minus engine-base interest savings (each at its
    own combined fixed point), plus both levels. The INCREMENT is the
    engine-consistent object; coverage restatement adds it to Lane 4's
    published margins."""
    fees, residual = ctx["fees"], ctx["residuals"][scen]
    base = combined_structure(tau_long, residual, fees, ctx["base_path"],
                              migrate=False)
    var = combined_structure(tau_long, residual, fees, ctx["base_path"],
                             migrate=True, s_inf_bp=s_inf_bp, gamma=gamma,
                             const_spread_pp=const_spread_pp)
    b_tot = float(base["savings"].sum()); v_tot = float(var["savings"].sum())
    return {"base_interest_bn": b_tot, "variant_interest_bn": v_tot,
            "gain_bn": v_tot - b_tot, "base": base, "variant": var}


def breakeven_spread(tau_long: float, scen: str, ctx: dict,
                     lo: float = 0.0, hi: float = 3.0,
                     tol_pp: float = 0.005) -> float:
    """Constant dspread (pp, all years) at which the variant's cumulative
    interest gain over the engine base is exactly zero. Bisection on the
    full fixed-point machinery (gain is monotone decreasing in the
    spread). Returns pp."""
    def gain(s_pp):
        return variant_gain(tau_long, scen, ctx,
                            const_spread_pp=s_pp)["gain_bn"]
    g_lo, g_hi = gain(lo), gain(hi)
    if g_lo <= 0:
        return lo
    if g_hi >= 0:
        return hi
    while hi - lo > tol_pp:
        mid = (lo + hi) / 2.0
        if gain(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


# ---------------------------------------------------------------------------
# Term-premium exhibit (SEPARATE line -- never added to coverage)
# ---------------------------------------------------------------------------
def term_premium_exhibit(tau_long: float, scen: str, ctx: dict,
                         tp_bp: float) -> pd.Series:
    """Interest saved by maturity shortening ALONE, at unchanged
    administered rates: excess bill stock (variant minus current
    structure, on the variant's combined path) x TP x PUBLIC_SHARE.
    TP is an ASSUMED scenario parameter. This saving exists with or
    without the fee and is reported separately by construction."""
    fees, residual = ctx["fees"], ctx["residuals"][scen]
    var = combined_structure(tau_long, residual, fees, ctx["base_path"],
                             migrate=True)
    run = var["run"]
    D = var["debt_path"]
    avg, _ = _avg_end_from_path({t: float(D[t]) for t in YEARS})
    excess = {t: float(run.loc[t, "bill_stock_bn"])
              - BILL_SHARE_0 * avg[t] for t in YEARS}
    return pd.Series({t: excess[t] * (tp_bp / 10000.0) * PUBLIC_SHARE
                      for t in YEARS}, name=f"tp_saving_{tp_bp:.0f}bp_bn")


# ---------------------------------------------------------------------------
# Regime D / E stress on Lane B's FRB/US administered paths (inputs only)
# ---------------------------------------------------------------------------
def frbus_plan_path(regime: str) -> dict[int, float]:
    """FY-average LEVEL of the funds rate (%) in Lane B's MCE b100 fee
    run for `regime` (FY t = (t-1)Q4..tQ3, the project's convention)."""
    import frbus_feedback as FB
    path = FB.FRBUS_OUT / f"paths_{regime}_b100_mce.csv"
    df = pd.read_csv(path)
    df["fy"] = df["period"].map(FB._fy_of)
    out = {}
    for fy, x in df.groupby("fy"):
        if 2027 <= fy <= 2036:
            out[int(fy)] = float(x["L_rff"].mean())
    return out


def frbus_shock_increment(regime: str) -> dict[int, float]:
    """The regime's increment to the PLAN's own administered path
    (decimal): FY-average L_rff in the regime's fee run minus the
    no-shock Regime C fee run. Positive under D (the shock elevates
    the fee regime's rate path -- Lane B: fee peaks 4.28% in 2029Q4
    vs 3.01% in C); negative under E (the path collapses toward the
    floor). Zero for C by construction; FY2027 = 0 (pre-effective).
    Using the increment -- not the regime's deviation vs its own
    matched baseline -- keeps the stress on the skeleton's rate basis:
    A_eff = A_skeleton - increment."""
    if regime == "C":
        return {t: 0.0 for t in YEARS}
    plan_c = frbus_plan_path("C")
    plan_r = frbus_plan_path(regime)
    out = {t: (plan_r.get(t, plan_c.get(t, 0.0)) - plan_c.get(t, 0.0)) / 100.0
           for t in YEARS}
    out[2027] = 0.0
    return out


def stress_interest(regime: str, tau_long: float, ctx: dict) -> dict:
    """Interest BILL (level) under the regime's administered path, on
    the BASELINE growing debt path (common to both structures, so the
    comparison isolates structure), dspread = 0 (pure rate channel).
    The administered path is the consolidation skeleton's (A from
    administered_decline) shifted by Lane B's measured increment for
    the regime. Returns per-structure interest/avg-rate paths."""
    A0 = CT.administered_decline()
    shock = frbus_shock_increment(regime)
    A = {t: A0[t] - shock[t] for t in YEARS}
    base_path = ctx["base_path"]
    D = {t: float(base_path.loc[t, "baseline_marketable_debt_bn"])
         for t in YEARS}
    avg, end = _avg_end_from_path(D)
    out = {}
    for migrate, name in ((False, "current"), (True, "migrated")):
        run = run_structure(avg, end, A, tau_long, migrate)
        out[name] = {"interest_consol_bn": run["interest_consol_bn"],
                     "avg_rate": run["avg_rate"], "run": run}
    return out


# ---------------------------------------------------------------------------
# 52-week cadence arithmetic (bracketed sponsor option)
# ---------------------------------------------------------------------------
# ASSUMED bill tenor weights (share of bills outstanding), approximating
# the current issuance mix: {weeks: weight}.
BILL_TENOR_WEIGHTS = {4: 0.13, 6: 0.07, 8: 0.13, 13: 0.28, 17: 0.09,
                      26: 0.20, 52: 0.10}   # ASSUMED (current mix, approx.)


def cadence_52wk() -> dict:
    """Effect of auctioning the 52-week bill weekly instead of every
    4 weeks on the bill stock's effective maturity. Under continuous
    issuance a tenor-tau stock has mean remaining maturity tau/2
    regardless of auction frequency; cadence changes only the
    lumpiness of the maturity profile. Arithmetic, not a model."""
    mean_orig = sum(w * wk for wk, w in BILL_TENOR_WEIGHTS.items())
    mean_rem = mean_orig / 2.0
    # peak single-date maturity concentration of the 52wk component:
    # 4-weekly: 13 auction dates/yr, each ~1/13 of the component's
    # annual issuance matures on one date; weekly: 52 dates, ~1/52.
    return {"mean_original_maturity_wk": mean_orig,
            "mean_remaining_maturity_wk": mean_rem,
            "mean_remaining_maturity_mo": mean_rem / 4.345,
            "delta_mean_maturity_from_cadence_wk": 0.0,
            "peak_share_of_52wk_stock_maturing_one_date_4wkly": 1 / 13,
            "peak_share_of_52wk_stock_maturing_one_date_wkly": 1 / 52}


def build_context() -> dict:
    return CC.build_context()


if __name__ == "__main__":
    ctx = build_context()
    for tau in TAU_LONGS:
        g = variant_gain(tau, "central", ctx)
        print(f"tau_long={tau}: engine base {g['base_interest_bn']:,.0f}  "
              f"variant {g['variant_interest_bn']:,.0f}  "
              f"gain {g['gain_bn']:+,.0f}")
