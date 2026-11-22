"""
Medicare for America (H.R.10924, 119th Cong.) -- gross-cost and
residual-financing module, v1.  MODELLER'S CONSTRUCTION.

There is NO CBO/JCT/CMS score of any version of DeLauro's Medicare for
America Act (verified, Lane C).  Every number this module produces is a
construction from the parameter table in parameters.py / data/parameters.csv;
each parameter is labelled SOURCED, ANCHORED (derived from a sourced
aggregate) or ASSUMPTION.  Ranges, not points.

Window: FY2028-36 (MFA costs begin 2028; FY2027 shown as zero where relevant).
Concept: FEDERAL OUTLAYS throughout, consolidated federal view.
Displaced Medicare = baseline NET outlays (net of baseline premiums);
MFA premiums are then MFA's own receipts -- no double count (see RESULTS).

Run:  python3 mfa_model.py   -> writes data/annual_detail.csv,
      data/financing_matrix.csv, data/summary.json and prints a digest.
Stdlib only.
"""

import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
YEARS = list(range(2028, 2037))          # FY2028..FY2036
YI = {y: i for i, y in enumerate(YEARS)}

# ----------------------------------------------------------------------------
# BASELINE POPULATIONS (millions, average annual) -- see data/parameters.csv
# CBO Feb 2026 Medicare baseline: Part A avg monthly enrollment (exact series)
MEDICARE_PARTA = [73.051, 74.510, 75.705, 76.639, 77.459, 78.229, 79.012, 79.840, 80.507]
# CBO Feb 2026 Medicaid baseline: average monthly enrollment, total (exact series)
MEDICAID_AVG = [79, 76, 75, 75, 75, 74, 74, 74, 73]
# CBO Feb 2026 Medicaid baseline: ACA-expansion adults, avg monthly (exact series)
MEDICAID_EXPANSION = [14, 12, 11, 11, 10, 10, 10, 10, 10]
# Dual eligibles (ASSUMPTION ~12M, CMS-scale, +1%/yr; subset of both programmes)
DUALS = [12.0, 12.1, 12.2, 12.4, 12.5, 12.6, 12.7, 12.9, 13.0]
# Nongroup/marketplace population (ANCHORED: CBO marketplace falls to ~13.1M in
# 2027; nongroup+Basic Health averages 19.3M 2026-36 -- blended, declining)
EXCHANGE_POP = [18.0, 17.0, 16.0, 15.0, 14.0, 13.5, 13.0, 13.0, 13.0]
# Uninsured (ANCHORED: CBO Feb/May 2026 -- ~30M in 2026 rising to ~37M in 2036)
UNINSURED = [31.5, 32.5, 33.0, 33.7, 34.4, 35.0, 35.7, 36.3, 37.0]
# Employment-based covered lives (SOURCED avg 169M, CBO subsidies baseline)
ESI_POP = [165, 166, 167, 168, 169, 170, 171, 172, 173]

# BASELINE FEDERAL OUTLAY STREAMS ($B)
# Medicaid federal outlays, CBO Feb 2026 baseline (exact series)
MEDICAID_OUTLAYS = [702, 707, 727, 751, 778, 812, 845, 878, 914]
# Medicare NET outlays: endpoints $1,140B (2027) -> $1,970B (2036), CBO Feb 2026;
# geometric interpolation between endpoints (CONSTRUCTION, labelled)
_g = (1970.0 / 1140.0) ** (1.0 / 9.0)
MEDICARE_NET_OUTLAYS = [1140.0 * _g ** (y - 2027) for y in YEARS]
# Marketplace premium tax credit outlays ($B): CBO Feb 2026 PTC baseline,
# $88B (2026) -> $116B (2036), geometric interpolation (CONSTRUCTION)
_g2 = (116.0 / 88.0) ** (1.0 / 10.0)
PTC_OUTLAYS = [88.0 * _g2 ** (y - 2026) for y in YEARS]
# CHIP federal outlays (ASSUMPTION ~$18B/yr, +4%/yr)
CHIP_OUTLAYS = [18.0 * 1.04 ** (y - 2028) for y in YEARS]

