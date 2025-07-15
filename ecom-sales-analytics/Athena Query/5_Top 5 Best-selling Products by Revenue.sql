-- Top 5 best-selling products by revenue

SELECT 
    p.name AS product_name,
    ROUND(SUM(s.quantity * p.price), 2) AS total_revenue
FROM sales s
JOIN products p 
  ON s.product_id = p.product_id
GROUP BY p.name
ORDER BY total_revenue DESC
LIMIT 5;