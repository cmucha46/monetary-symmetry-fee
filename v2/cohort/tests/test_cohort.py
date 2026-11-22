"""Sanity tests for the Monetary Symmetry Fee v2 cohort + fiscal skeleton.

These test accounting/mechanical properties only -- grandfathering, the
collections identity, asymptotic coverage, vintage consistency, and the
Treasury repricing calibration. They assert nothing about economic outcomes.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from cohort_model import default_fee_path, run_category, run_model, summary_table  # noqa: E402
from data import CATEGORIES, TREASURY  # noqa: E402
import fiscal  # noqa: E402

FEE = default_fee_path()


@pytest.fixture(scope="module")
def total():
    return summary_table(run_model(FEE, design="floating", delta_case="central"))


def test_no_coverage_before_effective_date(total):
    assert total.loc[2027, "covered_stock_bn"] == 0.0
    assert total.loc[2027, "collections_bn"] == 0.0


def test_covered_stock_starts_near_zero(total):
    # After one year only one year's originations are covered.
    assert total.loc[2028, "covered_share"] < 0.35


def test_covered_share_monotone_and_bounded(total):
    s = total["covered_share"].values
    assert np.all(np.diff(s) >= -1e-12)
    assert np.all((s >= 0) & (s <= 1.0))


def test_grandfathered_stock_decays(total):
    g = total["grandfathered_stock_bn"]
    assert g.loc[2036] < g.loc[2028]


def test_collections_identity_floating(total):
    # collections_t == f_t * average covered stock, every year.
    cov = total["covered_stock_bn"].values
    avg = 0.5 * (cov[:-1] + cov[1:])
    expect = total["fee_rate"].values[1:] * avg
    got = total["collections_bn"].values[1:]
    # FY2027->2028 step: C(2027)=0 so identity holds exactly there too.
    assert np.allclose(got, expect, atol=1e-6)


def test_stock_conservation_per_category():
    df = run_model(FEE)
    for _, row in df.iterrows():
        assert abs(row["covered_stock_bn"] + row["grandfathered_stock_bn"]
                   - row["eligible_stock_bn"]) < 1e-6


def test_asymptote_toward_full_coverage():
    # With a constant stock (g=0) and 50 years, coverage -> ~100%.
    fee = {y: 0.02 for y in range(2027, 2078)}
    df = run_category(1000.0, 0.10, 0.0, fee, "floating",
                      years=range(2027, 2078))
    assert df.iloc[-1]["covered_share"] > 0.99
    # Closed form: share(t) = 1 - (1-delta)^(t - 2027) after effective date.
    t = 10
    expect = 1 - 0.9 ** t
    got = df[df["fy"] == 2027 + t].iloc[0]["covered_share"]
    assert abs(got - expect) < 0.02  # within-year averaging tolerance


def test_locked_design_defers_collections_when_rates_rise():
    # Fee path rises over time, so locking vintages at origination rates
    # must collect LESS than the floating design in later years.
    fl = summary_table(run_model(FEE, design="floating"))
    lk = summary_table(run_model(FEE, design="locked"))
    assert lk.loc[2036, "collections_bn"] < fl.loc[2036, "collections_bn"]
    # But both designs must reach identical covered STOCKS.
    assert np.allclose(lk["covered_stock_bn"], fl["covered_stock_bn"])


def test_turnover_sensitivity_ordering():
    shares = {}
    for case in ("low", "central", "high"):
        st = summary_table(run_model(FEE, delta_case=case))
        shares[case] = st.loc[2036, "covered_share"]
    assert shares["low"] < shares["central"] < shares["high"]


def test_category_stocks_sum_to_documented_total():
    expect = sum(c["stock_bn"] for c in CATEGORIES.values())
    assert abs(expect - 30873.3) < 1.0  # see DATA.md build-up


def test_treasury_year1_repricing_matches_published():
    df = fiscal.treasury_repricing(dy=0.0)
    assert abs(df.iloc[0]["repriced_share"] - TREASURY["share_maturing_1yr"]) < 0.01


def test_treasury_zero_shift_zero_delta():
    d = fiscal.treasury_interest_delta(0.0)
    assert np.allclose(d["interest_delta_bn"], 0.0)


def test_fed_deferred_asset_identity():
    path = {y: 0.039 for y in range(2027, 2037)}
    df = fiscal.fed_remittances(path)
    # While the deferred asset is being rebuilt, cash remittances are zero
    # or earnings are first absorbed by it: deferred asset never exceeds 0
    # before cash flows, and earnings identity holds row by row.
    for _, r in df.iterrows():
        assert abs(r["net_earnings_bn"] - (r["interest_income_bn"]
                                           - r["iorb_expense_bn"] - 12.0)) < 1e-9
    assert (df["deferred_asset_bn"] <= 1e-9).all()
    assert (df["cash_remittance_bn"] >= 0).all()
