"""
E13 - 3PL Performance Analysis Pipeline (Demo Version)
=======================================================
Course: Foundation of Supply Chain Analytics
Mentored by: Trần Viết Thanh (https://www.linkedin.com/in/thanhtranviet248/)

This script automates the analysis of ~96,000 shipping orders across 5 carriers (A-E).
It replaces manual Excel workflows (INDEX-MATCH, IFS, Pivot Tables) with Python/Pandas.

Note: This is a partial demo showcasing core logic and techniques.
Full implementation is available upon request.
"""

import pandas as pd
import numpy as np

# ==============================================
# STEP 1: DATA LOADING
# ==============================================
FILE_NAME = "e13_exercise (ver2).xlsx"

# Load the main dataset (~96k rows) and lookup tables from different sheets
raw = pd.read_excel(FILE_NAME, sheet_name="raw_data")

# Load Table 1: City → Area mapping (714 records)
table1 = pd.read_excel(FILE_NAME, sheet_name="question_1", header=3, usecols="A:D", nrows=714)
table1.columns = ["state", "city", "urban_rural", "area"]

# Drop empty target columns to avoid merge conflicts (_x, _y suffixes)
cols_to_clear = ["seller_area", "buyer_area", "seller_in_urban_rural", 
                 "buyer_in_urban_rural", "route", "estimated_shipping_fee"]
raw = raw.drop(columns=[c for c in cols_to_clear if c in raw.columns])

print(f"✅ Data loaded: {len(raw):,} rows")

# ==============================================
# STEP 2: AREA MAPPING (Q1) — pd.merge replaces INDEX-MATCH
# ==============================================
# Instead of writing INDEX-MATCH for 96k cells in Excel,
# we use pd.merge() (LEFT JOIN) to map areas in one line.
# This is the single most powerful upgrade from Excel to Python.

# Merge for Seller: rename table1 columns to match seller fields, then LEFT JOIN
table1_seller = table1.rename(columns={
    "state": "seller_state", "city": "seller_city",
    "urban_rural": "seller_in_urban_rural", "area": "seller_area"
})
raw = raw.merge(table1_seller, on=["seller_state", "seller_city"], how="left")

# Merge for Buyer: same logic, different column names
table1_buyer = table1.rename(columns={
    "state": "buyer_state", "city": "buyer_city",
    "urban_rural": "buyer_in_urban_rural", "area": "buyer_area"
})
raw = raw.merge(table1_buyer, on=["buyer_state", "buyer_city"], how="left")

print("✅ Q1: Area mapping completed (pd.merge replaced INDEX-MATCH)")

# ==============================================
# STEP 3: ROUTE CLASSIFICATION — Dictionary lookup replaces matrix formula
# ==============================================
# In Excel, this required a complex INDEX-MATCH-MATCH formula
# to find the intersection of seller_area (row) and buyer_area (column).
# In Python, we build a dictionary from the route matrix and look up each pair.

table2 = pd.read_excel(FILE_NAME, sheet_name="question_1", header=5, usecols="F:L", nrows=7)
from_areas = pd.read_excel(FILE_NAME, sheet_name="question_1", 
                           header=None, usecols="F", skiprows=6, nrows=6).iloc[:, 0].tolist()
to_areas = table2.columns.tolist()

# Build route dictionary: (seller_area, buyer_area) → route_type
route_dict = {}
for i, from_a in enumerate(from_areas):
    for j, to_a in enumerate(to_areas):
        route_dict[(str(from_a).strip(), str(to_a).strip())] = str(table2.values[i][j]).strip()

# Apply dictionary lookup across all 96k rows
raw["route"] = raw.apply(
    lambda row: route_dict.get(
        (str(row["seller_area"]).strip(), str(row["buyer_area"]).strip()), ""
    ), axis=1
)

print("✅ Q1: Route classification completed (Dictionary replaced INDEX-MATCH-MATCH)")

# ==============================================
# STEP 4: SHIPPING FEE CALCULATION (Q2) — Custom function replaces IFS
# ==============================================
# In Excel, this was a nested IFS formula checking weight ranges × route types.
# In Python, we define a clean function with if-elif logic and apply it.

table3 = pd.read_excel(FILE_NAME, sheet_name="question_1", header=16, usecols="F:L", nrows=4)
table3.columns = ["weight_range", "Intra city", "Intra region", 
                  "Intra region tỉnh", "Cross region", "Cross region tỉnh", 
                  "Special same region"]
table3 = table3.set_index("weight_range")

def calculate_shipping_fee(row):
    """Calculate fee based on weight range × route type (replaces Excel IFS)"""
    weight_gram = row["weight_kg"] * 1000 if pd.notna(row["weight_kg"]) else 0
    route = row["route"]
    
    if weight_gram == 0 or route == "" or route not in table3.columns:
        return ""
    
    # Determine weight bracket
    if weight_gram <= 3000:     bracket = "0-3000 gr"
    elif weight_gram <= 6000:   bracket = "3001 - 6000 gr"
    elif weight_gram <= 15000:  bracket = "6001- 15000 gr"
    else:                       bracket = ">15000 gr"
    
    return table3.loc[bracket, route]

raw["estimated_shipping_fee"] = raw.apply(calculate_shipping_fee, axis=1)
print("✅ Q2: Shipping fee calculation completed")

# ==============================================
# STEPS 5-8: SLA, LEADTIME, ONTIME CHECK, ANALYTICS
# ==============================================
# The remaining steps follow the same pattern:
#   - Step 5: SLA lookup via pd.merge + date decoding with pd.to_datetime(origin="1899-12-30")
#   - Step 6: Leadtime calculation using np.where() (replaces Excel IF)
#   - Step 7: Ontime/Late evaluation with .normalize() for date-only comparison
#   - Step 8: Analytics via df.groupby() (replaces Pivot Tables) + matplotlib charts
#
# Key technique discovered: Excel stores dates as serial numbers (e.g., 44082.42).
# Python needs: pd.to_datetime(value, origin="1899-12-30", unit="D") to decode them.
#
# Full implementation handles all edge cases including:
#   - Missing weight values (NaN instead of Excel's silent 0)
#   - Trailing spaces in city names (.strip() before merge)
#   - Dropoff vs pickup shipment type differentiation
#
# 📧 Full source code available upon request.

print("\n" + "=" * 50)
print("Demo pipeline completed successfully!")
print(f"Total rows processed: {len(raw):,}")
print(f"Unique routes found: {raw['route'][raw['route'] != ''].nunique()}")
print(f"Unique 3PL carriers: {raw['3pl_name'].nunique()}")
print("=" * 50)
