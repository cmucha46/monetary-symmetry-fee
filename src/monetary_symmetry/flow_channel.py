"""Lane H -- the interest-income / reserve-flow channel FRB/US omits.

WHY THIS MODULE EXISTS
----------------------
Carlos's critique (2026-11-13) of the Lane D/G FRB/US potency ranking:
conventional tightening pays MORE net interest into the private sector
(IORB on reserves + Treasury coupons on a repricing debt stock), which is
an expansionary income injection working against the tightening; the fee
regime pays LESS of that injection AND redirects the policy-sensitive
borrowing charge from private creditors to the Treasury. FRB/US cannot
see any of this: Lane B verified it has no reserves, no IORB, no bank
balance sheet and no government interest-income flow among its 933
variables. This module quantifies the omitted flows with the repo's own
SFC ledger (sfc.py) and cohort outputs (score.py). It does NOT re-run or
modify FRB/US; it measures the size of what FRB/US leaves out.

ACCOUNTING (one consistent table; every dollar appears once)
------------------------------------------------------------
All regime figures are DELTAS, fee scenario minus conventional baseline,
for a permanent fee regime operating at the baseline desired stance
(policy.policy_for holds the all-in borrower cost at the desired path in
both regimes). Components per year:

  G        gross fee collections (cohort model, central covered base)
  net_fee  G x NET_RECEIPTS_FACTOR (0.87). The 13% haircut is a tax
           interaction: lenders' fee expense reduces other tax receipts.
           We attribute the offset to lenders (their income tax falls as
           their fee-bearing profits fall) -- labelled ASSUMPTION A1.
  E_i      IORB injection removed = baseline IORB expense - scenario
           IORB expense (sfc diffs 'iorb_remit_effect'). Paid by the Fed
           to banks in the conventional regime; not paid under the fee.
  E_p      Treasury coupon injection removed = baseline interest on
           public-held debt - scenario (sfc 'public_yield_effect').
           Recipients: public holders, incl. ~30% foreign (see
           FOREIGN_SHARE_PUBLIC_DEBT) whose lost income has no US demand
           effect -- that share is removed only in the demand step.
  E_f      MEMO ONLY: interest on Fed-held Treasuries falls by E_f in
           the scenario; the Fed's asset income falls by the same E_f.
           Internal to consolidated government; nets to zero; NEVER
           added to any total.

Sector net-income deltas (accrual; must sum to zero -- tested):
  Treasury          +net_fee + E_i + E_p
                    (net fee + all coupon savings + the Fed's accrual
                    gain passed through as ultimate remittances)
  Federal Reserve   0 on accrual: its income delta is +(E_i - E_f),
                    exactly offset by the change in its internal coupon
                    receipts and passed to Treasury as remittances on an
                    accrual basis. CASH differs: the deferred asset
                    absorbs the improvement first (memo lines in the
                    annual output: remittance_cash_delta,
                    deferred_asset paths). Cash timing is not income.
  Banks / lenders   -net_fee - E_i
                    (remit G, recoup (G - net_fee) via A1; lose E_i of
                    IORB. Identity: lenders' net loss on the lending
                    channel is exactly the fee, because borrower all-in
                    cost is held at the desired stance by construction:
                    of every borrower dollar, s-share now reaches
                    Treasury instead of creditor net income.)
  Borrowers         0 (all-in policy-sensitive cost held at the desired
                    stance in both regimes BY CONSTRUCTION of
                    policy_for. This is the regime definition, not a
                    finding.)
  Other private     -E_p (public-debt holders; foreign share memo'd)
  SUM               0

GOVERNMENT->PRIVATE NET INTEREST INJECTION (levels, for scale):
  injection_t = consolidated_net_interest_t (sfc) -- interest to public
  holders + IORB expense + Fed opex - Fed MBS income. Its delta is
  exactly -(E_i + E_p) = -consolidated_saving (tested). The fee regime's
  fiscal "interest saving" and the private sector's lost interest
  injection are the SAME dollars seen from two sides.

TREASURY USE OF THE FEE (demand variants; flows above are pre-use):
  (i)   deficit reduction / reduced issuance (the fiscal score's
        assumption): the net fee is not returned; private income falls
        by net_fee + E_i + E_p and stays out.
  (ii)  spent on Medicare for America benefits: net_fee returns to
        private recipients (providers / beneficiary households) whose
        MPC is labelled higher; the demand effect is a REDISTRIBUTION
        (low-MPC creditor income -> high-MPC health recipients), while
        E_i + E_p are still removed.
  (iii) TGA accumulation: settlement timing only (sfc.settlement_flows).
        A collected-but-unspent fee drains reserves into the TGA; any
        spend reverses it. Not a permanent flow; no demand term. Note
        also: in the ample-reserves floor system the Fed supplies
        reserves elastically at IORB, so a settlement drain does not
        mechanically tighten bank lending the way it would in a scarce-
        reserves corridor system. The demand-relevant object is the
        INCOME flow, not the reserve stock. (This qualifies, but does
        not overturn, the drain framing.)

DEMAND TRANSLATION (labelled assumptions, ranges only):
  MPC_INT   marginal propensity to spend of interest/fee-income
            recipients (creditors, banks' shareholders, domestic bond
            holders): 0.10-0.40 (task-specified range; consistent with
            Auclert-style evidence that saver/creditor MPCs are low and
            with interest income concentrating in high-wealth, low-MPC
            hands and abroad).
  MPC_HEALTH recipients under variant (ii): 0.60-0.90 (lower-income
            beneficiary households / provider payrolls).
  MULT      simple demand multiplier on first-round spending: 1.0-1.5.
  GDP       nominal GDP path: 2025 = $30.9T (BEA-scale, ANCHORED),
            +4.1%/yr nominal (PLACEHOLDER, CBO-consistent ballpark).

EPISODE SCALING (Lane G): +1.00pp desired tightening, 8 quarters,
s=0.75, beta=0.88: drff = q/(1+beta*k) = 0.275pp, f_inc = k*drff
= 0.824pp, wedge = q - drff = 0.725pp. Episode flows are computed
per episode-year on (a) the contemporaneous repo taxable book
(2027: no fee in force; 2028: intro year) and (b) a MATURE fee-paying
book (2032 taxable book) with an affected-principal share of 0.40-0.60
(only floating vintages and new originations reprice within 8 quarters;
fixed vintages are locked -- the rest of the book does not pay the
increment). Never conflate with the regime flows above.
"""
from dataclasses import dataclass

