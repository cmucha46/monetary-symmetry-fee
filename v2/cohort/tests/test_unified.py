"""Sanity tests for the UNIFIED BASE (Base B) extension.

Mechanical/accounting properties only, mirroring test_cohort.py's
discipline: grandfathering (zero pre-effective coverage), stock
conservation, monotone phase-in, the phase-in lag of slow-turnover bond
categories, and the headline/sensitivity relationship between the
unified base and loans-only Base A. Nothing here asserts an economic
outcome.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from cohort_model import default_fee_path, run_model, summary_table  # noqa: E402
from unified_data import BOND_CATEGORIES, UNIFIED_CATEGORIES, UNIFIED_TOTAL_BN  # noqa: E402
from unified_model import run_unified_model  # noqa: E402

FEE = default_fee_path()


@pytest.fixture(scope="module")
def unified():
    return run_unified_model(FEE, design="floating", delta_case="central")


@pytest.fixture(scope="module")
def unified_total(unified):
    return summary_table(unified)


def test_unified_eligible_total():
    expect = 30873.3 + 9321.4 + 3519.6  # loans + biz debt sec. + munis
    assert abs(UNIFIED_TOTAL_BN - expect) < 1.0
    assert abs(sum(c["stock_bn"] for c in UNIFIED_CATEGORIES.values())
               - expect) < 1.0


def test_bond_categories_present_with_documented_stocks():
    assert BOND_CATEGORIES["biz_bonds"]["stock_bn"] == 9321.4
    assert BOND_CATEGORIES["gov_muni_bonds"]["stock_bn"] == 3519.6


def test_no_coverage_before_effective_date(unified, unified_total):
    assert unified_total.loc[2027, "covered_stock_bn"] == 0.0
    assert unified_total.loc[2027, "collections_bn"] == 0.0
    bonds = unified[unified["category"].isin(BOND_CATEGORIES)]
    assert (bonds[bonds["fy"] == 2027]["covered_stock_bn"] == 0.0).all()
    assert (bonds[bonds["fy"] == 2027]["collections_bn"] == 0.0).all()


def test_covered_share_monotone_and_bounded_unified(unified_total):
    s = unified_total["covered_share"].values
    assert np.all(np.diff(s) >= -1e-12)
    assert np.all((s >= 0) & (s <= 1.0))


def test_stock_conservation_unified(unified):
    for _, row in unified.iterrows():
        assert abs(row["covered_stock_bn"] + row["grandfathered_stock_bn"]
                   - row["eligible_stock_bn"]) < 1e-6


def test_bond_phase_in_lags_fast_loan_categories(unified):
    share = (unified.pivot(index="fy", columns="category",
                           values="covered_share"))
    # Slow bond turnover (delta 0.09-0.11) must trail fast loan turnover
    # (business loans delta 0.33) at every horizon.
    for fy in (2030, 2033, 2036):
        assert share.loc[fy, "biz_bonds"] < share.loc[fy, "biz_loans_nonmortgage"]
        assert share.loc[fy, "gov_muni_bonds"] < share.loc[fy, "biz_loans_nonmortgage"]


def test_unified_share_below_loans_only_share(unified_total):
    # Adding slow-turnover bonds dilutes the covered share relative to
    # the loans-only base at every date, even though the unified covered
    # STOCK and collections are larger.
    a = summary_table(run_model(FEE, design="floating", delta_case="central"))
    assert (unified_total["covered_share"].values[1:]
            < a["covered_share"].values[1:]).all()


def test_unified_collections_exceed_loans_only(unified_total):
    a = summary_table(run_model(FEE, design="floating", delta_case="central"))
    assert (unified_total["collections_bn"].values
            >= a["collections_bn"].values).all()
    assert unified_total["collections_bn"].sum() > a["collections_bn"].sum()


def test_locked_design_same_covered_stock_bonds():
    fl = summary_table(run_unified_model(FEE, design="floating"))
    lk = summary_table(run_unified_model(FEE, design="locked"))
    assert np.allclose(lk["covered_stock_bn"], fl["covered_stock_bn"])
    # Rising fee path: locking vintages at origination rates collects
    # less in later years, for the unified base as for loans-only.
    assert lk.loc[2036, "collections_bn"] < fl.loc[2036, "collections_bn"]


def test_turnover_ordering_unified():
    shares = {}
    for case in ("low", "central", "high"):
        st = summary_table(run_unified_model(FEE, delta_case=case))
        shares[case] = st.loc[2036, "covered_share"]
    assert shares["low"] < shares["central"] < shares["high"]
