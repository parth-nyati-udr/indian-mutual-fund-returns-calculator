"""Thin client for api.mfapi.in (free, AMFI-sourced NAV history)."""
from __future__ import annotations

import pandas as pd
import requests

BASE = "https://api.mfapi.in/mf"


def search_scheme(query: str) -> pd.DataFrame:
    """Find scheme codes by name. Prefer 'Direct' + 'Growth' variants for analysis."""
    r = requests.get(f"{BASE}/search", params={"q": query}, timeout=30)
    r.raise_for_status()
    return pd.DataFrame(r.json())


def parse_nav_payload(payload: dict) -> pd.Series:
    """Convert mfapi JSON ({'meta':..., 'data':[{'date':'dd-mm-yyyy','nav':'..'}]}) to a Series."""
    df = pd.DataFrame(payload["data"])
    s = pd.Series(pd.to_numeric(df["nav"], errors="coerce").values,
                  index=pd.to_datetime(df["date"], format="%d-%m-%Y"))
    s = s[s > 0].sort_index()
    s.name = payload.get("meta", {}).get("scheme_name", "nav")
    return s


def fetch_nav(scheme_code: int | str) -> pd.Series:
    r = requests.get(f"{BASE}/{scheme_code}", timeout=30)
    r.raise_for_status()
    return parse_nav_payload(r.json())
