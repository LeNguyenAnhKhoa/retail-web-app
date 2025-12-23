class OrderQueries:
    GET_ALL_ORDERS = """
        SELECT * FROM order_summary_view
        ORDER BY created_at DESC, order_id ASC;
    """

    GET_ORDER_DETAIL = """
        SELECT * FROM order_detail_summary
        WHERE order_id = %s
        ORDER BY order_updated_time DESC, order_id ASC;
    """

    # Use stored procedure to create order
    CREATE_ORDER_PROCEDURE = """
        CALL CreateOrderWithDetails(%s, %s, %s, %s, %s, %s, %s, %s);
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

    GET_RECENT_COMPLETED_ORDERS = """
        SELECT 
            o.order_id, 
            c.name as customer_name, 
            o.total_amount, 
            o.status, 
            o.created_at 
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.status = 'COMPLETED'
        ORDER BY o.created_at DESC
        LIMIT 5;
    """

    GET_RECENT_COMPLETED_ORDERS_BY_USER = """
        SELECT 
            o.order_id, 
            c.name as customer_name, 
            o.total_amount, 
            o.status, 
            o.created_at 
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.status = 'COMPLETED' AND o.user_id = %s
        ORDER BY o.created_at DESC
        LIMIT 5;
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
        DELETE FROM order_items
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
        SELECT * FROM order_summary_view
        WHERE CAST(order_id AS CHAR) LIKE %s OR customer_name LIKE %s
        ORDER BY created_at DESC, order_id ASC;
    """
    
    GET_ORDER_BY_ID = """
        SELECT order_id FROM orders
        WHERE order_id = %s;
    """
    
    GET_ORDER_ITEMS_FOR_CANCELLATION = """
        SELECT poi.product_id, poi.quantity
        FROM product_order_items poi
        JOIN order_items oi ON poi.order_item_id = oi.order_item_id
        WHERE oi.order_id = %s;
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