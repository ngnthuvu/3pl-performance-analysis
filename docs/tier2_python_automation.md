# Tier 2 — Python Automation

## Purpose

Python reproduces the same business logic directly from source/reference data and turns the analysis into a repeatable pipeline.

Python does **not** depend on Excel-calculated output.

Conceptually:

```text
Raw orders
+ Location reference
+ Route reference
+ Shipping fee reference
+ SLA reference
        ↓
Python transformation
        ↓
Validated analytical outputs
```

## Main Transformation Stages

1. Map Seller and Buyer locations.
2. Derive Seller/Buyer Area and Urban/Rural.
3. Resolve Route using Seller as FROM and Buyer as TO.
4. Resolve Estimated Shipping Fee by Route + Weight Band.
5. Resolve Delivery SLA using Seller → Buyer.
6. Resolve Return SLA using Buyer → Seller.
7. Normalize datetime fields.
8. Calculate delivery and return lead times in hours.
9. Apply data-quality rules.
10. Derive Ontime/Late flags.
11. Aggregate Q3 and Q4 outputs.

## Why Python Adds Value

Compared with Excel, the Python layer provides:

- repeatability
- lower manual refresh risk
- explicit transformation functions
- easier data-quality assertions
- easier output generation
- a path toward scheduled or production workflows

## Public vs Private Code

The repository contains only a concise public demonstration.

The full implementation is intentionally kept private because it contains detailed parsing, mapping, validation, and transformation logic.

## Validation

The corrected Python pipeline was reconciled against the Excel results.

Examples:

```text
Carrier A return on-time rate = 71.95%
Carrier D return on-time rate = 22.68%

Cross region / Carrier A late rate = 8.26%
Intra city / Carrier B late rate = 11.72%
Special same region / Carrier D late rate = 4.44%
```

These results are also reproduced independently by the BigQuery layer.
