"""Godley-Lavoie stock-flow-consistent accounting core (Monetary Symmetry v2).

This module is an ACCOUNTING SKELETON. It contains balance-sheet and
transactions-flow structures and the identities they must satisfy. It contains
NO behavioural equations: every flow in a period is supplied explicitly by the
caller (see scenario.py), and the module's job is to refuse any period in
which a dollar appears or disappears without a counterpart.

Conventions (Godley & Lavoie, *Monetary Economics*, 2007)
---------------------------------------------------------
* Eight sectors: Treasury (TRE), Federal Reserve (FED), commercial banks
  (BNK), nonbank lenders (NBF), households (HHD), nonfinancial businesses
  (NFC), state & local governments (SLG), foreign sector (ROW).
* Balance-sheet entries are signed: assets +, liabilities -. Each sector's
  net worth is the residual that makes its column consistent.
* Transactions-flow matrix (TFM): each sector has a CURRENT and a CAPITAL
  column. Current legs: receipts +, payments -. Capital legs are signed as
  sources (+) / uses (-) of funds: acquiring an asset is a use (-),
  incurring a liability is a source (+). For every transaction, every
  sector's legs must sum to zero (the transaction is balance-sheet neutral
  for each sector *given its stock effects*), every row must sum to zero,
  and each sector's capital legs must equal (change in liabilities) minus
  (change in assets) implied by the transaction's stock effects.
* Stock-flow identity, per sector, per period:
      current-account balance == change in total net worth
      current-account balance - net tangible investment
                              == change in net FINANCIAL assets
  (the SNA statement that net lending equals the change in net financial
  worth). Revaluations are zero in this skeleton: stocks change only
  through transactions.

The Federal Credit Fee in this framework
----------------------------------------
The fee is a CURRENT transfer from lenders (BNK, NBF) to Treasury, settled
in reserves through the Treasury General Account (TGA): the paying bank's
reserves fall and the TGA rises; a paying nonbank's deposits fall, its
bank's reserves fall, and the TGA rises. Treasury spending is the exact
reverse settlement. The reserve drain is therefore visible in the matrices
as a stock movement, while the fee itself is counted exactly once, as a
current transfer (the v1 lesson: a temporary drain is not revenue twice).

Fed remittances and the deferred asset
---------------------------------------
Instrument FEDPAY is the Fed's remittance position NET of the deferred
asset: FEDPAY > 0 is remittances accrued payable to Treasury (Treasury
asset / Fed liability); FEDPAY < 0 is the deferred-asset position (the
Fed's claim on its own future earnings, presented institutionally as an
offset to future remittances). One signed instrument keeps every matrix
row two-sided for any sign of Fed income -- see MATRICES.md.
"""

from dataclasses import dataclass, field

TOL = 1e-9

SECTORS = ["TRE", "FED", "BNK", "NBF", "HHD", "NFC", "SLG", "ROW"]

SECTOR_NAMES = {
    "TRE": "Treasury",
    "FED": "Federal Reserve",
    "BNK": "Commercial banks",
    "NBF": "Nonbank lenders",
    "HHD": "Households",
    "NFC": "Nonfinancial businesses",
    "SLG": "State & local governments",
    "ROW": "Foreign sector (rest of world)",
}

# Financial instruments. For each: which sectors hold it as an ASSET and
# which sector carries it as a LIABILITY. Entries in the balance sheet are
# signed from the holder's perspective: assets +, liabilities -.
FINANCIAL_INSTRUMENTS = {
    "RES":    {"name": "Reserve balances at the Fed",
               "assets": {"BNK"}, "liabilities": {"FED"}},
    "TGA":    {"name": "Treasury General Account at the Fed",
               "assets": {"TRE"}, "liabilities": {"FED"}},
    "TS_PUB": {"name": "Treasury securities, public-held",
               "assets": {"BNK", "NBF", "HHD", "NFC", "SLG", "ROW"},
               "liabilities": {"TRE"}},
    "TS_FED": {"name": "Treasury securities, Fed-held",
               "assets": {"FED"}, "liabilities": {"TRE"}},
    "FEDPAY": {"name": "Fed remittances payable, net of deferred asset",
               "assets": {"TRE"}, "liabilities": {"FED"}},
    "DEP":    {"name": "Deposits at commercial banks",
               "assets": {"NBF", "HHD", "NFC", "SLG", "ROW"},
               "liabilities": {"BNK"}},
    "LN_COV": {"name": "Loans, COVERED (post-enactment originations)",
               "assets": {"BNK", "NBF"}, "liabilities": {"HHD", "NFC"}},
    "LN_GRD": {"name": "Loans, GRANDFATHERED (pre-enactment)",
               "assets": {"BNK", "NBF"}, "liabilities": {"HHD", "NFC"}},
    "CBN":    {"name": "Corporate bonds",
               "assets": {"BNK", "NBF", "HHD", "ROW"},
               "liabilities": {"NFC"}},
    "EQ":     {"name": "Equities (book value)",
               "assets": {"HHD", "ROW"}, "liabilities": {"BNK", "NBF", "NFC"}},
    "CUR":    {"name": "Currency in circulation",
               "assets": {"HHD", "ROW"}, "liabilities": {"FED"}},
}

