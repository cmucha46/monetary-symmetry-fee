# Fiscal consolidation + Monte Carlo (MSF v2, integration lane)

- `consolidation.py` — consolidated net fiscal benefit vs. baseline =
  net fee receipts + τ-conditional Treasury interest savings (non-Fed-held
  share only) + Δ Fed cash remittances (deferred-asset timing respected).
  Contains the EMPTY placeholder interface `apply_macro_feedback()` for
  the FRB/US + SFC Section IX pass.
- `monte_carlo.py` — discrete grid enumeration (288 combos per τ) over the
  literature lane's documented grids. NOT calibrated sampling; results are
  conditional simulation summaries, never confidence intervals, and never
  integrated over τ.
- `inputs.json` — base resolution config. The headline base is the
  UNIFIED base (loans + corporate bonds + municipal bonds, sponsor
  decision Nov 22 2026); swapping the cohort lane's unified CSVs in is a
  file change (candidate paths listed in the config), not a code change.
- `run_integration.py` — writes `outputs/` (central-case annual tables,
  all grid runs, per-τ summaries, results.json).
- `FISCAL_PROJECTION.md` / `MONTE_CARLO.md` — the reports of record.
- `tests/` — pytest sanity suite (11 tests): consolidation identity,
  no-double-count of Fed-held interest, τ=0 ⇒ zero savings, deferred-asset
  timing, repricing equivalence with the cohort skeleton, placeholder
  slots empty.

Run: `python3 run_integration.py && python3 -m pytest tests/ -q`
