"""Behavioural extension of the v2 SFC skeleton: the Section IX experiment.

Purpose (Carlos A. Mucha memo, Nov 22, 2026, Sections III.B and IX): test
-- not assume -- the interest-income hypothesis. Under conventional
tightening, part of the restraint leaks back as interest income to
creditor households, whose spending offsets it. Under Monetary Symmetry
at the SAME combined policy-sensitive charge (conventional i = 4% versus
synchronized i = 2% + fee f = 2%), part of that charge is remitted to
Treasury instead. Whether the fee regime is more disinflationary per unit
of borrower cost depends on (a) who loses the interest income and their
MPC, (b) how much of the difference banks recapture through the deposit
spread and pay out as dividends, and (c) how Congress recycles the fee
revenue. This module books both regimes through the identical accounting
engine and measures the first-round demand impulse difference.

SPONSOR AMENDMENT (Nov 22, 2026, supersedes the memo's loan-only base):
bonds are IN the fee base, grandfathered identically to loans. The fee is
paid by lenders on covered loans AND by borrowing ISSUERS on covered
bonds -- nonfinancial businesses on post-effective-date bond issuance and
state & local governments on theirs. Coverage follows the borrower's
obligation (each obligation taxed exactly once; no separate charge on
MBS or intermediary funding instruments).

Design of the extension
-----------------------
* Households are split into two sub-sectors: HHC (creditor households --
  hold the bulk of deposits and securities, receive the dividends) and
  HHD (debtor households -- hold the mortgages and consumer credit).
  The accounting core is loaded as a PRIVATE patched copy (extended
  sector and instrument tables) so the skeleton's own module, scenario
  and 23-test suite are completely untouched.
* New instruments: CBN_COV / CBN_GRD (corporate bonds, covered /
  grandfathered vintages, issuer NFC) and MUN_COV / MUN_GRD (state &
  local bonds, issuer SLG), alongside the skeleton's LN_COV / LN_GRD.
* Behavioural rules (each parameterized from ../lit/LITERATURE.md):
    - deposit rate = 0.4 + beta_dep * IORB, beta_dep in {0.45,0.55,0.65}
      (Lit. section 4.1: blended easing beta 0.45-0.65);
    - covered-loan rate = spread + IORB + theta * fee, theta in
      {0.5, 0.75, 1.0} (Lit. section 2.3: pass-through grid, UNCALIBRATED
      at fee scale);
    - consumption of each household group responds to its policy-
      sensitive cash flow (interest received, dividends received,
      interest paid) with its group MPC: creditors 0.05-0.20, debtors
      0.50-1.00 (Lit. section 1.2). Intercepts are calibrated so the
      CONVENTIONAL regime reproduces baseline consumption at every grid
      point; only the difference between regimes is behavioural.
    - dividends of BNK / NBF / NFC respond to each sector's policy-
      sensitive financial margin relative to the conventional
      configuration (payout ratios are ASSUMED, flagged in the results);
    - new covered lending volume responds to the all-in covered rate
      with semi-elasticity eps (ASSUMED, flagged; sensitivity-run);
    - revenue recycling is a SCENARIO, never averaged (Lit. section
      1.4): "deficit" (no spending of receipts), "transfers" (fee
      revenue transferred lump-sum to debtor households), "purchases"
      (fee revenue spent on government purchases from NFC).
* Held fixed across regimes BY CONSTRUCTION (stated, not hidden):
  Treasury and bond/muni coupon yields (the term-structure response tau
  is UNCALIBRATED per Lit. section 4.3 and belongs to another lane; two
  sensitivity switches relax this: grandfathered-book repricing and
  covered-bond coupon repricing). The grandfathered loan book's rate is
  held at the conventional level in both regimes in the headline runs,
  per Lit. section 1.3 (~92% of US mortgages are fixed-rate).

This is a one-period, first-round, qualitative-quantitative SFC
experiment. It is NOT a forecasting model and its magnitudes are NOT
FRB/US-comparable. See SECTION_IX_RESULTS.md.
"""

import importlib.util
import sys
import types
from dataclasses import dataclass, field
from pathlib import Path

_HERE = Path(__file__).parent


# ---------------------------------------------------------------------------
# Private patched copy of the accounting core (9 sectors, split households,
# covered/grandfathered bond instruments). The skeleton's sfc_core module
# is NOT mutated: the original test suite runs against it unchanged.
# ---------------------------------------------------------------------------

