-- Total revenue per product category(Showing category with providing most revenue)

SELECT 
    p.category,
    ROUND(SUM(s.quantity * p.price), 2) AS total_revenue
FROM sales s
JOIN products p 
  ON s.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;