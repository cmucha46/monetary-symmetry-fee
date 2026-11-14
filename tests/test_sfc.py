import pytest

from monetary_symmetry.config import IORB_BASE, YEARS
from monetary_symmetry.sfc import LedgerParams, run_ledger_pair, settlement_flows


def test_settlement_flows_zero_sum():
    f = settlement_flows(fee=0.40, treasury_spend=0.30)
    assert f["treasury_net"] + f["private_net"] + f["banks_net"] + f["fed_net"] == pytest.approx(0.0)
    assert f["reserves_delta"] + f["tga_delta"] == pytest.approx(0.0)


def test_reserve_drain_is_not_revenue_twice():
    # Collect F, spend nothing: reserves fall F, TGA rises F, private net worth
    # falls F, Treasury rises F -- one transfer, counted once.
    f = settlement_flows(fee=0.40, treasury_spend=0.0)
    assert f["reserves_delta"] == pytest.approx(-0.40)
    assert f["treasury_net"] == pytest.approx(0.40)
    # Spend it all back: reserves are fully restored; no permanent drain remains.
    f2 = settlement_flows(fee=0.40, treasury_spend=0.40)
    assert f2["reserves_delta"] == pytest.approx(0.0)
    assert f2["treasury_net"] == pytest.approx(0.0)


def test_consolidated_vs_gross_identity():
    # consolidated == gross interest on ALL debt - Fed economic net income,
    # every year, in both baseline and scenario (internal Fed-held interest nets out).
    base, scen, _ = run_ledger_pair(IORB_BASE, [r * 0.5 for r in IORB_BASE])
    for rows in (base, scen):
        for r in rows:
            assert r["consolidated_net_interest"] == pytest.approx(
                r["gross_interest_all_debt"] - r["fed_net_income"])


def test_decomposition_is_exact():
    _, _, diffs = run_ledger_pair(IORB_BASE, [r * 0.5 for r in IORB_BASE])
    for d in diffs:
        assert d["consolidated_saving"] == pytest.approx(
            d["public_yield_effect"] + d["iorb_remit_effect"])


def test_no_fee_baseline_zero_saving():
    _, _, diffs = run_ledger_pair(IORB_BASE, list(IORB_BASE))
    for d in diffs:
        assert d["consolidated_saving"] == pytest.approx(0.0)
        assert d["public_yield_effect"] == pytest.approx(0.0)


def test_deferred_asset_mechanics_negative_income():
    # Force deeply negative Fed income: IORB 10% on reserves, near-zero asset yields.
    p = LedgerParams(fed_treasury_yield_start=0.1, fed_mbs_yield=0.1,
                     deferred_asset_start=0.0, term_premium=0.0,
                     treasury_repricing_share=0.0, fed_asset_roll=0.0)
    base, _, _ = run_ledger_pair([10.0] * len(YEARS), [10.0] * len(YEARS), p)
    r0 = base[0]
    assert r0["fed_net_income"] < 0
    assert r0["remittance_cash"] == 0.0                       # remittances stop
    assert r0["deferred_asset"] == pytest.approx(-r0["fed_net_income"])  # shortfall accrues


def test_deferred_asset_paydown_before_remittance():
    # Start with a deferred asset and strong positive income: the first income
    # pays the asset down; cash remittance is only the excess.
    p = LedgerParams(fed_treasury_yield_start=5.0, fed_mbs_yield=5.0,
                     deferred_asset_start=0.05, term_premium=0.0,
                     treasury_repricing_share=0.0, fed_asset_roll=0.0)
    base, _, _ = run_ledger_pair([0.5] * len(YEARS), [0.5] * len(YEARS), p)
    r0 = base[0]
    assert r0["fed_net_income"] > 0.05
    assert r0["deferred_asset"] == pytest.approx(0.0)
    assert r0["remittance_cash"] == pytest.approx(r0["fed_net_income"] - 0.05)


def test_repricing_is_gradual_not_plugin():
    # A permanent 1pp lower IORB moves the effective public yield only by
    # repricing_share * transmission in year 1 -- not by the full amount, and
    # there is no CBO-weight anywhere in the calculation.
    p = LedgerParams()
    base, scen, _ = run_ledger_pair(IORB_BASE, [r - 1.0 for r in IORB_BASE], p)
    drop_y = base[0]["y_public"] - scen[0]["y_public"]
    assert 0 < drop_y < p.treasury_repricing_share * p.yield_transmission * 1.0 + 1e-9
    # and the effective yield keeps converging in later years
    drop_y_last = base[-1]["y_public"] - scen[-1]["y_public"]
    assert drop_y_last > drop_y


def test_fed_asset_income_does_not_reset_instantly():
    # Fed book yield moves by fed_asset_roll share only in year 1.
    p = LedgerParams()
    base, scen, _ = run_ledger_pair(IORB_BASE, [r - 1.0 for r in IORB_BASE], p)
    dy = abs(base[0]["y_fed_ts"] - scen[0]["y_fed_ts"])
    assert dy <= p.fed_asset_roll * p.yield_transmission + 1e-9
