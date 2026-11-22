# INPUT MEMO — VERBATIM — Carlos A. Mucha to Gus, November 22, 2026

# Monetary Symmetry Fee — Stock-Flow-Consistent Macroeconomic Simulation

## I. Objective

I want a rigorous macroeconomic simulation of a proposed reform to the Federal Reserve's monetary-policy framework, which I call the Monetary Symmetry Fee.

The proposal would replace part of the conventional interest-rate transmission mechanism with a federal fee assessed on outstanding private-loan principal.

The purpose is to determine whether Congress could enable the Federal Reserve to achieve its existing dual mandate—maximum employment and stable prices—while directing part of the financial burden of monetary restraint to the United States Treasury rather than exclusively through the private credit system.

The potential fiscal effects are considerable.

Treasury would receive a new stream of fee revenue. Moreover, because the fee would provide an additional instrument for restraining private credit, the Fed might achieve its objectives with lower conventional interest rates, reducing federal debt-service expenditures.

Our earlier exploratory Monte Carlo model suggested combined benefits approaching $6 trillion over ten years. That is a hypothesis to investigate, not a result to reproduce or a target to calibrate toward.

I believe the correct analytical framework is Wynne Godley's stock-flow-consistent (SFC) economics, supplemented by the Federal Reserve's FRB/US macroeconomic model and a detailed loan-cohort model.

We need to model the entire monetary-fiscal system, not merely estimate fee revenue by multiplying a tax rate by outstanding loans.

## II. Final Policy Specification

This supersedes our earlier proposals for a 75% public share or for a discretionary Federal Reserve dial ranging from 50% to 90%.

### A. Permanent 50/50 structure

Following a transition period, the Federal Credit Fee Rate will equal the interest rate paid on reserve balances (IORB).

Define:

* i_t: IORB rate.
* f_t: Federal Credit Fee Rate.
* p_t: Combined policy-sensitive credit charge.

After synchronization:

f_t = i_t

p_t = i_t + f_t = 2i_t

Thus, each change in IORB produces an equal change in the fee.

A quarter-percentage-point increase in IORB increases the fee by another quarter point. Under full pass-through and one-for-one conventional interest-rate transmission, the combined borrowing charge rises by half a percentage point.

Half the adjustment operates through the conventional interest-rate channel. Half is collected for Treasury.

Important: This 50/50 division refers to the policy-sensitive borrowing charge, not the entirety of a lender's interest income or profit. Ordinary lending spreads remain separate.

### B. Initial rate and transition

The fee begins at 0.15% annually.

This mirrors the initial 0.15% unified IORB rate established by the Federal Reserve in July 2021.

Congress would authorize a transition period of no more than 24 months.

During this period, the Board of Governors may adjust IORB and the new fee independently, with the objective of bringing the two into equality while maintaining its statutory objectives.

The Board may complete synchronization whenever monetary and financial conditions permit. If synchronization can safely be completed in six months, there is no requirement to continue transitioning for another eighteen.

By the end of the second year, synchronization is mandatory.

Thereafter, the fee changes automatically with IORB, without a separate revenue-setting decision.

### C. Federal funds rate

This is crucial.

The proposal is not to impose a substantial fee on top of an unchanged federal funds target.

We expect the FOMC to adjust its target range, and the Board to coordinate IORB and other administered rates, as the new fee assumes part of the work previously performed by conventional rate increases.

The federal funds rate would ordinarily continue moving close to IORB, consistent with the Fed's operating framework.

Thus, if an illustrative conventional equilibrium involved:

* IORB: 4%
* Federal fee: 0%
* Combined charge: 4%

A corresponding post-transition configuration might involve:

* IORB: 2%
* Federal fee: 2%
* Combined charge: 4%

The objective is to preserve comparable borrowing conditions while altering the distribution of the policy-sensitive charge.

Whether these configurations are economically equivalent is precisely what the model must determine.

The lower IORB rate may also affect Treasury yields, bank funding costs, deposit returns, exchange rates, and securities markets not subject to the fee.

Those interactions cannot be assumed away.

### D. Tax base and grandfathering

The fee is assessed annually on the outstanding principal of covered private loans, not on interest income.

The proposed legislation would grandfather existing obligations and protect fixed-rate contractual expectations.

The model must separately track:

1. Loans originated before enactment.
2. New fixed-rate loans.
3. New adjustable-rate loans.
4. Revolving credit.
5. Refinancing, repayments, and prepayments.
6. Loan sales, securitization, and nonbank lending.
7. Potentially exempt obligations, including government securities.

