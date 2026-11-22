"""Illustrative period construction for the v2 SFC skeleton.

Stocks and flows are PLAUSIBLE-MAGNITUDE ILLUSTRATIONS in $ trillions,
roughly US-scale (the covered-loan stock is shown a few years after
enactment, once post-enactment originations have accumulated). They are
not calibrated estimates and no result in this directory should be quoted
as a forecast. The point of the numbers is to exercise every row of the
matrices -- including the fee, IORB, remittances and the deferred-asset
mechanism -- under the accounting identities in sfc_core.py.

Settlement helpers encode the institutional plumbing ONCE, so individual
flows cannot be specified with inconsistent settlement:

* pay_via_deposits: payer and payee both hold deposits at commercial
  banks; the payment shifts deposit liabilities between them.
* treasury_pay / treasury_receive: Treasury settles through the TGA;
  the private counterparty settles in deposits; bank reserves move in
  mirror image (TGA up = reserves down, and conversely).
* pay_treasury_from_reserves: a bank pays Treasury directly in reserves
  (the bank leg of the Federal Credit Fee, and bank taxes).
* fed_pay_via_reserves: the Fed creates reserves to pay (IORB, opex);
  the recipient's bank credits the recipient's deposit.
"""

from sfc_core import BalanceSheet, Period, Transaction


# ---------------------------------------------------------------------------
# Opening balance sheet ($T, illustrative)
# ---------------------------------------------------------------------------

def opening_balance_sheet() -> BalanceSheet:
    e = {}
    def A(inst, sec, v): e[(inst, sec)] = v          # asset entry (+)
    def L(inst, sec, v): e[(inst, sec)] = -v         # liability entry (-)

    A("RES", "BNK", 3.00);  L("RES", "FED", 3.00)
    A("TGA", "TRE", 0.80);  L("TGA", "FED", 0.80)
    A("TS_FED", "FED", 4.40); L("TS_FED", "TRE", 4.40)
    L("TS_PUB", "TRE", 31.60)
    for sec, v in [("BNK", 5.0), ("NBF", 10.0), ("HHD", 5.0),
                   ("NFC", 0.8), ("SLG", 1.8), ("ROW", 9.0)]:
        A("TS_PUB", sec, v)
    # FEDPAY starts at 0: no accrued remittance payable, no deferred asset.
    A("DEP", "NBF", 0.50); A("DEP", "HHD", 11.00); A("DEP", "NFC", 4.50)
    A("DEP", "SLG", 1.00); A("DEP", "ROW", 1.00);  L("DEP", "BNK", 18.00)
    A("LN_COV", "BNK", 4.00); A("LN_COV", "NBF", 1.50)
    L("LN_COV", "HHD", 3.50); L("LN_COV", "NFC", 2.00)
    A("LN_GRD", "BNK", 9.00); A("LN_GRD", "NBF", 4.00)
    L("LN_GRD", "HHD", 8.00); L("LN_GRD", "NFC", 5.00)
    A("CBN", "BNK", 1.00); A("CBN", "NBF", 3.50); A("CBN", "HHD", 1.50)
    A("CBN", "ROW", 1.00); L("CBN", "NFC", 7.00)
    L("EQ", "BNK", 2.00); L("EQ", "NBF", 1.00); L("EQ", "NFC", 12.00)
    A("EQ", "HHD", 11.00); A("EQ", "ROW", 4.00)
    A("CUR", "HHD", 1.80); A("CUR", "ROW", 0.50); L("CUR", "FED", 2.30)
    A("K", "HHD", 15.00); A("K", "NFC", 20.00); A("K", "SLG", 5.00)
    return BalanceSheet(e)


# ---------------------------------------------------------------------------
# Settlement helpers
# ---------------------------------------------------------------------------

