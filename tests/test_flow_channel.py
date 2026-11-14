import pytest

from monetary_symmetry.config import NET_RECEIPTS_FACTOR
from monetary_symmetry.flow_channel import (BETA_CENTRAL, DIALS,
                                            FRBUS_GAP_S75_PP, episode_flows,
                                            gdp, regime_flows, regime_totals)
from monetary_symmetry.score import run_scenario


@pytest.mark.parametrize("s", DIALS)
def test_sector_table_zero_sum_every_year(s):
    for f in regime_flows(s):
        assert f.sector_sum() == pytest.approx(0.0, abs=1e-9)


@pytest.mark.parametrize("s", DIALS)
def test_injection_removed_equals_consolidated_saving(s):
    # The private sector's lost interest injection IS the fiscal score's
    # consolidated interest saving -- same dollars, two sides.
    res = run_scenario(s, BETA_CENTRAL)
    for f, d in zip(regime_flows(s), res["diffs"]):
        assert f.injection_removed == pytest.approx(d["consolidated_saving"])
        assert f.injection_removed == pytest.approx(f.e_iorb + f.e_coupon)
        assert f.injection_base - f.injection_scen == pytest.approx(
            f.injection_removed)


@pytest.mark.parametrize("s", DIALS)
def test_creditor_loss_identity(s):
    # Lenders' lending-channel net loss == net fee, every year: borrower
    # all-in cost is held at the desired stance, so the fee is creditor
    # income redirected to Treasury (net of the A1 tax offset).
    for f in regime_flows(s):
        lender_lending_loss = f.gross_fee - (f.gross_fee - f.net_fee)
        assert lender_lending_loss == pytest.approx(f.net_fee)
        assert f.net_fee == pytest.approx(f.gross_fee * NET_RECEIPTS_FACTOR)
        # banks/lenders sector = lending loss + IORB loss
        assert f.sec_banks_lenders == pytest.approx(-f.net_fee - f.e_iorb)
        assert f.sec_other_private == pytest.approx(-f.e_coupon)
        assert f.sec_borrowers == 0.0


def test_variant1_private_removed_equals_combined_score():
    # Under variant (i) the 10-yr private income removed equals the repo's
    # combined fiscal score (net fee + consolidated interest saving).
    for s in DIALS:
        flows = regime_flows(s)
        totals = regime_totals(flows)
        combined = run_scenario(s, BETA_CENTRAL)["totals"]["combined_total_10yr"]
        assert totals["private_income_removed_v1"] == pytest.approx(combined)


def test_flows_grow_with_dial():
    t50 = regime_totals(regime_flows(0.50))
    t75 = regime_totals(regime_flows(0.75))
    t90 = regime_totals(regime_flows(0.90))
    assert t50["injection_removed"] < t75["injection_removed"] < t90["injection_removed"]
    assert t50["gross_fee"] < t75["gross_fee"] < t90["gross_fee"]


def test_no_flows_before_fee_in_force():
    f2027 = regime_flows(0.75)[0]
    assert f2027.year == 2027
    assert f2027.gross_fee == 0.0
    assert f2027.injection_removed == pytest.approx(0.0)


def test_variant2_redistributes_not_removes():
    # Variant (ii): the net fee returns to private recipients, so the
    # demand range must lie ABOVE variant (i)'s (less contractionary or
    # expansionary) in every year with a fee.
    for f in regime_flows(0.75):
        if f.gross_fee > 0:
            assert f.demand_v2_hi > f.demand_v1_hi
            assert f.demand_v2_lo > f.demand_v1_lo


def test_episode_algebra_matches_lane_g():
    e = episode_flows(0.75, BETA_CENTRAL, book_basis="mature")
    assert e.drff_pp == pytest.approx(0.275, abs=0.002)
    assert e.f_inc_pp == pytest.approx(0.824, abs=0.002)
    assert e.wedge_pp == pytest.approx(0.725, abs=0.002)
    assert e.d_iorb_injection == pytest.approx(2.93 * 0.725 / 100.0, abs=1e-4)
    assert FRBUS_GAP_S75_PP == pytest.approx(0.649)


def test_episode_mature_book_exceeds_contemporaneous():
    em = episode_flows(0.75, BETA_CENTRAL, book_basis="mature")
    ec = episode_flows(0.75, BETA_CENTRAL, book_basis="contemporaneous")
    assert em.fee_net_hi > ec.fee_net_hi
    # demand effect is a relative contraction under variant (i)
    assert em.demand_hi < 0 and em.demand_lo < em.demand_hi


def test_gdp_path_monotone():
    assert gdp(2036) > gdp(2027) > 0
