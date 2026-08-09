# Layer 1: Data Analysis with Excel

This document explains in detail the approach to solving the delivery data processing and analysis problem using Microsoft Excel.

## Detailed Explanation of Questions (Q1-Q4)

### Question 1 (Q1): Determining Area and Route
*   **Objective:** Determine `seller_area`, `buyer_area`, and `Route`.
*   **Method:**
    *   **Area:** Use a combination of `INDEX` and `MATCH` (or `VLOOKUP`) functions to look up `seller_area` and `buyer_area` information from Table 1 (containing 714 records of cities/provinces). By matching `seller_city` and `buyer_city` with the reference table, we obtain the corresponding area (e.g., North, South, HCM, HN).
    *   **Route:** Once the seller and buyer areas are available, use the Route lookup matrix (Table 2) to determine the route type (e.g., Intra city, Cross region). The formula here is typically `INDEX` combined with two `MATCH` functions to find the exact intersection between the row (seller_area) and column (buyer_area) in the matrix.

### Question 2 (Q2): Calculating Estimated Shipping Fee and SLA
*   **Estimated Shipping Fee (`estimated_shipping_fee`):** Use the `IFS` function (or nested `IF` functions) to calculate the fee based on conditions regarding weight ranges and route types provided in Table 3.
*   **Service Level Agreement (SLA):** Use the `VLOOKUP` (or `INDEX-MATCH`) function to find the SLA value from Table 4 (containing 3969 state-pair route records). The SLA varies depending on whether the delivery is to an Urban or Rural area; therefore, the formula must combine route information and destination characteristics to retrieve the correct number of SLA days.

### Question 3 (Q3): Evaluating Delivery and Pickup Time
*   **Calculate Delivery Leadtime (`leadtime_delivery`):** The formula is `delivery_done - pickup_done` (in days).
*   **Evaluate Ontime Delivery (Ontime/Late):** Compare `leadtime_delivery` with `SLA`. If `leadtime_delivery <= SLA`, the order is evaluated as "Ontime", otherwise "Late".
*   **Evaluate Pickup (Pickup Check):** Compare the actual pickup date (`pickup_done`) with the scheduled pickup date (`schedule_date_to_pickup`).

### Question 4 (Q4): Visualization and Reporting
*   Build **Pivot Tables** to calculate and display:
    *   Average Leadtime for each third-party logistics partner (3PL).
    *   Average Fee by route type for each 3PL.
    *   Percentage of Late Delivery to evaluate the performance of 3PLs.

## Limitations of the Excel Approach
During the implementation in Excel, several limitations were discovered:
*   **Incomplete Analysis:** Initially, data analysis was only performed for Shipping Carrier A, omitting carriers B, C, D, and E due to large data size or flawed data filtering.
*   **Date Format Issues:** Excel struggled to interpret and synchronize date formats, leading to errors when calculating `leadtime_delivery` (#VALUE! error or incorrect day count).
*   **Missing Data Handling:** There is no mechanism to automatically handle blanks or `#N/A` errors well during lookups. Excel sometimes treats blank cells as 0, which distorts cost and time calculations.
*   **Data Quality:** When cross-referencing with Python results later, multiple issues were found with trailing spaces in text data, which caused `VLOOKUP/MATCH` functions in Excel to fail to find matches, resulting in silent data loss that is difficult to detect.