from .config import IORB_BASE, NET_RECEIPTS_FACTOR, YEARS
from .policy import policy_for
from .score import run_scenario
from .sfc import LedgerParams, run_ledger_pair

BETA_CENTRAL = 0.88
DIALS = (0.50, 0.75, 0.90)

# Labelled demand-translation assumptions (see module docstring).
MPC_INT_LO, MPC_INT_HI = 0.10, 0.40        # interest/creditor income recipients
MPC_HEALTH_LO, MPC_HEALTH_HI = 0.60, 0.90  # variant (ii) benefit recipients
MULT_LO, MULT_HI = 1.0, 1.5
FOREIGN_SHARE_PUBLIC_DEBT = 0.30           # ANCHORED approx: foreign holdings
                                           # ~$9T of ~$30T public Treasuries;
                                           # removed only in the demand step
GDP_2025 = 30.9                            # $T, ANCHORED (BEA scale)
GDP_NOMINAL_GROWTH = 0.041                 # PLACEHOLDER, CBO-consistent ballpark


def gdp(year: int) -> float:
    return GDP_2025 * (1.0 + GDP_NOMINAL_GROWTH) ** (year - 2025)


@dataclass(frozen=True)
class FlowYear:
    year: int
    s: float
    # levels (baseline = conventional regime)
    injection_base: float          # consolidated net interest, baseline $T
    injection_scen: float
    iorb_expense_base: float
    interest_public_base: float
    # deltas (fee - conventional)
    gross_fee: float
    net_fee: float
    e_iorb: float                  # IORB injection removed (>=0 = saving)
    e_coupon: float                # coupon injection removed
    e_fedheld_memo: float          # internal, nets zero -- memo only
    injection_removed: float       # == e_iorb + e_coupon == consolidated saving
    private_income_removed_v1: float  # variant (i): net_fee + injection_removed
    # sector net-income deltas (sum zero)
    sec_treasury: float
    sec_fed: float
    sec_banks_lenders: float
    sec_borrowers: float
    sec_other_private: float
    # cash-timing memos
    remittance_cash_delta: float   # scenario cash remittance - baseline cash
    deferred_asset_base: float
    deferred_asset_scen: float
    # demand translation, variant (i) and (ii): (low, high) $T, and % of GDP
    demand_v1_lo: float
    demand_v1_hi: float
    demand_v2_lo: float
    demand_v2_hi: float

    def sector_sum(self) -> float:
        return (self.sec_treasury + self.sec_fed + self.sec_banks_lenders
                + self.sec_borrowers + self.sec_other_private)