# Tangible (non-financial) assets: no counterpart liability; they enter net
# worth directly. Row does NOT sum to zero across sectors, by construction.
TANGIBLE_INSTRUMENTS = {
    "K": {"name": "Tangible assets (capital stock, housing, public assets)",
          "assets": {"HHD", "NFC", "SLG"}, "liabilities": set()},
}

ALL_INSTRUMENTS = {**FINANCIAL_INSTRUMENTS, **TANGIBLE_INSTRUMENTS}


class AccountingError(Exception):
    """Raised loudly whenever any stock-flow identity is violated."""


def _check_side(instrument, sector):
    spec = ALL_INSTRUMENTS[instrument]
    if sector in spec["assets"]:
        return "A"
    if sector in spec["liabilities"]:
        return "L"
    return None


class BalanceSheet:
    """Signed stocks: entries[(instrument, sector)] -> value ($ trillions
    in the scenario data; the unit is the caller's convention)."""

    def __init__(self, entries=None):
        self.entries = {}
        for (inst, sec), v in (entries or {}).items():
            self.set(inst, sec, v)

    def set(self, instrument, sector, value):
        if instrument not in ALL_INSTRUMENTS:
            raise AccountingError(f"unknown instrument {instrument!r}")
        if sector not in SECTORS:
            raise AccountingError(f"unknown sector {sector!r}")
        if _check_side(instrument, sector) is None:
            raise AccountingError(
                f"{sector} cannot hold {instrument} on that side of its "
                f"balance sheet (see FINANCIAL_INSTRUMENTS sides)")
        self.entries[(instrument, sector)] = float(value)

    def get(self, instrument, sector):
        return self.entries.get((instrument, sector), 0.0)

    def copy(self):
        return BalanceSheet(dict(self.entries))

    def add_deltas(self, deltas):
        out = self.copy()
        for (inst, sec), d in deltas.items():
            out.set(inst, sec, out.get(inst, sec) + d)
        return out

    # -- sector aggregates -------------------------------------------------
    def financial_assets(self, sector):
        return sum(v for (i, s), v in self.entries.items()
                   if s == sector and i in FINANCIAL_INSTRUMENTS
                   and _check_side(i, s) == "A")

    def financial_liabilities(self, sector):
        """Liabilities as a POSITIVE magnitude."""
        return -sum(v for (i, s), v in self.entries.items()
                    if s == sector and i in FINANCIAL_INSTRUMENTS
                    and _check_side(i, s) == "L")

    def net_financial_assets(self, sector):
        return self.financial_assets(sector) - self.financial_liabilities(sector)

    def tangible(self, sector):
        return sum(v for (i, s), v in self.entries.items()
                   if s == sector and i in TANGIBLE_INSTRUMENTS)

    def net_worth(self, sector):
        return self.net_financial_assets(sector) + self.tangible(sector)

    # -- validation ---------------------------------------------------------
    def validate(self, tol=TOL):
        """Every financial instrument must be two-sided: its entries across
        all sectors sum to zero (someone's asset is someone else's
        liability, in equal amount)."""
        problems = []
        for inst in FINANCIAL_INSTRUMENTS:
            total = sum(v for (i, s), v in self.entries.items() if i == inst)
            if abs(total) > tol:
                problems.append(
                    f"instrument {inst} is not two-sided: entries sum to "
                    f"{total:+.12g}, not 0")
        if problems:
            raise AccountingError("Balance sheet failed validation:\n  "
                                  + "\n  ".join(problems))
        return True


