from shared_utils import Database
from models import CategoryUpdateModel

class UpdateCategoryQuery:
    def __init__(self):
        self.db = Database()

    def execute(self, category_id: int, category: CategoryUpdateModel):
        query = """
        UPDATE categories
        SET name = %s, description = %s
        WHERE category_id = %s
        """
        params = (category.name, category.description, category_id)
        self.db.execute_query(query, params)
        self.db.close_pool()
        return True