def _load_patched_core():
    spec = importlib.util.spec_from_file_location(
        "sfc_core_ix", _HERE / "sfc_core.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    mod.SECTORS = ["TRE", "FED", "BNK", "NBF", "HHC", "HHD",
                   "NFC", "SLG", "ROW"]
    mod.SECTOR_NAMES = {
        "TRE": "Treasury", "FED": "Federal Reserve",
        "BNK": "Commercial banks", "NBF": "Nonbank lenders",
        "HHC": "Households, creditor", "HHD": "Households, debtor",
        "NFC": "Nonfinancial businesses",
        "SLG": "State & local governments",
        "ROW": "Foreign sector (rest of world)",
    }
    mod.FINANCIAL_INSTRUMENTS = {
        "RES":    {"name": "Reserve balances at the Fed",
                   "assets": {"BNK"}, "liabilities": {"FED"}},
        "TGA":    {"name": "Treasury General Account at the Fed",
                   "assets": {"TRE"}, "liabilities": {"FED"}},
        "TS_PUB": {"name": "Treasury securities, public-held",
                   "assets": {"BNK", "NBF", "HHC", "NFC", "SLG", "ROW"},
                   "liabilities": {"TRE"}},
        "TS_FED": {"name": "Treasury securities, Fed-held",
                   "assets": {"FED"}, "liabilities": {"TRE"}},
        "FEDPAY": {"name": "Fed remittances payable, net of deferred asset",
                   "assets": {"TRE"}, "liabilities": {"FED"}},
        "DEP":    {"name": "Deposits at commercial banks",
                   "assets": {"NBF", "HHC", "HHD", "NFC", "SLG", "ROW"},
                   "liabilities": {"BNK"}},
        "LN_COV": {"name": "Loans, COVERED (post-enactment originations)",
                   "assets": {"BNK", "NBF"}, "liabilities": {"HHD", "NFC"}},
        "LN_GRD": {"name": "Loans, GRANDFATHERED (pre-enactment)",
                   "assets": {"BNK", "NBF"}, "liabilities": {"HHD", "NFC"}},
        "CBN_COV": {"name": "Corporate bonds, COVERED (post-effective-date)",
                    "assets": {"BNK", "NBF", "HHC", "ROW"},
                    "liabilities": {"NFC"}},
        "CBN_GRD": {"name": "Corporate bonds, GRANDFATHERED",
                    "assets": {"BNK", "NBF", "HHC", "ROW"},
                    "liabilities": {"NFC"}},
        "MUN_COV": {"name": "State & local bonds, COVERED "
                            "(post-effective-date)",
                    "assets": {"BNK", "NBF", "HHC", "ROW"},
                    "liabilities": {"SLG"}},
        "MUN_GRD": {"name": "State & local bonds, GRANDFATHERED",
                    "assets": {"BNK", "NBF", "HHC", "ROW"},
                    "liabilities": {"SLG"}},
        "EQ":     {"name": "Equities (book value)",
                   "assets": {"HHC", "ROW"}, "liabilities": {"BNK", "NBF", "NFC"}},
        "CUR":    {"name": "Currency in circulation",
                   "assets": {"HHC", "HHD", "ROW"}, "liabilities": {"FED"}},
    }
    mod.TANGIBLE_INSTRUMENTS = {
        "K": {"name": "Tangible assets (capital stock, housing, public "
                      "assets)",
              "assets": {"HHC", "HHD", "NFC", "SLG"}, "liabilities": set()},
    }
    mod.ALL_INSTRUMENTS = {**mod.FINANCIAL_INSTRUMENTS,
                           **mod.TANGIBLE_INSTRUMENTS}
    return mod


core = _load_patched_core()
sys.modules.setdefault("sfc_core_ix", core)

# Reuse the skeleton's settlement helpers, bound to the patched core: the
# helpers are institutional plumbing (deposits / TGA / reserves) and are
# sector-agnostic except for the banking sector itself.
_src = (_HERE / "scenario.py").read_text().replace(
    "from sfc_core import", "from sfc_core_ix import")
_scen = types.ModuleType("scenario_ix")
exec(compile(_src, "scenario_ix", "exec"), _scen.__dict__)
_deposit_shift = _scen._deposit_shift
_tga_settle_out = _scen._tga_settle_out
pay_via_deposits = _scen.pay_via_deposits
treasury_pay = _scen.treasury_pay
treasury_receive = _scen.treasury_receive
pay_treasury_from_reserves = _scen.pay_treasury_from_reserves
fed_pay_via_reserves = _scen.fed_pay_via_reserves

BalanceSheet = core.BalanceSheet
Period = core.Period
Transaction = core.Transaction


# ---------------------------------------------------------------------------
# Opening balance sheet for the experiment ($T, illustrative, skeleton-scale;
# household stocks split HHC/HHD; SLG now carries bond debt, which the
# skeleton did not model -- flagged in SECTION_IX_RESULTS.md)
# ---------------------------------------------------------------------------

