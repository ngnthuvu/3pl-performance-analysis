# 3PL Performance Analysis

A three-layer analytics project evaluating third-party logistics (3PL) performance across pickup, delivery, return, cost, lead time, and route-level reliability.

The same business logic is implemented independently in:

1. **Excel** — business-rule exploration and validation
2. **Python** — reproducible automation
3. **BigQuery** — scalable relational analytics

The purpose is not to chain Excel → Python → BigQuery as technical dependencies. Instead, each layer reproduces the same analytical model from the source data and reference rules, allowing the outputs to be reconciled across tools.

---

## Business Questions

The analysis addresses four main questions:

- **Q1 — Order enrichment:** determine Seller/Buyer Area, Urban/Rural classification, route, and estimated shipping fee.
- **Q2 — SLA performance:** derive delivery/return SLA, lead time, data-quality flags, and Ontime/Late status.
- **Q3 — Carrier performance:** compare pickup, delivery, and return on-time rates across 3PL providers.
- **Q4 — Route performance:** compare cost, delivery lead time, and late-delivery rates by Route × 3PL.

---

## Architecture

```text
                           ┌── Excel
Raw orders + references ───┼── Python
                           └── BigQuery
                                │
                                ▼
                       Reconciled outputs
```

### Shared business rules

- Seller is the **FROM** side of a delivery route.
- Buyer is the **TO** side.
- Delivery SLA direction: **Seller → Buyer**.
- Return SLA direction: **Buyer → Seller**.
- If both Seller and Buyer are Urban, use the Urban SLA; otherwise use the Rural SLA.
- Delivery lead time = `delivery_done - pickup_done`, in hours.
- Return lead time = `returned - return_initiated`, in hours.
- Pickup performance excludes non-eligible observations such as Dropoff shipments.
- Performance rates use **eligible observations as the denominator**, not all orders.

---

## Repository Structure

```text
3pl-performance-analysis/
├── README.md
├── docs/
│   ├── tier1_excel_analysis.md
│   ├── tier2_python_automation.md
│   └── tier3_bigquery.md
├── src/
│   └── e13_pipeline_demo.py
├── sql/
│   └── bigquery_demo.sql
├── outputs/
│   ├── q3_3pl_performance.csv
│   ├── q4a_route_performance.csv
│   └── q4b_late_delivery.csv
├── assets/
│   └── q4b_late_delivery_rate.png
├── requirements.txt
└── .gitignore
```

The detailed production-style transformation code is intentionally kept private. Public files demonstrate the analytical approach and validated outputs without exposing the full implementation.

---

## Validated Results

### Q3 — 3PL On-time Performance

| Carrier | Pickup Ontime | Delivery Ontime | Return Ontime |
|---|---:|---:|---:|
| Shipping Carrier A | 89.94% | 87.84% | 71.95% |
| Shipping Carrier B | 89.44% | 90.21% | — |
| Shipping Carrier C | 90.22% | 79.94% | — |
| Shipping Carrier D | 94.70% | 76.39% | 22.68% |
| Shipping Carrier E | 91.69% | 78.09% | — |

A missing return rate means the carrier had no eligible return observations; it does **not** mean 0%.

### Q4 — Main route-level findings

- **Cross region:** Carrier A offers the strongest overall trade-off between speed and reliability at only a small cost premium.
- **Intra city:** Carrier B is more balanced than Carrier D; their speed and cost are similar, while Carrier B has much stronger SLA reliability.
- **Special same region:** Carrier D is the strongest premium option, combining the fastest delivery lead time with the lowest late-delivery rate despite a higher average fee.
- Carrier selection should therefore be **route-specific**, using cost, speed, and reliability together rather than relying on a single overall ranking.

---

## Cross-layer Validation

The final Excel, Python, and BigQuery implementations were reconciled against the same expected outputs.

Examples:

| Metric | Validated Result |
|---|---:|
| Carrier A pickup on-time rate | 89.94% |
| Carrier A delivery on-time rate | 87.84% |
| Carrier A return on-time rate | 71.95% |
| Carrier D return on-time rate | 22.68% |
| Cross region / Carrier A late rate | 8.26% |
| Intra city / Carrier B late rate | 11.72% |
| Special same region / Carrier D late rate | 4.44% |

This cross-tool reconciliation is used as a data-quality control rather than assuming that one implementation is automatically correct.

---

## Data-quality Debugging Example

During BigQuery implementation, route-level late-delivery rates were initially much higher than the validated Excel/Python results.

The issue was traced through:

```text
Q4b mismatch
→ check average delivery lead time
→ lead time too high by ~15–16 hours
→ inspect timestamp distribution
→ 100% of pickup_done values were at 00:00:00
→ raw CSV export had lost the pickup time component
→ preserve full datetime in source CSV
→ rerun pipeline
→ BigQuery matched Excel/Python
```

This illustrates why warehouse validation should include both final KPI reconciliation and intermediate data-quality checks.

---

## Tools

- Microsoft Excel / Power Query / PivotTable / Data Model
- Python / pandas / matplotlib
- Google BigQuery / GoogleSQL

---

## Notes

Raw source data, detailed transformation logic, and private implementation files are excluded from the public repository.
