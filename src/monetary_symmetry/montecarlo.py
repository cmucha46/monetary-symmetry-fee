"""Monte Carlo layer v2 (Lane I) -- parameter uncertainty over the fiscal
module, NOT a new macro model.

WHAT THIS IS
------------
`score.run_scenario` is deterministic: one (s, beta) pair, one covered
base, one set of placeholder behavioural parameters. This module samples
THOSE parameters -- the fiscal module's own inputs -- and re-runs the
unchanged cohort + SFC machinery (`cohort.run_cohorts`,
`sfc.run_ledger_pair`) on each draw. There is no Fed-discretion dial in
this lane (dial identification is a separate analysis; the audit showed
the prototype's dial distribution was an artefact of invented loss
weights, and none is reinvented here). There is no macro model here:
GDP, inflation and employment do not respond; the only demand-side
output is the Lane H flow-channel variant-(i) adjustment, reported
separately and NEVER added to the fiscal totals.

EVERY PRIOR BELOW IS JUDGEMENTAL. None is estimated from data. Priors
are taken from the prototype where the prototype had one (audit section
2) and re-centred on this module's structure where the module differs
(per-category turnover/avoidance; covered base as a discrete choice
among Lane F's three sourced variants instead of the prototype's single
invented covered-share draw). Ranges produced by this module are
CONDITIONAL SIMULATION RANGES under these priors -- they are not
confidence intervals, not forecast intervals, and P(>= $6T) is prior
mass above $6T, not a calibrated probability.

PRIORS (all draws independent across parameters, except where noted)
--------------------------------------------------------------------
beta (pass-through)      clipped N(0.88, 0.11) on [0.55, 1.00]
                         (prototype prior #6; audit notes 13.3% of the
                         prototype's mass piled at the 1.00 clip -- the
                         same censoring applies here and is disclosed)
tau (yield transmission) clipped N(0.32, 0.13) on [0.07, 0.65]
                         (prototype prior #7, now fed through the SFC
                         ledger's explicit repricing schedule instead of
                         the prototype's CBO plug-in. NOTE: in sfc.py
                         the public-yield effect is EXACTLY linear in
                         tau, so tau maps one-for-one into the coupon
                         term -- see the tau=0 / tau=1 bounds and the
                         sensitivity table in MONTECARLO_V2.md)
covered base variant     discrete: loans_plus_securitized (CENTRAL)
                         50%, loans_only (strict) 30%, lane_e_proxy
                         (v1 upper bound) 20% -- ANALYST CHOICE weights,
                         not data. This replaces prototype prior #1
                         (covered_share ~ 0.80 of an aggregate stock),
                         which Lane F showed conflated stocks with
                         loan-instrument definitions.
turnover, per category   relative factor ~ clipped N(1.00, 0.125) on
                         [0.75, 1.25] (i.e. +/-25% relative, ~2 sd to
                         the clip), drawn independently per category
                         and multiplied into the config defaults
                         (prototype had a single invented turnover
                         prior #2; this module's defaults are
                         per-category placeholders -- see config.py)
avoidance per fee pp     one economy-wide draw a ~ clipped
                         N(0.065, 0.035) on [0.01, 0.16] (prototype
                         prior #5); each category's placeholder
                         avoidance is scaled by a/0.065, preserving
                         the config's cross-category relativities
tax-interaction haircut  clipped N(0.13, 0.055) on [0.02, 0.33];
                         net fee = gross x (1 - haircut). The support
                         matches the prototype's implied haircut range
                         (net_receipts_factor 0.67-0.98, prior #4);
                         ~90% of mass falls in ~4-22%. UNESTIMATED --
                         no JCT interaction score for this instrument
                         exists.
IORB desired-stance path AR(1) annual deviations e_t from IORB_BASE:
                         e_t = 0.7 e_{t-1} + eps, eps sd = 0.5 x
                         sqrt(1-0.7^2) ~= 0.357 pp, e_0 drawn from the
                         stationary N(0, 0.5 pp). The SAME shifted path
                         is the baseline stance and the scenario's
                         desired stance, so the fee rate and BOTH
                         interest channels move jointly off one shock
                         -- fee and interest are never sampled
                         independently. Path floored at 0.05 pp
                         (policy.py floors the stance at 0 anyway;
                         the fee still degenerates as stance -> 0).
                         rho = 0.7 and the 0.5 pp stationary sd are
                         analyst choices, documented here.
debt growth (private)    clipped N(0.038, 0.012) on [0.005, 0.075]
                         (prototype prior #15, the prototype's nominal
                         private-debt growth). The PUBLIC debt path in
                         LedgerParams is NOT sampled in this lane
                         (held at the v1 placeholder; documented in
                         MONTECARLO_V2.md as a gap).
creditor MPC             U(0.10, 0.40) and demand multiplier
                         U(1.0, 1.5) -- used ONLY for the Lane H
                         variant-(i) flow-channel adjustment output;
                         they do not enter any fiscal total (the
                         sensitivity table confirms this as a null).

COMMON RANDOM NUMBERS: each parameter draw is evaluated at all three
dials s in {0.50, 0.75, 0.90}, so dial differences within a draw are
parameter-free comparisons, and the sensitivity regressions share one
parameter sample across dials.

FLOW-CHANNEL VARIANT-(i) OUTPUT (secondary, kept separate): per draw
and year, following flow_channel._demand_ranges variant (i) with the
multiplier and MPC SAMPLED instead of ranged:
    demand_T = -mpc x mult x (net_fee + E_i + (1 - 0.30) x E_p)
where E_i / E_p are that draw's IORB / public-coupon injections
removed and 0.30 is Lane H's foreign-holder share of public debt
(flow_channel.FOREIGN_SHARE_PUBLIC_DEBT), whose lost coupon income has
no US demand effect. Reported as % of Lane H's GDP path
(flow_channel.gdp). Negative = the fee regime is more contractionary
than conventional on this channel alone. This is a demand-side potency
offset, NOT revenue, and is never added to combined totals.

Requires numpy (the deterministic core of this package is stdlib-only;
the MC layer is not). Fixed seed: re-running with the same seed
reproduces every output bit-for-bit on the same numpy version.
"""
import csv
from dataclasses import replace
from pathlib import Path

