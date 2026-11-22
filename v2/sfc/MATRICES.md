# The Matrices — Monetary Symmetry Fee v2, SFC Skeleton

Human-readable balance-sheet and transactions-flow matrices for the
Godley–Lavoie stock-flow-consistent accounting skeleton. **The tables
below are generated from the code** (`python3 render_matrices.py`, data
structures in `sfc_core.py`, period construction in `scenario.py`) so
they cannot drift from the implementation. All figures are $ trillions,
illustrative magnitudes only — see README.md.

## Sectors

| Code | Sector | | Code | Sector |
|---|---|---|---|---|
| TRE | Treasury | | HHD | Households |
| FED | Federal Reserve | | NFC | Nonfinancial businesses |
| BNK | Commercial banks | | SLG | State & local governments |
| NBF | Nonbank lenders | | ROW | Foreign sector (rest of world) |

## Instruments

| Code | Instrument | Holder(s) | Issuer |
|---|---|---|---|
| RES | Reserve balances at the Fed | BNK | FED |
| TGA | Treasury General Account | TRE | FED |
| TS_PUB | Treasury securities, public-held | BNK, NBF, HHD, NFC, SLG, ROW | TRE |
| TS_FED | Treasury securities, Fed-held | FED | TRE |
| FEDPAY | Fed remittances payable, net of deferred asset | TRE | FED |
| DEP | Deposits at commercial banks | NBF, HHD, NFC, SLG, ROW | BNK |
| LN_COV | Loans, **covered** (post-enactment originations) | BNK, NBF | HHD, NFC |
| LN_GRD | Loans, **grandfathered** (pre-enactment) | BNK, NBF | HHD, NFC |
| CBN | Corporate bonds | BNK, NBF, HHD, ROW | NFC |
| EQ | Equities (book value) | HHD, ROW | BNK, NBF, NFC |
| CUR | Currency in circulation | HHD, ROW | FED |
| K | Tangible assets (capital, housing, public assets) | HHD, NFC, SLG | — (no counterpart liability) |

Sign convention: balance-sheet entries are signed from the holder's
perspective — assets **+**, liabilities **−**. Every financial instrument
row therefore sums to zero across sectors; the tangible-assets row does
not (it is the real counterpart of net worth), and the Net worth row is
entered negated so that every column sums to zero.

**FEDPAY** deserves a note. Institutionally, the Fed's deferred asset is
a claim on its *own* future earnings, presented as an offset to future
remittances — it is not a claim on any other sector. Rather than break
the two-sidedness of the matrix with a one-sided asset, the skeleton
carries a single signed instrument: FEDPAY > 0 is remittances accrued
payable to Treasury; FEDPAY < 0 *is* the deferred-asset position, in the
amount |FEDPAY|. Every identity then holds for either sign of Fed
income, and the remittance rule (accrue income to FEDPAY; pay cash only
down from a positive balance; losses deepen the negative balance) is
exactly the Fed's post-September-2022 practice.

## How the Federal Credit Fee enters the matrices

* **Balance sheet:** the fee is a flow, not a stock; it changes stocks
  only through settlement (RES down, TGA up) and through the current
  account's effect on net worth. The fee *base* is the LN_COV row —
  LN_GRD is structurally outside the base (grandfathering).
* **Current account (TFM):** two rows, `Federal Credit Fee (banks)` and
  `Federal Credit Fee (nonbanks)`: BNK −0.080, NBF −0.030, TRE +0.110 at
  the illustrative synchronized rates (fee rate = IORB = 2% on covered
  stocks of 4.00 and 1.50).
* **Capital account (settlement):** the bank leg settles in reserves
  (RES: BNK −0.080, FED liability shifts RES → TGA); the nonbank leg
  settles from the nonbank's deposits (DEP: NBF −0.030) and drains its
  bank's reserves by the same amount into the TGA. Treasury spending
  (`treasury_pay` in code) is the exact reverse: TGA down, reserves back
  up, recipient deposits credited. A fee collected and not yet spent is
  a *temporary* reserve drain and a one-time net-worth transfer — it is
  revenue exactly once.

## Reading the two TFM tables

The transactions-flow matrix is printed in two halves — current account
and capital account — with one column per sector in each. A transaction
row sums to zero **across both halves** (investment rows, for example,
show a current-account receipt for the producer and their offsetting
capital-account use of funds). Each sector's current balance equals the
change in its net worth; its current balance minus its net tangible
investment equals the change in its net financial assets. Both
identities, every row sum, and every column-pair sum are asserted by the
pytest suite on every run.