def opening_balance_sheet_ix() -> BalanceSheet:
    e = {}
    def A(inst, sec, v): e[(inst, sec)] = v
    def L(inst, sec, v): e[(inst, sec)] = -v

    A("RES", "BNK", 3.00);  L("RES", "FED", 3.00)
    A("TGA", "TRE", 0.80);  L("TGA", "FED", 0.80)
    A("TS_FED", "FED", 4.40); L("TS_FED", "TRE", 4.40)
    L("TS_PUB", "TRE", 31.60)
    for sec, v in [("BNK", 5.0), ("NBF", 10.0), ("HHC", 5.0),
                   ("NFC", 0.8), ("SLG", 1.8), ("ROW", 9.0)]:
        A("TS_PUB", sec, v)
    A("DEP", "NBF", 0.50); A("DEP", "HHC", 9.00); A("DEP", "HHD", 2.00)
    A("DEP", "NFC", 4.50); A("DEP", "SLG", 1.00); A("DEP", "ROW", 1.00)
    L("DEP", "BNK", 18.00)
    A("LN_COV", "BNK", 4.00); A("LN_COV", "NBF", 1.50)
    L("LN_COV", "HHD", 3.50); L("LN_COV", "NFC", 2.00)
    A("LN_GRD", "BNK", 9.00); A("LN_GRD", "NBF", 4.00)
    L("LN_GRD", "HHD", 8.00); L("LN_GRD", "NFC", 5.00)
    A("CBN_COV", "BNK", 0.40); A("CBN_COV", "NBF", 1.40)
    A("CBN_COV", "HHC", 0.60); A("CBN_COV", "ROW", 0.40)
    L("CBN_COV", "NFC", 2.80)
    A("CBN_GRD", "BNK", 0.60); A("CBN_GRD", "NBF", 2.10)
    A("CBN_GRD", "HHC", 0.90); A("CBN_GRD", "ROW", 0.60)
    L("CBN_GRD", "NFC", 4.20)
    A("MUN_COV", "BNK", 0.30); A("MUN_COV", "NBF", 0.50)
    A("MUN_COV", "HHC", 0.70); A("MUN_COV", "ROW", 0.20)
    L("MUN_COV", "SLG", 1.70)
    A("MUN_GRD", "BNK", 0.50); A("MUN_GRD", "NBF", 0.80)
    A("MUN_GRD", "HHC", 1.10); A("MUN_GRD", "ROW", 0.30)
    L("MUN_GRD", "SLG", 2.70)
    L("EQ", "BNK", 2.00); L("EQ", "NBF", 1.00); L("EQ", "NFC", 12.00)
    A("EQ", "HHC", 11.00); A("EQ", "ROW", 4.00)
    A("CUR", "HHC", 1.20); A("CUR", "HHD", 0.60); A("CUR", "ROW", 0.50)
    L("CUR", "FED", 2.30)
    A("K", "HHC", 5.00); A("K", "HHD", 10.00)
    A("K", "NFC", 20.00); A("K", "SLG", 5.00)
    return BalanceSheet(e)


COVERED_INSTRUMENTS = ("LN_COV", "CBN_COV", "MUN_COV")


# ---------------------------------------------------------------------------
# Behavioural specification
# ---------------------------------------------------------------------------

@dataclass
class BehaviorSpec:
    regime: str = "B"            # "A" conventional, "B" synchronized fee
    iorb: float = 2.0            # % ; regime A uses 4.0, fee 0
    fee_rate: float = 2.0        # % ; f == i after synchronization
    beta_dep: float = 0.55       # deposit beta (Lit. 4.1)
    theta: float = 1.0           # fee pass-through to covered-loan rates
    mpc_cred: float = 0.125      # creditor MPC out of interest income
    mpc_debt: float = 0.75       # debtor MPC out of cash flow
    salience: float = 1.0        # interest-income salience discount (Lit. 1.4)
    recycling: str = "deficit"   # deficit | transfers | purchases
    eps_credit: float = 0.03     # new-lending semi-elasticity per pp (ASSUMED)
    grd_repricing: bool = False  # sensitivity: grandfathered book follows IORB
    bond_repricing: bool = False # sensitivity: covered coupons fall by f
    payout: dict = field(default_factory=lambda: {
        "BNK": 0.6, "NBF": 0.6, "NFC": 0.5})   # ASSUMED payout ratios

    # Rate structure (% per period). Spreads are configuration-invariant.
    dep_spread: float = 0.4
    spread_cov: float = 2.0
    spread_grd: float = 1.5
    treasury_yield: float = 3.5
    bond_rate: float = 5.0
    muni_rate: float = 4.0
    fed_opex: float = 0.02
    conv_iorb: float = 4.0       # the conventional configuration's IORB

    def conventional(self) -> "BehaviorSpec":
        """The Regime-A twin of this spec: same grid parameters, IORB at
        the conventional level, no fee, no recycling (no revenue)."""
        kw = {k: v for k, v in self.__dict__.items()}
        kw.update(regime="A", iorb=self.conv_iorb, fee_rate=0.0,
                  recycling="deficit")
        return BehaviorSpec(**kw)


def _rates(spec: BehaviorSpec) -> dict:
    """All period rates (%) implied by a spec."""
    dep = spec.dep_spread + spec.beta_dep * spec.iorb
    cov = spec.spread_cov + spec.iorb + spec.theta * spec.fee_rate
    if spec.grd_repricing:
        grd = spec.spread_grd + spec.iorb
    else:
        # Headline: the grandfathered book's rate is locked at the
        # conventional configuration's level in BOTH regimes (Lit. 1.3:
        # ~92% of US mortgages are fixed-rate).
        grd = spec.spread_grd + spec.conv_iorb
    bond_cov = spec.bond_rate - (spec.fee_rate if spec.bond_repricing else 0.0)
    muni_cov = spec.muni_rate - (spec.fee_rate if spec.bond_repricing else 0.0)
    return {"dep": dep, "cov": cov, "grd": grd,
            "bond_cov": bond_cov, "bond_grd": spec.bond_rate,
            "muni_cov": muni_cov, "muni_grd": spec.muni_rate,
            "tsy": spec.treasury_yield, "iorb": spec.iorb}


def _int(stock, rate_pct):
    return stock * rate_pct / 100.0


