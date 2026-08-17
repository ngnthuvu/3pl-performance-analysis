# Tier 3 — BigQuery Analytics

## Purpose

BigQuery is implemented as an independent relational analytics layer.

It does **not** ingest the Python enriched output. Instead, it starts from the same raw orders and reference rules used by the Excel and Python layers.

## Source Tables

```text
stg_orders
ref_location
ref_route
ref_shipping_fee
ref_sla
```

Spreadsheet matrices are normalized before loading into BigQuery.

For example, a Route matrix becomes:

```text
from_area | to_area | route
```

and the Shipping Fee matrix becomes:

```text
min_weight_kg | max_weight_kg | route | fee
```

This makes the rules suitable for relational joins.

## Transformation Model

```text
stg_orders
    ↓
int_orders_location
    ↓
int_orders_route
    ↓
int_orders_fee
    ↓
int_orders_sla
    ↓
int_orders_datetime
    ↓
int_orders_leadtime
    ↓
fact_3pl_orders
    ↓
Q3 / Q4 analytical marts
```

Intermediate tables make each transformation stage independently testable.

## Key SQL Concepts

### Location Mapping

The same reference table is joined twice:

- once for Seller
- once for Buyer

### Route Mapping

```text
seller_area = from_area
buyer_area  = to_area
```

### Shipping Fee

The rule is matched using:

```text
route
+
weight range
```

### SLA

Delivery:

```text
Seller → Buyer
```

Return:

```text
Buyer → Seller
```

### Eligible Denominators

Q3 and Q4 rates use only non-null performance observations.

A carrier with no eligible return observations therefore has a NULL return rate, not 0%.

## Data-quality Debugging Case

The first BigQuery Q4b output did not match Excel/Python.

Investigation showed:

- route aggregation SQL was correct;
- average delivery lead times were ~15–16 hours too high;
- 100% of `pickup_done` values were exactly at midnight;
- the CSV export had removed the actual pickup time component.

After preserving full datetime values in the source CSV and rebuilding the pipeline, BigQuery matched the validated Excel/Python outputs.

This demonstrates the importance of validating staging data before assuming that an aggregation or business rule is wrong.

## Final Validation

The final BigQuery results matched the Python layer for:

- Q3 Pickup/Delivery/Return performance
- Q4a Average Lead Time and Estimated Shipping Fee
- Q4b Late Delivery Rate
