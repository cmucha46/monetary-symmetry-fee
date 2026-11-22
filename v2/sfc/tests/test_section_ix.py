"""Tests for the Section IX behavioural extension (behavior.py).

Two families: (1) ACCOUNTING tests for the household split and the
amended fee base -- the split balance sheet is two-sided, periods close
under the full Godley identities, and the fee is collected from lenders
on covered loans AND from issuers on covered bonds, exactly once, with
grandfathered vintages exempt; (2) BEHAVIOURAL sign tests for the
interest-income hypothesis at equal combined charge -- the conventional
regime (i = 4%, no fee) versus the synchronized regime (i = 2%, f = 2%).

The skeleton's own suite (test_sfc_v2.py, 23 tests) runs against the
unmodified sfc_core module and is unaffected by this extension, which
loads a private patched copy of the core.
"""

import pytest

import behavior as B


@pytest.fixture(scope="module")
def opening():
    return B.opening_balance_sheet_ix()


@pytest.fixture(scope="module")
def center():
    return B.BehaviorSpec()          # beta .55, theta 1, MPCs .125/.75


# ---------------------------------------------------------------------------
# The household split
# ---------------------------------------------------------------------------

def test_split_balance_sheet_is_two_sided(opening):
    assert opening.validate()
    assert set(B.core.SECTORS) == {"TRE", "FED", "BNK", "NBF", "HHC",
                                   "HHD", "NFC", "SLG", "ROW"}


def test_creditors_hold_the_assets_debtors_hold_the_loans(opening):
    household_dep = opening.get("DEP", "HHC") + opening.get("DEP", "HHD")
    assert opening.get("DEP", "HHC") / household_dep >= 0.8
    # All household loan liabilities sit with debtors; creditors hold none.
    for inst in ("LN_COV", "LN_GRD"):
        assert opening.get(inst, "HHD") < 0
        assert opening.get(inst, "HHC") == 0.0
    # Creditors hold the household share of securities and equities.
    assert opening.get("TS_PUB", "HHC") > 0
    assert opening.get("EQ", "HHC") > 0


def test_period_closes_under_full_identities_in_both_regimes(opening, center):
    for spec in (center.conventional(), center):
        res = B.build_period_ix(opening, spec).close()   # raises if broken
        for sec in B.core.SECTORS:
            assert res.current_balance(sec) + res.capital_balance(sec) \
                == pytest.approx(0.0), sec


# ---------------------------------------------------------------------------
# The amended fee base: lenders on loans, issuers on bonds, taxed once
# ---------------------------------------------------------------------------

def test_fee_covers_loans_and_bonds(opening, center):
    res = B.build_period_ix(opening, center).close()
    F = B.policy_flows(opening, center)
    got = sum(res.row_total(name, sector="TRE", account="current")
              for name in res.tfm if name.startswith("Federal Credit Fee"))
    expected = 0.02 * (opening.get("LN_COV", "BNK")
                       + opening.get("LN_COV", "NBF")
                       - opening.get("CBN_COV", "NFC")
                       - opening.get("MUN_COV", "SLG"))
    assert got == pytest.approx(expected) == pytest.approx(F["fee_total"])
    # Each channel is present: two lender rows, two issuer rows.
    for name in ("Federal Credit Fee (banks)",
                 "Federal Credit Fee (nonbanks)",
                 "Federal Credit Fee (NFC bond issuers)",
                 "Federal Credit Fee (SLG bond issuers)"):
        assert res.row_total(name, sector="TRE", account="current") > 0, name


def test_fees_vanish_when_no_covered_stock(opening, center):
    entries = dict(opening.entries)
    for key in [("LN_COV", "BNK"), ("LN_COV", "NBF"),
                ("LN_COV", "HHD"), ("LN_COV", "NFC"),
                ("CBN_COV", "BNK"), ("CBN_COV", "NBF"),
                ("CBN_COV", "HHC"), ("CBN_COV", "ROW"),
                ("CBN_COV", "NFC"),
                ("MUN_COV", "BNK"), ("MUN_COV", "NBF"),
                ("MUN_COV", "HHC"), ("MUN_COV", "ROW"),
                ("MUN_COV", "SLG")]:
        entries[key] = 0.0
    bs = B.BalanceSheet(entries)
    res = B.build_period_ix(bs, center).close()
    got = sum(res.row_total(name, sector="TRE", account="current")
              for name in res.tfm if name.startswith("Federal Credit Fee"))
    assert got == pytest.approx(0.0)
    # ...while grandfathered interest still flows (the books remain).
    assert res.row_total("Interest on grandfathered loans (HHD->BNK)",
                         sector="BNK", account="current") > 0


# ---------------------------------------------------------------------------
# Behavioural sign tests at equal combined charge (i 4% vs i 2% + f 2%)
# ---------------------------------------------------------------------------

def test_conventional_regime_reproduces_baseline_consumption(opening, center):
    resA = B.build_period_ix(opening, center.conventional()).close()
    for g in ("HHD", "HHC"):
        got = -resA.row_total(f"Consumption ({g})", sector=g,
                              account="current")
        assert got == pytest.approx(B.C0[g]), g


def test_ix_sign_under_deficit_recycling(opening, center):
    """The hypothesis: at theta = 1 with receipts NOT recycled, the fee
    regime is more contractionary -- creditor consumption falls (the
    removed low-MPC receipt) and total impulse is negative."""
    r = B.run_pair(opening, center)
    assert r["dC_hhc"] < 0
    assert r["decomp"]["creditor_interest"] < 0
    assert r["impulse"] < 0


def test_equal_charge_debtor_loan_neutrality_at_theta_one(opening, center):
    """At full pass-through the debtor's LOAN cash flow is identical
    across regimes; the only debtor difference at theta = 1 is the
    deposit-interest loss on debtors' own small deposit holdings."""
    FA = B.policy_flows(opening, center.conventional())
    FB = B.policy_flows(opening, center)
    assert FB["loan_paid"]["HHD"] == pytest.approx(FA["loan_paid"]["HHD"])
    assert FB["dep_int"]["HHD"] < FA["dep_int"]["HHD"]


def test_incomplete_pass_through_relaxes_debtor_cashflow(opening):
    spec = B.BehaviorSpec(theta=0.5)
    r = B.run_pair(opening, spec)
    FA = B.policy_flows(opening, spec.conventional())
    FB = B.policy_flows(opening, spec)
    assert FB["loan_paid"]["HHD"] < FA["loan_paid"]["HHD"]


def test_recycling_to_debtors_flips_the_impulse(opening, center):
    spec = B.BehaviorSpec(recycling="transfers")
    r = B.run_pair(opening, spec)
    assert r["decomp"]["recycling_transfers"] > 0
    assert r["impulse"] > 0      # high-MPC recipients outspend the offset


def test_recycling_as_purchases_flips_the_impulse(opening):
    spec = B.BehaviorSpec(recycling="purchases")
    r = B.run_pair(opening, spec)
    assert r["dG"] == pytest.approx(r["fee_total"])
    assert r["impulse"] > 0


def test_decomposition_reconciles_with_accounting(opening, center):
    r = B.run_pair(opening, center)
    total = sum(r["decomp"].values())
    direct = r["dC_hhc"] + r["dC_hhd"] + r["dG"] + r["dVol"]
    assert total == pytest.approx(direct)
    assert r["impulse"] == pytest.approx(direct)
