-- Monthly revenue trend

SELECT
    date_trunc('month', CAST(order_date AS DATE)) AS month,
    ROUND(SUM(s.quantity * p.price), 2) AS total_revenue
FROM sales s
JOIN products p
    ON s.product_id = p.product_id
GROUP BY date_trunc('month', CAST(order_date AS DATE))
ORDER BY date_trunc('month', CAST(order_date AS DATE));