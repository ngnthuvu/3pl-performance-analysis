"""
3PL Performance Analysis - Public Pipeline Summary
==================================================

This repository intentionally publishes only a high-level version of the
analysis pipeline. Detailed transformation rules, raw data, and the full
implementation are kept private.

Analysis flow
-------------
Q1  Data enrichment
    - Map seller/buyer location attributes
    - Derive route using the business routing matrix
    - Estimate shipping fee by route and weight band

Q2  SLA & order-level performance
    - Delivery SLA: Seller -> Buyer
    - Return SLA: Buyer -> Seller
    - Calculate delivery/return lead time in hours
    - Flag data-quality exceptions
    - Classify Pickup / Delivery / Return as Ontime or Late

Q3  Carrier KPI aggregation
    - Pickup Ontime Rate
    - Delivery Ontime Rate
    - Return Ontime Rate
    - Rates use eligible observations as denominators

Q4  Route x 3PL analysis
    - Average delivery lead time
    - Average estimated shipping fee
    - Late-delivery rate
    - Route-specific carrier comparison

The full source implementation is not included in the public repository.
"""

from pathlib import Path
import pandas as pd


Q4A_ROUTES = ["Intra city", "Cross region", "Special same region"]


def summarize_ontime_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Public example of the aggregation logic used in Q3.
    Detailed upstream transformation logic is intentionally omitted.
    """
    metrics = []

    for carrier, group in df.groupby("3pl_name"):
        row = {"3pl_name": carrier}

        for stage in ["pickup", "delivery", "return"]:
            col = f"check_{stage}_ontime"
            eligible = group[col].notna().sum()
            ontime = group[col].eq("Ontime").sum()

            row[f"{stage}_ontime_rate_pct"] = (
                ontime / eligible * 100 if eligible else None
            )

        metrics.append(row)

    return pd.DataFrame(metrics).round(2)


def summarize_route_performance(df: pd.DataFrame):
    """
    Public example of Q4 aggregation.

    The private pipeline creates the enriched/order-level fields before this
    step. Only the analytical aggregation is shown here.
    """
    q4a = (
        df[df["route"].isin(Q4A_ROUTES)]
        .groupby(["route", "3pl_name"])
        .agg(
            avg_delivery_leadtime_hours=("leadtime_delivery", "mean"),
            avg_estimated_shipping_fee=("estimated_shipping_fee", "mean"),
        )
        .round(2)
        .reset_index()
    )

    eligible = df[df["check_delivery_ontime"].notna()].copy()

    q4b = (
        eligible.assign(
            is_late=eligible["check_delivery_ontime"].eq("Late")
        )
        .groupby(["route", "3pl_name"])
        .agg(
            eligible_delivery_orders=("is_late", "size"),
            late_delivery_orders=("is_late", "sum"),
        )
        .reset_index()
    )

    q4b["late_delivery_rate_pct"] = (
        q4b["late_delivery_orders"]
        / q4b["eligible_delivery_orders"]
        * 100
    ).round(2)

    return q4a, q4b


def main():
    """
    The public demo expects an already-enriched dataset.

    Raw workbook parsing, reference-table transformations, reverse-return SLA
    mapping, and data-quality handling are part of the private implementation.
    """
    input_path = Path("outputs/enriched_orders.csv")

    if not input_path.exists():
        print(
            "Public demo only: enriched_orders.csv is not included. "
            "See README for methodology and sample outputs."
        )
        return

    df = pd.read_csv(input_path)

    q3 = summarize_ontime_performance(df)
    q4a, q4b = summarize_route_performance(df)

    print("\nQ3 - 3PL Ontime Performance")
    print(q3.to_string(index=False))

    print("\nQ4a - Route Cost & Leadtime")
    print(q4a.to_string(index=False))

    print("\nQ4b - Route Late Delivery")
    print(q4b.to_string(index=False))


if __name__ == "__main__":
    main()