def _deposit_shift(txn, payer, payee, amount):
    """Move `amount` of deposits from payer to payee (both deposit holders
    at commercial banks). If a party IS the banking sector, its side of
    the shift is its own deposit liability and needs no legs here."""
    if payer != "BNK":
        txn.delta("DEP", payer, -amount).leg(payer, "capital", +amount)
        txn.delta("DEP", "BNK", +amount).leg("BNK", "capital", -amount)
    if payee != "BNK":
        txn.delta("DEP", payee, +amount).leg(payee, "capital", -amount)
        txn.delta("DEP", "BNK", -amount).leg("BNK", "capital", +amount)


def _tga_settle_out(txn, amount):
    """Treasury pays `amount` out of the TGA into bank reserves (the
    counterparty's deposit credit is added by the caller)."""
    txn.delta("TGA", "TRE", -amount).leg("TRE", "capital", +amount)
    txn.delta("TGA", "FED", +amount).leg("FED", "capital", -amount)
    txn.delta("RES", "FED", -amount).leg("FED", "capital", +amount)
    txn.delta("RES", "BNK", +amount).leg("BNK", "capital", -amount)


def _tga_settle_in(txn, amount):
    """`amount` lands in the TGA, draining bank reserves one-for-one."""
    txn.delta("RES", "BNK", -amount).leg("BNK", "capital", +amount)
    txn.delta("RES", "FED", +amount).leg("FED", "capital", -amount)
    txn.delta("TGA", "FED", -amount).leg("FED", "capital", +amount)
    txn.delta("TGA", "TRE", +amount).leg("TRE", "capital", -amount)


def pay_via_deposits(name, payer, payee, amount, current=True):
    txn = Transaction(name)
    if current:
        txn.leg(payer, "current", -amount).leg(payee, "current", +amount)
    _deposit_shift(txn, payer, payee, amount)
    return txn


def treasury_pay(name, payee, amount, current=True):
    """Treasury pays `payee` (a deposit holder) out of the TGA."""
    txn = Transaction(name)
    if current:
        txn.leg("TRE", "current", -amount).leg(payee, "current", +amount)
    _tga_settle_out(txn, amount)
    txn.delta("DEP", payee, +amount).leg(payee, "capital", -amount)
    txn.delta("DEP", "BNK", -amount).leg("BNK", "capital", +amount)
    return txn


def treasury_receive(name, payer, amount, current=True):
    """A deposit holder pays Treasury; settlement lands in the TGA and
    drains reserves one-for-one."""
    txn = Transaction(name)
    if current:
        txn.leg(payer, "current", -amount).leg("TRE", "current", +amount)
    txn.delta("DEP", payer, -amount).leg(payer, "capital", +amount)
    txn.delta("DEP", "BNK", +amount).leg("BNK", "capital", -amount)
    _tga_settle_in(txn, amount)
    return txn


def pay_treasury_from_reserves(name, amount, current=True):
    """A commercial bank pays Treasury directly in reserves (fee, taxes)."""
    txn = Transaction(name)
    if current:
        txn.leg("BNK", "current", -amount).leg("TRE", "current", +amount)
    _tga_settle_in(txn, amount)
    return txn


def fed_pay_via_reserves(name, payee, amount, current=True):
    """The Fed pays by creating reserves; payee's bank credits its deposit.
    Used for IORB (payee BNK: reserves only) and Fed operating expenses."""
    txn = Transaction(name)
    if current:
        txn.leg("FED", "current", -amount).leg(payee, "current", +amount)
    txn.delta("RES", "FED", -amount).leg("FED", "capital", +amount)
    txn.delta("RES", "BNK", +amount).leg("BNK", "capital", -amount)
    if payee != "BNK":
        txn.delta("DEP", payee, +amount).leg(payee, "capital", -amount)
        txn.delta("DEP", "BNK", -amount).leg("BNK", "capital", +amount)
    return txn


# ---------------------------------------------------------------------------
# Policy / flow parameters for one illustrative period
# ---------------------------------------------------------------------------