### Opening balance sheet

| Instrument | TRE | FED | BNK | NBF | HHD | NFC | SLG | ROW | Row total |
|---|---|---|---|---|---|---|---|---|---|
| RES |  | -3.000 | +3.000 |  |  |  |  |  | +0.000 |
| TGA | +0.800 | -0.800 |  |  |  |  |  |  | +0.000 |
| TS_PUB | -31.600 |  | +5.000 | +10.000 | +5.000 | +0.800 | +1.800 | +9.000 | -0.000 |
| TS_FED | -4.400 | +4.400 |  |  |  |  |  |  | +0.000 |
| FEDPAY |  |  |  |  |  |  |  |  | +0.000 |
| DEP |  |  | -18.000 | +0.500 | +11.000 | +4.500 | +1.000 | +1.000 | +0.000 |
| LN_COV |  |  | +4.000 | +1.500 | -3.500 | -2.000 |  |  | +0.000 |
| LN_GRD |  |  | +9.000 | +4.000 | -8.000 | -5.000 |  |  | +0.000 |
| CBN |  |  | +1.000 | +3.500 | +1.500 | -7.000 |  | +1.000 | +0.000 |
| EQ |  |  | -2.000 | -1.000 | +11.000 | -12.000 |  | +4.000 | +0.000 |
| CUR |  | -2.300 |  |  | +1.800 |  |  | +0.500 | +0.000 |
| K |  |  |  |  | +15.000 | +20.000 | +5.000 |  | +40.000 |
| **Net worth** (residual) | +35.200 | +1.700 | -2.000 | -18.500 | -33.800 | +0.700 | -7.800 | -15.500 | -40.000 |
| **Column total** | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | |

Net worth by sector (assets - liabilities, $T): TRE -35.200, FED -1.700, BNK +2.000, NBF +18.500, HHD +33.800, NFC -0.700, SLG +7.800, ROW +15.500. The Net worth row is entered negated so every column sums to zero, per Godley-Lavoie convention.

### Transactions-flow matrix -- current account

| Transaction | TRE | FED | BNK | NBF | HHD | NFC | SLG | ROW | Row total |
|---|---|---|---|---|---|---|---|---|---|
| Wages | -1.200 |  | -0.600 | -0.200 | +12.000 | -9.000 | -1.000 |  | -0.000 |
| Consumption |  |  |  |  | -11.000 | +11.000 |  |  | +0.000 |
| Government purchases (federal) | -2.500 |  |  |  |  | +2.500 |  |  | +0.000 |
| Government purchases (state/local) |  |  |  |  |  | +1.200 | -1.200 |  | +0.000 |
| Investment (NFC own capital formation) |  |  |  |  |  | +3.000 |  |  | +3.000 |
| Investment (household housing) |  |  |  |  |  | +0.800 |  |  | +0.800 |
| Investment (state/local) |  |  |  |  |  | +0.400 |  |  | +0.400 |
| Taxes to Treasury (HHD) | +3.200 |  |  |  | -3.200 |  |  |  | +0.000 |
| Taxes to Treasury (NFC) | +1.200 |  |  |  |  | -1.200 |  |  | +0.000 |
| Taxes to Treasury (NBF) | +0.050 |  |  | -0.050 |  |  |  |  | +0.000 |
| Taxes to Treasury (BNK) | +0.150 |  | -0.150 |  |  |  |  |  | +0.000 |
| Taxes to state/local (HHD) |  |  |  |  | -0.900 |  | +0.900 |  | +0.000 |
| Taxes to state/local (NFC) |  |  |  |  |  | -0.400 | +0.400 |  | +0.000 |
| Transfers to households (federal) | -3.400 |  |  |  | +3.400 |  |  |  | +0.000 |
| Transfers to households (state/local) |  |  |  |  | +0.500 |  | -0.500 |  | +0.000 |
| Net exports |  |  |  |  |  | +0.600 |  | -0.600 | +0.000 |
| Dividends and distributed profits |  |  | -0.250 | -0.080 | +0.996 | -0.900 |  | +0.234 | -0.000 |
| Interest on covered loans (HHD->BNK) |  |  | +0.153 |  | -0.153 |  |  |  | +0.000 |
| Interest on covered loans (NFC->BNK) |  |  | +0.087 |  |  | -0.087 |  |  | +0.000 |
| Interest on covered loans (HHD->NBF) |  |  |  | +0.057 | -0.057 |  |  |  | +0.000 |
| Interest on covered loans (NFC->NBF) |  |  |  | +0.033 |  | -0.033 |  |  | +0.000 |
| Interest on grandfathered loans (HHD->BNK) |  |  | +0.305 |  | -0.305 |  |  |  | +0.000 |
| Interest on grandfathered loans (NFC->BNK) |  |  | +0.190 |  |  | -0.190 |  |  | +0.000 |
| Interest on grandfathered loans (HHD->NBF) |  |  |  | +0.135 | -0.135 |  |  |  | +0.000 |
| Interest on grandfathered loans (NFC->NBF) |  |  |  | +0.085 |  | -0.085 |  |  | +0.000 |
| Interest on deposits |  |  | -0.270 | +0.007 | +0.165 | +0.068 | +0.015 | +0.015 | -0.000 |
| Interest on reserve balances (IORB) |  | -0.060 | +0.060 |  |  |  |  |  | +0.000 |
| Interest on Treasury securities (public-held) | -1.106 |  | +0.175 | +0.350 | +0.175 | +0.028 | +0.063 | +0.315 | +0.000 |
| Interest on Treasury securities (Fed-held) | -0.154 | +0.154 |  |  |  |  |  |  | +0.000 |
| Interest on corporate bonds |  |  | +0.050 | +0.175 | +0.075 | -0.350 |  | +0.050 | +0.000 |
| Federal Credit Fee (banks) | +0.080 |  | -0.080 |  |  |  |  |  | +0.000 |
| Federal Credit Fee (nonbanks) | +0.030 |  |  | -0.030 |  |  |  |  | +0.000 |
| Federal Reserve operating expenses |  | -0.020 |  |  | +0.020 |  |  |  | +0.000 |
| Fed earnings accrual to remittance position | +0.074 | -0.074 |  |  |  |  |  |  | +0.000 |
| **Sector current balance (= change in net worth)** | -3.576 | +0.000 | -0.330 | +0.482 | +1.581 | +7.351 | -1.322 | +0.014 | +4.200 |

