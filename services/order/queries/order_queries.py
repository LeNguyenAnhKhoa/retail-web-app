class OrderQueries:
    GET_ALL_ORDERS = """
        SELECT v.*, u.username, (SELECT COALESCE(SUM(receive), 0) FROM order_details WHERE order_id = v.order_id) as total_receive
        FROM order_summary_view v
        JOIN users u ON v.user_id = u.user_id
        ORDER BY v.created_at DESC, v.order_id ASC;
    """

    GET_ORDER_DETAIL = """
        SELECT * FROM order_detail_summary
        WHERE order_id = %s
        ORDER BY order_updated_time DESC, order_id ASC;
    """

    # Use stored procedure to create order
    CREATE_ORDER_PROCEDURE = """
        CALL CreateOrderWithDetails(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    # Update product quantity using stored procedure
    UPDATE_PRODUCT_QUANTITY_PROCEDURE = """
        CALL UpdateProductQuantity(%s, %s);
    """

    # Get last inserted order ID after procedure call
    GET_LAST_ORDER_ID = """
        SELECT LAST_INSERT_ID() as order_id;
    """

    GET_ORDER = """
        SELECT order_id, customer_id, status, order_date, created_time, updated_time
        FROM orders
        WHERE order_id = %s;
    """

    # Legacy queries (kept for compatibility)
    CREATE_ORDER = """
        INSERT INTO orders (customer_id, status)
        VALUES (%s, %s);
    """

    CREATE_ORDER_ITEM = """
        INSERT INTO order_items (order_id)
        VALUES (%s);
    """
    
    CREATE_PRODUCT_ORDER_ITEM = """
        INSERT INTO product_order_items (product_id, order_item_id, quantity, total_price)
        VALUES (%s, %s, %s, %s);
    """

    DELETE_ORDER = """
        DELETE FROM orders
        WHERE order_id = %s;
    """
    
    DELETE_ORDER_ITEMS = """
        DELETE FROM order_details
        WHERE order_id = %s;
    """

    UPDATE_ORDER_STATUS = """
        UPDATE orders
        SET status = %s
        WHERE order_id = %s;
    """

    SEARCH_ORDERS = """
        SELECT * FROM orders
        WHERE CAST(order_id AS CHAR) LIKE %s OR customer_name LIKE %s
        ORDER BY order_date DESC;
    """
    
    GET_ALL_ORDERS_WITH_SEARCH = """
        SELECT v.*, u.username, (SELECT COALESCE(SUM(receive), 0) FROM order_details WHERE order_id = v.order_id) as total_receive
        FROM order_summary_view v
        JOIN users u ON v.user_id = u.user_id
        WHERE CAST(v.order_id AS CHAR) LIKE %s OR v.customer_name LIKE %s
        ORDER BY v.created_at DESC, v.order_id ASC;
    """
    
    GET_ORDER_BY_ID = """
        SELECT order_id FROM orders
        WHERE order_id = %s;
    """
    
    GET_ORDER_ITEMS_FOR_CANCELLATION = """
        SELECT product_id, quantity
        FROM order_details
        WHERE order_id = %s;
    """
    
    GET_RECENT_COMPLETED_ORDERS = """
        SELECT 
            order_id,
            customer_name,
            total_amount,
            created_at
        FROM order_summary_view 
        WHERE UPPER(status) = 'COMPLETED'
        ORDER BY created_at DESC 
        LIMIT 5;
    """
    
    GET_RECENT_COMPLETED_ORDERS_BY_USER = """
        SELECT 
            order_id,
            customer_name,
            total_amount,
            created_at
        FROM order_summary_view
        WHERE user_id = %s AND UPPER(status) = 'COMPLETED'
        ORDER BY created_at DESC
        LIMIT 5;
    """

    GET_SALES_REPORT = """
        SELECT 
            DATE(created_at) as report_date, 
            COUNT(order_id) as total_orders, 
            SUM(total_amount) as total_revenue
        FROM orders
        WHERE UPPER(status) = 'COMPLETED' 
        AND created_at >= %s AND created_at <= %s
        GROUP BY DATE(created_at)
        ORDER BY report_date;
    """

    GET_BEST_SELLING_PRODUCTS = """
        SELECT 
            p.name as product_name,
            p.unit,
            SUM(od.quantity) as total_sold,
            SUM(od.quantity * od.unit_price) as total_revenue
        FROM order_details od
        JOIN orders o ON od.order_id = o.order_id
        JOIN products p ON od.product_id = p.product_id
        WHERE UPPER(o.status) = 'COMPLETED'
        AND o.created_at >= %s AND o.created_at <= %s
        GROUP BY p.product_id, p.name, p.unit
        ORDER BY total_sold DESC
        LIMIT %s;
    """
