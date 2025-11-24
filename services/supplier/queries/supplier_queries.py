class SupplierQueries:
    GET_ALL_SUPPLIERS = """
        SELECT supplier_id, supplier_name, contact_name, phone, address, email,
               total_import_tickets, total_import_value, created_at, updated_at
        FROM supplier_summary_view
        ORDER BY updated_at DESC, supplier_id ASC;
    """
    
    GET_ALL_SUPPLIERS_BY_SEARCH = """
        SELECT supplier_id, supplier_name, contact_name, phone, address, email,
               total_import_tickets, total_import_value, created_at, updated_at
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
    
    CHECK_SUPPLIER_EXISTS = """
        SELECT * FROM suppliers
        WHERE supplier_id = %s;
    """

    CREATE_SUPPLIER = """
        INSERT INTO suppliers (name, contact_name, contact_email, phone)
        VALUES (%s, %s, %s, %s);
    """
    
    UPDATE_SUPPLIER = """
        UPDATE suppliers
        SET name = %s, contact_name = %s, contact_email = %s, phone = %s, updated_time = CURRENT_TIMESTAMP
        WHERE supplier_id = %s;
    """
    
    DELETE_SUPPLIER = """
        DELETE FROM suppliers
        WHERE supplier_id = %s;
    """
