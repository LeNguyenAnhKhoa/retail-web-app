"""
Inventory queries for warehouse management
"""

# Get all inventory tickets with filters
GET_INVENTORY_TICKETS = """
    SELECT 
        it.ticket_id,
        it.code,
        it.type,
        it.supplier_id,
        s.name AS supplier_name,
        it.user_id,
        u.full_name AS user_name,
        u.role AS user_role,
        it.note,
        it.created_at,
        it.updated_at
    FROM inventory_tickets it
    LEFT JOIN suppliers s ON it.supplier_id = s.supplier_id
    INNER JOIN users u ON it.user_id = u.user_id
    WHERE 1=1
    {filters}
    ORDER BY it.created_at DESC
    LIMIT %s OFFSET %s
"""

# Get inventory ticket by ID with details
GET_INVENTORY_TICKET_BY_ID = """
    SELECT 
        it.ticket_id,
        it.code,
        it.type,
        it.supplier_id,
        s.name AS supplier_name,
        it.user_id,
        u.full_name AS user_name,
        u.role AS user_role,
        it.note,
        it.created_at,
        it.updated_at
    FROM inventory_tickets it
    LEFT JOIN suppliers s ON it.supplier_id = s.supplier_id
    INNER JOIN users u ON it.user_id = u.user_id
    WHERE it.ticket_id = %s
"""

# Get ticket details
GET_TICKET_DETAILS = """
    SELECT 
        itd.id,
        itd.ticket_id,
        itd.product_id,
        p.code AS product_code,
        p.name AS product_name,
        itd.quantity,
        itd.price
    FROM inventory_ticket_details itd
    INNER JOIN products p ON itd.product_id = p.product_id
    WHERE itd.ticket_id = %s
"""

# Create inventory ticket
CREATE_INVENTORY_TICKET = """
    INSERT INTO inventory_tickets (code, type, supplier_id, user_id, note)
    VALUES (%s, %s, %s, %s, %s)
"""

# Create ticket detail
CREATE_TICKET_DETAIL = """
    INSERT INTO inventory_ticket_details (ticket_id, product_id, quantity, price)
    VALUES (%s, %s, %s, %s)
"""

# Update product stock
UPDATE_PRODUCT_STOCK = """
    UPDATE products 
    SET stock_quantity = stock_quantity + %s
    WHERE product_id = %s
"""

# Update product import price (for IMPORT tickets)
UPDATE_PRODUCT_IMPORT_PRICE = """
    UPDATE products 
    SET import_price = %s
    WHERE product_id = %s
"""

# Get product stock
GET_PRODUCT_STOCK = """
    SELECT stock_quantity 
    FROM products 
    WHERE product_id = %s
"""

# Check if ticket code exists
CHECK_TICKET_CODE_EXISTS = """
    SELECT COUNT(*) as count
    FROM inventory_tickets
    WHERE code = %s
"""

# Get stock movement for a product
GET_STOCK_MOVEMENT = """
    SELECT 
        p.product_id,
        p.code AS product_code,
        p.name AS product_name,
        p.stock_quantity AS current_stock,
        COALESCE(SUM(CASE WHEN it.type = 'IMPORT' THEN itd.quantity ELSE 0 END), 0) AS total_imported,
        COALESCE(SUM(CASE WHEN it.type = 'EXPORT_CANCEL' THEN ABS(itd.quantity) ELSE 0 END), 0) AS total_exported,
        COALESCE(SUM(CASE WHEN it.type = 'STOCK_CHECK' THEN itd.quantity ELSE 0 END), 0) AS total_adjusted
    FROM products p
    LEFT JOIN inventory_ticket_details itd ON p.product_id = itd.product_id
    LEFT JOIN inventory_tickets it ON itd.ticket_id = it.ticket_id
    WHERE p.product_id = %s
    GROUP BY p.product_id, p.code, p.name, p.stock_quantity
"""

# Get low stock products
GET_LOW_STOCK_PRODUCTS = """
    SELECT 
        p.product_id,
        p.code,
        p.name,
        p.stock_quantity,
        c.name AS category_name
    FROM products p
    INNER JOIN categories c ON p.category_id = c.category_id
    WHERE p.stock_quantity < %s AND p.is_active = TRUE
    ORDER BY p.stock_quantity ASC
"""
