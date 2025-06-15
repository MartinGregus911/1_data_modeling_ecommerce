-- Drop existing tables if they exist
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_category;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_region;
DROP TABLE IF EXISTS dim_time;

-- Create dim_category table
CREATE TABLE dim_category AS
SELECT DISTINCT
    category_id,
    name,
    parent_category_id
FROM staging_categories;

-- Create dim_product table
CREATE TABLE dim_product AS
SELECT DISTINCT
    product_id,
    name,
    category_id
FROM staging_products;

-- Create dim_region table
-- SQLite does not support ROW_NUMBER(), so create without region_id for now
CREATE TABLE dim_region AS
SELECT DISTINCT
    city,
    region,
    country
FROM staging_customers;

-- To add region_id as PRIMARY KEY AUTOINCREMENT later, you can do:
-- CREATE TABLE dim_region_new (
--   region_id INTEGER PRIMARY KEY AUTOINCREMENT,
--   city TEXT,
--   region TEXT,
--   country TEXT
-- );
-- INSERT INTO dim_region_new(city, region, country) SELECT DISTINCT city, region, country FROM staging_customers;
-- DROP TABLE dim_region;
-- ALTER TABLE dim_region_new RENAME TO dim_region;

-- Create dim_customer table, joining on city, region, country to get region_id
CREATE TABLE dim_customer AS
SELECT DISTINCT
    c.customer_id,
    c.full_name,
    c.email,
    r.city,
    r.region,
    r.country
FROM staging_customers c
JOIN dim_region r ON c.city = r.city AND c.region = r.region AND c.country = r.country;

-- Create dim_time table
CREATE TABLE dim_time AS
SELECT DISTINCT
    order_date AS date_id,
    CAST(strftime('%Y', order_date) AS INTEGER) AS year,
    CAST(strftime('%m', order_date) AS INTEGER) AS month,
    CAST(strftime('%d', order_date) AS INTEGER) AS day,
    CAST((strftime('%m', order_date) + 2) / 3 AS INTEGER) AS quarter,
    CAST(strftime('%w', order_date) AS INTEGER) AS weekday
FROM staging_orders;

-- Create fact_sales table
CREATE TABLE fact_sales AS
SELECT
    oi.order_id,
    o.customer_id,
    oi.product_id,
    o.order_date AS date_id,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) AS total_price
FROM staging_order_items oi
JOIN staging_orders o ON oi.order_id = o.order_id;
