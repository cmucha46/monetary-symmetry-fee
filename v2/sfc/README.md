# SFC Accounting Skeleton — Monetary Symmetry Fee v2

A Godley–Lavoie stock-flow-consistent (SFC) accounting core for the
Monetary Symmetry Fee as respecified in Carlos A. Mucha's memorandum of
November 22, 2026: a Federal Credit Fee on outstanding principal of
covered private loans, paid by lenders to Treasury and settled in
reserves through the Treasury General Account; after a transition of at
most 24 months the fee rate equals IORB (f = i, a permanent 50/50 split
of the policy-sensitive credit charge, combined charge p = 2i), with the
Fed's IORB path roughly half the conventional baseline. Pre-enactment
loans are grandfathered and outside the fee base.

**This directory is the accounting skeleton: matrices and reconciliation
tests first, behaviour second.** It proves that the proposed flows *can*
be booked without a dollar appearing or disappearing. It does not yet
say anything about whether the policy *works* — that requires the
behavioural equations, the FRB/US interface, and the loan-cohort model,
which are separate lanes.

## Files

| File | Contents |
|---|---|
| `sfc_core.py` | Sectors, instruments, `BalanceSheet`, `Transaction`, `Period` — the accounting machinery and its validators. Pure stdlib, original code. |
| `scenario.py` | Settlement helpers (deposits / TGA / reserves plumbing), an illustrative opening balance sheet, and `build_period()` assembling one full period of transactions. |
| `MATRICES.md` | Human-readable balance-sheet and transactions-flow matrices, generated from the code by `render_matrices.py`. |
| `render_matrices.py` | Regenerates the tables in MATRICES.md. |
| `tests/test_sfc_v2.py` | 23 pytest tests: every identity, the fee/IORB/remittance plumbing, the deferred-asset mechanism, and negative tests proving the accounting fails loudly on a broken flow. |

Run the tests:

```
cd ~/workspace/monetary-symmetry/v2/sfc
python3 -m pytest tests/ -q
```

## Accounting conventions

* **Eight sectors:** Treasury, Federal Reserve, commercial banks,
  nonbank lenders, households, nonfinancial businesses, state & local
  governments, foreign sector.
* **Signs.** Balance sheet: assets +, liabilities −; net worth is the
  residual. TFM: each sector has a current column (receipts +, payments
  −) and a capital column (sources of funds +, uses −).
* **Admissibility.** A `Transaction` is accepted only if every sector's
  legs sum to zero *and* its capital legs equal the liability-minus-asset
  changes implied by its stock effects. A flow without a counterpart
  cannot be entered — `Period.add()` raises `AccountingError` at
  insertion time, not at some later audit.
* **Identities asserted every period** (in `Period.close()` and again in
  the test suite): every financial instrument is two-sided in opening
  and closing balance sheets; every TFM row sums to zero; every sector's
  current + capital balances sum to zero; each sector's current balance
  equals the change in its net worth; each sector's financial balance
  (current balance − net tangible investment) equals the change in its
  net financial assets; economy-wide, total net worth changes only by
  net tangible investment.
* **Settlement is institutional, not decorative.** Treasury settles
  through the TGA; a dollar into the TGA is a dollar out of bank
  reserves, and conversely. Private payments settle in deposits. The Fed
  pays IORB and its operating expenses by creating reserves. These
  routes are encoded once, as helpers in `scenario.py`, so no flow can
  be specified with inconsistent plumbing.
* **Fed remittances and the deferred asset** are carried in one signed
  instrument, FEDPAY (remittances payable net of the deferred asset):
  income accrues to FEDPAY; cash is paid only out of a positive balance;
  losses drive FEDPAY negative, and that negative stock *is* the
  deferred asset. See MATRICES.md for the rationale.
* **Consolidation.** The suite asserts the v1 identity in matrix form:
  consolidated (Treasury + Fed) net interest equals gross interest on
  all federal debt minus the Fed's economic net income — interest on
  Fed-held debt nets out as an internal transfer, exactly once.

## How the fee enters

* **Base:** the LN_COV stock only (post-enactment originations, held by
  BNK and NBF). LN_GRD is never in the base — a test zeroes the covered
  stock and asserts the fee vanishes while $13T of grandfathered loans
  remain.
* **Current account:** `Federal Credit Fee (banks)` and `Federal Credit
  Fee (nonbanks)` rows: lenders −, Treasury +, amount = fee rate ×
  covered stock by lender. In the illustrative synchronized period,
  fee rate = IORB = 2%, yielding 0.110 on covered stocks of 5.50.
* **Settlement:** banks pay from reserves; nonbanks pay from deposits
  and their banks' reserves drain identically; the TGA rises by the
  total. Treasury spending reverses the settlement exactly. The reserve
  drain is a stock movement, distinct from the revenue, which is counted
  once — the distinction the November 22 memo (§III.A) insists on.
* **Designs not yet distinguished:** the memo asks the model to compare
  (i) a fee fixed at origination for fixed-rate cohorts vs (ii) an
  adjustable fee borne by lenders without repricing the borrower's
  contract. The skeleton books the fee as a lender-paid current transfer
  in both readings; the cohort-level split belongs to the loan-cohort
  lane, which will feed this one its LN_COV/LN_GRD stocks.

## What is still a skeleton (explicitly)

* **No behavioural equations.** Consumption, wages, taxes, investment,
  lending, issuance and portfolio shares in `scenario.py` are exogenous
  illustrative numbers that exercise the matrices. Nothing responds to
  interest rates, the fee, income, or wealth yet.
* **One average Treasury yield** for public- and Fed-held debt (v1's
  ledger distinguished book yields and repricing shares; maturity
  structure and repricing belong to the fiscal/cohort lane).
* **No revaluations:** stocks change only through transactions; capital
  gains/losses on securities and equities are not yet booked (equities
  are carried at book value).
* **No defaults or write-offs** yet — loan losses will enter as a
  capital-account (other-changes) transaction when the cohort lane lands.
* **One period at a time.** `build_period()` can be chained (period 2 in
  the test suite runs on period 1's closing sheet, which is how the
  deferred-asset paydown is tested), but there is no time-series driver,
  no transition path (0.15% initial fee → synchronization), and no
  stochastic simulation yet.
* Stocks and flows are **illustrative magnitudes**, not data. Calibration
  to H.4.1 / Financial Accounts (Z.1) magnitudes is a later step and must
  not be back-read into these numbers.
