"""Loan-cohort model v2, by category.

Salvages the prototype's conservative cohort partition (audit section 5.1:
no double-assessment, no stock leak) and fixes the defects the audit found:

  * split by category (mortgage / consumer / business / other), each with its
    own covered share, fixed share, turnover, maturity, avoidance;
  * FIXED vintages lock the fee RATE in force at origination; FLOATING
    vintages are charged the current year's fee rate;
  * the 2028 introductory flat fee (0.15 pp) is a TRANSITIONAL COLLECTION
    RATE, not a contract rate: a fixed loan originated in 2028 pays 0.15 pp
    during 2028 only and locks the full-formula rate of its origination year
    thereafter (see README, modelling decision D1);
  * phase-lock switch: by default (phase_lock_mode="lock_phase") a 2029 fixed
    vintage locks the half-phase rate, following the prototype / brief phase
    schedule. With phase_lock_mode="no_phase_lock" it locks the full-formula
    rate instead. The switch exists so the size of this artefact is measured,
    not hidden (sensitivity run in results/sensitivity_v1.csv);
  * turnover responds to the refinancing incentive when
    refi_elasticity > 0 (default 0.0 = prototype behaviour, switchable):
        turnover_eff = turnover * (1 + eta * max(0, desired_{t-1} - desired_t))
    i.e. a falling desired stance (pp) raises origination/refinance turnover;
  * avoidance: new cohorts shrink by exp(-avoidance_cat * fee_pp) at birth,
    per category (prototype functional form, retained and labelled).

Fiscal-year alignment: years are calendar years labelled FY; the federal
fiscal year (Oct-Sep) offset of one quarter is ignored, as in the prototype.
This approximation is stated, not hidden.
"""
import math
from dataclasses import dataclass, field

from .config import CATEGORIES, DEBT_GROWTH, YEARS, phase_for_year
from .policy import full_formula_rate, policy_for


@dataclass
class Vintage:
    balance: float          # $T of principal currently in this vintage
    locked_rate: float      # fee pp locked at origination (fixed vintages only)
    origin_year: int
    intro_year: bool = False  # originated in the 2028 introductory year


@dataclass
class CategoryBook:
    fixed: list = field(default_factory=list)     # list[Vintage]
    floating: list = field(default_factory=list)  # list[Vintage]

    def total(self) -> float:
        return sum(v.balance for v in self.fixed) + sum(v.balance for v in self.floating)


def effective_turnover(base_turnover: float, refi_elasticity: float,
                       desired_prev: float, desired_now: float) -> float:
    """Turnover after the refinancing-incentive response (capped at 0.95)."""
    incentive_pp = max(0.0, desired_prev - desired_now)
    return min(0.95, base_turnover * (1.0 + refi_elasticity * incentive_pp))


def run_cohorts(s: float, beta: float, iorb_base,
                refi_elasticity: float = 0.0,
                phase_lock_mode: str = "lock_phase",
                categories=None, years=None, debt_growth: float = DEBT_GROWTH):
    """Run the cohort model for one (s, beta) pair.

    Returns dict with:
      annual: list of per-year dicts {year, iorb, fee_rate, gross_fee_total,
              gross_fee_by_cat{name: $T}, taxable_book_total, eligible_total}
      books:  final CategoryBook per category (for inspection/tests)
    All money in $T, rates in percent (pp).
    """
    if phase_lock_mode not in ("lock_phase", "no_phase_lock"):
        raise ValueError("phase_lock_mode must be 'lock_phase' or 'no_phase_lock'")
    cats = categories if categories is not None else CATEGORIES
    yrs = years if years is not None else YEARS
    books = {c.name: CategoryBook() for c in cats}
    stocks = {c.name: c.start_stock for c in cats}
    annual = []
    desired_prev = None

    for j, year in enumerate(yrs):
        desired = iorb_base[j]
        phase = phase_for_year(year)
        iorb, fee = policy_for(desired, s, beta, phase)
        # Rate a NEW fixed vintage locks this year:
        if phase == -1.0:
            # 2028: lock the full-formula rate, not the 0.15 intro rate (D1).
            _, lock_rate = full_formula_rate(desired, s, beta)
        elif phase_lock_mode == "no_phase_lock" and 0.0 < phase < 1.0:
            _, lock_rate = full_formula_rate(desired, s, beta)
        else:
            lock_rate = fee

        gross_by_cat = {}
        book_total = 0.0
        eligible_total = 0.0
        for c in cats:
            prev_stock = stocks[c.name]
            stock = prev_stock * (1.0 + debt_growth) if j > 0 else prev_stock * (1.0 + debt_growth)
            # NOTE: stock in year 0 (2027) is start_stock grown one year, matching
            # the prototype's convention (audit section 7.2 #8 flags this; kept
            # explicit here rather than silently 'fixed').
            stocks[c.name] = stock
            eligible = stock * c.covered_share
            eligible_total += eligible
            book = books[c.name]
            gross = 0.0
            if year >= 2028:
                tau = effective_turnover(
                    c.turnover, refi_elasticity,
                    desired_prev if desired_prev is not None else desired, desired)
                decay = (1.0 - tau) * (stock / prev_stock)
                for v in book.fixed + book.floating:
                    v.balance *= decay
                add = eligible * tau * math.exp(-c.avoidance_per_fee_pp * max(fee, 0.0))
                book.fixed.append(Vintage(add * c.fixed_share, lock_rate, year,
                                          intro_year=(phase == -1.0)))
                book.floating.append(Vintage(add * (1.0 - c.fixed_share), fee, year,
                                             intro_year=(phase == -1.0)))
                for v in book.fixed:
                    rate = v.locked_rate
                    if v.intro_year and year == 2028:
                        rate = fee  # transitional collection rate in 2028 only
                    gross += v.balance * rate
                gross += sum(v.balance for v in book.floating) * fee
                gross /= 100.0  # $T x pp / 100 = $T
            gross_by_cat[c.name] = gross
            book_total += book.total()
        annual.append({
            "year": year, "iorb": iorb, "fee_rate": fee, "desired": desired,
            "gross_fee_by_cat": gross_by_cat,
            "gross_fee_total": sum(gross_by_cat.values()),
            "taxable_book_total": book_total, "eligible_total": eligible_total,
        })
        desired_prev = desired
    return {"annual": annual, "books": books}