@dataclass
class Transaction:
    """One named flow in a period.

    legs:  {(sector, "current"|"capital"): amount}
    stock: {(instrument, sector): delta}  -- signed balance-sheet deltas
           (assets increase +, liability entries become more negative).

    A transaction is admissible only if, for EVERY sector:
      (a) its legs sum to zero, and
      (b) its capital legs equal (liability increases) - (asset increases)
          implied by `stock` for that sector.
    Anything else means a dollar appeared or vanished, and validate()
    raises AccountingError.
    """
    name: str
    legs: dict = field(default_factory=dict)
    stock: dict = field(default_factory=dict)

    def leg(self, sector, account, amount):
        if amount != 0.0:
            key = (sector, account)
            self.legs[key] = self.legs.get(key, 0.0) + amount
        return self

    def delta(self, instrument, sector, amount):
        if amount != 0.0:
            key = (instrument, sector)
            self.stock[key] = self.stock.get(key, 0.0) + amount
        return self

    def validate(self, tol=TOL):
        problems = []
        total = sum(self.legs.values())
        if abs(total) > tol:
            problems.append(f"legs sum to {total:+.12g}, not 0 "
                            f"(a flow lacks a counterpart)")
        for sec in SECTORS:
            sec_legs = sum(v for (s, a), v in self.legs.items() if s == sec)
            if abs(sec_legs) > tol:
                problems.append(
                    f"sector {sec}: legs sum to {sec_legs:+.12g}, not 0")
            d_assets = sum(d for (i, s), d in self.stock.items()
                           if s == sec and _check_side(i, s) == "A")
            d_liabs = -sum(d for (i, s), d in self.stock.items()
                           if s == sec and _check_side(i, s) == "L")
            cap_legs = sum(v for (s, a), v in self.legs.items()
                           if s == sec and a == "capital")
            if abs(cap_legs - (d_liabs - d_assets)) > tol:
                problems.append(
                    f"sector {sec}: capital legs {cap_legs:+.12g} != "
                    f"(dLiabilities {d_liabs:+.12g} - dAssets {d_assets:+.12g}) "
                    f"implied by stock effects")
        if problems:
            raise AccountingError(f"Transaction {self.name!r} failed:\n  "
                                  + "\n  ".join(problems))
        return True


@dataclass
class PeriodResult:
    opening: BalanceSheet
    closing: BalanceSheet
    tfm: dict            # {row name: {(sector, account): amount}}
    transactions: list

    def current_balance(self, sector):
        return sum(v for row in self.tfm.values()
                   for (s, a), v in row.items()
                   if s == sector and a == "current")

    def capital_balance(self, sector):
        return sum(v for row in self.tfm.values()
                   for (s, a), v in row.items()
                   if s == sector and a == "capital")

    def tfm_row(self, name):
        return self.tfm.get(name, {})

    def row_total(self, name, sector=None, account=None):
        return sum(v for (s, a), v in self.tfm_row(name).items()
                   if (sector is None or s == sector)
                   and (account is None or a == account))


class Period:
    """Collect validated transactions against an opening balance sheet and
    close the period, checking every stock-flow identity."""

    def __init__(self, opening: BalanceSheet):
        opening.validate()
        self.opening = opening
        self.transactions = []

    def add(self, txn: Transaction):
        txn.validate()          # fails loudly at insertion time
        self.transactions.append(txn)
        return txn

    def close(self, tol=TOL) -> PeriodResult:
        deltas = {}
        tfm = {}
        for txn in self.transactions:
            row = tfm.setdefault(txn.name, {})
            for key, v in txn.legs.items():
                row[key] = row.get(key, 0.0) + v
            for key, d in txn.stock.items():
                deltas[key] = deltas.get(key, 0.0) + d
        closing = self.opening.add_deltas(deltas)
        closing.validate(tol)
        result = PeriodResult(self.opening, closing, tfm, list(self.transactions))

        problems = []
        for name, row in tfm.items():
            s = sum(row.values())
            if abs(s) > tol:
                problems.append(f"TFM row {name!r} sums to {s:+.12g}, not 0")
        for sec in SECTORS:
            cb = result.current_balance(sec)
            kb = result.capital_balance(sec)
            if abs(cb + kb) > tol:
                problems.append(f"sector {sec}: current {cb:+.12g} + capital "
                                f"{kb:+.12g} != 0")
            d_nw = closing.net_worth(sec) - self.opening.net_worth(sec)
            if abs(cb - d_nw) > tol:
                problems.append(
                    f"sector {sec}: current balance {cb:+.12g} != change in "
                    f"net worth {d_nw:+.12g}")
            d_nfa = (closing.net_financial_assets(sec)
                     - self.opening.net_financial_assets(sec))
            d_k = closing.tangible(sec) - self.opening.tangible(sec)
            if abs((cb - d_k) - d_nfa) > tol:
                problems.append(
                    f"sector {sec}: financial balance {cb - d_k:+.12g} != "
                    f"change in net financial assets {d_nfa:+.12g}")
        total_dnw = sum(closing.net_worth(s) - self.opening.net_worth(s)
                        for s in SECTORS)
        total_dk = sum(closing.tangible(s) - self.opening.tangible(s)
                       for s in SECTORS)
        if abs(total_dnw - total_dk) > tol:
            problems.append(
                f"economy-wide: total net worth changed by {total_dnw:+.12g} "
                f"but tangible assets changed by {total_dk:+.12g}; financial "
                f"assets must net to zero across sectors")
        if problems:
            raise AccountingError("Period failed stock-flow reconciliation:\n  "
                                  + "\n  ".join(problems))
        return result
