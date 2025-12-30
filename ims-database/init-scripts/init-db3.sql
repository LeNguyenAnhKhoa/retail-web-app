-- Views for new schema

-- Product view with category and created_by info
CREATE OR REPLACE VIEW product_summary_view AS
SELECT 
    p.product_id,
    p.code,
    p.name AS product_name,
    p.category_id,
    c.name AS category_name,
    p.unit,
    p.import_price,
    p.selling_price,
    p.stock_quantity,
    p.image_url,
    p.is_active,
    p.description,
    p.created_by,
    u.full_name AS created_by_name,
    u.role AS created_by_role,
    p.supplier_id,
    s.name AS supplier_name,
    p.created_at,
    p.updated_at
FROM 
    products p
    INNER JOIN categories c ON p.category_id = c.category_id
    INNER JOIN users u ON p.created_by = u.user_id
    LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id;

-- Supplier view
CREATE OR REPLACE VIEW supplier_summary_view AS
SELECT 
    s.supplier_id,
    s.name AS supplier_name,
    s.contact_name,
    s.phone,
    s.address,
    s.email,
    COUNT(p.product_id) AS total_products,
    COALESCE(SUM(p.stock_quantity), 0) AS total_product_quantity,
    COALESCE(AVG(p.selling_price), 0) AS avg_product_price,
    s.created_at,
    s.updated_at
FROM 
    suppliers s
    LEFT JOIN products p ON s.supplier_id = p.supplier_id AND p.is_active = TRUE
GROUP BY 
    s.supplier_id, s.name, s.contact_name, s.phone, s.address, s.email, s.created_at, s.updated_at;

-- Customer view with purchase history
CREATE OR REPLACE VIEW customer_summary_view AS
SELECT 
    c.customer_id,
    c.name AS customer_name,
    c.phone,
    c.address,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COALESCE(SUM(o.total_amount), 0) AS total_spent,
    MAX(o.created_at) AS last_purchase,
    c.created_at,
    c.updated_at
FROM 
    customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY 
    c.customer_id, c.name, c.phone, c.address, c.created_at, c.updated_at;

-- Order view with details
CREATE OR REPLACE VIEW order_summary_view AS
SELECT 
    o.order_id,
    o.code AS order_code,
    o.customer_id,
    c.name AS customer_name,
    c.phone AS customer_phone,
    o.user_id,
    u.full_name AS staff_name,
    u.role AS staff_role,
    o.total_amount,
    o.payment_method,
    o.status,
    COUNT(DISTINCT od.id) AS total_items,
    SUM(od.quantity) AS total_quantity,
    SUM(od.quantity * (od.unit_price - od.cost_price)) AS total_profit,
    o.created_at,
    o.updated_at
FROM 
    orders o
    LEFT JOIN customers c ON o.customer_id = c.customer_id
    INNER JOIN users u ON o.user_id = u.user_id
    LEFT JOIN order_details od ON o.order_id = od.order_id
GROUP BY 
    o.order_id, o.code, o.customer_id, c.name, c.phone, 
    o.user_id, u.full_name, u.role, o.total_amount, o.payment_method, 
    o.status, o.created_at, o.updated_at;

-- Sales report view (for revenue and profit)
CREATE OR REPLACE VIEW sales_report_view AS
SELECT 
    DATE(o.created_at) AS sale_date,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_revenue,
    SUM(od.quantity * od.cost_price) AS total_cost,
    SUM(od.quantity * (od.unit_price - od.cost_price)) AS total_profit,
    AVG(o.total_amount) AS avg_order_value
FROM 
    orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
WHERE 
    o.status = 'COMPLETED'
GROUP BY 
    DATE(o.created_at);

-- Order detail view (for order detail page)
CREATE OR REPLACE VIEW order_detail_summary AS
SELECT
    o.order_id,
    o.created_at AS order_date,
    o.status AS order_status,
    c.customer_id,
    c.name AS customer_name,
    '' AS customer_email,
    c.phone AS customer_phone,
    od.id AS order_item_id,
    p.product_id,
    p.name AS product_name,
    od.unit_price AS product_price,
    od.quantity AS quantity_ordered,
    (od.quantity * od.unit_price) AS total_price,
    o.created_at AS order_created_time,
    o.updated_at AS order_updated_time
FROM
    orders o
    LEFT JOIN customers c ON o.customer_id = c.customer_id
    INNER JOIN order_details od ON o.order_id = od.order_id
    INNER JOIN products p ON od.product_id = p.product_id;

-- Best selling products view
CREATE OR REPLACE VIEW best_selling_products_view AS
SELECT 
    p.product_id,
    p.code,
    p.name AS product_name,
    c.name AS category_name,
    COUNT(DISTINCT od.order_id) AS times_ordered,
    SUM(od.quantity) AS total_quantity_sold,
    SUM(od.quantity * od.unit_price) AS total_revenue,
    SUM(od.quantity * (od.unit_price - od.cost_price)) AS total_profit,
    AVG(od.unit_price) AS avg_selling_price
FROM 
    products p
    INNER JOIN categories c ON p.category_id = c.category_id
    INNER JOIN order_details od ON p.product_id = od.product_id
    INNER JOIN orders o ON od.order_id = o.order_id
WHERE 
    o.status = 'COMPLETED'
GROUP BY 
    p.product_id, p.code, p.name, c.name
ORDER BY 
    total_quantity_sold DESC;
