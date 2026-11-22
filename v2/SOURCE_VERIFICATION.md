# Source Verification — Monetary Symmetry Fee v2

**Task:** Verify, from primary sources, the four starting sources named in Carlos A. Mucha's memorandum of November 22, 2026 ("Monetary Symmetry Fee — Stock-Flow-Consistent Macroeconomic Simulation").
**Date of verification:** November 22, 2026.
**Standard applied:** Primary sources over summaries; exact figures quoted verbatim; anything not confirmed against a primary source is flagged **UNVERIFIED**.

**Headline findings**

1. **The New Zealand Mortgage Interest Levy (MIL) is real and documented in primary official sources** — but it was a *proposal developed by officials*, never enacted, and the official record is more cautionary than celebratory: the originating report did not endorse it, detailed design work was stopped early, the Finance Minister publicly declared it "dead in the water" in 2007, and Parliament's Finance and Expenditure Committee concluded in September 2008 that the evidence was "not sufficiently compelling" to pursue it. Two design features differ materially from the v2 specification: MIL receipts were to be **ring-fenced outside core Crown finances** (to fund a symmetric subsidy mode), **not** treated as general revenue; and the levy was to apply to **existing and new, fixed and floating** mortgages — i.e., **no grandfathering**, the opposite of the v2 design.
2. **The July 2021 IORB claim is exactly right:** the Board set the unified IORB rate at **0.15 percent, effective July 29, 2021**, the day the Regulation D amendment replacing IORR and IOER with the single IORB rate took effect. One nuance: 0.15% was not new on that date — IOER/IORR had already been raised to 0.15% on June 17, 2021; July 29 is when the *unified* rate began at that level.
3. **PyFRB/US is live and current:** the Fed's page shows the Python package **updated February 11, 2026** (confirming the memo's "last updated February 2026"), a separate data package updated October 13, 2026, and the page itself last updated November 4, 2026. It is distributed as a ZIP from federalreserve.gov, not via PyPI.
4. **Both SFC repositories exist as described, but they are very different animals:** `brianr747/SFC_models` is a Python framework whose last commit was **September 23, 2019** (dormant; implements only G&L ch. 3 SIM/SIMEX, ch. 4 PC, ch. 6 REG/OPENG in its `gl_book` subpackage); `joaomacalos/sfcr` is an actively maintained **R** package (CRAN v0.2.3, published October 9, 2025; MIT license) whose vignettes replicate G&L models from chapters 3, 4, 5, 6, 7, 9, 10, 11 and 12. Neither contains a ready-made 8-sector US model with a separate central bank, Treasury, commercial banks, nonbank lenders and foreign sector; both are equation-solver scaffolding plus textbook-model replications.

---

## 1. The New Zealand Mortgage Interest Levy (MIL)

### 1.1 Does it exist? Yes — as an official proposal, documented in two joint Treasury/Reserve Bank reports

**Origin.** In November 2005, the Minister of Finance asked the Reserve Bank of New Zealand (RBNZ) and the NZ Treasury to investigate "supplementary stabilisation instruments" (SSI) that could supplement the Official Cash Rate (OCR) during a prolonged housing boom that was pressuring inflation and the exchange rate. The resulting report:

- **Blackmore, M., P. Bushnell, T. Ng, A. Orr, M. Reddell and G. Spencer (2006), "Supplementary stabilisation instruments: Initial report to Governor, Reserve Bank of New Zealand and Secretary to the Treasury"** — report dated **10 February 2006**, publicly released **6 April 2006**.
  - Full text (Treasury): https://www.treasury.govt.nz/sites/default/files/2007-10/ssi-report-10feb06.pdf
  - Executive summary reprinted in *Reserve Bank of New Zealand Bulletin*, Vol. 69, No. 2 (June 2006): https://www.rbnz.govt.nz/-/media/project/sites/rbnz/files/publications/bulletins/2006/2006jun69-2ssisummary.pdf
  - Treasury information-release listing: https://www.treasury.govt.nz/publications/information-release/monetary-policy-information-releases

**Follow-up design report.** After further work was commissioned in late 2006:

