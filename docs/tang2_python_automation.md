# Layer 2: Automation with Python / Pandas

This document details the process of transitioning and automating data analysis operations from Excel to Python using the Pandas library.

## Prerequisites
*   Python 3.x
*   pandas
*   numpy
*   openpyxl (for reading/writing Excel files)
*   matplotlib (for data visualization)

## Step-by-step Walkthrough of bai_tap_e13.py

### Step 1: Data Loading
Use the `pd.read_excel()` function to read the raw data (`raw_data`) and lookup tables. Pandas allows reading directly from different sheets in an Excel file easily and quickly.

### Step 2: Area Mapping (Q1)
Instead of using `INDEX-MATCH` as in Excel, we use the `pd.merge()` method to perform a "Left Join".
*   **Left Join Concept:** Keep all data in the primary table (left table - containing transactions), and only append columns from the reference table (right table - area table) based on common key columns like `seller_city` and `buyer_city`. Records without a reference match will have NaN (Not a Number) values instead of throwing an error.

### Step 3: Route Mapping
Use the Dictionary data structure in Python for lookups instead of querying a matrix (Route lookup matrix) by row/column intersection in Excel. The keys of the dictionary are tuples containing the pair `(seller_area, buyer_area)` and the values are the corresponding routes. Pandas uses the `apply` or `.map` function to map this dictionary onto the dataframe very efficiently.

### Step 4: Fee Calculation (Q2)
Instead of using complex and deeply nested `IFS` functions, Python allows defining a custom function containing the logic for dividing weight ranges and routes. Then, applying this function to the data rows makes the code readable, maintainable, and less prone to errors.

### Step 5: Calculating SLA & Delivery Time (Leadtime)
*   Use `pd.to_datetime()` to handle date columns. For date values in Excel's Serial numbers format, we need to add the parameter `origin='1899-12-30'` for Python to correctly decode the numbers into Datetime format.
*   Use `np.where()` to calculate the conditions that generate the `leadtime_delivery` column. `np.where(condition, value_if_true, value_if_false)` provides an extremely fast vectorized way to assign values without iterating through each row (for loop).

### Step 6: Ontime Check (Q3)
Use `.dt.normalize()` to convert Datetime data to Date-only format (comparing only the date part, removing the hour/minute/second part). This helps accurately compare the delivery completion date and SLA just like in Excel.

### Step 7: Analytics (Q4)
Use the `.groupby()` method to replace the Pivot Table feature in Excel. `.groupby()` combined with aggregation functions like `.mean()` and `.count()` helps calculate the Average Leadtime and late percentage concisely, quickly outputting a structured data table.

### Step 8: Visualization
Use the `matplotlib` library to plot charts (e.g., Bar chart) displaying the average fee and delivery time by each shipping partner.

## Key Differences vs Excel
*   **Vectorized operations vs cell-by-cell:** Pandas computes across entire columns simultaneously (vectorized), resulting in processing speeds many times faster than Excel (which calculates sequentially cell-by-cell). Processing over 96,000 rows takes only a few seconds instead of several minutes or freezing the machine like Excel.
*   **Proper NaN handling:** Pandas has dedicated methods like `.fillna()` or `.dropna()` to manage missing values explicitly. Excel often considers blank cells as 0, leading to severe statistical deviations.
*   **Text Data Cleaning:** The `.str.strip()` method in Pandas easily removes leading/trailing spaces, addressing the root cause of Excel's VLOOKUP function frequently returning `#N/A` errors (silent lookup failures).

## Data Quality Issues Discovered and Resolved
Thanks to Python, the analysis process brought to light:
*   Trailing spaces in city and province name data that caused area mapping to be misaligned.
*   Missing data for certain shipping units that was not fully reflected in Layer 1.
*   Inconsistencies in the Datetime format of the source file, which were automatically standardized.

## Output Files Description
*   **bai_tap_e13.py:** The main source code script executing the entire logic.
*   **ket_qua_bai_tap_e13.csv / _utf8.csv:** The complete data after labeling, cleaning, and calculating fees and leadtime (note the large size, can be ignored in Git).
*   **Bieu_do_Q4_Python.png:** A chart showing the comparison results among the 3PLs.
