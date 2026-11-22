"""Render the balance-sheet and transactions-flow matrices as Markdown
tables, generated FROM the data structures in sfc_core/scenario so the
documentation can never drift from the code. Output is pasted into
MATRICES.md; regenerate with:  python3 render_matrices.py
"""

from sfc_core import (FINANCIAL_INSTRUMENTS, SECTORS, SECTOR_NAMES,
                      TANGIBLE_INSTRUMENTS)
from scenario import build_period, opening_balance_sheet


def fmt(v):
    return "" if v == 0 else f"{v:+.3f}"


def balance_sheet_table(bs, title):
    lines = [f"### {title}", ""]
    lines.append("| Instrument | " + " | ".join(SECTORS) + " | Row total |")
    lines.append("|" + "---|" * (len(SECTORS) + 2))
    for inst in list(FINANCIAL_INSTRUMENTS) + list(TANGIBLE_INSTRUMENTS):
        vals = [bs.get(inst, s) for s in SECTORS]
        lines.append(f"| {inst} | " + " | ".join(fmt(v) for v in vals)
                     + f" | {sum(vals):+.3f} |")
    nw = [bs.net_worth(s) for s in SECTORS]
    lines.append("| **Net worth** (residual) | "
                 + " | ".join(fmt(-v) for v in nw)
                 + f" | {-sum(nw):+.3f} |")
    lines.append("| **Column total** | "
                 + " | ".join("0.000" for _ in SECTORS) + " | |")
    lines.append("")
    lines.append("Net worth by sector (assets - liabilities, $T): "
                 + ", ".join(f"{s} {v:+.3f}" for s, v in zip(SECTORS, nw))
                 + ". The Net worth row is entered negated so every column "
                   "sums to zero, per Godley-Lavoie convention.")
    return "\n".join(lines)


def tfm_table(result, account, title):
    lines = [f"### {title}", ""]
    lines.append("| Transaction | " + " | ".join(SECTORS) + " | Row total |")
    lines.append("|" + "---|" * (len(SECTORS) + 2))
    for name, row in result.tfm.items():
        vals = [row.get((s, account), 0.0) for s in SECTORS]
        if all(v == 0 for v in vals):
            continue
        lines.append(f"| {name} | " + " | ".join(fmt(v) for v in vals)
                     + f" | {sum(vals):+.3f} |")
    if account == "current":
        totals = [result.current_balance(s) for s in SECTORS]
        label = "**Sector current balance (= change in net worth)**"
    else:
        totals = [result.capital_balance(s) for s in SECTORS]
        label = "**Sector capital balance (= -current balance)**"
    lines.append(f"| {label} | " + " | ".join(fmt(v) for v in totals)
                 + f" | {sum(totals):+.3f} |")
    return "\n".join(lines)


if __name__ == "__main__":
    opening = opening_balance_sheet()
    result = build_period(opening).close()
    print(balance_sheet_table(opening, "Opening balance sheet"))
    print()
    print(tfm_table(result, "current",
                    "Transactions-flow matrix -- current account"))
    print()
    print(tfm_table(result, "capital",
                    "Transactions-flow matrix -- capital account"))
    print()
    print(balance_sheet_table(result.closing, "Closing balance sheet"))
    print()
    print("Sectors: " + "; ".join(f"{s} = {SECTOR_NAMES[s]}"
                                  for s in SECTORS))