### Transactions-flow matrix -- capital account

| Transaction | TRE | FED | BNK | NBF | HHD | NFC | SLG | ROW | Row total |
|---|---|---|---|---|---|---|---|---|---|
| Wages | +1.200 |  | +0.600 | +0.200 | -12.000 | +9.000 | +1.000 |  | +0.000 |
| Consumption |  |  |  |  | +11.000 | -11.000 |  |  | +0.000 |
| Government purchases (federal) | +2.500 |  |  |  |  | -2.500 |  |  | +0.000 |
| Government purchases (state/local) |  |  |  |  |  | -1.200 | +1.200 |  | +0.000 |
| Investment (NFC own capital formation) |  |  |  |  |  | -3.000 |  |  | -3.000 |
| Investment (household housing) |  |  |  |  |  | -0.800 |  |  | -0.800 |
| Investment (state/local) |  |  |  |  |  | -0.400 |  |  | -0.400 |
| Taxes to Treasury (HHD) | -3.200 |  |  |  | +3.200 |  |  |  | +0.000 |
| Taxes to Treasury (NFC) | -1.200 |  |  |  |  | +1.200 |  |  | +0.000 |
| Taxes to Treasury (NBF) | -0.050 |  |  | +0.050 |  |  |  |  | +0.000 |
| Taxes to Treasury (BNK) | -0.150 |  | +0.150 |  |  |  |  |  | +0.000 |
| Taxes to state/local (HHD) |  |  |  |  | +0.900 |  | -0.900 |  | +0.000 |
| Taxes to state/local (NFC) |  |  |  |  |  | +0.400 | -0.400 |  | +0.000 |
| Transfers to households (federal) | +3.400 |  |  |  | -3.400 |  |  |  | +0.000 |
| Transfers to households (state/local) |  |  |  |  | -0.500 |  | +0.500 |  | +0.000 |
| Net exports |  |  |  |  |  | -0.600 |  | +0.600 | +0.000 |
| Dividends and distributed profits |  |  | +0.250 | +0.080 | -0.996 | +0.900 |  | -0.234 | +0.000 |
| Interest on covered loans (HHD->BNK) |  |  | -0.153 |  | +0.153 |  |  |  | +0.000 |
| Interest on covered loans (NFC->BNK) |  |  | -0.087 |  |  | +0.087 |  |  | +0.000 |
| Interest on covered loans (HHD->NBF) |  |  |  | -0.057 | +0.057 |  |  |  | +0.000 |
| Interest on covered loans (NFC->NBF) |  |  |  | -0.033 |  | +0.033 |  |  | +0.000 |
| Interest on grandfathered loans (HHD->BNK) |  |  | -0.305 |  | +0.305 |  |  |  | +0.000 |
| Interest on grandfathered loans (NFC->BNK) |  |  | -0.190 |  |  | +0.190 |  |  | +0.000 |
| Interest on grandfathered loans (HHD->NBF) |  |  |  | -0.135 | +0.135 |  |  |  | +0.000 |
| Interest on grandfathered loans (NFC->NBF) |  |  |  | -0.085 |  | +0.085 |  |  | +0.000 |
| Interest on deposits |  |  | +0.270 | -0.007 | -0.165 | -0.068 | -0.015 | -0.015 | +0.000 |
| Interest on reserve balances (IORB) |  | +0.060 | -0.060 |  |  |  |  |  | +0.000 |
| Interest on Treasury securities (public-held) | +1.106 |  | -0.175 | -0.350 | -0.175 | -0.028 | -0.063 | -0.315 | -0.000 |
| Interest on Treasury securities (Fed-held) | +0.154 | -0.154 |  |  |  |  |  |  | +0.000 |
| Interest on corporate bonds |  |  | -0.050 | -0.175 | -0.075 | +0.350 |  | -0.050 | +0.000 |
| Federal Credit Fee (banks) | -0.080 |  | +0.080 |  |  |  |  |  | +0.000 |
| Federal Credit Fee (nonbanks) | -0.030 |  |  | +0.030 |  |  |  |  | +0.000 |
| Federal Reserve operating expenses |  | +0.020 |  |  | -0.020 |  |  |  | +0.000 |
| Fed earnings accrual to remittance position | -0.074 | +0.074 |  |  |  |  |  |  | +0.000 |
| **Sector capital balance (= -current balance)** | +3.576 | -0.000 | +0.330 | -0.482 | -1.581 | -7.351 | +1.322 | -0.014 | -4.200 |

