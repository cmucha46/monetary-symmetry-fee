"""
Monetary Symmetry Fee v2 -- Lane B (FRB/US Design E) feedback extraction.

Reads Lane B's quarterly path CSVs (../frbus/regime_outputs/) and builds
the annual (federal fiscal year) series the consolidation needs:

    drag_t  =  d_surplus_t  -  receipts_t  +  d_interest_t

where d_surplus is the FRB/US deviation in the federal surplus
(gfsrpn), receipts are the fee receipts Lane B fed in via ugfsrp, and
d_interest is the deviation in federal interest payments (gfintn,
negative = saving). The drag is therefore the ENDOGENOUS revenue /
expenditure response -- output and employment running below the matched
baseline reduce other federal revenues and raise cyclical outlays. It
excludes, by construction, both the receipts themselves and the
in-model interest saving, so adding it to the consolidation (whose
savings channel is the separate tau surface) does not double-count.

Conventions
-----------
* Fiscal year: FY t = (t-1)Q4 .. tQ3. Quarterly FRB/US fiscal flows are
  SAAR, so annual values are sum(quarters)/4. This aggregation
  reproduces Lane B's published cumulative metrics (metrics.json) to
  rounding for every regime -- verified in the test suite.
* FY2027 is set to zero: the fee's effective date is 2027Q4 and Lane B's
  fiscal sums are FY2028-36; the tiny FY2027 deviations in the paths are
  pre-effective-date baseline noise.
* Headline runs: beta = 1.0, MCE expectations (Lane B's headline
  protocol). VAR series are loadable via the same function.

What Lane B is, and is not (REGIME_RESULTS.md sec. 7): Design E's rule
is outcome-reactive and cannot see the fee, so its measured offset
(57-63% of the fee) is a LOWER bound on the offset a stance-targeting
FOMC would deliver, and the drag extracted here is correspondingly an
UPPER-bound drag. The pre-feedback consolidation is the opposite end
of the interval. Both ends are reported; neither is hidden.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
FRBUS_OUT = HERE.parent / "frbus" / "regime_outputs"
YEARS = list(range(2027, 2037))
REGIMES = ("B", "C", "D", "E")


def _fy_of(period: str) -> int:
    year, q = int(period[:4]), int(period[-1])
    return year + 1 if q == 4 else year


def annual_series(regime: str, beta_tag: str = "b100",
                  mode: str = "mce") -> pd.DataFrame:
    """Annual FY series for one Lane B run: d_surplus, receipts,
    d_interest, and the residual endogenous drag ($B)."""
    if regime not in REGIMES:
        raise ValueError(f"regime must be one of {REGIMES}")
    path = FRBUS_OUT / f"paths_{regime}_{beta_tag}_{mode}.csv"
    df = pd.read_csv(path)
    df["fy"] = df["period"].map(_fy_of)
    rows = {}
    for fy, x in df.groupby("fy"):
        d_surp = x["D_gfsrpn"].sum() / 4.0
        rec = x["receipts_bn_saar"].sum() / 4.0
        d_int = x["D_gfintn"].sum() / 4.0
        rows[fy] = {"d_surplus_bn": d_surp, "receipts_bn": rec,
                    "d_interest_bn": d_int,
                    "drag_bn": d_surp - rec + d_int}
    out = pd.DataFrame.from_dict(rows, orient="index").reindex(YEARS)
    out.index.name = "fy"
    out = out.fillna(0.0)
    out.loc[2027, :] = 0.0  # pre-effective-date; see module docstring
    return out


def metrics(regime: str, beta_tag: str = "b100", mode: str = "mce") -> dict:
    """Lane B's published cumulative metrics for cross-checking."""
    m = json.loads((FRBUS_OUT / "metrics.json").read_text())
    return m[f"{regime}_{beta_tag}_{mode}"]


def regime_feedback(regime: str, skeleton_gross_total: float,
                    beta_tag: str = "b100", mode: str = "mce") -> dict:
    """The two feedback objects the consolidation consumes:

    * receipts_ratio -- Lane B cumulative receipts (loan-only base, at
      Lane B's own iterated f = rff fixed-point fee path) divided by the
      cohort skeleton's cumulative gross collections on the same
      loan-only base at the skeleton's input fee path. This is the
      measured fee-path reconciliation factor: >1 for B/C/D (Lane B's
      fixed point settles at f ~ 2.0-2.1% vs the skeleton's 1.95%, and
      synchronizes on the regime's schedule), ~0.57 for E (the fee
      collapses with rff at the recession floor -- revenue is
      procyclical by construction). Applied proportionally to the
      unified base's net fee receipts: an ASSUMED proportionality (the
      ratio is base-independent to first order; Lane B's kappa=1
      sensitivity, which previews the unified wedge, moves receipts by
      only ~-4% through the fixed point).
    * drag (annual, $B) -- scaled by the same ratio, on the documented
      assumption that the endogenous fiscal drag is proportional to the
      size of the intervention actually implemented.
    """
    s = annual_series(regime, beta_tag, mode)
    receipts_total = float(s.loc[2028:2036, "receipts_bn"].sum())
    ratio = receipts_total / skeleton_gross_total
    return {"regime": regime, "beta_tag": beta_tag, "mode": mode,
            "annual": s, "receipts_total_bn": receipts_total,
            "receipts_ratio": ratio,
            "drag_annual_bn": s["drag_bn"],
            "drag_total_bn": float(s.loc[2028:2036, "drag_bn"].sum()),
            "drag_scaled_total_bn":
                float(s.loc[2028:2036, "drag_bn"].sum()) * ratio}
