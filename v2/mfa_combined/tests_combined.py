"""Lane 3 tests. Run: python3 -m pytest tests_combined.py -q (this dir)."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent))
import consolidation_combined as CC  # noqa: E402


@pytest.fixture(scope="module")
def ctx():
    return CC.build_context()


def test_baseline_path_anchors(ctx):
    p = ctx["base_path"]
    assert p["baseline_deficit_bn"].sum() == pytest.approx(24400.0, rel=1e-9)
    assert float(p.loc[2027, "baseline_deficit_bn"]) == pytest.approx(1875.0, abs=15)
    assert float(p.loc[2036, "baseline_deficit_bn"]) == pytest.approx(3095.0, abs=30)
    assert float(p.loc[2036, "baseline_marketable_debt_bn"]) == pytest.approx(56029.0, abs=50)
    assert float(p.loc[2027, "baseline_marketable_debt_bn"]) > CC.MARKETABLE_2026


def test_flat_reproduces_banked_totals(ctx):
    """Flat-debt fee-only totals = v2 FINAL Regime C: 1793/2262/2731/3201."""
    banked = {0.0: 1793.0, 0.25: 2262.0, 0.5: 2731.0, 0.75: 3201.0}
    fees = ctx["fees"]
    for tau, want in banked.items():
        total = float((fees["net_receipts_bn"] + fees["frbus_drag_bn"]
                       + fees["delta_remittances_bn"]
                       + ctx["savings_flat"][tau]).sum())
        assert total == pytest.approx(want, abs=1.5), tau


def test_tau_zero_zero_savings(ctx):
    df = CC.coverage_table(0.0, "central", "growing", ctx)
    assert (df["interest_savings_bn"].abs() < 1e-6).all()


def test_coverage_identity_and_iteration(ctx):
    for tau in CC.TAUS:
        df = CC.coverage_table(tau, "central", "growing", ctx)
        recomputed = (df["net_receipts_bn"] + df["frbus_drag_bn"]
                      + df["delta_remittances_bn"] + df["interest_savings_bn"])
        assert np.allclose(recomputed, df["fee_contribution_bn"], atol=1e-9)
        assert np.allclose(df["cum_margin_bn"],
                           df["cum_contribution_bn"] - df["cum_residual_bn"])
        assert 1 <= df.attrs["iterations"] <= 10


def test_savings_monotone_in_tau(ctx):
    tots = [float(CC.coverage_table(t, "central", "growing", ctx)
                  ["interest_savings_bn"].sum()) for t in CC.TAUS]
    assert tots == sorted(tots) and tots[-1] > 0


def test_mfa_residual_totals(ctx):
    r = ctx["residuals"]
    assert float(r["low"].sum()) == pytest.approx(-1289.3, abs=1.0)
    assert float(r["central"].sum()) == pytest.approx(2523.6, abs=1.0)
    assert float(r["high_stress"].sum()) == pytest.approx(10730.2, abs=1.0)
    assert (r["central"].loc[2027] == 0.0)


def test_cbo_exhibit_arithmetic(ctx):
    ex = CC.cbo_exhibit(ctx)
    assert ex["model_per_01pp_consol_bn"] == pytest.approx(96.3, abs=1.0)
    assert ex["model_flat_consol_total_bn"] == pytest.approx(938.6, abs=1.5)
    assert 0 < ex["gap_closed_by_growth_share"] < 1
    assert ex["growing_per_01pp_bn"] > ex["model_per_01pp_consol_bn"]
    # CBO number is an exhibit comparator only -- it appears nowhere in
    # the coverage machinery (guard against plug-in regression).
    src = Path(CC.__file__).read_text()
    head = src.split("def cbo_exhibit")[0]
    assert "379" not in head  # CBO rule never enters the coverage machinery
