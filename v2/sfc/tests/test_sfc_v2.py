"""Reconciliation tests for the v2 Godley-Lavoie SFC skeleton.

Every test here is an ACCOUNTING test: it asserts that the matrices
reconcile, that the fee/IORB/remittance plumbing settles the way the
institutions actually settle, and that the machinery FAILS LOUDLY when a
flow lacks a counterpart. No behavioural claim is tested, because the
skeleton contains no behavioural equations yet.
"""

import copy

import pytest

from sfc_core import (ALL_INSTRUMENTS, FINANCIAL_INSTRUMENTS, SECTORS,
                      AccountingError, BalanceSheet, Period, Transaction)
from scenario import (PeriodSpec, build_period, fed_income,
                      opening_balance_sheet, pay_treasury_from_reserves,
                      treasury_pay)


@pytest.fixture(scope="module")
def opening():
    return opening_balance_sheet()


@pytest.fixture(scope="module")
def result(opening):
    return build_period(opening).close()


# ---------------------------------------------------------------------------
# Balance-sheet matrix
# ---------------------------------------------------------------------------

def test_opening_balance_sheet_is_two_sided(opening):
    assert opening.validate()
    for inst in FINANCIAL_INSTRUMENTS:
        total = sum(v for (i, s), v in opening.entries.items() if i == inst)
        assert total == pytest.approx(0.0), inst


def test_every_asset_has_a_matching_liability(opening, result):
    for bs in (opening, result.closing):
        for inst in FINANCIAL_INSTRUMENTS:
            assets = sum(v for (i, s), v in bs.entries.items()
                         if i == inst and v > 0)
            liabs = -sum(v for (i, s), v in bs.entries.items()
                         if i == inst and v < 0)
            assert assets == pytest.approx(liabs), inst


def test_eight_sectors_present(opening):
    assert {s for (_, s) in opening.entries} == set(SECTORS)
    assert len(SECTORS) == 8


# ---------------------------------------------------------------------------
# Transactions-flow matrix identities
# ---------------------------------------------------------------------------

def test_every_tfm_row_sums_to_zero(result):
    for name, row in result.tfm.items():
        assert sum(row.values()) == pytest.approx(0.0), name


def test_every_sector_column_pair_sums_to_zero(result):
    for sec in SECTORS:
        assert result.current_balance(sec) + result.capital_balance(sec) \
            == pytest.approx(0.0), sec


def test_financial_balance_equals_change_in_nfa(result):
    for sec in SECTORS:
        fin_balance = result.current_balance(sec) - (
            result.closing.tangible(sec) - result.opening.tangible(sec))
        d_nfa = (result.closing.net_financial_assets(sec)
                 - result.opening.net_financial_assets(sec))
        assert fin_balance == pytest.approx(d_nfa), sec


def test_current_balance_equals_change_in_net_worth(result):
    for sec in SECTORS:
        d_nw = (result.closing.net_worth(sec)
                - result.opening.net_worth(sec))
        assert result.current_balance(sec) == pytest.approx(d_nw), sec


def test_no_money_from_nowhere(result):
    total_dnw = sum(result.closing.net_worth(s) - result.opening.net_worth(s)
                    for s in SECTORS)
    total_dk = sum(result.closing.tangible(s) - result.opening.tangible(s)
                   for s in SECTORS)
    assert total_dnw == pytest.approx(total_dk)


# ---------------------------------------------------------------------------
# The Federal Credit Fee: plumbing and base
# ---------------------------------------------------------------------------

def test_fee_revenue_equals_rate_times_covered_stock(opening, result):
    spec = PeriodSpec()
    expected = spec.fee_rate / 100.0 * (
        opening.get("LN_COV", "BNK") + opening.get("LN_COV", "NBF"))
    got = sum(result.row_total(name, sector="TRE", account="current")
              for name in result.tfm if name.startswith("Federal Credit Fee"))
    assert got == pytest.approx(expected)
    # Synchronized design (Nov 22 memo): f == i, so the fee take also
    # equals IORB x covered stock.
    assert spec.fee_rate == spec.iorb