import numpy as np

from .cohort import run_cohorts
from .config import (DEBT_GROWTH, IORB_BASE, YEARS,
                     categories_for_variant)
from .flow_channel import FOREIGN_SHARE_PUBLIC_DEBT, gdp as _fc_gdp
from .sfc import LedgerParams, run_ledger_pair

SEED = 20261114
N_DRAWS_DEFAULT = 10_000
DIALS = (0.50, 0.75, 0.90)

# Variant order matters: index 0/1/2 map to these names everywhere.
VARIANTS = ("loans_plus_securitized", "loans_only", "lane_e_proxy")
VARIANT_WEIGHTS = (0.50, 0.30, 0.20)  # analyst choice, see docstring

STANCE_RHO = 0.7
STANCE_SD = 0.5            # stationary sd of stance deviations, pp
STANCE_FLOOR = 0.05        # pp


def _clip_normal(rng, mean, sd, lo, hi, n):
    return np.clip(rng.normal(mean, sd, size=n), lo, hi)


def sample_parameters(rng: np.random.Generator, n: int) -> dict:
    """Draw n parameter sets. Returns a dict of numpy arrays (n, ...)."""
    beta = _clip_normal(rng, 0.88, 0.11, 0.55, 1.00, n)
    tau = _clip_normal(rng, 0.32, 0.13, 0.07, 0.65, n)
    variant_idx = rng.choice(len(VARIANTS), size=n, p=VARIANT_WEIGHTS)
    # turnover relative factors: one per category (config order)
    n_cat = 4
    turnover_factor = np.clip(rng.normal(1.0, 0.125, size=(n, n_cat)), 0.75, 1.25)
    avoidance = _clip_normal(rng, 0.065, 0.035, 0.01, 0.16, n)
    haircut = _clip_normal(rng, 0.13, 0.055, 0.02, 0.33, n)
    # AR(1) stance deviations, stationary start
    innov_sd = STANCE_SD * float(np.sqrt(1.0 - STANCE_RHO ** 2))
    eps = rng.normal(0.0, innov_sd, size=(n, len(YEARS)))
    e = np.empty((n, len(YEARS)))
    e[:, 0] = rng.normal(0.0, STANCE_SD, size=n)
    for t in range(1, len(YEARS)):
        e[:, t] = STANCE_RHO * e[:, t - 1] + eps[:, t]
    base = np.asarray(IORB_BASE, dtype=float)
    stance_path = np.maximum(STANCE_FLOOR, base[None, :] + e)
    debt_growth = _clip_normal(rng, DEBT_GROWTH, 0.012, 0.005, 0.075, n)
    mpc = rng.uniform(0.10, 0.40, size=n)
    mult = rng.uniform(1.0, 1.5, size=n)
    return {
        "beta": beta, "tau": tau, "variant_idx": variant_idx,
        "turnover_factor": turnover_factor, "avoidance": avoidance,
        "haircut": haircut, "stance_dev": e, "stance_path": stance_path,
        "debt_growth": debt_growth, "mpc": mpc, "mult": mult,
    }


