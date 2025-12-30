class SupplierQueries:
    GET_ALL_SUPPLIERS = """
        SELECT supplier_id, supplier_name, contact_name, phone, address, email,
               total_products, total_product_quantity, avg_product_price, created_at, updated_at
        FROM supplier_summary_view
        ORDER BY updated_at DESC, supplier_id ASC;
    """
    
    GET_ALL_SUPPLIERS_BY_SEARCH = """
        SELECT supplier_id, supplier_name, contact_name, phone, address, email,
               total_products, total_product_quantity, avg_product_price, created_at, updated_at
        FROM supplier_summary_view
        WHERE LOWER(supplier_name) LIKE LOWER(CONCAT('%%', %s, '%%'))
        OR LOWER(contact_name) LIKE LOWER(CONCAT('%%', %s, '%%'))
        OR LOWER(email) LIKE LOWER(CONCAT('%%', %s, '%%'))
        OR LOWER(phone) LIKE LOWER(CONCAT('%%', %s, '%%'))
        ORDER BY updated_at DESC, supplier_id ASC;
    """
    
    GET_ALL_SUPPLIERS_WITH_PRODUCTS = """
        SELECT * FROM supplier_summary_view
        WHERE supplier_id = %s;
    """

    GET_SUPPLIER_WITH_PRODUCTS_BY_ID = """
        SELECT * FROM supplier_summary_view
        WHERE supplier_id = %s;
    """
    
    GET_PRODUCTS_BY_SUPPLIER_ID = """
        SELECT p.product_id, p.name, p.description, p.import_price, p.stock_quantity, c.name, p.created_at, p.updated_at
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        WHERE p.supplier_id = %s AND p.is_active = TRUE;
    """
    
    COUNT_ACTIVE_PRODUCTS_BY_SUPPLIER_ID = """
        SELECT COUNT(*) FROM products
        WHERE supplier_id = %s AND is_active = TRUE;
    """
    
    CHECK_SUPPLIER_EXISTS = """
        SELECT * FROM suppliers
        WHERE supplier_id = %s;
    """

    CHECK_PHONE_EXISTS = """
        SELECT supplier_id FROM suppliers WHERE phone = %s;
    """
    
    CHECK_EMAIL_EXISTS = """
        SELECT supplier_id FROM suppliers WHERE email = %s;
    """

    CREATE_SUPPLIER = """
        INSERT INTO suppliers (name, contact_name, email, phone, address)
        VALUES (%s, %s, %s, %s, %s);
    """
    
    UPDATE_SUPPLIER = """
        UPDATE suppliers
        SET name = %s, contact_name = %s, email = %s, phone = %s, address = %s, updated_at = CURRENT_TIMESTAMP
        WHERE supplier_id = %s;
    """
    
    DELETE_SUPPLIER = """
        DELETE FROM suppliers
        WHERE supplier_id = %s;
    """

    NULLIFY_PRODUCT_SUPPLIER = """
        UPDATE products SET supplier_id = NULL WHERE supplier_id = %s;
    """
