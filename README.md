# 🛒 E-Commerce Sales Analytics Project using AWS (Free Tier)

## 🌟 Project Overview

This project demonstrates a complete data analytics pipeline built entirely using **AWS Free Tier services**. The objective is to simulate a real-world e-commerce company and analyze its sales performance, customer behavior, and product insights using cloud-native tools.

It covers every step from **data generation**, **data storage**, **metadata management**, **SQL querying**, to **dashboard creation** and **GitHub publishing**. This project showcases practical data analytics skills and decision-making workflows.

---

## 📊 Problem Statement

To analyze sales performance and customer behavior for a fictional e-commerce company. We aim to uncover:

* Which products generate the most revenue?
* What are the monthly sales trends?
* Who are the top customers?
* How do different product categories perform?

---

## 💡 Tools & Technologies Used

| Tool                  | Purpose                                        |
| --------------------- | ---------------------------------------------- |
| **Python**            | Generate realistic e-commerce data             |
| **Amazon S3**         | Store raw CSV files                            |
| **AWS Glue**          | Catalog tables (both manually and via crawler) |
| **Amazon Athena**     | Query data using SQL                           |
| **Amazon QuickSight** | Create interactive dashboards                  |
| **GitHub**            | Document and host portfolio                    |

---

## 📁 Project Structure

```
ecom-sales-analytics/
├── data/             # Raw CSVs (customers, products, sales)
├── scripts/          # Python script to generate data
├── sql/              # Athena SQL query files
├── screenshots/      # Exported visuals from QuickSight
├── README.md         # Project documentation (this file)
```

---

## 🔄 End-to-End Steps (Detailed with Real Problems Faced)

### ✅ STEP 1: Simulate Dataset using Python

* Used **Faker** library to create customer, product, and transaction data.
* Wrote a script in `generate_data.py` to generate three CSV files:

  * `customers_customers.csv`
  * `products.csv`
  * `sales.csv`
* Saved them in the `data/` folder.

> **Issue faced:** Had to fix path errors while using `mkdir` on PowerShell. Fixed it by creating folders manually and ensuring proper navigation.

---

### ✅ STEP 2: Upload Data to Amazon S3

* Created an S3 bucket: `ecom-analytics-soura`
* Folder structure created:

```
raw/
  customers_customers/
  products/
  sales/
```

* Uploaded the respective CSV files to each folder.

> **Tip:** Folder structure in S3 should mirror how your Glue and Athena will expect it.

---

### ✅ STEP 3: Catalog Tables using AWS Glue

**Approach 1: Manual Schema Definition (Preferred)**

* Created Glue database: `ecom_db`
* Manually added tables for `sales`, `products`, and `customers_customers`
* Specified schema for each table manually (e.g., `product_id` as int, `order_date` as string)

> **Issue faced:** Athena threw `HIVE_BAD_DATA` error due to incorrect schema type (date column set as int). Fixed it by setting `order_date` as `string` and casting it in queries.

> **Another Issue:** Header rows caused type mismatch errors. Fixed it by adding `skip.header.line.count = 1` in table properties.

---

### ✅ STEP 4: Query in Amazon Athena

* Used SQL to perform analytical queries:

  * Revenue by product category
  * Monthly sales trends
  * Top 10 customers by spending
  * Orders per customer

* Example query:
--Preview the sales table:
```sql

SELECT * FROM sales LIMIT 10;
```
--Join sales with products to get revenue per order
```sql

SELECT 
    s.transaction_id,
    s.quantity,
    p.name AS product_name,
    p.category,
    p.price,
    (s.quantity * p.price) AS revenue
FROM sales s
JOIN products p 
  ON s.product_id = p.product_id
LIMIT 10;
```
-- Total revenue per product category(Showing category with providing most revenue)
```sql

SELECT 
    p.category,
    ROUND(SUM(s.quantity * p.price), 2) AS total_revenue
FROM sales s
JOIN products p 
  ON s.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
```
-- Monthly revenue trend
```sql

SELECT
    date_trunc('month', CAST(order_date AS DATE)) AS month,
    ROUND(SUM(s.quantity * p.price), 2) AS total_revenue
FROM sales s
JOIN products p
    ON s.product_id = p.product_id
GROUP BY date_trunc('month', CAST(order_date AS DATE))
ORDER BY date_trunc('month', CAST(order_date AS DATE));
```
-- Top 5 best-selling products by revenue
```sql

SELECT 
    p.name AS product_name,
    ROUND(SUM(s.quantity * p.price), 2) AS total_revenue
FROM sales s
JOIN products p 
  ON s.product_id = p.product_id
GROUP BY p.name
ORDER BY total_revenue DESC
LIMIT 5;
```
-- Number of orders per customer

