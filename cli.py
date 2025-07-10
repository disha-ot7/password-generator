#!/usr/bin/env python
"""
Fancy terminal front‑end for pwsmith
------------------------------------
Run:  python cli.py  (or  pwgen if you register an entry‑point)
"""

from rich import print, box
from rich.table import Table
from generator import generate_password, score_password, hibp_pwned

def main():
    pwd = generate_password()
    score_info = score_password(pwd)
    leaks = hibp_pwned(pwd)

    tbl = Table(title="Password Report", box=box.SIMPLE)
    tbl.add_column("Item"); tbl.add_column("Value", style="bold")
    tbl.add_row("Password", f"[cyan]{pwd}")
    tbl.add_row("Strength (0‑4)", str(score_info["score"]))
    tbl.add_row("Crack‑time offline 1e10/s",
                score_info["crack_times_display"]["offline_fast_hashing_1e10_per_second"])
    tbl.add_row("Leaked?", "[red]YES[/]" if leaks else "[green]NO[/]")
    if leaks:
        tbl.add_row("Leak count", f"{leaks:,}")

    print(tbl)

if __name__ == "__main__":
    main()