# ----------------------------------------------------------------------------
CASES = {
    #         rate   induced cs_shift dvh$  ltss_share ltss$ admin  topup% waitlist$B
    "low":    dict(rate=1.03, induced=0.00, cs=1.02, dvh=400,  ltss_sh=0.03, ltss_c=28000,
                   admin=0.02, g=0.040, topup=0.03, waitlist=15.0,
                   trans_take=0.25, unins_take=0.50, compliance=0.95,
                   esi_ramp=[0.01, 0.02, 0.03, 0.04, 0.05, 0.06],      # 2031..36
                   dual_exp_share=0.40),
    "central": dict(rate=1.06, induced=0.07, cs=1.05, dvh=650, ltss_sh=0.05, ltss_c=36000,
                    admin=0.03, g=0.048, topup=0.05, waitlist=35.0,
                    trans_take=0.40, unins_take=0.70, compliance=0.98,
                    esi_ramp=[0.02, 0.04, 0.06, 0.08, 0.10, 0.12],
                    dual_exp_share=0.47),
    "high":   dict(rate=1.10, induced=0.15, cs=1.08, dvh=900, ltss_sh=0.08, ltss_c=48000,
                   admin=0.05, g=0.058, topup=0.08, waitlist=60.0,
                   trans_take=0.55, unins_take=0.85, compliance=1.00,
                   esi_ramp=[0.04, 0.07, 0.10, 0.14, 0.18, 0.22],
                   dual_exp_share=0.54),
}

# Per-enrollee CORE plan-paid cost, 2028$, by origin cohort (ANCHORED/CONSTRUCTION)
CORE_2028 = dict(medicare=17500, dual=32000, medicaid=11500,
                 exchange=7800, uninsured=6800, esi=8600)
# Share of LTSS entitlement that is NEW cost (baseline already funds the rest)
LTSS_NEW_FACTOR = dict(medicare=1.00, dual=0.40, medicaid=0.35,
                       exchange=1.00, uninsured=1.00, esi=1.00)
# Premium income-bracket model (ASSUMPTION, CPS-style shares of enrollees)
PREM_SHARES = [0.33, 0.28, 0.17, 0.22]            # <200 / 200-400 / 400-600 / >600 % FPL
PREM_PAID_2028 = {  # avg premium actually paid per enrollee-yr, 2028$, brackets 2..4
    "low":     [0, 800, 1900, 3200],
    "central": [0, 1100, 2400, 3900],
    "high":    [0, 1400, 2900, 4600],
}
PREM_GROWTH = 0.04
# Employer contributions (from 2031): payroll of large employers 2031, $T (ASSUMPTION
# ~70% of ~$13.5T total wages), growing 4.2%/yr; non-offering share by case
EMP_PAYROLL_2031_T = 9.5
EMP_GROWTH = 0.042
EMP_NOOFFER = {"low": 0.10, "central": 0.25, "high": 0.40}
# Title II revenues FY2028-36, $T (sourced analogues / arithmetic -- see RESULTS)
TITLE2 = {
    "low":     dict(tcja_repeal=3.20, payroll=0.95, niit=0.38, surtax=0.22, stepup=0.13, excise_hsa=0.08),
    "central": dict(tcja_repeal=3.90, payroll=1.15, niit=0.47, surtax=0.30, stepup=0.17, excise_hsa=0.12),
    "high":    dict(tcja_repeal=4.60, payroll=1.35, niit=0.56, surtax=0.40, stepup=0.22, excise_hsa=0.18),
}
# Accelerated-MOE amendment variant (NOT in the bill): state Medicaid own-spending
# base $335B FY2024 (Pew/CMS-64, SOURCED), +3%/yr, paid from FY2030 (ASSUMPTION)
def accelerated_moe(year):
    if year < 2030:
        return 0.0
    return 335.0 * 1.03 ** (year - 2024)   # $B