def test_grandfathered_loans_pay_no_fee(opening):
    spec = PeriodSpec()
    spec.fee_rate = 2.0
    # Zero the covered stock: fee must vanish even though $13T of
    # grandfathered loans remain on the books.
    entries = dict(opening.entries)
    for key in [("LN_COV", "BNK"), ("LN_COV", "NBF"),
                ("LN_COV", "HHD"), ("LN_COV", "NFC")]:
        entries[key] = 0.0
    bs = BalanceSheet(entries)
    res = build_period(bs, spec).close()
    got = sum(res.row_total(name, sector="TRE", account="current")
              for name in res.tfm if name.startswith("Federal Credit Fee"))
    assert got == pytest.approx(0.0)


def test_fee_settlement_drains_reserves_into_tga(opening):
    fee = 0.11
    p = Period(opening)
    p.add(pay_treasury_from_reserves("Federal Credit Fee (banks)", fee))
    res = p.close()
    assert res.closing.get("RES", "BNK") == pytest.approx(
        opening.get("RES", "BNK") - fee)
    assert res.closing.get("TGA", "TRE") == pytest.approx(
        opening.get("TGA", "TRE") + fee)
    # The drain is a stock movement, not income twice: Treasury's net
    # worth rises by the fee exactly once, banks' falls by the fee.
    assert res.current_balance("TRE") == pytest.approx(fee)
    assert res.current_balance("BNK") == pytest.approx(-fee)


def test_treasury_spending_restores_reserves(opening):
    fee = 0.11
    p = Period(opening)
    p.add(pay_treasury_from_reserves("Federal Credit Fee (banks)", fee))
    p.add(treasury_pay("Treasury spending", "HHD", fee))
    res = p.close()
    assert res.closing.get("RES", "BNK") == pytest.approx(
        opening.get("RES", "BNK"))
    assert res.closing.get("TGA", "TRE") == pytest.approx(
        opening.get("TGA", "TRE"))


# ---------------------------------------------------------------------------
# Fed earnings, remittances, deferred asset
# ---------------------------------------------------------------------------

def test_fed_remittance_positive_income(opening, result):
    income = fed_income(opening, PeriodSpec())
    assert income > 0
    # Accrual credits Treasury's remittance claim by the full income...
    accrual = result.row_total("Fed earnings accrual to remittance position",
                               sector="TRE", account="current")
    assert accrual == pytest.approx(income)
    # ...and with no opening deferred asset, cash follows in full and the
    # closing FEDPAY position returns to zero.
    assert result.closing.get("FEDPAY", "TRE") == pytest.approx(0.0)
    remit = next(t for t in result.transactions
                 if t.name == "Fed cash remittance to Treasury")
    assert remit.stock[("TGA", "TRE")] == pytest.approx(income)


def test_deferred_asset_accrues_when_income_negative(opening):
    spec = PeriodSpec()
    spec.iorb = 9.0            # IORB expense swamps Fed asset income
    spec.fee_rate = 9.0        # keep f == i (synchronized), only for realism
    income = fed_income(opening, spec)
    assert income < 0
    res = build_period(opening, spec).close()
    # No cash remittance transaction exists in a loss period...
    assert "Fed cash remittance to Treasury" not in res.tfm
    # ...and the deferred asset is exactly the shortfall: FEDPAY < 0.
    assert res.closing.get("FEDPAY", "TRE") == pytest.approx(income)
    assert res.closing.get("FEDPAY", "FED") == pytest.approx(-income)


