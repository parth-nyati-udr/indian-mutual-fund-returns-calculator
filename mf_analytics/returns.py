"""Point-to-point and rolling returns on a NAV series."""
from __future__ import annotations

import pandas as pd


def point_to_point_cagr(nav: pd.Series, years: float) -> float | None:
    """Trailing CAGR using the last NAV on/before (latest - years). None if too short."""
    nav = nav.sort_index().dropna()
    past = nav.loc[:nav.index[-1] - pd.DateOffset(years=years)]
    if past.empty:
        return None
    return float((nav.iloc[-1] / past.iloc[-1]) ** (1 / years) - 1)


def rolling_returns(nav: pd.Series, years: int) -> pd.Series:
    """Annualised return for every start date with a full `years` window.

    Calendar-based (not bar count) because MF NAVs skip holidays unevenly:
    for each date d, compare NAV(d) with the last NAV on/before d - years.
    """
    nav = nav.sort_index().dropna()
    starts = nav.reindex(nav.index - pd.DateOffset(years=years), method="ffill")
    starts.index = nav.index
    valid = starts.notna() & (nav.index - pd.DateOffset(years=years) >= nav.index[0])
    return ((nav[valid] / starts[valid]) ** (1 / years) - 1).rename(f"rolling_{years}y")


def rolling_summary(nav: pd.Series, years: int = 3) -> dict:
    """Distribution of rolling returns: how often the fund delivered what."""
    r = rolling_returns(nav, years)
    if r.empty:
        return {"windows": 0}
    return {"windows": len(r), "min_%": round(r.min() * 100, 2), "median_%": round(r.median() * 100, 2),
            "max_%": round(r.max() * 100, 2), "below_0_%": round((r < 0).mean() * 100, 1),
            "above_12_%": round((r > 0.12).mean() * 100, 1)}