def enrollment(case):
    """Average-annual MFA enrollment by origin cohort (millions)."""
    p = CASES[case]
    out = {k: [0.0] * 9 for k in CORE_2028}
    for i, y in enumerate(YEARS):
        nondual_medicare = MEDICARE_PARTA[i] - DUALS[i]
        nondual_medicaid = MEDICAID_AVG[i] - DUALS[i]
        expansion = MEDICAID_EXPANSION[i]
        residual_medicaid = nondual_medicaid - expansion
        if y in (2028, 2029):   # transitional public option only
            out["exchange"][i] = EXCHANGE_POP[i] * p["trans_take"]
        elif y >= 2033:         # exchanges terminate 2033 -> MFA
            out["exchange"][i] = EXCHANGE_POP[i] * p["compliance"]
        out["uninsured"][i] = UNINSURED[i] * p["unins_take"] if y >= 2028 else 0.0
        if y >= 2030:           # Medicare benefits end 2030 (non-duals)
            out["medicare"][i] = nondual_medicare * p["compliance"]
        if y >= 2033:           # duals (Medicare ends for duals 2033)
            out["dual"][i] = DUALS[i] * p["compliance"]
            out["medicaid"][i] += expansion * p["compliance"]
        if y >= 2035:           # residual Medicaid entitlement ends 2035
            out["medicaid"][i] += residual_medicaid * p["compliance"]
        if y >= 2031:           # large-employer enrollment process from 2031
            out["esi"][i] = ESI_POP[i] * p["esi_ramp"][y - 2031]
    return out


def gross_cost(case, enr):
    """Federal gross MFA outlays $B by year: core benefits + DVH + LTSS + admin
    + s.2206(b)(4) Medicaid rate top-up (2028-33) + s.124 waiting-list clearance."""
    p = CASES[case]
    rows = []
    for i, y in enumerate(YEARS):
        mult = p["rate"] * (1 + p["induced"]) * p["cs"]
        growth = (1 + p["g"]) ** (y - 2028)
        total_enr = sum(enr[k][i] for k in enr)
        core = sum(enr[k][i] * CORE_2028[k] for k in enr) / 1000.0 * mult * growth  # $B
        dvh = total_enr * p["dvh"] / 1000.0 * growth
        ltss = sum(enr[k][i] * LTSS_NEW_FACTOR[k] for k in enr) / 1000.0 \
            * p["ltss_sh"] * p["ltss_c"] * growth
        benefits = core + dvh + ltss
        admin = benefits * p["admin"]
        topup = p["topup"] * MEDICAID_OUTLAYS[i] if 2028 <= y <= 2033 else 0.0
        waitlist = p["waitlist"] * {2028: 0.60, 2029: 0.25, 2030: 0.15}.get(y, 0.0)
        rows.append(dict(year=y, enrollment_M=total_enr, core_B=core, dvh_B=dvh,
                         ltss_B=ltss, admin_B=admin, topup_B=topup,
                         waitlist_B=waitlist,
                         gross_B=benefits + admin + topup + waitlist))
    return rows


def displaced(case):
    """Displaced baseline federal outlays $B by year (OUTLAYS concept, phased
    per bill ss.112/2207 timing -- never steady-state)."""
    p = CASES[case]
    rows = []
    for i, y in enumerate(YEARS):
        med = 0.0
        if y in (2030, 2031, 2032):
            med = MEDICARE_NET_OUTLAYS[i] * 0.70 * p["compliance"]  # non-dual spend share (ASSUMPTION 0.70)
        elif y >= 2033:
            med = MEDICARE_NET_OUTLAYS[i] * p["compliance"]
        mcaid = 0.0
        if y in (2033, 2034):
            mcaid = (MEDICAID_OUTLAYS[i] + CHIP_OUTLAYS[i]) * p["dual_exp_share"] * p["compliance"]
        elif y >= 2035:
            mcaid = (MEDICAID_OUTLAYS[i] + CHIP_OUTLAYS[i]) * p["compliance"]
        ptc = PTC_OUTLAYS[i] * p["compliance"] if y >= 2033 else 0.0
        rows.append(dict(year=y, medicare_B=med, medicaid_chip_B=mcaid, ptc_B=ptc,
                         displaced_B=med + mcaid + ptc))
    return rows


def premiums(case, enr):
    p = CASES[case]
    paid = PREM_PAID_2028[case]
    avg = sum(s * v for s, v in zip(PREM_SHARES, paid))   # $ per enrollee-yr, 2028$
    return [sum(enr[k][i] for k in enr) * avg / 1000.0 * (1 + PREM_GROWTH) ** (y - 2028)
            for i, y in enumerate(YEARS)]                  # $B


