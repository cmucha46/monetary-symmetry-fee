# Cohort + fiscal skeleton (MSF v2)

- `data.py` -- documented stocks/parameters (see DATA.md)
- `cohort_model.py` -- grandfathered cohort phase-in engine (designs: floating / locked fee)
- `fiscal.py` -- Treasury repricing + Fed remittance accounting skeleton
- `run_cohort.py` -- writes outputs/*.csv for both designs x 3 turnover cases
- `tests/` -- pytest sanity suite (13 tests): `python3 -m pytest tests/ -q`
- `DATA.md` -- every series, value, source, assumption, and weak point
