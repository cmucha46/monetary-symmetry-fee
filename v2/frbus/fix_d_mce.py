"""Regime D (MCE) correction: rescale the inflation add-factor.

Measured in diag_shock.py: under MCE (mcap+wp), picxfe_aerr is amplified
~13.4x (linear, one-quarter lead) -- +2.0 gives a +26.9pp realised peak
deviation (de-anchoring explosion), vs +4.46pp under VAR for the same
input. To run the SAME realised shock under MCE (peak core-inflation
deviation ~ +4.5pp), the add-factor is rescaled to +0.33 for 2028Q1-Q4.
This script recomputes ONLY the MCE inflation-shocked baseline and the
two MCE Regime D fee runs, overwriting their CSVs, and patches run_log.
"""
import json
import pandas as pd
import regime_runs as rr

SCALE = 0.33
_orig = rr.shock_aerr
def patched(state):
    if state == "infl":
        return {"picxfe_aerr": (pd.Period("2028Q1"), pd.Period("2028Q4"), SCALE)}
    return _orig(state)
rr.shock_aerr = patched

lane = rr.Lane("mce")
plain = lane.baseline("plain")
b = lane.baseline("infl")
rr.write_run_csv("A_infl_mce", b, b, None, None)
dev = {
    "xgdp_trough_pct": float((100 * (b.loc[rr.QUARTERS, "xgdp"]
        / plain.loc[rr.QUARTERS, "xgdp"] - 1)).min()),
    "lur_peak_dev_pp": float((b.loc[rr.QUARTERS, "lur"]
        - plain.loc[rr.QUARTERS, "lur"]).max()),
    "picxfe_peak_dev_pp": float((b.loc[rr.QUARTERS, "picxfe"]
        - plain.loc[rr.QUARTERS, "picxfe"]).max()),
    "rff_peak_dev_pp": float((b.loc[rr.QUARTERS, "rff"]
        - plain.loc[rr.QUARTERS, "rff"]).max()),
}
print("corrected MCE infl shock size:", {k: round(v, 2) for k, v in dev.items()})

log = {}
for runid, beta in [("D_b100", 1.0), ("D_b075", 0.75)]:
    sol, f, receipts, hist = rr.run_fee_regime(
        lane, "D", "C", "infl", beta, rr.KAPPA_RBBB_LOANONLY, log)
    rr.write_run_csv(f"{runid}_mce", sol, b, f, receipts)
    print(runid, "redone,", len(hist), "iterations")

main_log = json.loads((rr.OUT / "run_log.json").read_text())
main_log["runs"]["A_infl_mce_shocksize"] = dev
main_log["corrections"] = {
    "D_mce": ("Original MCE inflation shock (picxfe_aerr +2.0) produced a "
              "+26.9pp realised peak inflation deviation (measured ~13.4x "
              "amplification of the add-factor under mcap+wp, one-quarter "
              "lead; see diag_shock.py). Replaced by aerr +0.33, chosen so "
              "the REALISED shock matches the VAR design (peak picxfe dev "
              "~+4.5pp). A_infl_mce baseline and D_b100/D_b075 MCE runs "
              "recomputed by fix_d_mce.py; VAR D runs unchanged."),
    "log_entries": log,
}
(rr.OUT / "run_log.json").write_text(json.dumps(main_log, indent=1, default=str))
print("run_log patched")