def policy_flows(opening: BalanceSheet, spec: BehaviorSpec) -> dict:
    """Closed-form interest / fee / Fed-income amounts for a spec, on
    opening stocks. The period builder books EXACTLY these amounts, and
    the consumption / dividend rules read them -- one source of truth."""
    bs = opening
    r = _rates(spec)
    F = {"rates": r}

    # Loan interest by (instrument, lender, borrower)
    loan = {}
    for inst, rate in (("LN_COV", r["cov"]), ("LN_GRD", r["grd"])):
        total_liab = -(bs.get(inst, "HHD") + bs.get(inst, "NFC"))
        for lender in ("BNK", "NBF"):
            ls = bs.get(inst, lender)
            for borrower in ("HHD", "NFC"):
                share = (-bs.get(inst, borrower) / total_liab
                         if total_liab else 0.0)
                loan[(inst, lender, borrower)] = _int(ls * share, rate)
    F["loan"] = loan
    F["loan_paid"] = {b: sum(v for (i, l, bb), v in loan.items() if bb == b)
                      for b in ("HHD", "NFC")}
    F["loan_recv"] = {l: sum(v for (i, ll, b), v in loan.items() if ll == l)
                      for l in ("BNK", "NBF")}

    F["dep_int"] = {h: _int(bs.get("DEP", h), r["dep"])
                    for h in ("NBF", "HHC", "HHD", "NFC", "SLG", "ROW")}
    F["dep_int_total"] = sum(F["dep_int"].values())
    F["iorb_amt"] = _int(bs.get("RES", "BNK"), spec.iorb)
    F["ts_pub"] = {h: _int(bs.get("TS_PUB", h), r["tsy"])
                   for h in ("BNK", "NBF", "HHC", "NFC", "SLG", "ROW")}
    F["ts_fed"] = _int(bs.get("TS_FED", "FED"), r["tsy"])

    sec_int = {}
    for inst, rate in (("CBN_COV", r["bond_cov"]), ("CBN_GRD", r["bond_grd"]),
                       ("MUN_COV", r["muni_cov"]), ("MUN_GRD", r["muni_grd"])):
        for holder in ("BNK", "NBF", "HHC", "ROW"):
            sec_int[(inst, holder)] = _int(bs.get(inst, holder), rate)
    F["sec_int"] = sec_int
    F["sec_recv"] = {h: sum(v for (i, hh), v in sec_int.items() if hh == h)
                     for h in ("BNK", "NBF", "HHC", "ROW")}
    F["sec_paid"] = {
        "NFC": sum(v for (i, h), v in sec_int.items() if i.startswith("CBN")),
        "SLG": sum(v for (i, h), v in sec_int.items() if i.startswith("MUN"))}

    # THE FEE -- lender-paid on covered loans; issuer-paid on covered
    # bonds (sponsor amendment, Nov 22 2026). Taxed exactly once, on the
    # borrower's obligation; grandfathered vintages never pay.
    fr = spec.fee_rate
    F["fee_bnk"] = _int(bs.get("LN_COV", "BNK"), fr)
    F["fee_nbf"] = _int(bs.get("LN_COV", "NBF"), fr)
    F["fee_nfc"] = _int(-bs.get("CBN_COV", "NFC"), fr)
    F["fee_slg"] = _int(-bs.get("MUN_COV", "SLG"), fr)
    F["fee_total"] = F["fee_bnk"] + F["fee_nbf"] + F["fee_nfc"] + F["fee_slg"]

    F["fed_income"] = F["ts_fed"] - F["iorb_amt"] - spec.fed_opex
    return F


# ---------------------------------------------------------------------------
# Behavioural calibration: dividends and consumption
# ---------------------------------------------------------------------------

DIV0 = {"BNK": 0.25, "NBF": 0.08, "NFC": 0.9}     # skeleton baselines ($T)
DIV_ROW_SHARE = 0.19                               # skeleton convention
C0 = {"HHD": 8.0, "HHC": 3.0}                      # baseline consumption ($T)
WAGE_SPLIT = {"HHD": 9.6, "HHC": 2.4}              # of 12.0 total wages


def _fin_margin(F, sector):
    """Policy-sensitive financial margin entering the dividend rule."""
    if sector == "BNK":
        return (F["loan_recv"]["BNK"] + F["ts_pub"]["BNK"]
                + F["sec_recv"]["BNK"] + F["iorb_amt"]
                - F["dep_int_total"] - F["fee_bnk"])
    if sector == "NBF":
        return (F["loan_recv"]["NBF"] + F["ts_pub"]["NBF"]
                + F["sec_recv"]["NBF"] + F["dep_int"]["NBF"] - F["fee_nbf"])
    if sector == "NFC":
        return (-F["loan_paid"]["NFC"] - F["sec_paid"]["NFC"] - F["fee_nfc"])
    raise KeyError(sector)


def dividends(opening, spec) -> dict:
    """Dividend by payer: baseline plus payout share of the change in the
    sector's policy-sensitive financial margin vs the conventional
    configuration (same grid point). Floored at zero."""
    F = policy_flows(opening, spec)
    FA = policy_flows(opening, spec.conventional())
    out = {}
    for sec in ("BNK", "NBF", "NFC"):
        d = DIV0[sec] + spec.payout[sec] * (_fin_margin(F, sec)
                                            - _fin_margin(FA, sec))
        out[sec] = max(0.0, d)
    out["total"] = sum(out.values())
    out["to_hhc"] = out["total"] * (1.0 - DIV_ROW_SHARE)
    out["to_row"] = out["total"] * DIV_ROW_SHARE
    return out


