from shared_utils import Database

class ExportInventoryReportQuery:
    def __init__(self):
        self.db = Database()
        
    def close(self):
        self.db.close_pool()

    def execute(self, min_stock, max_stock):
        query = """
            SELECT 
                product_name, 
                unit, 
                stock_quantity 
            FROM product_summary_view 
            WHERE stock_quantity < %s OR stock_quantity > %s
            ORDER BY stock_quantity ASC
        """
        result = self.db.execute_query(query, (min_stock, max_stock))
        
        if not result:
            return []
            
        return [
            {
                "product_name": row[0],
                "unit": row[1],
                "stock_quantity": row[2]
            }
            for row in result
        ]
