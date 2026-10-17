"""One-call fund report, optionally exported to Excel."""
from __future__ import annotations

import pandas as pd

from .mfapi import fetch_nav
from .returns import point_to_point_cagr, rolling_summary
from .sip import simulate_sip


def fund_report(codes: list[int], sip_amount: float = 10_000, sip_start: str = "2021-01-01",
                excel_path: str | None = None) -> pd.DataFrame:
    """Trailing CAGR, 3y rolling distribution and SIP XIRR for several schemes."""
    rows = []
    for code in codes:
        nav = fetch_nav(code)
        sip = simulate_sip(nav, sip_amount, sip_start)
        roll = rolling_summary(nav, 3)
        rows.append({"code": code, "scheme": nav.name, "as_of": nav.index[-1].date(),
                     **{f"cagr_{y}y_%": (None if (v := point_to_point_cagr(nav, y)) is None else round(v * 100, 2))
                        for y in (1, 3, 5)},
                     "sip_xirr_%": sip["xirr_%"],
                     **{f"roll3y_{k}": v for k, v in roll.items()}})
    df = pd.DataFrame(rows)
    if excel_path:
        df.to_excel(excel_path, index=False)  # needs openpyxl
    return df
