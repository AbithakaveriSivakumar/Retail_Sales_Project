import pandas as pd
import json
import mysql.connector

# -----------------------------
# 1. LOAD DATA
# -----------------------------

sales = pd.read_csv("sales 1.csv")
products = pd.read_csv("products.csv")

with open("customers.json", "r") as file:
    customers = pd.DataFrame(json.load(file))

print("Data Loaded Successfully")

print("Sales:", sales.shape)
print("Products:", products.shape)
print("Customers:", customers.shape)


# -----------------------------
# 2. BASIC CLEANING
# -----------------------------

# Sales
sales["Timestamp"] = pd.to_datetime(
    sales["Timestamp"], errors="coerce"
)

sales["SalesAmount"] = pd.to_numeric(
    sales["SalesAmount"], errors="coerce"
)

sales["Quantity"] = pd.to_numeric(
    sales["Quantity"], errors="coerce"
)

# Remove incomplete sales transactions
sales = sales.dropna(
    subset=["SaleID", "ProductID", "CustomerID",
            "SalesAmount", "Quantity", "Timestamp"]
)

# Remove duplicate sales
sales = sales.drop_duplicates(subset=["SaleID"])


# -----------------------------
# 3. CUSTOMER CLEANING
# -----------------------------

customers = customers.drop_duplicates(
    subset=["CustomerID"]
)

# Standardize gender
customers["Gender"] = (
    customers["Gender"]
    .str.strip()
    .str.lower()
    .replace({
        "m": "Male",
        "male": "Male",
        "f": "Female",
        "female": "Female"
    })
)

# Standardize regions
region_map = {
    "ny": "New York",
    "new york": "New York",
    "new yorkk": "New York",
    "nw york": "New York",

    "california": "California",
    "californiya": "California",

    "texas": "Texas",
    "texaz": "Texas",

    "ohio": "Ohio",
    "ohho": "Ohio"
}

customers["Region"] = (
    customers["Region"]
    .str.strip()
    .str.lower()
    .map(region_map)
    .fillna("Unknown")
)


# -----------------------------
# 4. PRODUCT CLEANING
# -----------------------------

products = products.drop_duplicates(
    subset=["ProductID"]
)

products["ProductName"] = products["ProductName"].str.strip()
products["Category"] = products["Category"].str.strip()


# -----------------------------
# 5. CUSTOMER SEGMENTATION
# -----------------------------

customer_sales = (
    sales.groupby("CustomerID")["SalesAmount"]
    .sum()
)

q1 = customer_sales.quantile(0.33)
q2 = customer_sales.quantile(0.66)

def segment(value):
    if value <= q1:
        return "Low"
    elif value <= q2:
        return "Medium"
    else:
        return "High"

customers["CustomerSegment"] = (
    customers["CustomerID"]
    .map(customer_sales)
    .fillna(0)
    .apply(segment)
)


# -----------------------------
# 6. REGION DIMENSION
# -----------------------------

regions = pd.DataFrame({
    "Region": sorted(customers["Region"].unique())
})

regions["RegionID"] = range(1, len(regions) + 1)


# Add RegionID to customers
customers = customers.merge(
    regions,
    on="Region",
    how="left"
)


# -----------------------------
# 7. ADD REGION TO SALES
# -----------------------------

sales = sales.merge(
    customers[["CustomerID", "RegionID"]],
    on="CustomerID",
    how="left"
)


# -----------------------------
# 8. DATE DIMENSION
# -----------------------------

dates = pd.DataFrame({
    "Date": pd.date_range(
        sales["Timestamp"].min().date(),
        sales["Timestamp"].max().date()
    )
})

dates["Year"] = dates["Date"].dt.year
dates["Month"] = dates["Date"].dt.month
dates["MonthName"] = dates["Date"].dt.strftime("%B")


# -----------------------------
# 9. DISPLAY CLEAN DATA
# -----------------------------

print("\nETL Cleaning Completed")

print("Clean Sales:", len(sales))
print("Clean Customers:", len(customers))
print("Products:", len(products))

print("\nSales Preview")
print(sales.head())

print("\nCustomer Preview")
print(customers.head())

print("\nProduct Preview")
print(products.head())




sales = sales.astype(object).where(
    pd.notna(sales), None
)

customers = customers.astype(object).where(
    pd.notna(customers), None
)

products = products.astype(object).where(
    pd.notna(products), None
)
# -----------------------------
# 10. CONNECT TO MYSQL
# -----------------------------

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="retail_dw"
)

cursor = conn.cursor()

print("\nConnected to MySQL")


# -----------------------------
# 11. LOAD REGION
# -----------------------------

region_data = [
    (int(row.RegionID), row.Region)
    for row in regions.itertuples()
]

cursor.executemany(
    """
    INSERT INTO dim_region
    (RegionID, Region)
    VALUES (%s, %s)
    """,
    region_data
)


# -----------------------------
# 12. LOAD PRODUCTS
# -----------------------------

product_data = [
    (int(row.ProductID),
     row.ProductName,
     row.Category)
    for row in products.itertuples()
]

cursor.executemany(
    """
    INSERT INTO dim_product
    (ProductID, ProductName, Category)
    VALUES (%s, %s, %s)
    """,
    product_data
)


# -----------------------------
# 13. LOAD CUSTOMERS
# -----------------------------

customer_data = [
    (
        row.CustomerID,
        row.FirstName,
        row.LastName,
        row.Gender,
        int(row.RegionID),
        row.CustomerSegment
    )
    for row in customers.itertuples()
]

cursor.executemany(
    """
    INSERT INTO dim_customer
    (CustomerID, FirstName, LastName,
     Gender, RegionID, CustomerSegment)
    VALUES (%s, %s, %s, %s, %s, %s)
    """,
    customer_data
)


# -----------------------------
# 14. LOAD DATES
# -----------------------------

date_data = [
    (
        row.Date.date(),
        int(row.Year),
        int(row.Month),
        row.MonthName
    )
    for row in dates.itertuples()
]

cursor.executemany(
    """
    INSERT INTO dim_date
    (Date, Year, Month, MonthName)
    VALUES (%s, %s, %s, %s)
    """,
    date_data
)


# -----------------------------
# 15. LOAD SALES
# -----------------------------

sales_data = [
    (
        row.SaleID,
        int(row.ProductID),
        row.CustomerID,
        int(row.RegionID),
        row.Timestamp.date(),
        float(row.SalesAmount),
        int(row.Quantity)
    )
    for row in sales.itertuples()
]

cursor.executemany(
    """
    INSERT INTO fact_sales
    (SaleID, ProductID, CustomerID,
     RegionID, SaleDate, SalesAmount, Quantity)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """,
    sales_data
)

conn.commit()

print("All data loaded successfully")

cursor.close()
conn.close()