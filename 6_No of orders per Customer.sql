-- Number of orders per customer

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