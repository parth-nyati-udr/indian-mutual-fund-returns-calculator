"""SIP simulation on a NAV series."""
from __future__ import annotations

from datetime import date

import pandas as pd

from .xirr import xirr


def _nav_on_or_after(nav: pd.Series, d: pd.Timestamp) -> tuple[pd.Timestamp, float] | None:
    """NAV on the instalment date, or the next business day with a NAV (as AMCs do)."""
    later = nav.loc[d:]
    return (later.index[0], float(later.iloc[0])) if len(later) else None


def sip_cashflows(start: str, end: str, day: int = 5) -> list[pd.Timestamp]:
    """Monthly instalment dates on `day` of each month between start and end."""
    months = pd.date_range(pd.Timestamp(start).to_period("M").to_timestamp(),
                           pd.Timestamp(end), freq="MS")
    dates = [m + pd.Timedelta(days=day - 1) for m in months]
    return [d for d in dates if pd.Timestamp(start) <= d <= pd.Timestamp(end)]


def simulate_sip(nav: pd.Series, amount: float, start: str, end: str | None = None,
                 day: int = 5) -> dict:
    """Run a monthly SIP and value it at the last NAV on/before `end`.

    Returns invested, units, current value, absolute return and XIRR, plus
    the instalment ledger. Stamp duty and exit loads are ignored.
    """
    nav = nav.sort_index().dropna()
    end_ts = pd.Timestamp(end) if end else nav.index[-1]
    ledger = []
    for d in sip_cashflows(start, str(end_ts.date()), day):
        hit = _nav_on_or_after(nav, d)
        if hit and hit[0] <= end_ts:
            ledger.append({"date": hit[0], "nav": hit[1], "amount": amount, "units": amount / hit[1]})
    if not ledger:
        raise ValueError("No instalments fall inside the NAV history.")
    led = pd.DataFrame(ledger)
    val_date = nav.loc[:end_ts].index[-1]
    value = led["units"].sum() * float(nav.loc[val_date])
    invested = led["amount"].sum()
    flows = [(r.date.date(), -r.amount) for r in led.itertuples()] + [(val_date.date(), value)]
    return {
        "instalments": len(led), "invested": round(invested, 2),
        "units": round(led["units"].sum(), 4), "value": round(value, 2),
        "abs_return_%": round((value / invested - 1) * 100, 2),
        "xirr_%": round(xirr(flows) * 100, 2), "as_of": val_date.date(), "ledger": led,
    }


def lumpsum_return(nav: pd.Series, start: str, end: str | None = None) -> dict:
    """Lump sum bought on `start` (next NAV) and valued at `end`."""
    nav = nav.sort_index().dropna()
    d0, n0 = _nav_on_or_after(nav, pd.Timestamp(start))
    sub = nav.loc[:pd.Timestamp(end)] if end else nav
    d1, n1 = sub.index[-1], float(sub.iloc[-1])
    years = (d1 - d0).days / 365.0
    return {"from": d0.date(), "to": d1.date(), "abs_%": round((n1 / n0 - 1) * 100, 2),
            "cagr_%": round(((n1 / n0) ** (1 / years) - 1) * 100, 2) if years > 0 else None}
