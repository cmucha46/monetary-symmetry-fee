import pytest

from monetary_symmetry.config import INTRO_FEE_2028_PP
from monetary_symmetry.policy import fee_from_iorb, policy_for


def test_fee_formula_at_bounds():
    # f = r * s/(1-s): at s=0.5, f == r; at s=0.9, f == 9r
    assert fee_from_iorb(3.0, 0.50) == pytest.approx(3.0)
    assert fee_from_iorb(3.0, 0.90) == pytest.approx(27.0)
    assert fee_from_iorb(2.0, 0.75) == pytest.approx(6.0)


def test_fee_formula_rejects_out_of_range_dial():
    with pytest.raises(ValueError):
        fee_from_iorb(3.0, 0.49)
    with pytest.raises(ValueError):
        fee_from_iorb(3.0, 0.91)
    with pytest.raises(ValueError):
        policy_for(3.0, 0.95, 0.88, 1.0)


def test_all_in_identity():
    # desired == IORB + beta * fee whenever the ZLB does not bind
    for s in (0.5, 0.75, 0.9):
        for beta in (0.7, 0.88, 1.0):
            iorb, fee = policy_for(3.4, s, beta, 1.0)
            assert iorb + beta * fee == pytest.approx(3.4)


def test_zlb_floor_and_fee_collapse():
    # r >= 0 always; at desired = 0 the fee degenerates to 0 even at s = 0.9
    iorb, fee = policy_for(0.0, 0.90, 0.88, 1.0)
    assert iorb == 0.0 and fee == 0.0
    assert fee_from_iorb(0.0, 0.90) == 0.0
    # as r -> 0 at s = 0.9, f = 9r -> 0 linearly (no explosion once IORB is solved down)
    assert fee_from_iorb(0.10, 0.90) == pytest.approx(0.90)
    assert fee_from_iorb(0.01, 0.90) == pytest.approx(0.09)
    iorb, fee = policy_for(-1.0, 0.90, 0.88, 1.0)  # negative desired is floored
    assert iorb == 0.0 and fee == 0.0


def test_2028_intro_branch():
    iorb, fee = policy_for(3.9, 0.75, 0.88, -1.0)
    assert fee == INTRO_FEE_2028_PP
    assert iorb == pytest.approx(3.9 - 0.88 * INTRO_FEE_2028_PP)


def test_phase_zero_no_fee():
    iorb, fee = policy_for(4.1, 0.9, 0.88, 0.0)
    assert (iorb, fee) == (4.1, 0.0)