An important question is whether fixed-rate loan cohorts should retain the fee applicable at origination or bear an adjustable fee paid by lenders without repricing the borrower's contractual interest rate.

Model both designs. The distinction matters for the Fed's countercyclical transmission and for lenders' balance sheets.

## III. The Godley Framework

A conventional macroeconomic model is not enough because the proposal changes both the price of credit and the distribution of financial income.

We need a complete, internally consistent set of sectoral balance sheets and transactions-flow matrices.

At minimum, distinguish:

| Sector | Principal stocks and flows |
|---|---|
| Treasury | Federal debt, fee receipts, expenditures, interest obligations |
| Federal Reserve | Treasury securities, reserves, IORB payments, earnings, remittances |
| Commercial banks | Loans, deposits, reserves, securities, funding costs |
| Nonbank lenders | Credit assets, funding liabilities, securitizations |
| Households | Mortgages, consumer credit, deposits, interest income, consumption |
| Nonfinancial businesses | Borrowing, investment, employment, profits |
| State and local governments | Revenue, spending, financial balances |
| Foreign sector | Cross-border lending, securities, exchange-rate effects |

Build a Godley-style transactions-flow matrix in which every financial flow has an identifiable payer and recipient.

Every financial asset must have a corresponding liability.

Every sector's financial balance must reconcile with changes in its net financial asset position, including valuation effects where relevant.

The model must fail its accounting tests if a dollar appears or disappears without a corresponding transaction.

### A. The reserve drain

When lenders pay the fee:

* Bank reserves decrease.
* Treasury's account at the Fed increases.
* The fee payer's financial position deteriorates by the amount paid, subject to any pass-through to borrowers.

When Treasury subsequently spends:

* Treasury's account decreases.
* Bank reserves increase.
* Recipients receive deposits.

We should distinguish temporary reserve drains from persistent changes in private-sector financial positions.

The fee is a fiscal withdrawal, but the reserve drain itself is not an additional source of revenue.

The Federal Reserve may also adjust its asset holdings or liquidity operations to maintain its desired interest-rate framework.

### B. Interest income

Model the difference between:

1. Interest paid by private borrowers.
2. Interest received by lenders.
3. Interest passed through to depositors and other creditors.
4. IORB payments to banks.
5. Interest paid by Treasury on federal debt.
6. Fee receipts paid to Treasury.
7. Federal Reserve remittances to Treasury.

This is the heart of the proposal.

Under conventional tightening, higher policy rates increase some private-sector interest receipts even as they restrain borrowing.

Under Monetary Symmetry, some of the additional policy-sensitive charge is paid to Treasury instead.

We need to determine how the resulting changes in disposable income, spending, saving, and investment affect inflation and output.

### C. Federal consolidation

Calculate both unconsolidated Treasury and Federal Reserve accounts and the consolidated federal government's position.

Specifically, avoid double-counting:

* Treasury interest paid on securities held by the Fed.
* Federal Reserve interest expense on reserves.
* Federal Reserve earnings and remittances.
* Deferred Federal Reserve losses.
* Treasury fee revenue and its reserve-settlement effect.

The relevant fiscal benefit is the change in consolidated federal deficits compared with an appropriate conventional monetary-policy baseline.

## IV. Behavioral Economics

Accounting identities will ensure the model is coherent. They will not establish that the policy works.

We need empirically grounded behavioral equations.

At minimum, model the response of:

Borrowers: Changes in consumption, mortgage demand, revolving credit, business investment, and refinancing.

Lenders: Changes in margins, deposit pricing, credit availability, underwriting, and loan ownership.

Savers and investors: Changes in income, consumption, portfolio allocation, Treasury demand, and risk-taking.

Treasury markets: Changes in yields across maturities, debt refinancing, and term premiums.

Foreign investors: Changes in capital flows, exchange rates, offshore borrowing, and substitution toward untaxed credit.

Federal Reserve: Adjustments in IORB, the federal funds target, and other monetary instruments in pursuit of maximum employment and stable prices.

The model should not assume that lowering IORB by one point necessarily reduces every Treasury yield by one point.

Nor should it assume all lenders pass the fee through completely.

Estimate the consequences of incomplete pass-through, changing credit spreads, and substitution toward untaxed financing.

## V. Monetary-Policy Reaction Function

The Fed's response must be endogenous.