def _demand_ranges(net_fee, e_iorb, e_coupon):
    """(variant_i (lo,hi), variant_ii (lo,hi)) first-round x multiplier, $T.

    Negative = fee regime more contractionary than conventional.
    Domestic coupon term excludes the foreign-holder share.
    """
    dom_coupon = e_coupon * (1.0 - FOREIGN_SHARE_PUBLIC_DEBT)
    int_loss = e_iorb + dom_coupon  # interest-income removed, US-relevant
    # Variant (i): everything removed is private income not returned.
    v1_first_lo = MPC_INT_LO * (net_fee + int_loss)
    v1_first_hi = MPC_INT_HI * (net_fee + int_loss)
    v1 = (-v1_first_hi * MULT_HI, -v1_first_lo * MULT_LO)  # (lo, hi), negative
    # Variant (ii): net fee respent to high-MPC recipients.
    gain_lo = MPC_HEALTH_LO * net_fee - MPC_INT_HI * net_fee - MPC_INT_HI * int_loss
    gain_hi = MPC_HEALTH_HI * net_fee - MPC_INT_LO * net_fee - MPC_INT_LO * int_loss
    v2 = (gain_lo * MULT_LO if gain_lo < 0 else gain_lo * MULT_LO,
          gain_hi * MULT_HI)
    # widen correctly when the low end is negative
    v2_lo = gain_lo * (MULT_HI if gain_lo < 0 else MULT_LO)
    v2 = (v2_lo, gain_hi * MULT_HI if gain_hi > 0 else gain_hi * MULT_LO)
    return v1, v2


def regime_flows(s: float, beta: float = BETA_CENTRAL,
                 covered_base_variant: str = "loans_plus_securitized"):
    """Annual flow comparison for one dial: list[FlowYear], FY2027-36."""
    res = run_scenario(s, beta, covered_base_variant=covered_base_variant)
    base, scen, diffs = res["base"], res["scen"], res["diffs"]
    annual = {a["year"]: a for a in res["annual"]}
    out = []
    for b, sc, d in zip(base, scen, diffs):
        yr = b["year"]
        gross = annual[yr]["gross_fee"]
        net = annual[yr]["net_fee"]
        e_iorb = d["iorb_remit_effect"]
        e_coupon = d["public_yield_effect"]
        v1, v2 = _demand_ranges(net, e_iorb, e_coupon)
        out.append(FlowYear(
            year=yr, s=s,
            injection_base=b["consolidated_net_interest"],
            injection_scen=sc["consolidated_net_interest"],
            iorb_expense_base=b["iorb_expense"],
            interest_public_base=b["interest_public"],
            gross_fee=gross, net_fee=net,
            e_iorb=e_iorb, e_coupon=e_coupon,
            e_fedheld_memo=b["interest_fedheld"] - sc["interest_fedheld"],
            injection_removed=d["consolidated_saving"],
            private_income_removed_v1=net + d["consolidated_saving"],
            sec_treasury=net + e_iorb + e_coupon,
            sec_fed=0.0,
            sec_banks_lenders=-net - e_iorb,
            sec_borrowers=0.0,
            sec_other_private=-e_coupon,
            remittance_cash_delta=sc["remittance_cash"] - b["remittance_cash"],
            deferred_asset_base=b["deferred_asset"],
            deferred_asset_scen=sc["deferred_asset"],
            demand_v1_lo=v1[0], demand_v1_hi=v1[1],
            demand_v2_lo=v2[0], demand_v2_hi=v2[1],
        ))
    return out


