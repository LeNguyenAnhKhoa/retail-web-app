from shared_utils import Database

class CountTotalProductsQuery:
    def __init__(self):
        self.db = Database()
        

    def close(self):
        self.db.close_pool()
        
        
    def count_all_products(self, search: str = None):
        if search:
            query = """
            SELECT COUNT(*) FROM product_summary_view 
            WHERE is_active = TRUE AND (product_name LIKE %s OR category_name LIKE %s)
            """
            search_term = f"%{search}%"
            result = self.db.execute_query(query, (search_term, search_term))
        else:
            query = """
            SELECT COUNT(*) FROM products WHERE is_active = TRUE
            """
            result = self.db.execute_query(query)
        return result[0][0] if result else 0