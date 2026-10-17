"""XIRR: the annualised rate r that sets the NPV of dated cashflows to zero.

    sum( CF_i / (1 + r) ** ((d_i - d_0) / 365) ) = 0

Solved with Brent's method (scipy.optimize.brentq): bracketed, so it always
converges when a root exists, unlike Newton which can diverge.
Sign convention: investments negative, redemptions / current value positive.
"""
from __future__ import annotations

from datetime import date

from scipy.optimize import brentq


def _npv(rate: float, flows: list[tuple[date, float]]) -> float:
    d0 = flows[0][0]
    return sum(cf / (1 + rate) ** ((d - d0).days / 365.0) for d, cf in flows)


def xirr(flows: list[tuple[date, float]], lo: float = -0.9999, hi: float = 10.0) -> float:
    """Annualised internal rate of return for irregular cashflows.

    Raises ValueError if flows don't contain both signs or no root exists in
    [lo, hi] (e.g. > 1000%/yr).
    """
    flows = sorted(flows)
    if not any(cf < 0 for _, cf in flows) or not any(cf > 0 for _, cf in flows):
        raise ValueError("Need at least one negative and one positive cashflow.")
    try:
        return float(brentq(_npv, lo, hi, args=(flows,), xtol=1e-10, maxiter=500))
    except ValueError as e:
        raise ValueError(f"No XIRR root in [{lo}, {hi}]") from e
