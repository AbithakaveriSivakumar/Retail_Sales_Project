
CREATE DATABASE IF NOT EXISTS retail_dw;

USE retail_dw;

-- Dimension: Region
CREATE TABLE IF NOT EXISTS dim_region (
    RegionID INT PRIMARY KEY,
    Region VARCHAR(50)
);

-- Dimension: Product
CREATE TABLE IF NOT EXISTS dim_product (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(50)
);

-- Dimension: Customer
CREATE TABLE IF NOT EXISTS dim_customer (
    CustomerID VARCHAR(20) PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Gender VARCHAR(10),
    RegionID INT,
    CustomerSegment VARCHAR(20),
    FOREIGN KEY (RegionID)
        REFERENCES dim_region(RegionID)
);

-- Dimension: Date
CREATE TABLE IF NOT EXISTS dim_date (
    Date DATE PRIMARY KEY,
    Year INT,
    Month INT,
    MonthName VARCHAR(20)
);

-- Fact: Sales
CREATE TABLE IF NOT EXISTS fact_sales (
    SaleID VARCHAR(50) PRIMARY KEY,
    ProductID INT,
    CustomerID VARCHAR(20),
    RegionID INT,
    SaleDate DATE,
    SalesAmount DECIMAL(12,2),
    Quantity INT,

    FOREIGN KEY (ProductID)
        REFERENCES dim_product(ProductID),

    FOREIGN KEY (CustomerID)
        REFERENCES dim_customer(CustomerID),

    FOREIGN KEY (RegionID)
        REFERENCES dim_region(RegionID),

    FOREIGN KEY (SaleDate)
        REFERENCES dim_date(Date)
);