def _household_policy_income(opening, spec, divs=None):
    """(interest part, dividend part) of each household group's policy-
    sensitive cash flow. Debtors' interest part is net of interest PAID."""
    F = policy_flows(opening, spec)
    if divs is None:
        divs = dividends(opening, spec)
    int_hhc = (F["dep_int"]["HHC"] + F["ts_pub"]["HHC"]
               + F["sec_recv"]["HHC"])
    int_hhd = F["dep_int"]["HHD"] - F["loan_paid"]["HHD"]
    return {"HHC": (int_hhc, divs["to_hhc"]),
            "HHD": (int_hhd, 0.0)}


def consumption(opening, spec) -> dict:
    """Consumption by household group. Intercepts are calibrated on the
    conventional twin so Regime A reproduces C0 at every grid point;
    Regime B's consumption is then purely the behavioural response.
    Recycling transfers to debtors enter debtor cash flow directly."""
    divs = dividends(opening, spec)
    pol = _household_policy_income(opening, spec, divs)
    specA = spec.conventional()
    polA = _household_policy_income(opening, specA,
                                    dividends(opening, specA))
    out = {}
    for g, mpc in (("HHC", spec.mpc_cred), ("HHD", spec.mpc_debt)):
        if g == "HHC":
            eff = lambda p: spec.salience * p[0] + p[1]
        else:
            eff = lambda p: p[0] + p[1]
        alpha = C0[g] - mpc * eff(polA[g])
        c = alpha + mpc * eff(pol[g])
        if g == "HHD" and spec.regime == "B" and spec.recycling == "transfers":
            c += spec.mpc_debt * policy_flows(opening, spec)["fee_total"]
        out[g] = c
    return out


def new_lending_factor(opening, spec) -> float:
    """Credit-demand response: new covered lending scales with the gap
    between this regime's all-in covered rate and the conventional one."""
    gap_pp = _rates(spec)["cov"] - _rates(spec.conventional())["cov"]
    return max(0.0, 1.0 - spec.eps_credit * gap_pp)


# ---------------------------------------------------------------------------
# Period builder -- same institutional plumbing as the skeleton, behavioural
# consumption / dividends / credit volume, split households, bond fees.
# ---------------------------------------------------------------------------

# Exogenous flows carried over from the skeleton (unchanged totals).
WAGES = {"NFC": 9.0, "BNK": 0.6, "NBF": 0.2, "TRE": 1.2, "SLG": 1.0}
GOV_PURCH_TRE, GOV_PURCH_SLG = 2.5, 1.2
TAXES_TRE = {"HHD": 2.4, "HHC": 0.8, "NFC": 1.2, "NBF": 0.05}
TAXES_TRE_BNK = 0.15
TAXES_SLG = {"HHD": 0.7, "HHC": 0.2, "NFC": 0.4}
TRANSFERS_TRE = {"HHD": 3.0, "HHC": 0.4}
TRANSFERS_SLG = {"HHD": 0.4, "HHC": 0.1}
NET_EXPORTS = 0.6
NEW_COVERED = {"BNK": {"HHD": 0.9, "NFC": 0.6}, "NBF": {"HHD": 0.3}}
COVERED_REPAY = {"BNK": {"HHD": 0.35, "NFC": 0.25}, "NBF": {"HHD": 0.12}}
GRD_REPAY = {"BNK": {"HHD": 0.55, "NFC": 0.35},
             "NBF": {"HHD": 0.25, "NFC": 0.15}}
TS_ISSUANCE = 1.6
ISSUANCE_SHARES = {"BNK": 0.15, "NBF": 0.30, "HHC": 0.10,
                   "NFC": 0.05, "SLG": 0.05, "ROW": 0.35}
FED_TS_PURCHASE = 0.2
BOND_ISSUANCE = {"NBF": 0.20, "HHC": 0.10}   # new issuance = covered vintage
EQUITY_ISSUANCE = 0.1