def _categories_for_draw(params: dict, i: int):
    variant = VARIANTS[int(params["variant_idx"][i])]
    cats = categories_for_variant(variant)
    avoid_factor = float(params["avoidance"][i]) / 0.065
    out = []
    for j, c in enumerate(cats):
        out.append(replace(
            c,
            turnover=c.turnover * float(params["turnover_factor"][i, j]),
            avoidance_per_fee_pp=c.avoidance_per_fee_pp * avoid_factor,
        ))
    return out


def run_one_draw(params: dict, i: int, s: float):
    """One fiscal-module evaluation: draw i at dial s.

    Mirrors score.run_scenario exactly, with the sampled stance path,
    haircut, variant categories and tau substituted for the defaults.
    With all parameters at the deterministic defaults it reproduces
    score.run_scenario totals (tested).
    Returns (totals dict, annual list of dicts).
    """
    stance = [float(x) for x in params["stance_path"][i]]
    cats = _categories_for_draw(params, i)
    cohort = run_cohorts(s, float(params["beta"][i]), stance,
                         categories=cats,
                         debt_growth=float(params["debt_growth"][i]))
    iorb_path = [row["iorb"] for row in cohort["annual"]]
    ledger_params = replace(LedgerParams(),
                            yield_transmission=float(params["tau"][i]))
    base, scen, diffs = run_ledger_pair(stance, iorb_path, ledger_params, YEARS)
    net_factor = 1.0 - float(params["haircut"][i])
    mpc = float(params["mpc"][i])
    mult = float(params["mult"][i])
    annual = []
    for crow, drow in zip(cohort["annual"], diffs):
        gross = crow["gross_fee_total"]
        net = gross * net_factor
        e_i = drow["iorb_remit_effect"]
        e_p = drow["public_yield_effect"]
        cons = drow["consolidated_saving"]
        # Lane H variant (i), sampled MPC/multiplier (see docstring).
        demand_T = -mpc * mult * (net + e_i + (1.0 - FOREIGN_SHARE_PUBLIC_DEBT) * e_p)
        annual.append({
            "year": crow["year"], "iorb": crow["iorb"],
            "fee_rate": crow["fee_rate"], "gross_fee": gross, "net_fee": net,
            "public_yield_effect": e_p, "iorb_remit_effect": e_i,
            "consolidated_interest_saving": cons,
            "combined": net + cons,
            "demand_v1_pct_gdp": 100.0 * demand_T / _fc_gdp(crow["year"]),
        })
    totals = {
        "gross_fee_10yr": sum(a["gross_fee"] for a in annual),
        "net_fee_10yr": sum(a["net_fee"] for a in annual),
        "public_yield_saving_10yr": sum(a["public_yield_effect"] for a in annual),
        "iorb_remit_saving_10yr": sum(a["iorb_remit_effect"] for a in annual),
        "consolidated_interest_saving_10yr":
            sum(a["consolidated_interest_saving"] for a in annual),
    }
    totals["combined_total_10yr"] = (totals["net_fee_10yr"]
                                     + totals["consolidated_interest_saving_10yr"])
    # Flow-channel secondary aggregate: mean annual variant-(i) demand
    # effect over the mature years 2030-36, % of GDP (negative =
    # fee regime more contractionary than conventional on this channel).
    mature = [a["demand_v1_pct_gdp"] for a in annual if a["year"] >= 2030]
    totals["demand_v1_pct_gdp_2030_36"] = float(np.mean(mature))
    totals["demand_v1_pct_gdp_2036"] = annual[-1]["demand_v1_pct_gdp"]
    return totals, annual


