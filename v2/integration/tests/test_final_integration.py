"""Tests for the final integration pass: Lane B feedback extraction,
its application in the consolidation, and the Treasuries appendix.

Run from the integration directory:  python3 -m pytest tests/ -q
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "cohort"))

from consolidation import TAUS, consolidate, load_summary  # noqa: E402
from frbus_feedback import annual_series, metrics, regime_feedback  # noqa: E402
from treasuries_appendix import treasuries_appendix  # noqa: E402

CENTRAL = dict(base="unified", design="floating", turnover="central",
               theta=1.0, erosion_yr5=0.10)
LOANS_GROSS = float(load_summary("loans_only", "floating", "central")
                    ["collections_bn"].sum())


# ----------------------------------------------------------------------
# Lane B extraction: the drag identity reproduces Lane B's own metrics
# ----------------------------------------------------------------------
@pytest.mark.parametrize("regime", ["B", "C", "D", "E"])
def test_drag_identity_matches_lane_b_metrics(regime):
    s = annual_series(regime)
    m = metrics(regime)
    w = slice(2028, 2036)
    assert s.loc[w, "receipts_bn"].sum() == pytest.approx(
        m["receipts_total_bn"], abs=2.0)
    assert s.loc[w, "d_surplus_bn"].sum() == pytest.approx(
        m["cum_dgfsrpn_bn"], abs=2.0)
    assert s.loc[w, "d_interest_bn"].sum() == pytest.approx(
        m["cum_dgfintn_bn"], abs=2.0)
    drag = (m["cum_dgfsrpn_bn"] - m["receipts_total_bn"]
            + m["cum_dgfintn_bn"])
    assert s.loc[w, "drag_bn"].sum() == pytest.approx(drag, abs=2.0)
    assert drag < 0  # the endogenous fiscal drag is negative in all regimes


def test_receipts_ratios():
    """Fee-path reconciliation: B/C/D settle above the skeleton path;
    E collapses (procyclical revenue)."""
    for regime in ("B", "C", "D"):
        fb = regime_feedback(regime, LOANS_GROSS)
        assert 1.05 < fb["receipts_ratio"] < 1.20
    fb_e = regime_feedback("E", LOANS_GROSS)
    assert fb_e["receipts_ratio"] < 0.70


# ----------------------------------------------------------------------
# Application: feedback lowers the total, scales fees, leaves SFC empty
# ----------------------------------------------------------------------
@pytest.fixture(scope="module")
def with_feedback():
    return consolidate(macro_feedback="C", **CENTRAL)


@pytest.fixture(scope="module")
def without_feedback():
    return consolidate(**CENTRAL)


def test_feedback_reduces_total_every_tau(with_feedback, without_feedback):
    for tau in TAUS:
        assert (with_feedback[tau]["consolidated_net_bn"].sum()
                < without_feedback[tau]["consolidated_net_bn"].sum())


def test_feedback_scales_fees_and_preserves_skeleton(with_feedback):
    fb = regime_feedback("C", LOANS_GROSS)
    df = with_feedback[0.5]
    assert np.allclose(df["net_fee_receipts_bn"],
                       df["net_fee_receipts_skeleton_bn"]
                       * fb["receipts_ratio"], atol=1e-9)
    assert np.allclose(df["fee_path_ratio"], fb["receipts_ratio"])


def test_feedback_identity(with_feedback):
    """Consolidated = skeleton components + fee rescaling + drag."""
    for tau in TAUS:
        df = with_feedback[tau]
        recomputed = (df["net_fee_receipts_bn"]
                      + df["treasury_savings_consol_bn"]
                      + df["delta_remittances_bn"]
                      + df["frbus_feedback_bn"])
        assert np.allclose(recomputed, df["consolidated_net_bn"], atol=1e-9)


def test_sfc_slot_still_empty_by_design(with_feedback):
    df = with_feedback[0.5]
    assert df["sfc_ix_adjustment_bn"].isna().all()
    assert df["frbus_feedback_bn"].notna().all()


def test_regime_e_fee_collapse(without_feedback):
    e = consolidate(macro_feedback="E", **CENTRAL)
    assert (e[0.5]["net_fee_receipts_bn"].sum()
            < 0.7 * without_feedback[0.5]["net_fee_receipts_bn"].sum())


# ----------------------------------------------------------------------
# Treasuries appendix
# ----------------------------------------------------------------------
@pytest.fixture(scope="module")
def tsy():
    return treasuries_appendix()


def test_issuer_assessed_nets_exactly_zero(tsy):
    assert (tsy["issuer_assessed_net_bn"] == 0.0).all()
    assert tsy["issuer_assessed_churn_bn"].sum() > 1000  # churn is large


def test_holder_assessed_nets_to_timing_residual(tsy):
    """Holder-assessed: receipts and extra interest are both ~$2T+
    consolidated over the window; the net is a small timing residual
    relative to the gross flows -- inclusion buys ~nothing."""
    rec = tsy["receipts_consol_bn"].sum()
    ext = tsy["extra_interest_consol_bn"].sum()
    net = tsy["net_consol_bn"].sum()
    assert rec > 2000 and ext > 2000
    assert abs(net) < 0.15 * rec
    assert net == pytest.approx(rec - ext, rel=1e-9)