def build_period_ix(opening: BalanceSheet, spec: BehaviorSpec) -> Period:
    bs = opening
    F = policy_flows(opening, spec)
    divs = dividends(opening, spec)
    cons = consumption(opening, spec)
    vf = new_lending_factor(opening, spec)
    p = Period(opening)

    # ---- wages (split across household groups) ---------------------------
    wages = Transaction("Wages")
    for payer, amt in WAGES.items():
        wages.leg(payer, "current", -amt)
        for g, share_amt in ((g, amt * WAGE_SPLIT[g] / 12.0)
                             for g in ("HHD", "HHC")):
            wages.leg(g, "current", +share_amt)
            if payer == "TRE":
                wages.delta("DEP", g, +share_amt).leg(g, "capital", -share_amt)
                wages.delta("DEP", "BNK", -share_amt) \
                     .leg("BNK", "capital", +share_amt)
            else:
                _deposit_shift(wages, payer, g, share_amt)
        if payer == "TRE":
            _tga_settle_out(wages, amt)
    p.add(wages)

    # ---- behavioural consumption ------------------------------------------
    for g in ("HHD", "HHC"):
        p.add(pay_via_deposits(f"Consumption ({g})", g, "NFC", cons[g]))

    # ---- government purchases (+ recycling purchases in Regime B) ---------
    purch = GOV_PURCH_TRE
    if spec.regime == "B" and spec.recycling == "purchases":
        purch += F["fee_total"]
    p.add(treasury_pay("Government purchases (federal)", "NFC", purch))
    p.add(pay_via_deposits("Government purchases (state/local)", "SLG",
                           "NFC", GOV_PURCH_SLG))

    # ---- investment ---------------------------------------------------------
    inv_nfc = Transaction("Investment (NFC own capital formation)")
    inv_nfc.leg("NFC", "current", +3.0).leg("NFC", "capital", -3.0)
    inv_nfc.delta("K", "NFC", +3.0)
    p.add(inv_nfc)
    housing = pay_via_deposits("Investment (household housing)", "HHD",
                               "NFC", 0.8, current=False)
    housing.leg("NFC", "current", +0.8).leg("HHD", "capital", -0.8)
    housing.delta("K", "HHD", +0.8)
    p.add(housing)
    slg_inv = pay_via_deposits("Investment (state/local)", "SLG", "NFC",
                               0.4, current=False)
    slg_inv.leg("NFC", "current", +0.4).leg("SLG", "capital", -0.4)
    slg_inv.delta("K", "SLG", +0.4)
    p.add(slg_inv)

    # ---- taxes and transfers -------------------------------------------------
    for payer, amt in TAXES_TRE.items():
        p.add(treasury_receive(f"Taxes to Treasury ({payer})", payer, amt))
    p.add(pay_treasury_from_reserves("Taxes to Treasury (BNK)", TAXES_TRE_BNK))
    for payer, amt in TAXES_SLG.items():
        p.add(pay_via_deposits(f"Taxes to state/local ({payer})", payer,
                               "SLG", amt))
    for g, amt in TRANSFERS_TRE.items():
        p.add(treasury_pay(f"Transfers to households (federal, {g})", g, amt))
    for g, amt in TRANSFERS_SLG.items():
        p.add(pay_via_deposits(f"Transfers to households (state/local, {g})",
                               "SLG", g, amt))
    if spec.regime == "B" and spec.recycling == "transfers":
        p.add(treasury_pay("Transfers to households (recycled fee revenue)",
                           "HHD", F["fee_total"]))

    # ---- net exports ----------------------------------------------------------
    nx = Transaction("Net exports")
    nx.leg("NFC", "current", +NET_EXPORTS).leg("ROW", "current", -NET_EXPORTS)
    _deposit_shift(nx, "ROW", "NFC", NET_EXPORTS)
    p.add(nx)

    # ---- dividends (behavioural) ----------------------------------------------
    div = Transaction("Dividends and distributed profits")
    total_div = divs["total"]
    for payer in ("BNK", "NBF", "NFC"):
        amt = divs[payer]
        if not amt:
            continue
        div.leg(payer, "current", -amt)
        _deposit_shift(div, payer, "HHC", amt * (1.0 - DIV_ROW_SHARE))
        _deposit_shift(div, payer, "ROW", amt * DIV_ROW_SHARE)
    div.leg("HHC", "current", +divs["to_hhc"]) \
       .leg("ROW", "current", +divs["to_row"])
    p.add(div)

    # ---- loan interest -----------------------------------------------------------
    for inst, label in (("LN_COV", "covered"), ("LN_GRD", "grandfathered")):
        for lender in ("BNK", "NBF"):
            for borrower in ("HHD", "NFC"):
                amt = F["loan"][(inst, lender, borrower)]
                if amt:
                    p.add(pay_via_deposits(
                        f"Interest on {label} loans ({borrower}->{lender})",
                        borrower, lender, amt))

    # ---- deposit interest -----------------------------------------------------------
    dep_int = Transaction("Interest on deposits")
    for holder, amt in F["dep_int"].items():
        if amt:
            dep_int.leg(holder, "current", +amt)
            _deposit_shift(dep_int, "BNK", holder, amt)
    dep_int.leg("BNK", "current", -F["dep_int_total"])
    p.add(dep_int)

    # ---- IORB -----------------------------------------------------------------------
    p.add(fed_pay_via_reserves("Interest on reserve balances (IORB)",
                               "BNK", F["iorb_amt"]))

    # ---- Treasury interest ------------------------------------------------------------
    ts_pub = Transaction("Interest on Treasury securities (public-held)")
    total_pub = 0.0
    for holder, amt in F["ts_pub"].items():
        if not amt:
            continue
        total_pub += amt
        ts_pub.leg(holder, "current", +amt)
        _tga_settle_out(ts_pub, amt)
        if holder != "BNK":
            ts_pub.delta("DEP", holder, +amt).leg(holder, "capital", -amt)
            ts_pub.delta("DEP", "BNK", -amt).leg("BNK", "capital", +amt)
    ts_pub.leg("TRE", "current", -total_pub)
    p.add(ts_pub)

    tint = Transaction("Interest on Treasury securities (Fed-held)")
    tint.leg("TRE", "current", -F["ts_fed"]).leg("FED", "current", +F["ts_fed"])
    tint.delta("TGA", "TRE", -F["ts_fed"]).leg("TRE", "capital", +F["ts_fed"])
    tint.delta("TGA", "FED", +F["ts_fed"]).leg("FED", "capital", -F["ts_fed"])
    p.add(tint)

    # ---- bond and muni interest (issuers NFC / SLG pay holders) -----------------------
    for inst, issuer, label in (("CBN_COV", "NFC", "corporate bonds (covered)"),
                                ("CBN_GRD", "NFC", "corporate bonds (grandfathered)"),
                                ("MUN_COV", "SLG", "state/local bonds (covered)"),
                                ("MUN_GRD", "SLG", "state/local bonds (grandfathered)")):
        txn = Transaction(f"Interest on {label}")
        tot = 0.0
        for holder in ("BNK", "NBF", "HHC", "ROW"):
            amt = F["sec_int"][(inst, holder)]
            if amt:
                txn.leg(holder, "current", +amt)
                _deposit_shift(txn, issuer, holder, amt)
                tot += amt
        txn.leg(issuer, "current", -tot)
        p.add(txn)

    # ---- THE FEDERAL CREDIT FEE ---------------------------------------------------------
    # Lender-paid on covered loans (banks settle in reserves, nonbanks from
    # deposits); issuer-paid on covered bonds (sponsor amendment).
    if F["fee_bnk"]:
        p.add(pay_treasury_from_reserves("Federal Credit Fee (banks)",
                                         F["fee_bnk"]))
    if F["fee_nbf"]:
        p.add(treasury_receive("Federal Credit Fee (nonbanks)", "NBF",
                               F["fee_nbf"]))
    if F["fee_nfc"]:
        p.add(treasury_receive(
            "Federal Credit Fee (NFC bond issuers)", "NFC", F["fee_nfc"]))
    if F["fee_slg"]:
        p.add(treasury_receive(
            "Federal Credit Fee (SLG bond issuers)", "SLG", F["fee_slg"]))

    # ---- Fed opex, remittance accrual and cash -------------------------------------------
    p.add(fed_pay_via_reserves("Federal Reserve operating expenses",
                               "HHD", spec.fed_opex))
    income = F["fed_income"]
    opening_payable = bs.get("FEDPAY", "TRE")
    accrual = Transaction("Fed earnings accrual to remittance position")
    accrual.leg("FED", "current", -income).leg("TRE", "current", +income)
    accrual.delta("FEDPAY", "TRE", +income).leg("TRE", "capital", -income)
    accrual.delta("FEDPAY", "FED", -income).leg("FED", "capital", +income)
    p.add(accrual)
    cash_remittance = max(0.0, opening_payable + income)
    if cash_remittance > 0:
        remit = Transaction("Fed cash remittance to Treasury")
        remit.delta("FEDPAY", "TRE", -cash_remittance) \
             .leg("TRE", "capital", +cash_remittance)
        remit.delta("FEDPAY", "FED", +cash_remittance) \
             .leg("FED", "capital", -cash_remittance)
        remit.delta("TGA", "TRE", +cash_remittance) \
             .leg("TRE", "capital", -cash_remittance)
        remit.delta("TGA", "FED", -cash_remittance) \
             .leg("FED", "capital", +cash_remittance)
        p.add(remit)

    # ---- lending and repayment (capital account; new covered lending is
    # ---- behaviourally scaled by the credit-demand rule) ----------------------
    for lender, borrowers in NEW_COVERED.items():
        for borrower, base_amt in borrowers.items():
            amt = base_amt * vf
            txn = Transaction(f"New covered loans ({lender}->{borrower})")
            txn.leg(lender, "capital", -amt).leg(borrower, "capital", +amt)
            txn.delta("LN_COV", lender, +amt).delta("LN_COV", borrower, -amt)
            if lender == "BNK":
                txn.delta("DEP", borrower, +amt) \
                   .leg(borrower, "capital", -amt)
                txn.delta("DEP", "BNK", -amt).leg("BNK", "capital", +amt)
            else:
                _deposit_shift(txn, lender, borrower, amt)
            p.add(txn)
    for book, bookmap, label in [
            ("LN_COV", COVERED_REPAY, "Covered loan repayments"),
            ("LN_GRD", GRD_REPAY, "Grandfathered loan repayments")]:
        for lender, borrowers in bookmap.items():
            for borrower, amt in borrowers.items():
                txn = pay_via_deposits(f"{label} ({borrower}->{lender})",
                                       borrower, lender, amt, current=False)
                txn.delta(book, lender, -amt).delta(book, borrower, +amt)
                txn.leg(lender, "capital", +amt) \
                   .leg(borrower, "capital", -amt)
                p.add(txn)

    # ---- Treasury issuance, Fed purchases, bond & equity issuance --------------
    for holder, share in ISSUANCE_SHARES.items():
        amt = TS_ISSUANCE * share
        txn = Transaction(f"Treasury issuance (public, {holder})")
        txn.delta("TS_PUB", "TRE", -amt).leg("TRE", "capital", +amt)
        txn.delta("TS_PUB", holder, +amt).leg(holder, "capital", -amt)
        txn.delta("TGA", "TRE", +amt).leg("TRE", "capital", -amt)
        txn.delta("TGA", "FED", -amt).leg("FED", "capital", +amt)
        txn.delta("RES", "FED", +amt).leg("FED", "capital", -amt)
        if holder == "BNK":
            txn.delta("RES", "BNK", -amt).leg("BNK", "capital", +amt)
        else:
            txn.delta("DEP", holder, -amt).leg(holder, "capital", +amt)
            txn.delta("DEP", "BNK", +amt).leg("BNK", "capital", -amt)
            txn.delta("RES", "BNK", -amt).leg("BNK", "capital", +amt)
        p.add(txn)

    qe = Transaction("Fed purchases of Treasury securities (from banks)")
    amt = FED_TS_PURCHASE
    qe.delta("TS_FED", "FED", +amt).leg("FED", "capital", -amt)
    qe.delta("TS_FED", "TRE", -amt).leg("TRE", "capital", +amt)
    qe.delta("TS_PUB", "TRE", +amt).leg("TRE", "capital", -amt)
    qe.delta("TS_PUB", "BNK", -amt).leg("BNK", "capital", +amt)
    qe.delta("RES", "BNK", +amt).leg("BNK", "capital", -amt)
    qe.delta("RES", "FED", -amt).leg("FED", "capital", +amt)
    p.add(qe)

    for holder, amt in BOND_ISSUANCE.items():
        txn = pay_via_deposits(f"Corporate bond issuance ({holder})",
                               holder, "NFC", amt, current=False)
        txn.delta("CBN_COV", holder, +amt).delta("CBN_COV", "NFC", -amt)
        txn.leg(holder, "capital", -amt).leg("NFC", "capital", +amt)
        p.add(txn)

    eq = pay_via_deposits("Equity issuance (HHC buys NFC shares)", "HHC",
                          "NFC", EQUITY_ISSUANCE, current=False)
    eq.delta("EQ", "HHC", +EQUITY_ISSUANCE) \
      .delta("EQ", "NFC", -EQUITY_ISSUANCE)
    eq.leg("HHC", "capital", -EQUITY_ISSUANCE) \
      .leg("NFC", "capital", +EQUITY_ISSUANCE)
    p.add(eq)

    return p


