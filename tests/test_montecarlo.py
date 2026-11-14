"""Lane I (Monte Carlo v2) tests.

Covers: exact equivalence with the deterministic module at default
parameters; seed reproducibility; accounting identities on sampled
draws; exact linearity of the public-yield term in tau (incl. the
tau = 0 bound); prior supports; and bracketing -- the deterministic
score sits inside the MC distribution, with the small median gap
explained by the covered-base variant mixture (see MONTECARLO_V2.md).
"""
import numpy as np
import pytest

from monetary_symmetry.config import IORB_BASE
from monetary_symmetry.montecarlo import (DIALS, VARIANTS, run_montecarlo,
                                          run_one_draw, sample_parameters,
                                          tau_bounds)
from monetary_symmetry.score import run_scenario
from monetary_symmetry.sfc import settlement_flows


def _default_params():
    """A one-draw parameter dict with every parameter at its
    deterministic default (central variant, no stance deviation)."""
    return {
        "beta": np.array([0.88]), "tau": np.array([0.32]),
        "variant_idx": np.array([0]),
        "turnover_factor": np.ones((1, 4)),
        "avoidance": np.array([0.065]), "haircut": np.array([0.13]),
        "stance_dev": np.zeros((1, 10)),
        "stance_path": np.array([IORB_BASE], dtype=float),
        "debt_growth": np.array([0.038]),
        "mpc": np.array([0.25]), "mult": np.array([1.25]),
    }


def test_mc_runner_reproduces_deterministic_score():
    totals, _ = run_one_draw(_default_params(), 0, 0.75)
    det = run_scenario(0.75, 0.88)["totals"]
    for k in ("gross_fee_10yr", "net_fee_10yr", "public_yield_saving_10yr",
              "iorb_remit_saving_10yr", "consolidated_interest_saving_10yr",
              "combined_total_10yr"):
        assert totals[k] == pytest.approx(det[k], rel=1e-9)


def test_seed_reproducibility():
    a = run_montecarlo(n_draws=40, seed=12345)
    b = run_montecarlo(n_draws=40, seed=12345)
    for s in DIALS:
        assert np.array_equal(a["totals"][s]["combined_total_10yr"],
                              b["totals"][s]["combined_total_10yr"])
    assert a["summary_rows"] == b["summary_rows"]
    c = run_montecarlo(n_draws=40, seed=999)
    assert not np.array_equal(a["totals"][0.75]["combined_total_10yr"],
                              c["totals"][0.75]["combined_total_10yr"])


def test_accounting_identities_on_sampled_draws():
    rng = np.random.default_rng(7)
    params = sample_parameters(rng, 25)
    for i in range(25):
        totals, annual = run_one_draw(params, i, 0.75)
        assert totals["combined_total_10yr"] == pytest.approx(
            totals["net_fee_10yr"] + totals["consolidated_interest_saving_10yr"])
        assert totals["consolidated_interest_saving_10yr"] == pytest.approx(
            totals["public_yield_saving_10yr"] + totals["iorb_remit_saving_10yr"])
        for a in annual:
            # per-year consolidated identity from the SFC ledger diffs
            assert a["consolidated_interest_saving"] == pytest.approx(
                a["public_yield_effect"] + a["iorb_remit_effect"])
            assert a["gross_fee"] >= 0.0
            assert a["iorb_remit_effect"] >= -1e-12
            assert a["public_yield_effect"] >= -1e-12
            # variant (i): fee regime never LESS contractionary here
            assert a["demand_v1_pct_gdp"] <= 1e-12
    # SFC settlement spot-check on a sampled fee magnitude: net-worth
    # changes sum to zero and the reserve drain is a stock movement.
    flows = settlement_flows(fee=0.437, treasury_spend=0.311)
    assert flows["treasury_net"] + flows["private_net"] == pytest.approx(0.0)
    assert flows["reserves_delta"] + flows["tga_delta"] == pytest.approx(0.0)


def test_tau_linearity_and_zero_bound():
    base = _default_params()
    outs = {}
    for tau in (0.0, 0.32, 0.64):
        p = dict(base)
        p["tau"] = np.array([tau])
        outs[tau], _ = run_one_draw(p, 0, 0.75)
    assert outs[0.0]["public_yield_saving_10yr"] == pytest.approx(0.0, abs=1e-12)
    assert outs[0.64]["public_yield_saving_10yr"] == pytest.approx(
        2.0 * outs[0.32]["public_yield_saving_10yr"], rel=1e-6)
    # tau touches only the coupon term: IORB/remittance line is invariant
    for tau in (0.0, 0.64):
        assert outs[tau]["iorb_remit_saving_10yr"] == pytest.approx(
            outs[0.32]["iorb_remit_saving_10yr"], rel=1e-9)
    # the published bounding cases bracket the deterministic centre
    bounds = tau_bounds()
    centre = run_scenario(0.75, 0.88)["totals"]["combined_total_10yr"]
    assert bounds[0.0][0.75]["combined_total_10yr"] < centre
    assert bounds[1.0][0.75]["combined_total_10yr"] > centre


def test_prior_supports():
    rng = np.random.default_rng(2026)
    p = sample_parameters(rng, 2000)
    assert p["beta"].min() >= 0.55 and p["beta"].max() <= 1.00
    assert p["tau"].min() >= 0.07 and p["tau"].max() <= 0.65
    assert p["avoidance"].min() >= 0.01 and p["avoidance"].max() <= 0.16
    assert p["haircut"].min() >= 0.02 and p["haircut"].max() <= 0.33
    assert p["debt_growth"].min() >= 0.005 and p["debt_growth"].max() <= 0.075
    assert p["turnover_factor"].min() >= 0.75
    assert p["turnover_factor"].max() <= 1.25
    assert set(np.unique(p["variant_idx"])) == {0, 1, 2}
    # stance path stays at/above the floor and is centred near IORB_BASE
    assert p["stance_path"].min() >= 0.05
    assert abs(p["stance_dev"].mean()) < 0.05


def test_deterministic_centre_is_bracketed():
    mc = run_montecarlo(n_draws=300, seed=20261114)
    for row in mc["summary_rows"]:
        det = row["deterministic_combined"]
        comb = mc["totals"][row["s"]]["combined_total_10yr"]
        p5, p95 = np.percentile(comb, [5, 95])
        assert p5 < det < p95
        # Median sits below the deterministic centre at every dial:
        # the deterministic run conditions on the CENTRAL covered base,
        # while 30% of draws use the strict loans-only base. The gap is
        # a mixture effect, bounded here at 12% (observed ~5% at
        # n = 10,000); conditional on the central variant the median is
        # within ~1% of deterministic (MONTECARLO_V2.md).
        assert abs(row["combined_total_median"] - det) / det < 0.12
    # variant shares land near the analyst-chosen 50/30/20 weights
    shares = np.bincount(mc["params"]["variant_idx"], minlength=3) / 300
    assert shares[0] == pytest.approx(0.50, abs=0.10)
    assert len(VARIANTS) == 3
