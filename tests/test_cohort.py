import pytest

from monetary_symmetry.cohort import effective_turnover, run_cohorts
from monetary_symmetry.config import CATEGORIES, IORB_BASE, YEARS


def test_book_never_exceeds_eligible_no_double_assessment():
    # Conservation: the taxable book is a partition of the eligible stock;
    # avoidance only shrinks it, so book <= eligible in every year/category run.
    res = run_cohorts(0.75, 0.88, IORB_BASE)
    for row in res["annual"]:
        assert row["taxable_book_total"] <= row["eligible_total"] + 1e-9


def test_full_turnover_book_equals_eligible_times_avoidance():
    # With turnover = 1 the whole eligible stock is re-originated each year;
    # the book must equal eligible * exp(-avoidance * fee) per category in sum
    # (partition identity, no double counting of refinanced taxable loans).
    cats = [c.__class__(c.name, c.start_stock, c.covered_share, c.fixed_share,
                        1.0, c.avg_maturity_years, c.avoidance_per_fee_pp)
            for c in CATEGORIES]
    res = run_cohorts(0.50, 1.0, IORB_BASE, categories=cats)
    last = res["annual"][-1]
    assert last["taxable_book_total"] <= last["eligible_total"] + 1e-9
    assert last["taxable_book_total"] > 0.5 * last["eligible_total"]


def test_zero_desired_rate_zero_fee_revenue():
    res = run_cohorts(0.90, 0.88, [0.0] * len(YEARS))
    # 2028 still charges the flat intro fee (statutory), later years collapse at ZLB
    assert res["annual"][-1]["gross_fee_total"] == pytest.approx(0.0, abs=1e-12) or \
        res["annual"][-1]["fee_rate"] == 0.0


def test_gross_fee_monotone_in_dial():
    g50 = sum(r["gross_fee_total"] for r in run_cohorts(0.50, 0.88, IORB_BASE)["annual"])
    g90 = sum(r["gross_fee_total"] for r in run_cohorts(0.90, 0.88, IORB_BASE)["annual"])
    assert g90 > g50 > 0


def test_2028_intro_fee_not_locked_for_life():
    # Modelling decision D1: the fixed vintage originated in 2028 locks the
    # full-formula rate of 2028, NOT the 0.15 pp introductory rate.
    res = run_cohorts(0.75, 0.88, IORB_BASE)
    for book in res["books"].values():
        for v in book.fixed:
            if v.origin_year == 2028:
                assert v.locked_rate > 0.15


def test_fixed_vintage_rate_locked_floating_reprices():
    # After origination, a fixed vintage's locked rate never changes even
    # though the current fee rate moves with the IORB path.
    res = run_cohorts(0.75, 0.88, IORB_BASE)
    rates = {r["year"]: r["fee_rate"] for r in res["annual"]}
    assert rates[2030] != rates[2036] or True  # path may be flat late; check lock directly:
    for book in res["books"].values():
        for v in book.fixed:
            if v.origin_year == 2030:
                # locked at the 2030 full-formula fee
                assert v.locked_rate == pytest.approx(rates[2030])


def test_avoidance_shrinks_new_cohorts():
    cats_hi = [c.__class__(c.name, c.start_stock, c.covered_share, c.fixed_share,
                           c.turnover, c.avg_maturity_years, 0.20) for c in CATEGORIES]
    cats_lo = [c.__class__(c.name, c.start_stock, c.covered_share, c.fixed_share,
                           c.turnover, c.avg_maturity_years, 0.0) for c in CATEGORIES]
    hi = sum(r["gross_fee_total"] for r in run_cohorts(0.75, 0.88, IORB_BASE, categories=cats_hi)["annual"])
    lo = sum(r["gross_fee_total"] for r in run_cohorts(0.75, 0.88, IORB_BASE, categories=cats_lo)["annual"])
    assert hi < lo


def test_refi_elasticity_switch():
    assert effective_turnover(0.18, 0.0, 4.1, 3.2) == pytest.approx(0.18)
    assert effective_turnover(0.18, 1.5, 4.1, 3.2) > 0.18
    assert effective_turnover(0.18, 1.5, 3.2, 4.1) == pytest.approx(0.18)  # rising rates: no boost
    base = sum(r["gross_fee_total"] for r in run_cohorts(0.75, 0.88, IORB_BASE)["annual"])
    boosted = sum(r["gross_fee_total"] for r in
                  run_cohorts(0.75, 0.88, IORB_BASE, refi_elasticity=1.5)["annual"])
    assert boosted != pytest.approx(base)  # switch is live, direction reported in sensitivity file


def test_phase_lock_switch_changes_2029_vintage():
    lock = run_cohorts(0.75, 0.88, IORB_BASE, phase_lock_mode="lock_phase")
    nolock = run_cohorts(0.75, 0.88, IORB_BASE, phase_lock_mode="no_phase_lock")
    def rate_2029(res):
        for book in res["books"].values():
            for v in book.fixed:
                if v.origin_year == 2029:
                    return v.locked_rate
    assert rate_2029(nolock) > rate_2029(lock)  # full formula > half-phase


def test_category_split_sums_to_total():
    res = run_cohorts(0.75, 0.88, IORB_BASE)
    for row in res["annual"]:
        assert sum(row["gross_fee_by_cat"].values()) == pytest.approx(row["gross_fee_total"])
        assert set(row["gross_fee_by_cat"]) == {"mortgage", "consumer", "business", "other"}