def regime_totals(flows):
    """10-year sums of the main flow lines."""
    keys = ("gross_fee", "net_fee", "e_iorb", "e_coupon", "injection_removed",
            "private_income_removed_v1")
    return {k: sum(getattr(f, k) for f in flows) for k in keys}


# --------------------------------------------------------------------------
# Episode scaling (Lane G): +100bp desired tightening for 8 quarters.
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class EpisodeFlows:
    s: float
    beta: float
    q_pp: float                 # desired tightening increment, pp
    drff_pp: float              # funds-rate / IORB component
    f_inc_pp: float             # incremental fee on repricing principal
    wedge_pp: float             # q - drff
    years: int                  # episode length in years (8 quarters)
    # per-episode-year flow deltas (fee - conventional), $T
    d_iorb_injection: float     # IORB injection removed per year
    d_coupon_injection_avg: float  # coupon injection removed, avg over episode
    book_basis: str             # 'contemporaneous' or 'mature'
    fee_net_lo: float           # net fee increment per year (range via
    fee_net_hi: float           # affected-principal share 0.40-0.60)
    demand_lo: float            # variant (i) relative demand effect, $T/yr
    demand_hi: float
    demand_pct_gdp_lo: float
    demand_pct_gdp_hi: float


def episode_flows(s: float = 0.75, beta: float = BETA_CENTRAL,
                  book_basis: str = "mature",
                  affected_share_lo: float = 0.40,
                  affected_share_hi: float = 0.60):
    """Flow deltas for Lane G's +1.00pp / 8-quarter episode at dial s.

    IORB term uses the repo ledger's reserves stock ($2.93T, constant in
    v1). Coupon term uses Lane G's realised rg10 deviations (conventional
    +0.399pp vs s=0.75 +0.109pp mean over the 8 quarters; for other dials
    the rg10 mean is scaled from Lane G's table: s=0.50 +0.212,
    s=0.90 +0.044) fed through the repo's repricing schedule (18%/yr of
    the public stock at the new yield). Fee term: f_inc x affected
    principal x NET_RECEIPTS_FACTOR.
    """
    from .sfc import LedgerParams as _LP
    p = _LP()
    q = 1.00
    k = s / (1.0 - s)
    drff = q / (1.0 + beta * k)
    f_inc = k * drff
    wedge = q - drff
    # IORB injection removed per episode year ($T): reserves x wedge.
    d_iorb = p.reserves_start * wedge / 100.0
    # Coupon injection removed: yield gap on new issues, repricing build-up.
    rg10_conv = 0.399
    rg10_by_s = {0.50: 0.212, 0.75: 0.109, 0.90: 0.044}
    yield_gap = (rg10_conv - rg10_by_s[s]) / 100.0  # fraction
    stock_avg = p.public_debt_start + 1.7  # ~avg public stock over episode
    # average repriced share over a 2-year episode: (0.18 + (1-(1-.18)^2))/2
    share_y1 = p.treasury_repricing_share
    share_y2 = 1.0 - (1.0 - p.treasury_repricing_share) ** 2
    d_coupon_avg = stock_avg * yield_gap * (share_y1 + share_y2) / 2.0
    # Fee-paying book by basis.
    if book_basis == "contemporaneous":
        # Lane G window is 2027-28: 2027 has no fee in force; 2028 is the
        # intro year. Use the repo's 2028 taxable book for s, averaged
        # with 2027's zero -> halve it. Labelled: this is why the literal
        # Lane G window shows a small fee flow.
        res = run_scenario(s, beta)
        book = {a["year"]: a["taxable_book"] for a in res["annual"]}
        book_avg = book[2028] / 2.0
    elif book_basis == "mature":
        res = run_scenario(s, beta)
        book = {a["year"]: a["taxable_book"] for a in res["annual"]}
        book_avg = book[2032]
    else:
        raise ValueError("book_basis must be 'contemporaneous' or 'mature'")
    fee_net_lo = f_inc / 100.0 * book_avg * affected_share_lo * NET_RECEIPTS_FACTOR
    fee_net_hi = f_inc / 100.0 * book_avg * affected_share_hi * NET_RECEIPTS_FACTOR
    # Variant (i) demand: fee-regime contraction relative to conventional.
    def _dem(fee_net):
        first = MPC_INT_LO * (fee_net + d_iorb + d_coupon_avg), \
                MPC_INT_HI * (fee_net + d_iorb + d_coupon_avg)
        return first
    lo_first = _dem(fee_net_lo)[0]
    hi_first = _dem(fee_net_hi)[1]
    dem_lo, dem_hi = -hi_first * MULT_HI, -lo_first * MULT_LO
    g = gdp(2028)
    return EpisodeFlows(
        s=s, beta=beta, q_pp=q, drff_pp=drff, f_inc_pp=f_inc, wedge_pp=wedge,
        years=2, d_iorb_injection=d_iorb, d_coupon_injection_avg=d_coupon_avg,
        book_basis=book_basis, fee_net_lo=fee_net_lo, fee_net_hi=fee_net_hi,
        demand_lo=dem_lo, demand_hi=dem_hi,
        demand_pct_gdp_lo=100.0 * dem_lo / g, demand_pct_gdp_hi=100.0 * dem_hi / g)


