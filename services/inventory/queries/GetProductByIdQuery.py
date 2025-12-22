from shared_utils import Database

class GetProductByIdQuery:
    def __init__(self):
        self.db = Database()
        
    def close(self):
        self.db.close_pool()
        
    def execute(self, product_id):
        query = """
        SELECT 
            p.product_id,
            p.code,
            p.name,
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
            u.full_name AS created_by_name
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        JOIN users u ON p.created_by = u.user_id
        WHERE p.product_id = %s
        """
        
        result = self.db.execute_query(query, (product_id,))
        self.db.close_pool()
        if not result:
            return {}
        
        row = result[0]
        
        formatted_result = {
            "product_id": row[0],
            "code": row[1],
            "name": row[2],
            "category_id": row[3],
            "category_name": row[4],
            "unit": row[5],
            "import_price": float(row[6]),
            "selling_price": float(row[7]),
            "stock_quantity": row[8],
            "image_url": row[9],
            "is_active": row[10],
            "description": row[11],
            "created_by": row[12],
            "created_by_name": row[13]
        }
        
        return formatted_result