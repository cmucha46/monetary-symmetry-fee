"""Lane F: covered-base variants (loans-only correction of the v1 proxy)."""
import pytest

from monetary_symmetry.config import (CATEGORIES, COVERED_BASE_VARIANTS,
                                      DEFAULT_COVERED_BASE_VARIANT,
                                      categories_for_variant, eligible_base)
from monetary_symmetry.score import run_scenario


def test_variant_names_and_default():
    assert set(COVERED_BASE_VARIANTS) == {
        "loans_only", "loans_plus_securitized", "lane_e_proxy"}
    assert DEFAULT_COVERED_BASE_VARIANT == "loans_plus_securitized"


def test_unknown_variant_raises():
    with pytest.raises(ValueError):
        categories_for_variant("bonds_too")
    with pytest.raises(ValueError):
        run_scenario(0.75, 0.88, covered_base_variant="nope")


def test_lane_e_proxy_replicates_v1_categories():
    assert categories_for_variant("lane_e_proxy") == CATEGORIES


def test_eligible_base_ordering_and_business_fix():
    lane_e = eligible_base("lane_e_proxy")
    central = eligible_base("loans_plus_securitized")
    strict = eligible_base("loans_only")
    # Business: v1 proxy counted 23.292 x 0.70 = 16.304 of eligible principal,
    # including corporate bonds/CP. Corrected loan base is Z.1 L.102 loans.
    assert lane_e["business"] == pytest.approx(23.292 * 0.70)
    assert central["business"] == pytest.approx(13.419)
    assert strict["business"] < central["business"]
    # Total eligible ordering: proxy > central > strict.
    assert sum(lane_e.values()) > sum(central.values()) > sum(strict.values())
    # Consumer: federal-government-held credit (Direct student loans) excluded.
    assert central["consumer"] == pytest.approx(5.099 * 0.69057)
    assert central["consumer"] < lane_e["consumer"]


def test_corrected_fee_below_v1_but_interest_line_unchanged():
    v1 = run_scenario(0.75, 0.88, covered_base_variant="lane_e_proxy")["totals"]
    central = run_scenario(0.75, 0.88)["totals"]  # default = central variant
    strict = run_scenario(0.75, 0.88, covered_base_variant="loans_only")["totals"]
    # v1 centre replicates RESULTS_V1.md exactly.
    assert v1["gross_fee_10yr"] == pytest.approx(5.893491664752234)
    assert v1["combined_total_10yr"] == pytest.approx(7.015307113784073)
    assert strict["gross_fee_10yr"] < central["gross_fee_10yr"] < v1["gross_fee_10yr"]
    # The consolidated interest line does not depend on the covered base
    # (IORB path is solved from the desired stance, not from the base).
    for t in (central, strict):
        assert t["consolidated_interest_saving_10yr"] == pytest.approx(
            v1["consolidated_interest_saving_10yr"])


def test_categories_mutually_exclusive_names_all_variants():
    for variant in COVERED_BASE_VARIANTS:
        names = [c.name for c in categories_for_variant(variant)]
        assert names == ["mortgage", "consumer", "business", "other"]
