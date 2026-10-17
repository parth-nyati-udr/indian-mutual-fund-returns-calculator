from datetime import date

import numpy as np
import pandas as pd
import pytest

from mf_analytics import (lumpsum_return, point_to_point_cagr, rolling_returns,
                          rolling_summary, simulate_sip, sip_cashflows, xirr)
from mf_analytics.mfapi import parse_nav_payload

IDX = pd.bdate_range("2015-01-01", "2026-10-15")


def nav_at(rate):
    t = (IDX - IDX[0]).days / 365.0
    return pd.Series(10 * (1 + rate) ** t, index=IDX)


# ---- XIRR ---------------------------------------------------------------
def test_xirr_simple_one_year():
    assert xirr([(date(2025, 1, 1), -1000), (date(2026, 1, 1), 1100)]) == pytest.approx(0.10, abs=1e-6)


def test_xirr_negative_return():
    assert xirr([(date(2025, 1, 1), -1000), (date(2026, 1, 1), 800)]) == pytest.approx(-0.20, abs=1e-6)


def test_xirr_order_independent():
    f = [(date(2026, 1, 1), 2300), (date(2024, 1, 1), -1000), (date(2025, 1, 1), -1000)]
    assert xirr(f) == pytest.approx(xirr(sorted(f)))


def test_xirr_rejects_one_sided_flows():
    with pytest.raises(ValueError):
        xirr([(date(2025, 1, 1), -1000), (date(2026, 1, 1), -10)])


# ---- SIP ----------------------------------------------------------------
def test_sip_dates_monthly_on_day():
    d = sip_cashflows("2024-01-01", "2024-06-30", day=5)
    assert len(d) == 6 and all(x.day == 5 for x in d)


def test_sip_flat_nav_gives_zero_return():
    r = simulate_sip(pd.Series(10.0, index=IDX), 1000, "2020-01-01", "2023-12-31")
    assert r["abs_return_%"] == 0 and abs(r["xirr_%"]) < 1e-6


def test_sip_xirr_matches_underlying_growth():
    """Every instalment compounds at the NAV growth rate, so XIRR = that rate."""
    r = simulate_sip(nav_at(0.12), 5000, "2018-01-01", "2024-12-31")
    assert r["xirr_%"] == pytest.approx(12.0, abs=0.1)
    assert r["instalments"] == 84


def test_sip_holiday_uses_next_nav():
    nav = pd.Series([10.0, 11.0], index=pd.to_datetime(["2024-01-04", "2024-01-08"]))
    r = simulate_sip(nav, 1000, "2024-01-05", "2024-01-08")
    assert r["ledger"].iloc[0]["date"] == pd.Timestamp("2024-01-08")


def test_lumpsum():
    r = lumpsum_return(nav_at(0.10), "2016-01-01", "2026-01-01")
    assert r["cagr_%"] == pytest.approx(10.0, abs=0.1)


# ---- returns ------------------------------------------------------------
def test_point_to_point():
    assert point_to_point_cagr(nav_at(0.15), 5) == pytest.approx(0.15, abs=0.002)
    assert point_to_point_cagr(nav_at(0.15).iloc[-300:], 3) is None


def test_rolling_returns_constant():
    r = rolling_returns(nav_at(0.09), 3)
    assert len(r) > 1500 and r.between(0.085, 0.095).all()


def test_rolling_summary_counts():
    s = rolling_summary(nav_at(0.15), 3)
    assert s["below_0_%"] == 0 and s["above_12_%"] == 100


# ---- mfapi parsing ------------------------------------------------------
def test_parse_nav_payload_sorts_and_cleans():
    payload = {"meta": {"scheme_name": "Test Fund"},
               "data": [{"date": "03-01-2024", "nav": "12.5"}, {"date": "01-01-2024", "nav": "12.0"},
                        {"date": "02-01-2024", "nav": "0"}]}
    s = parse_nav_payload(payload)
    assert list(s.values) == [12.0, 12.5] and s.name == "Test Fund"
