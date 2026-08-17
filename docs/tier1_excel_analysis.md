# Tier 1 — Excel Analysis

## Purpose

Excel is used as the business-rule exploration and validation layer.

The objective is not merely to calculate KPIs, but to make the mapping logic visible enough to inspect individual orders, validate reference matrices, and test assumptions before automation.

## Q1 — Order Enrichment

The workflow enriches each raw order with:

```text
Seller State + City
    → Seller Urban/Rural
    → Seller Area

Buyer State + City
    → Buyer Urban/Rural
    → Buyer Area

Seller Area (FROM) + Buyer Area (TO)
    → Route

Route + Weight Band
    → Estimated Shipping Fee
```

Key implementation patterns:

- Location mapping: structured-reference lookup using State + City.
- Route mapping: two-dimensional lookup against the Route matrix.
- Seller is treated as **FROM** and Buyer as **TO**.
- Shipping fee depends jointly on Route and Weight Band.

A PivotTable was used as a QA check: each Seller Area + Buyer Area combination should resolve to one route.

## Q2 — SLA and Lead Time

Delivery SLA direction:

```text
Seller → Buyer
```

Return SLA direction:

```text
Buyer → Seller
```

SLA is stored in **hours**.

Urban/Rural logic:

```text
Both Urban → Urban SLA
Otherwise  → Rural SLA
```

Delivery lead time:

```text
(delivery_done - pickup_done) × 24
```

Return lead time:

```text
(returned - return_initiated) × 24
```

Invalid delivery observations are excluded when the event sequence is inconsistent, including cases where a return is initiated before the recorded delivery completion.

## Q3 — 3PL On-time Performance

Excel Data Model measures use eligible observations as the denominator.

Conceptually:

```text
Ontime Rate
=
Ontime Eligible Orders
/
All Eligible Orders
```

This prevents non-applicable rows from being counted as failures.

## Q4 — Route-level Analysis

Q4a compares:

- Average Delivery Lead Time
- Average Estimated Shipping Fee

for:

- Cross region
- Intra city
- Special same region

Q4b compares Late Delivery Rate by Route × 3PL.

The analytical interpretation focuses on trade-offs between:

- cost
- speed
- reliability

rather than identifying a single carrier as universally “best”.
