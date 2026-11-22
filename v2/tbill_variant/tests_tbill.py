"""Tests for the T-Bill Variant machinery (tbill_variant.py)."""
import inspect

import pytest

import tbill_variant as TV


@pytest.fixture(scope="module")
def ctx():
    return TV.build_context()


def test_bucket_conservation_under_migration(ctx):
    g = TV.variant_gain(0.5, "central", ctx)
    run = g["variant"]["run"]
    tot = sum(run[f"bal_{b}_bn"] for b in TV.BUCKETS)
    assert ((tot - run["avg_total_bn"]).abs()
            / run["avg_total_bn"]).max() < 1e-9


def test_bill_share_monotone_and_large(ctx):
    run = TV.variant_gain(0.5, "central", ctx)["variant"]["run"]
    sh = run["bill_share"]
    assert sh.is_monotonic_increasing
    assert sh.iloc[0] > TV.BILL_SHARE_0          # already migrating FY27
    assert sh.iloc[-1] > 0.75                    # >3/4 bills by FY36


def test_variant_interest_is_tau_long_invariant(ctx):
    vals = [TV.variant_gain(t, "central", ctx)["variant_interest_bn"]
            for t in TV.TAU_LONGS]
    # Legacy survivors are never refinanced in kind, so tau_long has no
    # long new-issue rate to act on inside the variant.
    assert max(vals) - min(vals) < 1e-6


def test_gain_positive_at_zero_spread(ctx):
    for tau in TV.TAU_LONGS:
        assert TV.variant_gain(tau, "central", ctx)["gain_bn"] > 0


def test_gain_decreasing_in_spread_asymptote(ctx):
    gains = [TV.variant_gain(0.5, "central", ctx, s_inf_bp=s)["gain_bn"]
             for s in (0.0, 25.0, 50.0, 100.0)]
    assert all(a > b for a, b in zip(gains, gains[1:]))


def test_breakeven_brackets_zero(ctx):
    be = TV.breakeven_spread(0.5, "central", ctx)
    assert 0.3 < be < 1.5                        # pp; observed 0.79
    g_lo = TV.variant_gain(0.5, "central", ctx,
                           const_spread_pp=be - 0.1)["gain_bn"]
    g_hi = TV.variant_gain(0.5, "central", ctx,
                           const_spread_pp=be + 0.1)["gain_bn"]
    assert g_lo > 0 > g_hi


def test_engine_base_reconciles_with_lane4(ctx):
    # Characterization (not identity): Lane 4 runs a 33% front segment
    # through the full bucket recursion; the engine assigns segment dy
    # by actual bucket (bills+FRN = 24.7% of stock, repricing fraction
    # 1.0). The engine base must sit ABOVE Lane 4's (faster front
    # realization), with the gap largest at tau_long=0 and small at
    # 0.75. Bounds are the documented reconciliation, regression-guarded.
    import consolidation_tau_maturity as CT
    for tau, lo, hi in ((0.0, 1.0, 1.55), (0.75, 0.95, 1.15)):
        df = CT.coverage_table_corrected(tau, 0.0, "central", ctx)
        lane4 = float(df["interest_savings_bn"].sum())
        eng = TV.variant_gain(tau, "central", ctx)["base_interest_bn"]
        assert lo <= eng / lane4 <= hi


def test_term_premium_exhibit_is_separate(ctx):
    s0 = TV.term_premium_exhibit(0.5, "central", ctx, 0.0)
    assert float(s0.sum()) == 0.0
    s50 = TV.term_premium_exhibit(0.5, "central", ctx, 50.0)
    assert float(s50.sum()) > 0
    # the coverage machinery has no term-premium input at all
    assert "tp" not in inspect.signature(TV.variant_gain).parameters
    assert "tp" not in inspect.signature(TV.combined_structure).parameters


def test_cbo_guard():
    src = inspect.getsource(TV)
    assert "379" not in src  # CBO rule is never an input (cf. Lane 3/4)


def test_spread_schedule_endpoints():
    assert TV.spread_schedule(TV.BILL_SHARE_0, 50.0) == 0.0
    assert TV.spread_schedule(1.0, 50.0) == pytest.approx(0.005)
    assert TV.spread_schedule(0.1, 50.0) == 0.0   # below today's share


def test_cadence_arithmetic():
    c = TV.cadence_52wk()
    assert c["delta_mean_maturity_from_cadence_wk"] == 0.0
    assert c["mean_remaining_maturity_wk"] == pytest.approx(8.775)
    assert (c["peak_share_of_52wk_stock_maturing_one_date_wkly"]
            < c["peak_share_of_52wk_stock_maturing_one_date_4wkly"])


def test_shock_increment_signs():
    d = TV.frbus_shock_increment("D")
    e = TV.frbus_shock_increment("E")
    c = TV.frbus_shock_increment("C")
    assert d[2029] > 0.015          # shock elevates the plan path, peak
    assert e[2030] < -0.015         # recession collapses it
    assert all(v == 0.0 for v in c.values())
    assert d[2027] == e[2027] == 0.0