# Lane G's measured FRB/US gap at s=0.75 (xgdp troughs, %): the yardstick.
FRBUS_GAP_S75_PP = 1.190 - 0.541   # 0.649 pp of GDP


def main():
    import csv
    from pathlib import Path
    outdir = Path(__file__).resolve().parents[2] / "results"
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    for s in DIALS:
        for f in regime_flows(s):
            g = gdp(f.year)
            rows.append({
                "scaling": "regime", "s": f.s, "beta": BETA_CENTRAL,
                "year": f.year,
                "injection_base_T": round(f.injection_base, 4),
                "injection_scen_T": round(f.injection_scen, 4),
                "iorb_expense_base_T": round(f.iorb_expense_base, 4),
                "interest_public_base_T": round(f.interest_public_base, 4),
                "gross_fee_T": round(f.gross_fee, 4),
                "net_fee_T": round(f.net_fee, 4),
                "e_iorb_removed_T": round(f.e_iorb, 4),
                "e_coupon_removed_T": round(f.e_coupon, 4),
                "e_fedheld_memo_T": round(f.e_fedheld_memo, 4),
                "injection_removed_T": round(f.injection_removed, 4),
                "private_income_removed_v1_T": round(f.private_income_removed_v1, 4),
                "sec_treasury_T": round(f.sec_treasury, 4),
                "sec_fed_T": round(f.sec_fed, 4),
                "sec_banks_lenders_T": round(f.sec_banks_lenders, 4),
                "sec_borrowers_T": round(f.sec_borrowers, 4),
                "sec_other_private_T": round(f.sec_other_private, 4),
                "sector_sum_T": round(f.sector_sum(), 10),
                "remittance_cash_delta_T": round(f.remittance_cash_delta, 4),
                "deferred_asset_base_T": round(f.deferred_asset_base, 4),
                "deferred_asset_scen_T": round(f.deferred_asset_scen, 4),
                "demand_v1_lo_T": round(f.demand_v1_lo, 4),
                "demand_v1_hi_T": round(f.demand_v1_hi, 4),
                "demand_v1_lo_pct_gdp": round(100 * f.demand_v1_lo / g, 3),
                "demand_v1_hi_pct_gdp": round(100 * f.demand_v1_hi / g, 3),
                "demand_v2_lo_T": round(f.demand_v2_lo, 4),
                "demand_v2_hi_T": round(f.demand_v2_hi, 4),
                "demand_v2_lo_pct_gdp": round(100 * f.demand_v2_lo / g, 3),
                "demand_v2_hi_pct_gdp": round(100 * f.demand_v2_hi / g, 3),
                "gdp_T": round(g, 2),
            })
    for basis in ("contemporaneous", "mature"):
        e = episode_flows(0.75, BETA_CENTRAL, book_basis=basis)
        rows.append({
            "scaling": f"episode_{basis}", "s": e.s, "beta": e.beta,
            "year": "per_episode_year",
            "injection_base_T": "", "injection_scen_T": "",
            "iorb_expense_base_T": "", "interest_public_base_T": "",
            "gross_fee_T": "", "net_fee_T": round((e.fee_net_lo + e.fee_net_hi) / 2, 4),
            "e_iorb_removed_T": round(e.d_iorb_injection, 4),
            "e_coupon_removed_T": round(e.d_coupon_injection_avg, 4),
            "e_fedheld_memo_T": "", "injection_removed_T":
                round(e.d_iorb_injection + e.d_coupon_injection_avg, 4),
            "private_income_removed_v1_T": "",
            "sec_treasury_T": "", "sec_fed_T": "", "sec_banks_lenders_T": "",
            "sec_borrowers_T": "", "sec_other_private_T": "",
            "sector_sum_T": "", "remittance_cash_delta_T": "",
            "deferred_asset_base_T": "", "deferred_asset_scen_T": "",
            "demand_v1_lo_T": round(e.demand_lo, 4),
            "demand_v1_hi_T": round(e.demand_hi, 4),
            "demand_v1_lo_pct_gdp": round(e.demand_pct_gdp_lo, 3),
            "demand_v1_hi_pct_gdp": round(e.demand_pct_gdp_hi, 3),
            "demand_v2_lo_T": "", "demand_v2_hi_T": "",
            "demand_v2_lo_pct_gdp": "", "demand_v2_hi_pct_gdp": "",
            "gdp_T": round(gdp(2028), 2),
            "fee_net_lo_T": round(e.fee_net_lo, 4),
            "fee_net_hi_T": round(e.fee_net_hi, 4),
            "f_inc_pp": round(e.f_inc_pp, 3), "drff_pp": round(e.drff_pp, 3),
            "wedge_pp": round(e.wedge_pp, 3),
            "frbus_gap_pp": FRBUS_GAP_S75_PP,
        })
    path = outdir / "flow_channel_v1.csv"
    fields = list(rows[0].keys())
    for r in rows:  # union of keys, stable order
        for k in r:
            if k not in fields:
                fields.append(k)
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})
    print(f"wrote {path} ({len(rows)} rows)")
    for s in DIALS:
        t = regime_totals(regime_flows(s))
        print(f"s={s:.2f} 10yr: gross_fee={t['gross_fee']:.3f} net_fee={t['net_fee']:.3f} "
              f"E_iorb={t['e_iorb']:.3f} E_coupon={t['e_coupon']:.3f} "
              f"injection_removed={t['injection_removed']:.3f} "
              f"private_removed_v1={t['private_income_removed_v1']:.3f}")
    for basis in ("contemporaneous", "mature"):
        e = episode_flows(0.75, BETA_CENTRAL, book_basis=basis)
        print(f"episode s=0.75 ({basis}): dIORB={e.d_iorb_injection:.4f} "
              f"dCoupon={e.d_coupon_injection_avg:.4f} fee_net=[{e.fee_net_lo:.4f},"
              f"{e.fee_net_hi:.4f}] demand=[{e.demand_lo:.4f},{e.demand_hi:.4f}] $T/yr "
              f"= [{e.demand_pct_gdp_lo:.3f},{e.demand_pct_gdp_hi:.3f}]% GDP "
              f"vs FRB/US gap {FRBUS_GAP_S75_PP:.3f}pp")
    return rows


if __name__ == "__main__":
    main()