def employer(case):
    out = []
    for y in YEARS:
        if y < 2031:
            out.append(0.0)
        else:
            payroll = EMP_PAYROLL_2031_T * (1 + EMP_GROWTH) ** (y - 2031)  # $T
            out.append(payroll * 1000.0 * EMP_NOOFFER[case] * 0.08)        # $B
    return out


def run():
    annual = []
    summary = {}
    for case in CASES:
        enr = enrollment(case)
        g = gross_cost(case, enr)
        d = displaced(case)
        prem = premiums(case, enr)
        emp = employer(case)
        t2 = sum(TITLE2[case].values())                    # $T over window
        moe_acc = sum(accelerated_moe(y) for y in YEARS) / 1000.0  # $T
        tot = dict(
            gross=sum(r["gross_B"] for r in g) / 1000.0,
            displaced=sum(r["displaced_B"] for r in d) / 1000.0,
            premiums=sum(prem) / 1000.0,
            employer=sum(emp) / 1000.0,
            title2=t2,
        )
        tot["increment_pre_offsets"] = tot["gross"] - tot["displaced"]
        tot["residual"] = (tot["gross"] - tot["displaced"] - tot["premiums"]
                           - tot["employer"] - tot["title2"])     # state MOE = $0 (bill)
        tot["residual_accel_moe"] = tot["residual"] - moe_acc
        tot["accel_moe"] = moe_acc
        tot["enrollee_years_M"] = sum(r["enrollment_M"] for r in g)
        summary[case] = tot
        for i, y in enumerate(YEARS):
            annual.append(dict(case=case, year=y,
                               enrollment_M=round(g[i]["enrollment_M"], 2),
                               gross_B=round(g[i]["gross_B"], 1),
                               core_B=round(g[i]["core_B"], 1),
                               dvh_B=round(g[i]["dvh_B"], 1),
                               ltss_B=round(g[i]["ltss_B"], 1),
                               admin_B=round(g[i]["admin_B"], 1),
                               topup_B=round(g[i]["topup_B"], 1),
                               waitlist_B=round(g[i]["waitlist_B"], 1),
                               displaced_B=round(d[i]["displaced_B"], 1),
                               premiums_B=round(prem[i], 1),
                               employer_B=round(emp[i], 1),
                               accel_moe_B=round(accelerated_moe(y), 1)))
    return summary, annual


# Fee-project combined totals (fee + consolidated interest saving), $T FY27-36,
# from repo/results/deterministic_score_v2.csv (Lane F corrected base, beta=0.88)
FEE_CASES = {
    "s50_central": 4.4415, "s75_strict": 5.6009,
    "s75_central": 6.7113, "s90_central": 8.1176,
}

if __name__ == "__main__":
    summary, annual = run()
    ddir = os.path.join(HERE, "data")
    os.makedirs(ddir, exist_ok=True)
    with open(os.path.join(ddir, "annual_detail.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(annual[0].keys()))
        w.writeheader(); w.writerows(annual)
    with open(os.path.join(ddir, "financing_matrix.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["mfa_residual_case", "residual_T_bill_moe0",
                    "residual_T_accel_moe_amendment"] +
                   [f"surplus_vs_{k}_T" for k in FEE_CASES])
        for case, t in summary.items():
            w.writerow([case, round(t["residual"], 2), round(t["residual_accel_moe"], 2)] +
                       [round(v - t["residual"], 2) for v in FEE_CASES.values()])
    with open(os.path.join(ddir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    for case, t in summary.items():
        print(f"{case:8s} gross ${t['gross']:.2f}T  displaced ${t['displaced']:.2f}T  "
              f"premiums ${t['premiums']:.2f}T  employer ${t['employer']:.2f}T  "
              f"TitleII ${t['title2']:.2f}T  RESIDUAL ${t['residual']:.2f}T  "
              f"(accel-MOE variant ${t['residual_accel_moe']:.2f}T)")
    print("\nFinancing matrix (fee total - residual = surplus + / shortfall -), $T:")
    for case, t in summary.items():
        cells = "  ".join(f"{k}: {v - t['residual']:+.2f}" for k, v in FEE_CASES.items())
        print(f"  {case:8s} {cells}")