Use a reaction function consistent with its dual mandate, rather than instructing the simulated Fed to generate a particular amount of revenue.

The objective should penalize deviations from:

* The Fed's 2% longer-run inflation objective.
* Sustainable maximum employment.
* Financial stability, including disruptive credit-market or liquidity conditions.

During the transition, the Board may independently adjust the fee and IORB, subject to the statutory synchronization deadline.

Following synchronization, the equality constraint becomes binding:

f_t = i_t

Test alternative monetary-policy reaction functions, including variants of Taylor-type rules and FRB/US policy rules.

Do not assume the combined policy charge maps one-for-one to the effective borrowing rate across all credit markets.

Instead, estimate its transmission.

An especially important experiment is whether the Fed can accomplish synchronization substantially before the 24-month statutory deadline without impairing macroeconomic stability.

## VI. Simulation Architecture

Use three linked components.

Component 1: Godley–Lavoie stock-flow model

Build the financial accounts, transactions-flow matrix, sectoral balances, credit stocks, and interest-payment relationships.

Useful starting repositories:

* https://github.com/brianr747/SFC_models
* https://github.com/joaomacalos/sfcr

These provide starting structures, not ready-made solutions for the proposed fee.

Component 2: Federal Reserve FRB/US

Use the Federal Reserve's official Python implementation as the principal reference for inflation, output, employment, policy-rate transmission, and macroeconomic responses.

Official source:

https://www.federalreserve.gov/econres/us-models-python.htm

Do not merely enter the fee as an ordinary tax shock.

The relevant changes include both its fiscal effects and its direct influence on private-credit pricing.

Extend the model or build a documented interface capable of transmitting both effects without double counting.

If full integration cannot be achieved, report precisely which behavioral relationships remain externally assumed.

Component 3: Credit and federal fiscal model

Build a loan-cohort model tracking:

* Covered outstanding principal.
* Fixed and adjustable loan shares.
* Originations, refinancing, repayments, and defaults.
* Fee rates applicable to each cohort.
* Annual collections.
* Federal debt outstanding by maturity.
* Treasury interest costs.
* Federal Reserve net earnings and remittances.

Use actual federal debt maturity structures rather than assuming the entire federal debt reprices immediately when IORB changes.

## VII. Required Experiments

Run the following regimes against identical economic shocks.

| Regime | Description |
|---|---|
| A | Conventional monetary policy, no credit fee |
| B | 50/50 synchronization completed as early as feasible |
| C | 50/50 synchronization completed over the full 24 months |
| D | Synchronization under a severe inflationary shock |
| E | Synchronization under a recessionary shock |

Also conduct sensitivity tests for fixed-rate grandfathering, tax-base breadth, offshore credit substitution, fee pass-through, and Treasury-yield responses.

For each regime, run stochastic simulations over FY 2027–2036, using an explicitly dated legislative-effective-date assumption.

Model calendar-quarter economic dynamics and aggregate correctly into federal fiscal years.

Use multiple calibration alternatives rather than assuming one distribution of uncertain parameters is authoritative.

Where empirical information is insufficient, identify the parameter as uncalibrated and report sensitivity rather than presenting a fabricated confidence interval.

## VIII. Questions to Answer

I want numerical answers to the following.

1. Synchronization

How quickly can the Fed synchronize the two rates while meeting its dual mandate?

What are the estimated transition paths for IORB, the fee, and the federal funds target?

2. Federal Credit Fee revenue

How much does Treasury receive annually?

What are the cumulative gross and net receipts over ten years?

How much does revenue change as the eligible loan stock grows?

3. Treasury interest savings

How much lower are Treasury yields than in the conventional baseline?

How do the savings vary with debt maturity and refinancing?

What is the net effect after Federal Reserve earnings and remittances are accounted for?

4. Private credit conditions

Do borrowers actually face comparable overall borrowing costs?

Does the proposal disproportionately affect mortgages, small businesses, or other borrowers?

Does credit migrate to untaxed instruments or offshore lenders?

5. Macroeconomic stabilization

Are inflation and employment outcomes comparable to, better than, or worse than conventional monetary policy?

How much of the outcome depends on the spending behavior of creditors versus other households?

6. Fiscal outcome

Does the reform produce a positive net fiscal benefit?

Is the benefit large enough to approach our earlier $6 trillion ten-year hypothesis?

If not, which assumptions fail?

## IX. Special Issue: Interest Income and Inflation

