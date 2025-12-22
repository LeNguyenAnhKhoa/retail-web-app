from shared_utils import Database

class GetAllProductQuery:
    def __init__(self):
        self.db = Database()
        
    def close(self):
        self.db.close_pool()

    def get_all_products_by_admin(self, params=(100, 0), search=None):
        where_conditions = []
        query_params = []
        
        # Build search conditions - search across name and category
        if search:
            where_conditions.append("(name LIKE %s OR category_name LIKE %s)")
            search_term = f"%{search}%"
            query_params.extend([search_term, search_term])
        
        # Build query
        query = "SELECT * FROM product_summary_view"
        if where_conditions:
            query += " WHERE " + " AND ".join(where_conditions)
        query += " LIMIT %s OFFSET %s"
        
        # Add limit and offset parameters
        query_params.extend([params[0], params[1]])
        
        result = self.db.execute_query(query, tuple(query_params))
        if not result:
            return []
        formatted_result = [
            {
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
                "created_by_name": row[13],
                "supplier_id": row[15],
                "supplier_name": row[16]
            }
            for row in result
        ]
        return formatted_result

    def get_all_product_by_user(self, user_id, params=(100, 0), search=None):
        where_conditions = []
        query_params = []
        
        # Build search conditions - search across name and category
        if search:
            where_conditions.append("(name LIKE %s OR category_name LIKE %s)")
            search_term = f"%{search}%"
            query_params.extend([search_term, search_term])
        
        # Build query
        query = "SELECT * FROM product_summary_view"
        if where_conditions:
            query += " WHERE " + " AND ".join(where_conditions)
        query += " LIMIT %s OFFSET %s"
        
        # Add limit and offset parameters
        query_params.extend([params[0], params[1]])
        
        result = self.db.execute_query(query, tuple(query_params))
        if not result:
            return []
        formatted_result = [
            {
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
                "created_by_name": row[13],
                "supplier_id": row[15],
                "supplier_name": row[16]
            }
            for row in result
        ]
        return formatted_result