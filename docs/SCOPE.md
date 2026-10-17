# Scope

## The ask
Replace spreadsheet XIRR and fact-sheet "trailing returns" with a reproducible tool that answers: what did my SIP actually earn, and how consistent has this fund been across every possible holding period?

## In scope
- Indian mutual fund NAVs via mfapi.in (any AMFI scheme code).
- XIRR for arbitrary dated cashflows.
- Monthly SIP simulation; lump sum CAGR.
- Trailing and rolling returns with distribution statistics.
- Excel export.

## Out of scope
- Parsing CAS statements or broker exports (see `fund-data-extractors`).
- Tax computation, exit loads, stamp duty.
- Portfolio-level allocation or look-through.

## Assumptions
- Instalments on a non-NAV day are allotted at the next available NAV.
- Day count Actual/365 (Excel XIRR convention).

## Success criteria
Tests reproduce analytically known results; live report matches fact-sheet trailing returns within rounding.
