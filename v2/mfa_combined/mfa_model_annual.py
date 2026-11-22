"""
Medicare for America v1 -- ANNUAL extension (Lane 1, Combined Study:
Monetary Symmetry Fee v2 + MFA under a spending closure).

This module imports the UNMODIFIED v1 model (mfa_model.py, copied verbatim
into this directory from ~/workspace/monetary-symmetry/mfa/) and adds the
one thing v1 does not contain: an ANNUAL profile for Title II revenues.

WHY AN EXTENSION IS NEEDED
--------------------------
In v1, TITLE2 is a dict of FY2028-36 WINDOW TOTALS ONLY ($T per component
per scenario).  The model never distributes Title II across years, so v1
by itself cannot produce an annual residual.  Any annual residual therefore
requires an annualization assumption that is NOT in v1.  It is stated here
explicitly and must be carried with the output wherever it is cited:

ANNUALIZATION ASSUMPTION (this lane, NOT v1, NOT a JCT/CBO score):
  Each Title II component's v1 window total is distributed across
  FY2028-36 in proportion to a nominal growth path of 4.2%/yr -- the v1
  model's own nominal payroll-growth assumption (EMP_GROWTH = 0.042),
  Title II bases being predominantly earnings/investment-income bases --
  normalized so each component's annual values sum EXACTLY to its v1
  window total.  All components are treated as in effect for the full
  window from FY2028, consistent with H.R.10924 s.201 (TCJA + P.L.119-21
  repeal for years beginning after Dec 31, 2027) and with v1's window
  totals, which are defined over FY2028-36.  No partial first year, no
  phase-in, and no component-specific effective-date split is modelled,
  because RESULTS_MFA_V1.md documents no other Title II effective date.

Everything else (gross cost and its components, displaced outlays,
premiums, employer contributions) is taken UNROUNDED from the v1 model
functions, so window sums reproduce v1's summary.json to full precision.

NO CBO/JCT/CMS score of H.R.10924 (119th Cong.) exists.  All figures are
a modeller's construction; the TCJA + P.L.119-21 repeal component is an
extension-analogue ASSUMPTION, not a JCT score of the bill.

Run:  python3 mfa_model_annual.py   -> writes mfa_rebased_annual.csv
      (columns in $B; scenario "high" is reported as "high_stress")
Stdlib only.
"""

import csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import mfa_model as m  # the verbatim v1 copy in this directory

TITLE2_GROWTH = 0.042  # = mfa_model.EMP_GROWTH; see docstring

# v1 component key -> output column suffix
COMPONENTS = [
    ("tcja_repeal", "title2_tcja_repeal_bn"),
    ("payroll",     "title2_payroll_bn"),
    ("niit",        "title2_niit_bn"),
    ("surtax",      "title2_surtax_bn"),
    ("stepup",      "title2_stepup_bn"),
    ("excise_hsa",  "title2_excises_hsa_bn"),
]

SCENARIO_OUT = {"low": "low", "central": "central", "high": "high_stress"}


def title2_annual(case):
    """Annual Title II by component, $B.  Returns {year: {component: $B}}
    plus per-year totals.  Sums over the window equal m.TITLE2[case]
    exactly (to float precision)."""
    weights = [(1 + TITLE2_GROWTH) ** (y - 2028) for y in m.YEARS]
    wsum = sum(weights)
    out = {}
    for i, y in enumerate(m.YEARS):
        row = {}
        for key, _col in COMPONENTS:
            row[key] = m.TITLE2[case][key] * 1000.0 * weights[i] / wsum  # $T -> $B
        row["total"] = sum(row.values())
        out[y] = row
    return out


def build_rows():
    rows = []
    for case in ("low", "central", "high"):
        enr = m.enrollment(case)
        g = m.gross_cost(case, enr)
        d = m.displaced(case)
        prem = m.premiums(case, enr)
        emp = m.employer(case)
        t2 = title2_annual(case)
        for i, y in enumerate(m.YEARS):
            residual = (g[i]["gross_B"] - d[i]["displaced_B"] - prem[i]
                        - emp[i] - t2[y]["total"])
            row = dict(
                scenario=SCENARIO_OUT[case],
                year=y,
                gross_bn=round(g[i]["gross_B"], 1),
                core_bn=round(g[i]["core_B"], 1),
                dvh_bn=round(g[i]["dvh_B"], 1),
                ltss_bn=round(g[i]["ltss_B"], 1),
                admin_bn=round(g[i]["admin_B"], 1),
                topup_bn=round(g[i]["topup_B"], 1),
                waitlist_bn=round(g[i]["waitlist_B"], 1),
                displaced_bn=round(d[i]["displaced_B"], 1),
                premiums_bn=round(prem[i], 1),
                employer_bn=round(emp[i], 1),
                title2_total_bn=round(t2[y]["total"], 1),
                residual_bn=round(residual, 1),
            )
            for key, col in COMPONENTS:
                row[col] = round(t2[y][key], 1)
            rows.append(row)
    return rows


FIELDNAMES = ["scenario", "year", "gross_bn", "core_bn", "dvh_bn",
              "ltss_bn", "admin_bn", "topup_bn", "waitlist_bn",
              "displaced_bn", "premiums_bn", "employer_bn",
              "title2_total_bn", "title2_tcja_repeal_bn",
              "title2_payroll_bn", "title2_niit_bn", "title2_surtax_bn",
              "title2_stepup_bn", "title2_excises_hsa_bn", "residual_bn"]


if __name__ == "__main__":
    rows = build_rows()
    path = os.path.join(HERE, "mfa_rebased_annual.csv")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        w.writerows(rows)
    # verification digest: unrounded window sums vs v1
    summary, _annual = m.run()
    for case in ("low", "central", "high"):
        t2 = title2_annual(case)
        t2_window = sum(t2[y]["total"] for y in m.YEARS) / 1000.0
        print(f"{case:8s} TitleII annualization sums to ${t2_window:.4f}T "
              f"(v1 window total ${summary[case]['title2']:.4f}T); "
              f"v1 residual ${summary[case]['residual']:.4f}T")
    print(f"wrote {path} ({len(rows)} rows)")