I particularly want an investigation of the interest-income feedback mechanism.

Higher policy rates restrain credit demand but also increase certain interest receipts.

Those receipts may support consumption and potentially offset part of the intended disinflationary effect.

This is related to modern discussions of monetary-policy income redistribution, although it should not be confused with Keynes's original historical observation known as Gibson's paradox.

Model the competing effects explicitly.

The Monetary Symmetry hypothesis is that redirecting part of policy-sensitive interest-related payments to Treasury could reduce inflationary income feedback while preserving credit restraint.

That hypothesis is central to the proposal.

It should be tested, not assumed.

## X. Healthcare Financing: Separate the Models

Do not initially optimize the Monetary Symmetry Fee for Medicare for America.

First determine whether the fee improves monetary stabilization and produces a positive fiscal dividend.

Only after those findings are established should the fiscal model consider alternative congressional uses of the resulting revenue.

One application is Representative Rosa DeLauro's Medicare for America legislation.

A subsequent fiscal study should calculate the proposed healthcare program's incremental federal cost after:

* Existing federal healthcare spending displaced.
* Household premiums.
* Employer contributions.
* State Medicaid maintenance-of-effort payments.
* Other financing and provider-payment effects.

The Monetary Symmetry Fee's net fiscal benefit could then be incorporated into that analysis.

Importantly, Congress's appropriation for the healthcare entitlement need not be capped by actual annual fee receipts. Budget scoring at enactment and legal authority to pay benefits are separate questions.

The Federal Reserve must remain free to reduce rates—and therefore fee revenue—during a recession without threatening healthcare benefits.

## XI. Required Deliverables

I want the following:

A. Reproducible research repository. All code, environment specifications, data sources, pinned package versions, assumptions, and instructions to reproduce the results.

B. Stock-flow-consistent accounting model. Complete balance-sheet and transactions-flow matrices, with automated reconciliation tests.

C. Macroeconomic simulation. The conventional and Monetary Symmetry regimes run against common economic shocks.

D. Ten-year fiscal projection. Annual IORB rates, fee rates, covered loan balances, fee collections, Treasury interest savings, Federal Reserve effects, and net deficit impacts.

E. Monte Carlo results. Means, medians, uncertainty ranges, and sensitivities for fiscal and macroeconomic outcomes.

F. Critical assessment. Identify the strongest evidence for and against the proposal and explain the economic circumstances under which it would fail.

G. Executive summary. A concise report suitable for discussion with monetary economists, congressional staff, Treasury officials, and Federal Reserve researchers.

Distinguish all simulated projections from actual Fed or CBO forecasts.

## XII. Research Standard

The earlier exploratory Monte Carlo produced approximately $5.6 trillion in combined ten-year fiscal benefits under a discretionary public-share design.

That design is now superseded.

The current proposal has a fixed 50/50 division, a maximum two-year transition, and automatic synchronization thereafter.

Do not calibrate the new model to reproduce the old fiscal result.

If the evidence supports $2 trillion, report $2 trillion.

If it supports $8 trillion, report $8 trillion.

If the fiscal benefit disappears when realistic lender behavior or Treasury-yield responses are incorporated, explain why.

I am interested in determining whether the proposal actually works, not constructing a model that declares it successful.

The central research question

Can Congress redesign monetary-policy transmission so that the Federal Reserve achieves its dual mandate through a combination of conventional interest rates and a principal-based federal lending fee, producing equivalent private-credit restraint while reducing the conventional interest-rate path and improving the federal government's net fiscal position?

That is the hypothesis.

Wynne Godley would insist that every balance sheet and every financial flow reconcile. We should insist upon the same.

The economic model must then tell us whether the resulting arrangements are sustainable.

If they are, Congress will have discovered that some of the fiscal consequences it has long treated as unavoidable are actually consequences of monetary arrangements it has the authority to change.

Verified starting sources for Gus

The Federal Reserve's official FRB/US Python package is available, with its Python package last updated February 2026. The SFC_models repository implements models from Godley and Lavoie's Monetary Economics. FRB/US in Python +1

The New Zealand Mortgage Interest Levy report provides the key institutional precedent, and the Fed's July 2021 implementation note confirms the 0.15% opening IORB rate. The Treasury +1

One instruction I would emphasize to Gus: The simulation must not treat the 50/50 formula as proof that borrowing costs remain unchanged. That's the intended mechanism; establishing whether it works in actual credit and Treasury markets is the principal research task.
