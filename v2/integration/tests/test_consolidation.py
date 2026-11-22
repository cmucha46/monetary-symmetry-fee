"""Sanity tests for the MSF v2 consolidation engine.

Run from the integration directory:  python3 -m pytest tests/ -q
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "cohort"))

from consolidation import (  # noqa: E402
    FED_SHARE, PUBLIC_SHARE, TAUS, TAX_INTERACTION_HAIRCUT, YEARS,
    base_status, consolidate, dy_path_for_tau, erosion_path,
    load_fiscal_skeleton, treasury_savings_by_year)

CENTRAL = dict(base="loans_only", design="floating", turnover="central",
               theta=1.0, erosion_yr5=0.10)


@pytest.fixture(scope="module")
def tables():
    return consolidate(**CENTRAL)


def test_consolidation_identity(tables):
    """Components sum to the consolidated total, every year, every tau."""
    for tau in TAUS:
        df = tables[tau]
        recomputed = (df["net_fee_receipts_bn"]
                      + df["treasury_savings_consol_bn"]
                      + df["delta_remittances_bn"])
        assert np.allclose(recomputed, df["consolidated_net_bn"],
                           atol=1e-9), f"identity fails at tau={tau}"


def test_no_double_count_fed_held_interest(tables):
    """Consolidated savings are exactly the non-Fed-held share of gross
    savings; the Fed-held share is excluded once, not counted twice
    (memo sec. III.C)."""
    assert FED_SHARE + PUBLIC_SHARE == pytest.approx(1.0)
    assert 0.0 < FED_SHARE < 1.0
    for tau in TAUS:
        df = tables[tau]
        assert np.allclose(df["treasury_savings_consol_bn"],
                           df["treasury_savings_gross_bn"] * PUBLIC_SHARE,
                           atol=1e-9)


def test_tau_zero_means_zero_savings(tables):
    """tau = 0 => no yield response => zero Treasury interest savings."""
    df = tables[0.0]
    assert (df["treasury_savings_gross_bn"].abs() < 1e-9).all()
    assert (df["treasury_savings_consol_bn"].abs() < 1e-9).all()
    skel = load_fiscal_skeleton()
    assert all(v == 0.0 for v in dy_path_for_tau(0.0, skel).values())


def test_savings_monotone_in_tau(tables):
    """Higher tau cannot reduce savings (dy is weakly more negative)."""
    totals = [tables[tau]["treasury_savings_consol_bn"].sum() for tau in TAUS]
    assert totals == sorted(totals)
    assert totals[-1] > 0  # tau=0.75 produces real savings by construction


def test_deferred_asset_timing_respected(tables):
    """No cash remittance delta while the deferred asset is being rebuilt:
    the skeleton's MS path pays $0 cash in FY2027-29 despite higher
    earnings, and the first positive MS cash remittance (FY2030) coincides
    with the deferred asset reaching zero."""
    skel = load_fiscal_skeleton()
    for t in (2027, 2028, 2029):
        assert skel.loc[t, "deferred_asset_bn_ms"] < 0
        assert skel.loc[t, "cash_remittance_bn_ms"] == 0.0
    assert skel.loc[2030, "deferred_asset_bn_ms"] == 0.0
    assert skel.loc[2030, "cash_remittance_bn_ms"] > 0
    df = tables[0.5]  # any tau: remittances are tau-independent in this pass
    for t in (2027, 2028, 2029):
        assert df.loc[t, "delta_remittances_bn"] == 0.0
    assert df.loc[2030, "delta_remittances_bn"] > 0


def test_repricing_matches_cohort_skeleton():
    """Time-varying repricing with a CONSTANT dy=-100bp must reproduce the
    cohort lane's fiscal.treasury_interest_delta(-0.01) (sign flipped:
    savings = -(interest delta))."""
    import fiscal as cohort_fiscal
    delta = cohort_fiscal.treasury_interest_delta(-0.01).set_index("fy")
    mine = treasury_savings_by_year({t: -0.01 for t in YEARS})
    for t in YEARS:
        assert mine[t] == pytest.approx(-delta.loc[t, "interest_delta_bn"],
                                        rel=1e-9)


def test_erosion_bounds_and_zero_case():
    assert all(v == 0.0 for v in erosion_path(0.0, 1.15).values())
    e = erosion_path(0.40, 1.15)
    assert max(e.values()) <= 0.60 + 1e-12          # cap respected
    assert e[2027] == 0.0 and e[2032] == pytest.approx(0.46)
    assert e[2028] < e[2030] < e[2032]              # phase-in is monotone


def test_net_fee_formula(tables):
    """Net = gross x (1 - erosion) x (1 - haircut), haircut as documented."""
    df = tables[0.25]
    expected = (df["gross_collections_bn"] * (1 - df["erosion_rate"])
                * (1 - TAX_INTERACTION_HAIRCUT))
    assert np.allclose(expected, df["net_fee_receipts_bn"], atol=1e-9)


def test_first_year_is_zero(tables):
    """FY2027: no collections (pre-effective-date), no savings (IORB paths
    have not diverged), no remittance delta => consolidated net is zero."""
    for tau in TAUS:
        assert tables[tau].loc[2027, "consolidated_net_bn"] == 0.0


def test_base_status_consistency():
    """If unified outputs are absent, the engine must fall back to
    loans-only AND flag it; if present, they must pass provenance."""
    status = base_status()
    if status["unified_present"]:
        assert status["headline"] == "unified"
    else:
        assert status["headline"] == "loans_only"
        assert "NOT YET PRESENT" in status["note"] or "provenance" in status["note"]


def test_placeholder_slots_are_empty(tables):
    """FRB/US + SFC Section IX slots exist and are EMPTY (NaN) -- present
    as an interface, never fabricated."""
    df = tables[0.5]
    assert "frbus_feedback_bn" in df.columns
    assert "sfc_ix_adjustment_bn" in df.columns
    assert df["frbus_feedback_bn"].isna().all()
    assert df["sfc_ix_adjustment_bn"].isna().all()
