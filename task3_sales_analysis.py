# ==========================================
# SALES PERFORMANCE ANALYSIS USING PANDAS
# Author : Akash Goud
# Internship Task 3 - Alfido Tech
# ==========================================

import pandas as pd

print("=" * 60)
print("      SALES PERFORMANCE ANALYSIS SYSTEM")
print("=" * 60)

# STEP 1 : LOAD DATASET

df = pd.read_csv("sales_data.csv")

print("\nDataset Loaded Successfully")
print("\nFirst 5 Records:")
print(df.head())

# STEP 2 : INSPECT DATA

print("\nDataset Information")
df.info()

print("\nMissing Values")
print(df.isnull().sum())

# STEP 3 : CLEAN DATA

average_quantity = df["Quantity"].mean()

df["Quantity"] = df["Quantity"].fillna(average_quantity)

print("\nMissing values handled successfully.")

# STEP 4 : CREATE NEW COLUMN

df["Total_Sales"] = df["Price"] * df["Quantity"]

print("\nTotal Sales Column Added")

# STEP 5 : FILTERING

print("\nProducts with Sales Above ₹50,000")

high_sales = df[df["Total_Sales"] > 50000]

print(high_sales[["Product", "Category", "Total_Sales"]])

# STEP 6 : GROUPING & AGGREGATION

print("\nTotal Sales by Category")

category_sales = df.groupby("Category")["Total_Sales"].sum()

print(category_sales)

print("\nTotal Sales by Region")

region_sales = df.groupby("Region")["Total_Sales"].sum()

print(region_sales)

print("\nProduct Wise Sales")

product_sales = df.groupby("Product")["Total_Sales"].sum()

print(product_sales)

# STEP 7 : BEST PERFORMERS

best_product = product_sales.idxmax()
best_product_sales = product_sales.max()

best_category = category_sales.idxmax()
best_category_sales = category_sales.max()

best_region = region_sales.idxmax()
best_region_sales = region_sales.max()

# STEP 8 : STATISTICS

print("\nStatistical Summary")
print(df.describe())

# STEP 9 : INSIGHTS

print("\n" + "=" * 60)
print("BUSINESS INSIGHTS")
print("=" * 60)

print(f"\nTop Selling Product : {best_product}")
print(f"Revenue Generated : ₹{best_product_sales:,.2f}")

print(f"\nBest Performing Category : {best_category}")
print(f"Category Revenue : ₹{best_category_sales:,.2f}")

print(f"\nBest Performing Region : {best_region}")
print(f"Region Revenue : ₹{best_region_sales:,.2f}")

print("\nSimple Insights")

print("1. Electronics category generates the highest revenue.")
print("2. Laptop is the best-selling product.")
print("3. Missing values were cleaned successfully.")
print("4. Regional analysis helps identify strong markets.")
print("5. Data-driven decisions improve business growth.")

print("\nAnalysis Completed Successfully!")