def test_deferred_asset_pays_down_before_cash_remittance(opening):
    # Period 1: losses create a deferred asset.
    spec1 = PeriodSpec(); spec1.iorb = 9.0; spec1.fee_rate = 9.0
    res1 = build_period(opening, spec1).close()
    da = -res1.closing.get("FEDPAY", "TRE")
    assert da > 0
    # Period 2: strong positive income on the period-1 closing sheet
    # (low IORB, higher book yield on the Fed's portfolio).
    spec2 = PeriodSpec(); spec2.iorb = 0.5; spec2.fee_rate = 0.5
    spec2.treasury_yield = 5.0
    income2 = fed_income(res1.closing, spec2)
    assert income2 > da > 0
    res2 = build_period(res1.closing, spec2).close()
    # Deferred asset fully repaid; FEDPAY back to zero; cash remitted is
    # income minus the paydown (the paydown itself moves no cash).
    assert res2.closing.get("FEDPAY", "TRE") == pytest.approx(0.0)
    remit = next(t for t in res2.transactions
                 if t.name == "Fed cash remittance to Treasury")
    assert remit.stock[("TGA", "TRE")] == pytest.approx(income2 - da)


def test_consolidated_government_identity(opening, result):
    """Consolidated (Treasury+Fed) net interest == gross interest on ALL
    federal debt minus the Fed's economic net income: interest on
    Fed-held debt is an internal transfer and must net out exactly."""
    spec = PeriodSpec()
    int_public = -result.row_total(
        "Interest on Treasury securities (public-held)",
        sector="TRE", account="current")
    int_fedheld = -result.row_total(
        "Interest on Treasury securities (Fed-held)",
        sector="TRE", account="current")
    iorb = -result.row_total("Interest on reserve balances (IORB)",
                             sector="FED", account="current")
    consolidated = int_public + iorb + spec.fed_opex
    gross_minus_fed_income = (int_public + int_fedheld) - fed_income(
        opening, spec)
    assert consolidated == pytest.approx(gross_minus_fed_income)


def test_iorb_paid_on_reserve_stock(opening, result):
    spec = PeriodSpec()
    expected = opening.get("RES", "BNK") * spec.iorb / 100.0
    got = result.row_total("Interest on reserve balances (IORB)",
                           sector="BNK", account="current")
    assert got == pytest.approx(expected)


# ---------------------------------------------------------------------------
# Negative tests: the accounting must FAIL LOUDLY
# ---------------------------------------------------------------------------

def test_broken_flow_missing_counterpart_is_caught():
    bad = Transaction("Phantom transfer")
    bad.leg("HHD", "current", -1.0)          # household pays...
    # ...and nobody receives. No counterpart leg, no stock effect.
    with pytest.raises(AccountingError):
        bad.validate()


def test_broken_flow_unsettled_transfer_is_caught():
    bad = Transaction("Unsettled wage")
    bad.leg("NFC", "current", -1.0).leg("HHD", "current", +1.0)
    # Current legs balance, but no settlement: capital legs do not match
    # any stock effect, so each sector's legs fail to sum to zero.
    with pytest.raises(AccountingError):
        bad.validate()


def test_broken_flow_stock_without_legs_is_caught():
    bad = Transaction("Loans from nowhere")
    bad.delta("LN_COV", "BNK", +1.0).delta("LN_COV", "HHD", -1.0)
    with pytest.raises(AccountingError):
        bad.validate()


def test_tampered_balance_sheet_is_caught(opening):
    entries = dict(opening.entries)
    entries[("DEP", "HHD")] += 0.5           # deposits appear from nowhere
    with pytest.raises(AccountingError):
        BalanceSheet(entries).validate()


def test_period_rejects_broken_transaction(opening):
    p = Period(opening)
    bad = Transaction("Phantom fee")
    bad.leg("BNK", "current", -0.1).leg("TRE", "current", +0.1)
    with pytest.raises(AccountingError):
        p.add(bad)


def test_deepcopy_tamper_with_closed_period_is_caught(result):
    # Corrupt one closing stock after the fact: re-running the balance
    # sheet's own validation must catch the one-sided instrument.
    closing = copy.deepcopy(result.closing)
    closing.entries[("RES", "BNK")] += 1.0
    with pytest.raises(AccountingError):
        closing.validate()
