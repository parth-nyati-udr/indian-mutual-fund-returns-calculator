# Indian Mutual Fund Returns Calculator

Accurate return analytics for Indian mutual funds using free AMFI NAV data from [mfapi.in](https://www.mfapi.in): **XIRR** for irregular cashflows, **SIP simulation** with holiday handling, and **rolling-return distributions** that show how consistently a fund delivered, not just its best trailing number.

## Features
- `xirr(flows)`: bracketed Brent solver, always converges when a root exists.
- `simulate_sip(nav, amount, start)`: monthly SIP ledger, value, absolute return, XIRR.
- `rolling_returns(nav, years)` / `rolling_summary`: calendar-correct rolling CAGR and its distribution (% of windows < 0, > 12%).
- `fund_report([codes], excel_path=...)`: one table for several schemes, optional Excel export.

## Install & run
```bash
pip install -e ".[dev,excel]"
python -c "
from mf_analytics import search_scheme
from mf_analytics.report import fund_report
print(search_scheme('flexi cap direct growth').head())
print(fund_report([122639], sip_amount=10000, sip_start='2021-01-01'))"
```

Your own cashflows:
```python
from datetime import date
from mf_analytics import xirr
xirr([(date(2024,1,5), -10000), (date(2024,2,5), -10000), (date(2026,10,15), 24500)])
```

## Layout
```
mf_analytics/
  xirr.py     XIRR via scipy brentq
  sip.py      SIP dates, simulation, lump sum
  returns.py  point-to-point and rolling returns
  mfapi.py    search + NAV fetch + payload parsing
  report.py   multi-fund summary, Excel export
tests/        13 offline tests with analytically known answers
docs/         SCOPE.md, METHODOLOGY.md, TEST_PLAN.md
```

## Limitations
Ignores stamp duty, exit loads and taxes. mfapi.in is a free community service: if it is down, NAVs are also published by AMFI. Not investment advice.

## License
MIT