# ---------------------------------------------------------------------------
# Summaries
# ---------------------------------------------------------------------------

def _stats(x):
    x = np.asarray(x, dtype=float)
    return {"mean": float(np.mean(x)), "median": float(np.median(x)),
            "p10": float(np.percentile(x, 10)), "p90": float(np.percentile(x, 90))}


TOTAL_KEYS = ("gross_fee_10yr", "net_fee_10yr", "public_yield_saving_10yr",
              "iorb_remit_saving_10yr", "consolidated_interest_saving_10yr",
              "combined_total_10yr", "demand_v1_pct_gdp_2030_36",
              "demand_v1_pct_gdp_2036")
ANNUAL_KEYS = ("gross_fee", "net_fee", "public_yield_effect",
               "iorb_remit_effect", "consolidated_interest_saving",
               "combined", "demand_v1_pct_gdp")


def _ranks(x):
    """Average ranks (for Spearman), 0-based."""
    x = np.asarray(x, dtype=float)
    order = np.argsort(x, kind="mergesort")
    ranks = np.empty(len(x), dtype=float)
    ranks[order] = np.arange(len(x), dtype=float)
    # average ties
    sx = x[order]
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and sx[j + 1] == sx[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = ranks[order[i:j + 1]].mean()
        i = j + 1
    return ranks


def sensitivity(params: dict, y: np.ndarray):
    """Standardised OLS coefficients + Spearman rho of y on the inputs.

    Regressors: the continuous sampled parameters (+ variant dummies,
    central variant as reference). mpc/mult are included deliberately:
    they must show ~zero for fiscal totals (null check).
    """
    n = len(y)
    cols = {
        "beta": params["beta"],
        "tau": params["tau"],
        "haircut": params["haircut"],
        "avoidance": params["avoidance"],
        "debt_growth": params["debt_growth"],
        "stance_mean_dev_pp": params["stance_dev"].mean(axis=1),
        "turnover_factor_mean": params["turnover_factor"].mean(axis=1),
        "variant_loans_only": (params["variant_idx"] == 1).astype(float),
        "variant_lane_e_proxy": (params["variant_idx"] == 2).astype(float),
        "mpc_null_check": params["mpc"],
        "mult_null_check": params["mult"],
    }
    yz = (y - y.mean()) / y.std()
    rows = []
    X = []
    names = []
    for name, col in cols.items():
        col = np.asarray(col, dtype=float)
        sd = col.std()
        xz = (col - col.mean()) / sd if sd > 0 else np.zeros(n)
        X.append(xz)
        names.append(name)
    X = np.column_stack(X)
    coef, *_ = np.linalg.lstsq(X, yz, rcond=None)
    yr = _ranks(y)
    for name, c in zip(names, coef):
        xr = _ranks(cols[name])
        rho = float(np.corrcoef(xr, yr)[0, 1])
        rows.append({"parameter": name, "std_beta": float(c),
                     "spearman_rho": rho})
    rows.sort(key=lambda r: -abs(r["std_beta"]))
    return rows


def tau_bounds():
    """Deterministic bounding cases: tau = 0 and tau = 1, all other
    parameters at the deterministic defaults (beta 0.88, central
    variant, default turnover/avoidance/haircut/debt growth, baseline
    stance path). By the exact linearity of the coupon term in tau
    (sfc.py), combined(tau) interpolates linearly between these."""
    from .score import run_scenario
    out = {}
    for tau in (0.0, 1.0):
        lp = replace(LedgerParams(), yield_transmission=tau)
        out[tau] = {s: run_scenario(s, 0.88, ledger_params=lp)["totals"]
                    for s in DIALS}
    return out


def run_montecarlo(n_draws: int = N_DRAWS_DEFAULT, seed: int = SEED):
    """Run the MC. Returns dict with params, per-dial totals arrays,
    annual arrays, summary rows, annual summary rows, sensitivity rows,
    and the tau bounding cases."""
    rng = np.random.default_rng(seed)
    params = sample_parameters(rng, n_draws)
    totals = {s: {k: np.empty(n_draws) for k in TOTAL_KEYS} for s in DIALS}
    annual = {s: {k: np.empty((n_draws, len(YEARS))) for k in ANNUAL_KEYS}
              for s in DIALS}
    for i in range(n_draws):
        for s in DIALS:
            t, a = run_one_draw(params, i, s)
            for k in TOTAL_KEYS:
                totals[s][k][i] = t[k]
            for k in ANNUAL_KEYS:
                annual[s][k][i, :] = [row[k] for row in a]

    summary_rows = []
    det = _deterministic_reference()
    bounds = tau_bounds()
    for s in DIALS:
        row = {"s": s, "n_draws": n_draws, "seed": seed}
        for k in ("gross_fee_10yr", "net_fee_10yr",
                  "public_yield_saving_10yr", "iorb_remit_saving_10yr",
                  "consolidated_interest_saving_10yr", "combined_total_10yr"):
            st = _stats(totals[s][k])
            short = k.replace("_10yr", "")
            for stat, val in st.items():
                row[f"{short}_{stat}"] = val
        comb = totals[s]["combined_total_10yr"]
        row["p_combined_ge_6t"] = float(np.mean(comb >= 6.0))
        row["p_net_fee_ge_6t"] = float(np.mean(totals[s]["net_fee_10yr"] >= 6.0))
        row["deterministic_combined"] = det[s]["combined_total_10yr"]
        row["deterministic_net_fee"] = det[s]["net_fee_10yr"]
        # flow-channel secondary output (separate from fiscal totals)
        for k in ("demand_v1_pct_gdp_2030_36", "demand_v1_pct_gdp_2036"):
            st = _stats(totals[s][k])
            for stat, val in st.items():
                row[f"{k}_{stat}"] = val
        row["combined_tau0_deterministic"] = bounds[0.0][s]["combined_total_10yr"]
        row["combined_tau1_deterministic"] = bounds[1.0][s]["combined_total_10yr"]
        row["public_yield_tau1_deterministic"] = \
            bounds[1.0][s]["public_yield_saving_10yr"]
        summary_rows.append(row)

    annual_rows = []
    for s in DIALS:
        for j, year in enumerate(YEARS):
            row = {"s": s, "year": year}
            for k in ANNUAL_KEYS:
                st = _stats(annual[s][k][:, j])
                for stat, val in st.items():
                    row[f"{k}_{stat}"] = val
            annual_rows.append(row)

    sens_rows = []
    for s in DIALS:
        for r in sensitivity(params, totals[s]["combined_total_10yr"]):
            sens_rows.append({"s": s, "target": "combined_total_10yr", **r})
        for r in sensitivity(params, totals[s]["demand_v1_pct_gdp_2030_36"]):
            sens_rows.append({"s": s, "target": "demand_v1_pct_gdp_2030_36", **r})

    return {"params": params, "totals": totals, "annual": annual,
            "summary_rows": summary_rows, "annual_rows": annual_rows,
            "sensitivity_rows": sens_rows, "tau_bounds": bounds,
            "n_draws": n_draws, "seed": seed}


def _deterministic_reference():
    from .score import run_scenario
    return {s: run_scenario(s, 0.88)["totals"] for s in DIALS}


# ---------------------------------------------------------------------------
# IO
# ---------------------------------------------------------------------------

def _write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def draws_rows(mc):
    """Per-draw parameter + totals table (the stored draws behind the
    sensitivity regressions and the bracketing tests)."""
    p = mc["params"]
    rows = []
    cat_names = ("mortgage", "consumer", "business", "other")
    for i in range(mc["n_draws"]):
        row = {
            "draw": i,
            "beta": float(p["beta"][i]), "tau": float(p["tau"][i]),
            "variant": VARIANTS[int(p["variant_idx"][i])],
            "avoidance": float(p["avoidance"][i]),
            "haircut": float(p["haircut"][i]),
            "debt_growth": float(p["debt_growth"][i]),
            "stance_mean_dev_pp": float(p["stance_dev"][i].mean()),
            "mpc": float(p["mpc"][i]), "mult": float(p["mult"][i]),
        }
        for j, cn in enumerate(cat_names):
            row[f"turnover_factor_{cn}"] = float(p["turnover_factor"][i, j])
        for t in range(len(YEARS)):
            row[f"stance_dev_{YEARS[t]}"] = float(p["stance_dev"][i, t])
        for s in DIALS:
            tag = f"s{int(s * 100)}"
            row[f"gross_fee_{tag}"] = float(mc["totals"][s]["gross_fee_10yr"][i])
            row[f"net_fee_{tag}"] = float(mc["totals"][s]["net_fee_10yr"][i])
            row[f"public_yield_{tag}"] = float(
                mc["totals"][s]["public_yield_saving_10yr"][i])
            row[f"iorb_remit_{tag}"] = float(
                mc["totals"][s]["iorb_remit_saving_10yr"][i])
            row[f"combined_{tag}"] = float(mc["totals"][s]["combined_total_10yr"][i])
            row[f"demand_v1_pct_gdp_2030_36_{tag}"] = float(
                mc["totals"][s]["demand_v1_pct_gdp_2030_36"][i])
        rows.append(row)
    return rows


def main(outdir=None, n_draws: int = N_DRAWS_DEFAULT, seed: int = SEED):
    outdir = Path(outdir) if outdir else Path(__file__).resolve().parents[2] / "results"
    mc = run_montecarlo(n_draws=n_draws, seed=seed)
    _write_csv(outdir / "montecarlo_v2.csv", mc["summary_rows"])
    _write_csv(outdir / "montecarlo_annual_v2.csv", mc["annual_rows"])
    _write_csv(outdir / "montecarlo_sensitivity_v2.csv", mc["sensitivity_rows"])
    _write_csv(outdir / "montecarlo_draws_v2.csv", draws_rows(mc))
    for row in mc["summary_rows"]:
        print(f"s={row['s']:.2f}  combined mean={row['combined_total_mean']:.3f} "
              f"median={row['combined_total_median']:.3f} "
              f"p10={row['combined_total_p10']:.3f} p90={row['combined_total_p90']:.3f} "
              f"P(>=6T)={row['p_combined_ge_6t']:.3f} "
              f"(det={row['deterministic_combined']:.3f}; "
              f"tau0={row['combined_tau0_deterministic']:.3f} "
              f"tau1={row['combined_tau1_deterministic']:.3f})")
    return mc


if __name__ == "__main__":
    main()