- **Reserve Bank of New Zealand / The Treasury, "Mortgage Interest Levy: A Detailed Option — Report to Governor, Reserve Bank of New Zealand & Secretary to the Treasury," February 2007**, released 23 February 2007 with a cover letter to the Minister of Finance dated 20 February 2007.
  - Full text (Treasury): https://www.treasury.govt.nz/sites/default/files/2007-10/mil-do-feb07.pdf
  - Treasury release page: https://www.treasury.govt.nz/publications/information-release/mortgage-interest-levy-detailed-option-information-release

### 1.2 The design, as specified in the primary documents

From the SSI report's summary table (Feb 2006) and the Detailed Option report's executive summary (Feb 2007), verbatim or closely paraphrased with quotes:

- **Purpose / mechanism.** An adjustable levy intended "to force a wedge between the price paid for credit by mortgage borrowers and the returns available to the savers financing those loans" — i.e., raise mortgage borrowing costs *without* raising returns to (especially foreign) savers, so the OCR and the exchange rate would not have to do all the work. The Detailed Option report frames it as "an additional demand management instrument, to be used in fairly exceptional circumstances, to supplement the OCR in periods when housing market-related pressures in New Zealand were particularly intense."
- **Base.** All loans secured on an economic interest in residential property ("residential mortgages"), by all lenders — subject to a "predominant use" test. SSI summary: "Would apply to all loans outstanding, by all lenders, secured using mortgages on residential property." The report estimated the MIL "could be expected to cover around 40 per cent of total New Zealand dollar credit." A broader all-credit base was considered and rejected as infeasible (unsecured corporate credit is hard to identify and easy to move offshore).
- **Rate structure.** A single flat rate expressed in basis points per annum on outstanding principal: SSI summary — "expressed as a set number of basis points per annum, levied on all residential mortgage loans outstanding." Detailed Option report: "The MIL would be a flat rate (x basis points) across all residential mortgages, fixed or floating, existing or new." **No specific rate was ever proposed** — the rate is literally "(x basis points)" in the report. **No grandfathering**: existing loans were expressly included.
- **Symmetric (two-sided) design.** "The MIL could be operated in either levy mode or subsidy mode (the latter in periods when housing-related pressures etc were particularly weak)."
- **Who pays / who collects.** Legal liability on the borrower; collection through the tax system: "The MIL would be collected (paid out) by IRD [Inland Revenue Department] from lenders, although the ultimate liability for the levy would rest with the borrower." (The 2006 summary table puts it as: "levied on the borrower, but with an obligation on the lender to collect the levy.")
- **Who sets the rate.** Not the central bank alone: "Decisions to adjust the MIL would be made by the Minister of Finance, on the recommendation of the Reserve Bank," with the factors the Bank must consider "laid out in statute," a duty on the Bank to explain its recommendation publicly, and a duty on the Minister to explain publicly any rejection of a Bank recommendation.
- **Use of receipts — the critical divergence from v2.** "Funds raised (when the MIL was in levy mode) would be held separately outside core Crown finances, and would not ease the government's fiscal constraints. These funds would be used to finance use of the MIL in subsidy mode." The MIL was designed as a **self-financing stabilisation fund, not a revenue raiser**.
- **Expected potency (officials' own estimate).** "Our provisional estimates are that for each 100 basis points of MIL, no more than 50 basis points of relief on the OCR would be provided." Mortgage borrowers' finance costs would be *higher* than otherwise; all other borrowers' costs *lower* than otherwise.
- **Anti-avoidance.** The legislative net "would need to be cast quite widely to minimise domestic avoidance opportunities"; international avoidance was judged manageable "provided that all lenders registering a residential mortgage were required to be registered in New Zealand for tax purposes."

### 1.3 Was it endorsed by its own authors? No

The SSI report canvassed the MIL as one of six options but was explicitly lukewarm about the whole class of instruments: "there are no simple, or readily implemented, options that would provide large payoffs" (executive summary). Of the MIL/LVR pair it said such instruments "go well beyond the mainstream of international thinking about managing cycles," and flagged "issues around the extent to which such new statutory powers could appropriately be delegated (especially tax-based provisions), consistency with New Zealand's international commitments, and the difficulty of maintaining a strong and ongoing enforcement regime," plus risks to "the operational autonomy of the Reserve Bank." A contemporaneous Westpac economics bulletin (9 February 2007) summarised the official position accurately: the levy "was not endorsed by the RBNZ, the Treasury, or the authors of the report" (https://assets.dam.westpac.co.nz/is/content/wnzl/dist/all-of-bank/economic-reports/research-papers/Research-Papers_Taxing-Times_bulletin_09Feb07.pdf).

The February 2007 Detailed Option report expressly declined to recommend adoption: "This report does not attempt to undertake an overall assessment of whether an MIL instrument should be introduced to the toolkit," noting the instrument "has no direct international precedent." It also records that "work on this project has been drawn to a close earlier than had originally been envisaged," leaving "a variety of detailed issues that would need to be resolved."

### 1.4 What happened to it: abandoned in 2007; formally rejected by Parliament's committee in 2008; never enacted

- Finance Minister Michael Cullen floated the levy publicly in February 2007 (e.g., GoodReturns, "Spectre of mortgage levy looms," 12 February 2007: https://www.goodreturns.co.nz/article/976510007/spectre-of-mortgage-levy-looms.html), stressing it was "at a very preliminary stage." It drew immediate political attack.
- The Treasury's own release page states the end state in one sentence: **"Work on the MIL has now stopped."**
- In a 2007 address to the Wood Processors Association, Cullen recounted a December 2006 meeting with opposition leaders at which "a variable mortgage rate levy" had been discussed, and concluded: "let me be clear, the mortgage levy concept is dead in the water and it will not happen" (speech text reproduced at https://www.infonews.co.nz/news.cfm?id=9948).
- The **Finance and Expenditure Committee, "Inquiry into the future monetary policy framework," Report, September 2008** (48th Parliament, I.3N) — https://selectcommittees.parliament.nz/download/SelectCommitteeReport/135ea268-fd7f-4773-9247-18f19880a95b — recorded that it "heard extensive evidence concerning supplementary stabilisation instruments, such as a mortgage interest rate levy … but did not find the arguments in their favour compelling enough to support them being pursued further at this time." The committee's key finding, as later summarised in a BusinessNZ submission: "the evidence at the present time was not sufficiently compelling to support the pursuit of supplementary stabilisation instruments such as a mortgage interest rate levy."
- **No MIL legislation was ever introduced or enacted** (no Act, regulation or levy collection ever existed). The instrument NZ actually adopted later for housing-cycle management was the macroprudential route the SSI report also canvassed — LVR restrictions (introduced 2013) — not a price-based levy. (This last point is general background; the LVR date was not re-verified against a primary source in this pass — treat as **UNVERIFIED** detail, though the SSI report's canvassing of LVR limits is verified above.)

### 1.5 Official / external evaluations

- **OECD, *Economic Surveys: New Zealand 2007* (April 2007)**, Chapter 1, Box 1.1, summarised the SSI options and concluded of the levy-type instruments that "these negative aspects would seem to outweigh the appealing advantages of such an instrument" (survey PDF via oecd.org; box text also reproduced at thefreelibrary.com, "Chapter 1: raising New Zealand's living standards").
- **RBNZ retrospective:** "The Reserve Bank and macro-financial stability" (RBNZ Bulletin article, via thefreelibrary.com) recounts that in the SSI report the Bank and Treasury "considered there were no easy ways to solve the problem," listing the MIL among options that "might assist."
- Treasury/RBNZ also published a related volume, *Testing stabilisation policy limits in a small open economy* (October 2006) — existence verified from the Treasury release listing; its internal treatment of the MIL was not reviewed in this pass (**UNVERIFIED** as to content).
- **Academic literature specifically evaluating the MIL is thin.** In this pass, no peer-reviewed journal article devoted to the MIL was located; discussion appears mainly in official reports, the OECD Survey, parliamentary material, and bank-economist commentary. Flagged honestly: **the trail beyond the official documents above is thin** — searches surfaced news coverage and commentary, not a scholarly evaluation literature.

### 1.6 Relevance — and non-relevance — to the v2 specification

What genuinely transfers: (i) proof that a principal-based, basis-points-per-annum levy on loan balances, collected via lenders, has been designed in full operational detail by a central bank and a treasury; (ii) the "wedge" logic — raising borrower costs without raising saver returns — is the same family of idea as the v2 interest-income hypothesis; (iii) officials' own transmission estimate (≤50 bp of policy-rate relief per 100 bp of levy, on a base covering ~40% of credit) is a useful, sobering calibration anchor.
What does **not** transfer: the MIL was (a) sectoral (residential mortgages only), (b) discretionary and episodic rather than permanently synchronised to the policy rate, (c) revenue-neutral by construction (ring-fenced fund), (d) applied to the existing stock with no grandfathering, and (e) set by the Minister of Finance on central-bank recommendation rather than by the central bank. The v2 proposal is therefore not an adoption of the MIL; it is a different instrument that shares one mechanism (a principal-based levy collected through lenders) with a documented but rejected NZ proposal.

---

## 2. The Federal Reserve's July 2021 IORB implementation note — VERIFIED

**Primary source:** Federal Reserve, "Implementation Note issued July 28, 2021," https://www.federalreserve.gov/newsevents/pressreleases/monetary20210728a1.htm

Verbatim:

> "The Board of Governors of the Federal Reserve System voted unanimously to establish the interest rate paid on reserve balances at 0.15 percent, effective July 29, 2021."

Footnote 1 of the same note:

> "As announced on June 2, 2021, the Federal Reserve Board approved a final rule, effective July 29, amending Regulation D to eliminate references to an interest on required reserves (IORR) rate and to an interest on excess reserves (IOER) rate and replace them with a single interest on reserve balances (IORB) rate. Therefore, the Board voted on one rate, the IORB rate, at this meeting and will continue to do so going forward."

**Corroboration.**

- The Regulation D final rule was published June 4, 2021 (Docket No. R-1737), effective July 29, 2021; a follow-on final rule (Docket No. R-1754, *Federal Register* Vol. 86, No. 171, September 8, 2021, https://www.govinfo.gov/content/pkg/FR-2021-09-08/html/2021-19280.htm) amended 12 CFR §204.10(b)(1) to specify the IORB rate at 0.15 percent, "applicable on July 29, 2021."
- The Board's 2021 Record of Policy Actions states the unification replaced IORR/IOER with IORB effective July 29, 2021, and that the 0.15% IORB level was "the level of the IORR and IOER rates in effect prior to the Board's action" (https://www.federalreserve.gov/publications/2021-ar-record-of-policy-actions-of-the-board-of-governors.htm).
- FRED series IORB begins 2021-07-29 at 0.15 (https://fred.stlouisfed.org/data/IORB).

**Nuance the memo should carry:** the 0.15% *level* was set a month earlier — on June 16, 2021 the Board raised the rates paid on required and excess reserves from 0.10% to 0.15%, effective June 17, 2021 (a "technical adjustment"). The June 2/July 28 actions then unified the two rates into the single IORB at that same 0.15% level effective July 29, 2021. So "the initial 0.15% unified IORB rate established in July 2021" (memo §II.B) is accurate as to the unified rate and its start date; the level itself dates from June 17, 2021.

---

## 3. FRB/US in Python (PyFRB/US) — VERIFIED

**Primary source:** Federal Reserve Board, "FRB/US in Python," https://www.federalreserve.gov/econres/us-models-python.htm (page last update: **November 04, 2026**).

Verbatim / near-verbatim facts from the page:

- "The FRB/US model Python package, or PyFRB/US, is a Python-based platform to run simulations with the FRB/US model. This package includes the FRB/US model equations, simulation code, example programs, and technical documentation on the usage of the FRB/US model in Python."
- Contents: a README "with installation instructions and basic information"; the *pyfrbus* directory ("the platform code required to solve the model"); the *models* directory (FRB/US equations); the *demos* directory (example programs); the *docs* directory (HTML technical documentation on "PyFRB/US features, installation, model API, and simulation options").
- **"FRB/US Python package (ZIP) (Updated: February 11, 2026)"** — this confirms the memo's statement that the package was "last updated February 2026."
- **"This package requires Python 3 and is not compatible with Python 2."** No finer Python-version constraint is stated on the web page; detailed installation requirements are inside the ZIP's README/docs (**UNVERIFIED** at that level in this pass — the ZIP was not downloaded).
- Data are distributed separately: "FRB/US data package (ZIP) (Updated: October 13, 2026)"; users copy the LONGBASE.TXT dataset into the model's *data* folder. The page carries the Fed's disclaimer that the data package's trajectories "are not FRB/US model forecasts."
- Distribution channel: direct ZIP download from federalreserve.gov. There is **no official PyPI package** under the Fed's control that this page points to (**the page lists only the ZIP**; a same-named third-party PyPI entry, if any, is not the official source — treat any pip install of "pyfrbus" as **UNVERIFIED** provenance).
- Secondary technical corroboration: the R `bimets` vignette "The U.S. Federal Reserve quarterly model in R with bimets" (CRAN) describes pyfrbus as "a python-based simulation platform for the Federal Reserve Board's FRB/US model, which depends on the SuiteSparse code," loads the model via `from pyfrbus.frbus import Frbus; frbus = Frbus("model.xml")`, and notes the Feb. 2024 FRB/US version had 284 equations and 365 variables (https://cran.r-project.org/web/packages/bimets/vignettes/frb2bimets.pdf). The SuiteSparse dependency and equation counts are from that secondary source, not the Fed page.

---

## 4. The two SFC starting repositories — VERIFIED, with fitness assessment

### 4.1 brianr747/SFC_models (Python)

- URL: https://github.com/brianr747/SFC_models — "Stock-Flow Consistent (SFC) models in Python," by Brian Romanchuk.
- **License:** Apache License 2.0 (repo metadata and LICENSE file). Copyright 2016–2017 Brian Romanchuk.
- **Activity:** Created 2016-10-15; 130 commits; 42 stars; 15 forks; **last commit September 23, 2019** (the v1.0.3 release commits, "Fix to equation parsing for Python 3.7"); not archived, but dormant for ~7 years. Latest version 1.0.3. Developed originally under Python 3.4 (README also claims Python 2.7 compatibility) — expect bit-rot on current Python versions.
- **What it is:** a *framework* (`sfc_models`) that generates model equations algorithmically from `Country`/`Sector`/`Market` objects and solves the simultaneous system iteratively (fixed-point iteration, x = f(x)); 100% test coverage claimed on master.
- **Godley–Lavoie content** (subpackage `sfc_models.gl_book`, per README): **Chapter 3 — Models SIM, SIMEX; Chapter 4 — Model PC; Chapter 6 — Models REG, REG2 (and a variant of OPENG).** That is all. No BMW (ch. 7), no growth/open-economy advanced models, no multi-sector banking model.
- **Fitness for v2:** The sector-object architecture (sectors with automatically generated financial-asset/income equations) is conceptually the closest of the two to building a bespoke multi-sector model in Python, and it is Python — the same language as pyfrbus, which matters for the Component 1↔2 interface. But the G&L coverage is three textbook chapters, the solver is simple fixed-point iteration (the README itself flags that a more robust search will be "needed for flexible currency models"), and the code has been unmaintained since 2019. Realistic role: **design reference / prototyping scaffold, not a production base.**

### 4.2 joaomacalos/sfcr (R)

- URL: https://github.com/joaomacalos/sfcr — "Simulate Stock-Flow Consistent Models," by João Macalos. Also on CRAN: https://CRAN.R-project.org/package=sfcr ; documentation site: https://joaomacalos.github.io/sfcr/
- **License:** MIT + file LICENSE (per CRAN). (GitHub's license detector reports "Other/NOASSERTION" because of the CRAN-style LICENSE file; CRAN's MIT designation is authoritative.)
- **Activity:** Created 2020-10-21; 116 commits; 34 stars; 15 forks; last push **October 9, 2025**; **CRAN version 0.2.3, published 2025-10-09** — actively maintained. Solvers: Gauss–Seidel and Broyden (per CRAN description, citing Kinsella & O'Shea 2010); models are written as R formula sets (`sfcr_set`, `sfcr_baseline`, `sfcr_scenario`, `sfcr_shock`) with tidyverse (tibble) output; includes DAG/validation tooling and a multis (multi-country) extension.
- **Godley–Lavoie content** (package vignettes/articles, https://joaomacalos.github.io/sfcr/articles/): **Ch. 3 SIM; Ch. 4 PC; Ch. 5 LP; Ch. 6 REG and OPEN; Ch. 7 BMW; Ch. 9 DIS and DISINF; Ch. 10 INSOUT; Ch. 11 GROWTH; Ch. 12 Advanced OPEN** — i.e., essentially the whole textbook sequence except ch. 8. This includes models with banks and loan creation (BMW), portfolio choice (PC, LP), and open-economy variants (OPEN).
- **Fitness for v2:** Far more complete as a *validated library of G&L building blocks* (each vignette replicates published textbook results — useful as unit tests for a new model's sector blocks), and its scenario/shock machinery maps naturally onto the memo's Regime A–E design. Costs: it is **R, not Python**, so interfacing with pyfrbus means a language bridge or a port; and like SFC_models it supplies *textbook* models — none has a Treasury/Fed split with IORB, remittances and deferred assets, a distinct nonbank-lender sector, or loan cohorts. The v2 8-sector structure (Treasury, Fed, banks, nonbanks, households, firms, state/local, foreign) must be built new in either case; sfcr offers the better-tested parts bin, SFC_models the same-language chassis.

### 4.3 Bottom line on Component 1 starting points

Both citations in the memo are accurate as to existence and general character ("starting structures, not ready-made solutions" — the memo's own caveat is correct). Neither repository, as shipped, can represent the v2 fee: there is no existing model in either with (i) a central bank paying IORB and remitting earnings, (ii) a principal-based levy on loan stocks flowing to the Treasury, or (iii) fixed/adjustable loan cohorts. Budget the Component 1 work as new model construction that borrows solver code and textbook validation cases, not as adaptation of an existing 8-sector model.

---

## Appendix — verification ledger

| Claim in memo (Nov 22, 2026) | Status | Primary source |
|---|---|---|
| NZ Mortgage Interest Levy report is "the key institutional precedent" for a principal-based levy used as a monetary instrument | **Verified as to existence and mechanism; qualified as to precedent value** — real official proposal (2006–07), principal-based (bp p.a. on outstanding mortgages), lender-collected; but never enacted, not endorsed by its authors, work stopped 2007, rejected by FEC 2008; receipts ring-fenced, not revenue | Treasury/RBNZ reports (Feb 2006; Feb 2007); FEC Report I.3N (Sep 2008) |
| Fed's July 2021 implementation note confirms 0.15% opening unified IORB | **Verified** (0.15%, effective July 29, 2021; IORR/IOER replaced by single IORB). Nuance: 0.15% level first set June 17, 2021 | federalreserve.gov implementation note, July 28, 2021; FR Vol. 86 No. 171 |
| FRB/US Python package "last updated February 2026" | **Verified** — package ZIP updated February 11, 2026; data package October 13, 2026; page updated November 4, 2026 | federalreserve.gov/econres/us-models-python.htm |
| github.com/brianr747/SFC_models implements Godley–Lavoie models | **Verified** — framework + gl_book models SIM/SIMEX (ch. 3), PC (ch. 4), REG/OPENG (ch. 6); Apache-2.0; dormant since Sep 23, 2019 | GitHub repo + commit history |
| github.com/joaomacalos/sfcr implements Godley–Lavoie models | **Verified** — R package, CRAN 0.2.3 (Oct 9, 2025), MIT; vignettes replicate G&L chs. 3–7, 9–12 models | GitHub repo; CRAN; pkgdown site |
| Detailed pyfrbus install requirements (exact Python 3.x floor, dependency pins) | **UNVERIFIED** — inside the ZIP's README/docs, not on the web page; ZIP not downloaded in this pass | — |
| NZ later adopted LVR restrictions (2013) instead of a levy | **UNVERIFIED** in this pass (general background only) | — |