class PeriodSpec:
    """Rates in % per period; flows in $T. Defaults = a SYNCHRONIZED
    period under the Nov 22, 2026 memo: fee rate == IORB, and the IORB
    path is half the conventional baseline (2% vs 4%)."""
    iorb = 2.0
    fee_rate = 2.0            # f == i after synchronization (50/50)
    deposit_rate = 1.5
    loan_rate_cov = 6.0
    loan_rate_grd = 5.5
    treasury_yield = 3.5      # single average rate, skeleton simplification
    bond_rate = 5.0
    fed_opex = 0.02

    # Exogenous current flows ($T)
    wages = {"NFC": 9.0, "BNK": 0.6, "NBF": 0.2, "TRE": 1.2, "SLG": 1.0}
    consumption = 11.0        # HHD -> NFC
    gov_purchases = {"TRE": 2.5, "SLG": 1.2}   # buyer -> NFC
    taxes_tre = {"HHD": 3.2, "NFC": 1.2, "NBF": 0.05}
    taxes_tre_banks = 0.15    # banks pay Treasury from reserves
    taxes_slg = {"HHD": 0.9, "NFC": 0.4}
    transfers = {"TRE": 3.4, "SLG": 0.5}       # payer -> HHD
    net_exports = 0.6         # NFC receipts from ROW (net)
    dividends = {"BNK": 0.25, "NBF": 0.08, "NFC": 0.9}
    dividend_row_share = 0.19  # share of dividends accruing to ROW

    # Stock-change flows ($T)
    new_covered = {"BNK": {"HHD": 0.9, "NFC": 0.6}, "NBF": {"HHD": 0.3}}
    covered_repay = {"BNK": {"HHD": 0.35, "NFC": 0.25}, "NBF": {"HHD": 0.12}}
    grd_repay = {"BNK": {"HHD": 0.55, "NFC": 0.35},
                 "NBF": {"HHD": 0.25, "NFC": 0.15}}
    treasury_issuance_public = 1.6
    issuance_shares = {"BNK": 0.15, "NBF": 0.30, "HHD": 0.10,
                       "NFC": 0.05, "SLG": 0.05, "ROW": 0.35}
    fed_ts_purchase = 0.2     # Fed buys TS_PUB from BNK in secondary market
    bond_issuance = {"NBF": 0.20, "HHD": 0.10}   # NFC issues, holders buy
    equity_issuance = 0.1     # NFC issues to HHD


def _interest(stock, rate_pct):
    return stock * rate_pct / 100.0


def fed_income(opening: BalanceSheet, spec: PeriodSpec = PeriodSpec()):
    """Fed net income BEFORE remittance, computed on opening stocks."""
    return (_interest(opening.get("TS_FED", "FED"), spec.treasury_yield)
            - _interest(opening.get("RES", "BNK"), spec.iorb)
            - spec.fed_opex)


