# Retail Sales & Customer Insights

## 1. Project Overview

This project develops a retail sales and customer insights system using Python, MySQL and Power BI.

The project integrates customer, product and sales data, performs data cleaning and transformation, creates a star-schema data warehouse, and develops an interactive dashboard for business analysis.

## 2. Objectives

* Extract customer, product and sales data.
* Clean and transform the source datasets.
* Create a star-schema data warehouse.
* Load transformed data into MySQL.
* Analyse sales using SQL.
* Develop a Power BI dashboard.
* Identify product, customer and regional sales insights.

## 3. Technologies Used

* Python
* Pandas
* MySQL
* MySQL Workbench
* Power BI Desktop
* Git and GitHub

## 4. Project Structure

```text
Retail_Sales_Project/
│
├── retail_etl.py
├── customers.json
├── products.csv
├── sales 1.csv
├── database.sql
├── README.md
└── .gitignore
```

## 5. Data Processing

The Python ETL script performs the following tasks:

1. Extracts data from CSV and JSON files.
2. Cleans missing and duplicate records.
3. Standardizes gender and region values.
4. Creates customer segments.
5. Prepares data for the MySQL data warehouse.

## 6. Data Warehouse

The data warehouse follows a star-schema design.

### Fact Table

* fact_sales

### Dimension Tables

* dim_customer
* dim_product
* dim_region
* dim_date

## 7. SQL Analysis

The project analyses:

* Total sales revenue
* Top-selling products
* Sales by category
* Sales by region
* Customer purchasing behaviour
* Monthly sales trends

## 8. Power BI Dashboard

The dashboard includes:

* Total Sales
* Total Quantity
* Total Transactions
* Average Transaction Value
* Top Selling Products
* Sales by Category
* Monthly Sales Trend
* Regional Sales Performance
* Customer Segmentation

## 9. How to Run

### Install Python packages

```bash
pip install pandas mysql-connector-python
```

### Run the ETL script

```bash
python retail_etl.py
```

### Database

Execute `database.sql` in MySQL Workbench.

### Dashboard

Connect the `retail_dw` database to Power BI using the configured MySQL ODBC connection.

## 10. Conclusion

The project transforms raw retail data into a structured data warehouse and interactive reporting dashboard. It demonstrates data extraction, cleaning, ETL, SQL analysis and business intelligence visualization.

## 11. Author

Abithakaveri
