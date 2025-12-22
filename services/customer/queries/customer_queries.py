class CustomerQueries:
    GET_ALL_CUSTOMERS = """
        SELECT *
        FROM customer_summary_view
        ORDER BY updated_at DESC, customer_id ASC;
    """
    
    GET_ALL_CUSTOMERS_BY_SEARCH = """
        SELECT *
        FROM customer_summary_view
        WHERE LOWER(customer_name) LIKE LOWER(CONCAT('%%', %s, '%%'))
        OR LOWER(phone) LIKE LOWER(CONCAT('%%', %s, '%%'))
        ORDER BY updated_at DESC, customer_id ASC;
    """

    GET_CUSTOMER_BY_ID = """
        SELECT *
        FROM customer_summary_view
        WHERE customer_id = %s
        ORDER BY customer_updated_time DESC, customer_id ASC;
    """

    CREATE_CUSTOMER = """
        INSERT INTO customers (name, phone, address)
        VALUES (%s, %s, %s);
    """

    GET_LAST_INSERTED_CUSTOMER = """
        SELECT customer_id, name, phone, address
        FROM customers
        ORDER BY customer_id DESC
        LIMIT 1;
    """

    UPDATE_CUSTOMER = """
        UPDATE customers
        SET name = %s, phone = %s, address = %s
        WHERE customer_id = %s;
    """

    DELETE_CUSTOMER = """
        DELETE FROM customers
        WHERE customer_id = %s;
    """

    # GET_CUSTOMER_BY_EMAIL = """
    #     SELECT customer_id, name, phone, address, created_at, updated_at
    #     FROM customers
    #     WHERE email = %s;
    # """ 
    
    COUNT_CUSTOMERS = """
        SELECT COUNT(*) FROM customers;
    """