# ---------------------------------------------------------------------------
# The Section IX comparison
# ---------------------------------------------------------------------------

def run_pair(opening: BalanceSheet, spec: BehaviorSpec) -> dict:
    """Run Regime A (conventional twin) and Regime B (the given spec)
    through the identical builder; return the demand-impulse comparison
    with its channel decomposition. All amounts $T."""
    specA = spec.conventional()
    resA = build_period_ix(opening, specA).close()
    resB = build_period_ix(opening, spec).close()
    FA, FB = policy_flows(opening, specA), policy_flows(opening, spec)
    divA, divB = dividends(opening, specA), dividends(opening, spec)
    polA = _household_policy_income(opening, specA, divA)
    polB = _household_policy_income(opening, spec, divB)

    def cons_of(res, g):
        return -res.row_total(f"Consumption ({g})", sector=g,
                              account="current")

    dC_hhc = cons_of(resB, "HHC") - cons_of(resA, "HHC")
    dC_hhd = cons_of(resB, "HHD") - cons_of(resA, "HHD")
    dG = (resB.row_total("Government purchases (federal)", sector="TRE",
                         account="current")
          - resA.row_total("Government purchases (federal)", sector="TRE",
                           account="current"))
    dG = -dG  # purchases are a TRE payment; demand rises when it grows
    base_lending = sum(sum(b.values()) for b in NEW_COVERED.values())
    dVol = base_lending * (new_lending_factor(opening, spec) - 1.0)

    impulse = dC_hhc + dC_hhd + dG + dVol
    ifm = FA["loan_paid"]["HHD"] + FA["loan_paid"]["NFC"]  # Regime-A loan
    # interest paid by private borrowers: the interest-flow magnitude.

    decomp = {
        "creditor_interest": spec.mpc_cred * spec.salience
                             * (polB["HHC"][0] - polA["HHC"][0]),
        "creditor_dividends": spec.mpc_cred * (divB["to_hhc"] - divA["to_hhc"]),
        "debtor_cashflow": spec.mpc_debt * (polB["HHD"][0] - polA["HHD"][0]),
        "recycling_transfers": (spec.mpc_debt * FB["fee_total"]
                                if spec.recycling == "transfers" else 0.0),
        "recycling_purchases": dG,
        "credit_volume": dVol,
    }
    return {"spec": spec, "resA": resA, "resB": resB,
            "impulse": impulse, "impulse_pct_ifm": 100.0 * impulse / ifm,
            "ifm": ifm, "dC_hhc": dC_hhc, "dC_hhd": dC_hhd, "dG": dG,
            "dVol": dVol, "fee_total": FB["fee_total"],
            "fee_parts": {k: FB[k] for k in
                          ("fee_bnk", "fee_nbf", "fee_nfc", "fee_slg")},
            "decomp": decomp}


GRID = {
    "beta_dep": (0.45, 0.55, 0.65),
    "theta": (0.5, 0.75, 1.0),
    "mpc_cred": (0.05, 0.125, 0.20),
    "mpc_debt": (0.50, 0.75, 1.00),
}
RECYCLING = ("deficit", "transfers", "purchases")


def run_grid(opening=None) -> list:
    if opening is None:
        opening = opening_balance_sheet_ix()
    out = []
    for recycling in RECYCLING:
        for beta in GRID["beta_dep"]:
            for theta in GRID["theta"]:
                for mc in GRID["mpc_cred"]:
                    for md in GRID["mpc_debt"]:
                        spec = BehaviorSpec(
                            beta_dep=beta, theta=theta, mpc_cred=mc,
                            mpc_debt=md, recycling=recycling)
                        out.append(run_pair(opening, spec))
    return out
