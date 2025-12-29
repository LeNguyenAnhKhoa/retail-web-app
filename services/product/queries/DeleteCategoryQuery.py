from shared_utils import Database

class DeleteCategoryQuery:
    def __init__(self):
        self.db = Database()

    def execute(self, category_id: int):
        query = "DELETE FROM categories WHERE category_id = %s"
        self.db.execute_query(query, (category_id,))
        self.db.close_pool()
        return True
