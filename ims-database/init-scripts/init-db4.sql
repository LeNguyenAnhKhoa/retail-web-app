-- Indexes for new schema

-- Users indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_active ON users(is_active);

-- Products indexes
CREATE INDEX idx_products_code ON products(code);
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_created_by ON products(created_by);
CREATE INDEX idx_products_is_active ON products(is_active);

-- Orders indexes
CREATE INDEX idx_orders_code ON orders(code);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_orders_payment_method ON orders(payment_method);

-- Order details indexes
CREATE INDEX idx_order_details_order ON order_details(order_id);
CREATE INDEX idx_order_details_product ON order_details(product_id);

-- Customers indexes
CREATE INDEX idx_customers_phone ON customers(phone);
CREATE INDEX idx_customers_name ON customers(name);

-- Suppliers indexes
CREATE INDEX idx_suppliers_name ON suppliers(name);
CREATE INDEX idx_suppliers_phone ON suppliers(phone);

-- Categories indexes
CREATE INDEX idx_categories_name ON categories(name);

-- Stored Procedures

-- Procedure: Create Order with Details
DELIMITER $$

CREATE PROCEDURE CreateOrderWithDetails(
    IN p_order_code VARCHAR(50),
    IN p_customer_id INT,
    IN p_user_id INT,
    IN p_payment_method ENUM('CASH', 'TRANSFER', 'CARD'),
    IN p_product_ids TEXT,      -- comma-separated: '1,2,3'
    IN p_quantities TEXT,        -- comma-separated: '2,1,5'
    IN p_unit_prices TEXT,       -- comma-separated: '10.00,20.00,5.50'
    IN p_cost_prices TEXT,       -- comma-separated: '8.00,15.00,4.00'
    IN p_receives TEXT,          -- comma-separated: '10.00,20.00,5.50'
    IN p_give_backs TEXT         -- comma-separated: '0.00,0.00,0.00'
)
BEGIN
    DECLARE v_order_id INT;
    DECLARE v_total_amount DECIMAL(10,2) DEFAULT 0;
    DECLARE i INT DEFAULT 1;
    DECLARE n INT;
    DECLARE v_product_id INT;
    DECLARE v_quantity INT;
    DECLARE v_unit_price DECIMAL(10,2);
    DECLARE v_cost_price DECIMAL(10,2);
    DECLARE v_receive DECIMAL(10,2);
    DECLARE v_give_back DECIMAL(10,2);
    DECLARE v_line_total DECIMAL(10,2);
    DECLARE v_stock INT;
    
    -- Start transaction
    START TRANSACTION;
    
    -- Count number of items
    SET n = (LENGTH(p_product_ids) - LENGTH(REPLACE(p_product_ids, ',', '')) + 1);
    
    -- Calculate total amount and validate stock
    WHILE i <= n DO
        SET v_product_id = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_product_ids, ',', i), ',', -1) AS UNSIGNED);
        SET v_quantity = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_quantities, ',', i), ',', -1) AS UNSIGNED);
        SET v_unit_price = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_unit_prices, ',', i), ',', -1) AS DECIMAL(10,2));
        
        -- Check stock
        SELECT stock_quantity INTO v_stock FROM products WHERE product_id = v_product_id;
        IF v_stock < v_quantity THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient stock';
        END IF;
        
        SET v_line_total = v_quantity * v_unit_price;
        SET v_total_amount = v_total_amount + v_line_total;
        SET i = i + 1;
    END WHILE;
    
    -- Insert order
    INSERT INTO orders (code, customer_id, user_id, total_amount, payment_method, status)
    VALUES (p_order_code, p_customer_id, p_user_id, v_total_amount, p_payment_method, 'COMPLETED');
    
    SET v_order_id = LAST_INSERT_ID();
    
    -- Insert order details and update stock
    SET i = 1;
    WHILE i <= n DO
        SET v_product_id = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_product_ids, ',', i), ',', -1) AS UNSIGNED);
        SET v_quantity = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_quantities, ',', i), ',', -1) AS UNSIGNED);
        SET v_unit_price = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_unit_prices, ',', i), ',', -1) AS DECIMAL(10,2));
        SET v_cost_price = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_cost_prices, ',', i), ',', -1) AS DECIMAL(10,2));
        SET v_receive = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_receives, ',', i), ',', -1) AS DECIMAL(10,2));
        SET v_give_back = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(p_give_backs, ',', i), ',', -1) AS DECIMAL(10,2));
        
        -- Insert order detail
        INSERT INTO order_details (order_id, product_id, quantity, unit_price, cost_price, receive, give_back)
        VALUES (v_order_id, v_product_id, v_quantity, v_unit_price, v_cost_price, v_receive, v_give_back);
        
        -- Update product stock
        UPDATE products SET stock_quantity = stock_quantity - v_quantity WHERE product_id = v_product_id;
        
        SET i = i + 1;
    END WHILE;
    
    COMMIT;
    SELECT v_order_id AS order_id, v_total_amount AS total_amount;
END$$

DELIMITER ;

-- Function: Calculate Revenue by Date Range
DELIMITER $$

CREATE FUNCTION GetRevenueByDateRange(
    p_start_date DATE,
    p_end_date DATE
)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_revenue DECIMAL(10,2);
    
    SELECT COALESCE(SUM(total_amount), 0) INTO v_revenue
    FROM orders
    WHERE status = 'COMPLETED'
        AND DATE(created_at) BETWEEN p_start_date AND p_end_date;
    
    RETURN v_revenue;
END$$

DELIMITER ;

-- Function: Calculate Profit by Date Range
DELIMITER $$

CREATE FUNCTION GetProfitByDateRange(
    p_start_date DATE,
    p_end_date DATE
)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_profit DECIMAL(10,2);
    
    SELECT COALESCE(SUM(od.quantity * (od.unit_price - od.cost_price)), 0) INTO v_profit
    FROM orders o
    INNER JOIN order_details od ON o.order_id = od.order_id
    WHERE o.status = 'COMPLETED'
        AND DATE(o.created_at) BETWEEN p_start_date AND p_end_date;
    
    RETURN v_profit;
END$$

DELIMITER ;
