"""Lane 4 tests. Run: python3 -m pytest tests_tau_maturity.py -q (this dir)."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent))
import consolidation_combined as CC  # noqa: E402
import consolidation_tau_maturity as CT  # noqa: E402


@pytest.fixture(scope="module")
def ctx():
    return CT.build_context_corrected()


@pytest.fixture(scope="module")
def avg_base(ctx):
    avg, prev = {}, CT.MARKETABLE_2026
    for t in CT.YEARS:
        avg[t] = (prev + float(ctx["base_path"].loc[
            t, "baseline_marketable_debt_bn"])) / 2
        prev = float(ctx["base_path"].loc[t, "baseline_marketable_debt_bn"])
    return avg


def test_front_weight_from_maturity_structure():
    assert CT.W_FRONT == pytest.approx(0.33)
    assert CT.W_FRONT + CT.W_LONG == pytest.approx(1.0)


def test_front_end_tau_one_identity(avg_base):
    """Front-end dy at spread 0 IS the scalar tau=1 dy (transmission 1 by
    arbitrage), and front segment savings = W_FRONT x scalar tau=1 savings
    on the same debt path."""
    import consolidation as C
    skel = C.load_fiscal_skeleton()
    scalar_tau1 = C.dy_path_for_tau(1.0, skel)
    assert CT.dy_front(0.0) == pytest.approx(scalar_tau1)
    front, _ = CT.segment_savings_on_path(avg_base, 0.5, 0.0)
    full_tau1 = CC.savings_on_path(avg_base, scalar_tau1)
    assert np.allclose(front, CT.W_FRONT * full_tau1, atol=1e-9)


def test_administered_decline_verified():
    A = CT.administered_decline()
    assert all(A[t] == 0.0 for t in (2027, 2028, 2029))
    assert all(A[t] == pytest.approx(0.0195) for t in range(2030, 2037))


def test_spread_sign_and_long_unaffected(avg_base):
    f_lo, l_lo = CT.segment_savings_on_path(avg_base, 0.5, -0.25)
    f_0, l_0 = CT.segment_savings_on_path(avg_base, 0.5, 0.0)
    f_hi, l_hi = CT.segment_savings_on_path(avg_base, 0.5, 0.15)
    assert float(f_lo.sum()) > float(f_0.sum()) > float(f_hi.sum())
    assert np.allclose(l_lo, l_0) and np.allclose(l_0, l_hi)


def test_corrected_ge_scalar_growing(ctx):
    """Corrected interest line >= Lane 3 scalar at every long-segment tau
    (spread 0 and +0.15), combined growing path, central scenario."""
    for ds in (0.0, 0.15):
        for tau in CT.TAU_LONGS:
            corr = CT.coverage_table_corrected(tau, ds, "central", ctx)
            scalar = CC.coverage_table(tau, "central", "growing", ctx)
            assert float(corr["interest_savings_bn"].sum()) >= \
                float(scalar["interest_savings_bn"].sum()) - 1e-6, (ds, tau)


def test_corrected_ge_scalar_flat_v2():
    ctx2 = CT.build_context_corrected()
    for r in CT.v2_restatement(ctx2):
        assert r["corrected_interest_bn"] >= r["v2_scalar_interest_bn"] - 1e-6
        assert r["interest_delta_bn"] > 0  # understated at EVERY tau_long


def test_tau_long_zero_still_saves(ctx):
    """At tau_long=0 the front end still saves (arbitrage), unlike scalar."""
    df = CT.coverage_table_corrected(0.0, 0.0, "central", ctx)
    assert float(df["interest_savings_bn"].sum()) > 800
    assert (df["long_savings_bn"].abs() < 1e-6).all()


def test_split_adds_to_total(ctx):
    df = CT.coverage_table_corrected(0.5, 0.0, "central", ctx)
    assert np.allclose(df["front_savings_bn"] + df["long_savings_bn"],
                       df["interest_savings_bn"], atol=1e-9)


def test_cbo_guard_still_passing():
    """The CBO comparator figure appears nowhere in the coverage machinery
    of either Lane 3 or Lane 4 (exhibit functions excluded)."""
    for mod in (CC, CT):
        src = Path(mod.__file__).read_text()
        marker = "def cbo_exhibit" if mod is CC else "def cbo_corrected"
        assert "379" not in src.split(marker)[0], mod.__name__


def test_cbo_corrected_figure(ctx):
    ex = CT.cbo_corrected(ctx)
    assert ex["corrected_per_01pp_bn"] == pytest.approx(190.6, abs=1.5)
    assert ex["gap_closed_total_share"] == pytest.approx(0.334, abs=0.01)
    assert ex["gap_closed_total_share"] > ex["gap_closed_by_growth_share_lane3"]
