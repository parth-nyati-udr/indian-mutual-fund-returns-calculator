# Test plan

Run `pytest -q`. All offline; expected values are analytic.

| Test | Scenario | Expected |
|---|---|---|
| `test_xirr_simple_one_year` | −1000 → +1100 in 1 yr | 10.000% |
| `test_xirr_negative_return` | −1000 → +800 | −20% |
| `test_xirr_order_independent` | Shuffled flows | Same result |
| `test_xirr_rejects_one_sided_flows` | All negative | ValueError |
| `test_sip_dates_monthly_on_day` | Jan–Jun, day 5 | 6 dates, all on the 5th |
| `test_sip_flat_nav_gives_zero_return` | Constant NAV | 0% abs, 0% XIRR |
| `test_sip_xirr_matches_underlying_growth` | NAV at 12%/yr, 84 months | XIRR ≈ 12% |
| `test_sip_holiday_uses_next_nav` | No NAV on the 5th | Allotted next NAV date |
| `test_lumpsum` | 10%/yr for 10 yrs | CAGR ≈ 10% |
| `test_point_to_point` | 15%/yr; short history | ≈ 15%; None |
| `test_rolling_returns_constant` | 9%/yr | All windows ≈ 9% |
| `test_rolling_summary_counts` | 15%/yr | 0% below zero, 100% above 12% |
| `test_parse_nav_payload_sorts_and_cleans` | Unsorted, zero NAV | Sorted, zero dropped |

## Manual checks
Run `fund_report` on a known scheme and compare 1/3/5-year CAGR with the AMC fact sheet.
