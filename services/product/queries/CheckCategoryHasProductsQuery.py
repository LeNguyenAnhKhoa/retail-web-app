from shared_utils import Database

class CheckCategoryHasProductsQuery:
    def __init__(self):
        self.db = Database()

    def execute(self, category_id: int):
        query = "SELECT COUNT(*) FROM products WHERE category_id = %s"
        result = self.db.execute_query(query, (category_id,))
        self.db.close_pool()
        if result and result[0][0] > 0:
            return True
        return False