def build_period(opening: BalanceSheet, spec: PeriodSpec = PeriodSpec()) -> Period:
    """Assemble one full period of transactions against `opening`."""
    bs = opening
    S = spec
    p = Period(opening)

    # ---- production, income, and spending --------------------------------
    wages = Transaction("Wages")
    for payer, amt in S.wages.items():
        wages.leg(payer, "current", -amt).leg("HHD", "current", +amt)
        if payer == "TRE":
            _tga_settle_out(wages, amt)
            wages.delta("DEP", "HHD", +amt).leg("HHD", "capital", -amt)
            wages.delta("DEP", "BNK", -amt).leg("BNK", "capital", +amt)
        else:
            _deposit_shift(wages, payer, "HHD", amt)
    p.add(wages)

    p.add(pay_via_deposits("Consumption", "HHD", "NFC", S.consumption))

    p.add(treasury_pay("Government purchases (federal)", "NFC",
                       S.gov_purchases["TRE"]))
    p.add(pay_via_deposits("Government purchases (state/local)", "SLG",
                           "NFC", S.gov_purchases["SLG"]))

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

    # ---- taxes and transfers ----------------------------------------------
    for payer, amt in S.taxes_tre.items():
        p.add(treasury_receive(f"Taxes to Treasury ({payer})", payer, amt))
    p.add(pay_treasury_from_reserves("Taxes to Treasury (BNK)",
                                     S.taxes_tre_banks))
    for payer, amt in S.taxes_slg.items():
        p.add(pay_via_deposits(f"Taxes to state/local ({payer})", payer,
                               "SLG", amt))
    p.add(treasury_pay("Transfers to households (federal)", "HHD",
                       S.transfers["TRE"]))
    p.add(pay_via_deposits("Transfers to households (state/local)", "SLG",
                           "HHD", S.transfers["SLG"]))

    nx = Transaction("Net exports")
    nx.leg("NFC", "current", +S.net_exports) \
      .leg("ROW", "current", -S.net_exports)
    _deposit_shift(nx, "ROW", "NFC", S.net_exports)
    p.add(nx)

    div = Transaction("Dividends and distributed profits")
    total_div = sum(S.dividends.values())
    to_row = total_div * S.dividend_row_share
    to_hhd = total_div - to_row
    for payer, amt in S.dividends.items():
        div.leg(payer, "current", -amt)
        _deposit_shift(div, payer, "HHD", amt * (to_hhd / total_div))
        _deposit_shift(div, payer, "ROW", amt * (to_row / total_div))
    div.leg("HHD", "current", +to_hhd).leg("ROW", "current", +to_row)
    p.add(div)

    # ---- interest on loans (opening stocks; lender interest allocated ---
    # ---- across borrowers by each borrower's share of the instrument) ---
    for inst, rate, label in [("LN_COV", S.loan_rate_cov, "covered"),
                              ("LN_GRD", S.loan_rate_grd, "grandfathered")]:
        total_liab = -(bs.get(inst, "HHD") + bs.get(inst, "NFC"))
        for lender in ("BNK", "NBF"):
            lender_stock = bs.get(inst, lender)
            if lender_stock == 0 or total_liab == 0:
                continue
            for borrower in ("HHD", "NFC"):
                share = -bs.get(inst, borrower) / total_liab
                amt = _interest(lender_stock * share, rate)
                if amt:
                    p.add(pay_via_deposits(
                        f"Interest on {label} loans ({borrower}->{lender})",
                        borrower, lender, amt))

    dep_int = Transaction("Interest on deposits")
    total_dep_int = 0.0
    for holder in ("NBF", "HHD", "NFC", "SLG", "ROW"):
        amt = _interest(bs.get("DEP", holder), S.deposit_rate)
        if amt:
            dep_int.leg(holder, "current", +amt)
            _deposit_shift(dep_int, "BNK", holder, amt)
            total_dep_int += amt
    dep_int.leg("BNK", "current", -total_dep_int)
    p.add(dep_int)

    # IORB: Fed -> banks, settled by creating reserves.
    iorb_amt = _interest(bs.get("RES", "BNK"), S.iorb)
    p.add(fed_pay_via_reserves("Interest on reserve balances (IORB)",
                               "BNK", iorb_amt))

    # Treasury interest, public-held: paid out of the TGA into reserves;
    # bank holders keep the receipt as reserves, other holders are
    # credited deposits at their banks.
    ts_pub = Transaction("Interest on Treasury securities (public-held)")
    total_pub = 0.0
    for holder in ("BNK", "NBF", "HHD", "NFC", "SLG", "ROW"):
        amt = _interest(bs.get("TS_PUB", holder), S.treasury_yield)
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

    # Treasury interest, Fed-held: settles entirely inside the TGA.
    fed_int_amt = _interest(bs.get("TS_FED", "FED"), S.treasury_yield)
    tint = Transaction("Interest on Treasury securities (Fed-held)")
    tint.leg("TRE", "current", -fed_int_amt) \
        .leg("FED", "current", +fed_int_amt)
    tint.delta("TGA", "TRE", -fed_int_amt).leg("TRE", "capital", +fed_int_amt)
    tint.delta("TGA", "FED", +fed_int_amt).leg("FED", "capital", -fed_int_amt)
    p.add(tint)

    bond_int = Transaction("Interest on corporate bonds")
    total_bond = 0.0
    for holder in ("BNK", "NBF", "HHD", "ROW"):
        amt = _interest(bs.get("CBN", holder), S.bond_rate)
        if amt:
            bond_int.leg(holder, "current", +amt)
            _deposit_shift(bond_int, "NFC", holder, amt)
            total_bond += amt
    bond_int.leg("NFC", "current", -total_bond)
    p.add(bond_int)

    # ---- THE FEDERAL CREDIT FEE -------------------------------------------
    # Assessed on COVERED principal only, by lender. Banks settle in
    # reserves; nonbanks settle from deposits (their bank's reserves drain
    # by the same amount when the payment lands in the TGA).
    fee_bnk = _interest(bs.get("LN_COV", "BNK"), S.fee_rate)
    fee_nbf = _interest(bs.get("LN_COV", "NBF"), S.fee_rate)
    p.add(pay_treasury_from_reserves("Federal Credit Fee (banks)", fee_bnk))
    p.add(treasury_receive("Federal Credit Fee (nonbanks)", "NBF", fee_nbf))

    # ---- Fed operating expenses, remittance accrual & cash ----------------
    p.add(fed_pay_via_reserves("Federal Reserve operating expenses",
                               "HHD", S.fed_opex))
    income = fed_income(bs, S)
    opening_payable = bs.get("FEDPAY", "TRE")  # >0 payable, <0 deferred asset
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

    # ---- lending and repayment (capital account) --------------------------
    for lender, borrowers in S.new_covered.items():
        for borrower, amt in borrowers.items():
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
            ("LN_COV", S.covered_repay, "Covered loan repayments"),
            ("LN_GRD", S.grd_repay, "Grandfathered loan repayments")]:
        for lender, borrowers in bookmap.items():
            for borrower, amt in borrowers.items():
                txn = pay_via_deposits(f"{label} ({borrower}->{lender})",
                                       borrower, lender, amt, current=False)
                txn.delta(book, lender, -amt).delta(book, borrower, +amt)
                txn.leg(lender, "capital", +amt) \
                   .leg(borrower, "capital", -amt)
                p.add(txn)

    # ---- Treasury net issuance to the public (settled through the TGA) ----
    for holder, share in S.issuance_shares.items():
        amt = S.treasury_issuance_public * share
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

    # ---- Fed secondary-market purchase of Treasuries from banks -----------
    qe = Transaction("Fed purchases of Treasury securities (from banks)")
    amt = S.fed_ts_purchase
    qe.delta("TS_FED", "FED", +amt).leg("FED", "capital", -amt)
    qe.delta("TS_FED", "TRE", -amt).leg("TRE", "capital", +amt)
    qe.delta("TS_PUB", "TRE", +amt).leg("TRE", "capital", -amt)
    qe.delta("TS_PUB", "BNK", -amt).leg("BNK", "capital", +amt)
    qe.delta("RES", "BNK", +amt).leg("BNK", "capital", -amt)
    qe.delta("RES", "FED", -amt).leg("FED", "capital", +amt)
    p.add(qe)

    # ---- Corporate bond and equity issuance --------------------------------
    for holder, amt in S.bond_issuance.items():
        txn = pay_via_deposits(f"Corporate bond issuance ({holder})",
                               holder, "NFC", amt, current=False)
        txn.delta("CBN", holder, +amt).delta("CBN", "NFC", -amt)
        txn.leg(holder, "capital", -amt).leg("NFC", "capital", +amt)
        p.add(txn)

    eq = pay_via_deposits("Equity issuance (HHD buys NFC shares)", "HHD",
                          "NFC", S.equity_issuance, current=False)
    eq.delta("EQ", "HHD", +S.equity_issuance) \
      .delta("EQ", "NFC", -S.equity_issuance)
    eq.leg("HHD", "capital", -S.equity_issuance) \
      .leg("NFC", "capital", +S.equity_issuance)
    p.add(eq)

    return p