```sql
SELECT 
    c.customer_id,
    c.name,
    COUNT(s.transaction_id) AS total_orders
FROM sales s
JOIN customers_customers c 
  ON s.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_orders DESC
LIMIT 10;
```

> **Issue faced:** Athena doesn't allow using alias in GROUP BY → repeated expressions.

> **Another Issue:** Table not found error due to missing `customers_customers` table. Fixed by manually re-creating it in Glue.

---

### ✅ STEP 5: Creating Dashboard in QuickSight

* Enabled QuickSight Standard Edition with **QuickSight-managed roles** and **IAM Federation (SSO)**
* Connected QuickSight to Athena data source
* Imported all three tables: `sales`, `products`, `customers_customers`

**Joined tables visually**:

* `sales.product_id` = `products.product_id`
* `sales.customer_id` = `customers_customers.customer_id`

> **Issue faced:** QuickSight auto-joined `products` and `customers_customers` incorrectly. Deleted unwanted join manually.

---

### ✅ STEP 6: Built Visuals Using AWS QuickSight

Built the following visuals inside QuickSight:

#### 📅 Line Chart: Monthly Revenue Trend

* X-axis: `order_date` (parsed to date)
* Y-axis: calculated field `revenue = quantity * price`
* Aggregated by: **Month**

🖼️ [View Chart]

(https://github.com/user-attachments/assets/f14aa3f4-b074-456b-9eb6-b1124f2ba110)

#### 📊 Bar Chart: Revenue by Product

* X-axis: `product_name`
* Y-axis: `revenue`
* Sorted descending to show best performers

🖼️ [View Chart]

(https://github.com/user-attachments/assets/3e594fad-2be6-4a87-80ce-7af474e4084f)

#### 🥧 Pie Chart: Sales Distribution

* Group: `category`
* Value: `revenue`

🖼️ [View Chart]

(https://github.com/user-attachments/assets/512c785d-8626-4462-aee6-63f7851b22ce)

#### 👤 Table: Top 10 Customers

* Fields: `customer_id`, `name`, `email`, `revenue`
* Filter: Top 10 by total revenue

🖼️ [View Table]

(https://github.com/user-attachments/assets/b6071d25-9df4-417e-8f0e-8009f90b5e5c)

> **Issue faced:** Had to create a `revenue` calculated field manually and apply filters using QuickSight Top N functionality.

> **Another Issue faced:** While creating a 'Line Chart' of order_date from sales table, order_date was still a string. While dragging order_date on the x axis, I wasn't able to aggregate it by month.
Then, I added a ' Calculated field' and named it as order_date_parsed and written a formula-
                              parseDate({order_date}, 'yyyy-MM-dd')
Then I added this new field to x axis and from the dropdown, I have aggregated the chart by month. 
---

## 📸 STEP 7: Export Visuals for GitHub

* Took screenshots of all visuals
* Saved in `/screenshots` folder
* Filenames used:

  * `monthly_revenue_trend.png`
  * `top_10_customers.png`
  * `revenue_by_product.png`
  * `sales_distribution_pie.png`

---

## 📝 STEP 8: Save Queries and Upload to GitHub

* Saved all Athena queries in `.sql` files inside `/sql` folder
* Wrote this `README1.md` to document the journey step-by-step
* Uploaded everything to [GitHub Repo](https://github.com/yourusername/ecom-sales-analytics)

---

## 📈 Key Insights

* ₹ Revenue trends clearly highlight seasonal spikes
* Top 10 products account for over 60% of total revenue
* 20% of customers contribute to \~80% of sales (Pareto pattern)

---

## 💼 Resume-Worthy Highlights

* Built and hosted a complete analytics project using AWS cloud
* Used SQL, Athena, and QuickSight to generate business-ready insights
* Handled real-world troubleshooting (schema errors, data type issues, joining problems)
* Demonstrated full-stack analytics skills: ETL → SQL → BI → GitHub

---

## 🚀 How to Run This Project Yourself

1. Clone the GitHub repo
2. Create an AWS Free Tier account
3. Upload data to your S3 bucket
4. Manually catalog tables using Glue
5. Query data in Athena
6. Visualize insights in QuickSight

---

## 📢 About Me

**Souradeep-ghosh** – Data Analyst | SQL | AWS | Python | BI Tools
[LinkedIn](https://www.linkedin.com/in/souradeep-ghosh-165802150/) | [GitHub](https://github.com/Souradeep-ghosh)

> Made with curiosity, cloud, and caffeine. ☕
