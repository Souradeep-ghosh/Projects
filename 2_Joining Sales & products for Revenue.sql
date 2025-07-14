--Join sales with products to get revenue per order

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