### Closing balance sheet

| Instrument | TRE | FED | BNK | NBF | HHD | NFC | SLG | ROW | Row total |
|---|---|---|---|---|---|---|---|---|---|
| RES |  | -5.176 | +5.176 |  |  |  |  |  | +0.000 |
| TGA | -1.176 | +1.176 |  |  |  |  |  |  | +0.000 |
| TS_PUB | -33.000 |  | +5.040 | +10.480 | +5.160 | +0.880 | +1.880 | +9.560 | +0.000 |
| TS_FED | -4.600 | +4.600 |  |  |  |  |  |  | +0.000 |
| FEDPAY |  |  |  |  |  |  |  |  | +0.000 |
| DEP |  |  | -20.546 | +0.522 | +11.351 | +9.020 | -0.802 | +0.454 | -0.000 |
| LN_COV |  |  | +4.900 | +1.680 | -4.230 | -2.350 |  |  | -0.000 |
| LN_GRD |  |  | +8.100 | +3.600 | -7.200 | -4.500 |  |  | -0.000 |
| CBN |  |  | +1.000 | +3.700 | +1.600 | -7.300 |  | +1.000 | +0.000 |
| EQ |  |  | -2.000 | -1.000 | +11.100 | -12.100 |  | +4.000 | +0.000 |
| CUR |  | -2.300 |  |  | +1.800 |  |  | +0.500 | +0.000 |
| K |  |  |  |  | +15.800 | +23.000 | +5.400 |  | +44.200 |
| **Net worth** (residual) | +38.776 | +1.700 | -1.670 | -18.983 | -35.381 | -6.651 | -6.478 | -15.514 | -44.200 |
| **Column total** | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | |

Net worth by sector (assets - liabilities, $T): TRE -38.776, FED -1.700, BNK +1.670, NBF +18.983, HHD +35.381, NFC +6.651, SLG +6.478, ROW +15.514. The Net worth row is entered negated so every column sums to zero, per Godley-Lavoie convention.

Sectors: TRE = Treasury; FED = Federal Reserve; BNK = Commercial banks; NBF = Nonbank lenders; HHD = Households; NFC = Nonfinancial businesses; SLG = State & local governments; ROW = Foreign sector (rest of world)
