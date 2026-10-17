"""mf-analytics: XIRR, SIP simulation and rolling returns for Indian mutual funds."""
from .xirr import xirr
from .sip import sip_cashflows, simulate_sip, lumpsum_return
from .returns import point_to_point_cagr, rolling_returns, rolling_summary
from .mfapi import search_scheme, fetch_nav

__version__ = "1.0.0"
