"""Fee / IORB algebra.

Statutory design (project brief): the fee on covered principal is

    f = IORB * s / (1 - s),   s in [0.50, 0.90]

and the Fed chooses IORB so that the policy-sensitive all-in borrowing cost
stays at its desired stance:

    desired = IORB + beta * f        (beta = pass-through, explicit parameter)

Solving:  IORB = desired / (1 + beta * k * phase),  f = k * phase * IORB,
where k = s / (1 - s) and `phase` is the statutory phase factor.

ZLB behaviour: IORB is floored at 0. As desired -> 0, IORB -> 0 and therefore
f -> 0 at ANY s, including s = 0.90: the fee instrument degenerates at the
zero lower bound because the fee is defined as a multiple of IORB. This is a
property of the statutory formula, not a modelling choice, and it is tested
in tests/test_policy.py.
"""
from .config import INTRO_FEE_2028_PP


def fee_from_iorb(iorb_percent: float, s: float) -> float:
    """Statutory fee (pp of principal) implied by an IORB level and dial s."""
    if not 0.50 <= s <= 0.90:
        raise ValueError(f"dial s={s} outside statutory range [0.50, 0.90]")
    if iorb_percent < 0:
        raise ValueError("IORB cannot be negative in this model")
    return iorb_percent * s / (1.0 - s)


def policy_for(desired_percent: float, s: float, beta: float, phase: float):
    """Return (iorb_percent, fee_pp) implementing `desired` all-in stance.

    phase = 0    -> no fee yet (2027)
    phase = -1   -> 2028 introductory flat fee (INTRO_FEE_2028_PP), IORB reduced
                    by beta * fee (identical all-in identity, additive form)
    phase in (0,1] -> proportional phase-in of the full formula
    """
    if not 0.50 <= s <= 0.90:
        raise ValueError(f"dial s={s} outside statutory range [0.50, 0.90]")
    if not 0.0 < beta <= 1.0:
        raise ValueError("beta (pass-through) must be in (0, 1] in v1 scenarios")
    desired = max(0.0, desired_percent)
    if phase == 0.0:
        return desired, 0.0
    if phase == -1.0:
        fee = INTRO_FEE_2028_PP
        return max(0.0, desired - beta * fee), fee
    k = s / (1.0 - s)
    iorb = desired / (1.0 + beta * k * phase)
    iorb = max(0.0, iorb)  # ZLB floor
    fee = k * phase * iorb
    return iorb, fee


def full_formula_rate(desired_percent: float, s: float, beta: float):
    """(iorb, fee) that WOULD apply at full phase (phase=1) for a given desired
    stance. Used to set fixed-vintage lock rates for 2028/29 vintages so the
    transitional phase-in is not locked into loan contracts for life."""
    return policy_for(desired_percent, s, beta, 1.0)
