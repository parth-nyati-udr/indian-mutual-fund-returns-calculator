# Methodology

## XIRR
Find r such that Σ CFᵢ / (1 + r)^((dᵢ − d₀)/365) = 0. Solved with Brent's method on [−99.99%, +1000%]. Brent is bracketed, so unlike Newton–Raphson it cannot diverge or jump to a spurious root. Flows are sorted first, so input order doesn't matter. All-negative or all-positive flows raise an error.

## SIP
Instalment on day *k* of each month; if no NAV exists that day (holiday/weekend), the next NAV is used. Units = amount ÷ NAV. Valuation at the last NAV on or before the end date. XIRR uses −instalments and +final value.

Sanity property (tested): if NAV grows at a constant rate g, every instalment compounds at g, so SIP XIRR = g.

## Rolling returns
For each date *d*, compare NAV(d) with the last NAV on or before *d − N years* (calendar offset, not bar count, because NAV calendars have uneven gaps). Summary: min / median / max, share of windows below 0%, and share above 12%.

## Why rolling, not trailing
A trailing 3-year number depends entirely on today's start date. Rolling distributions show what an investor entering at any point actually experienced.
