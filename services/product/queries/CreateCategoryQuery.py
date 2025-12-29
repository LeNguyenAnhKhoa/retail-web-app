from shared_utils import Database
from models import CategoryCreateModel

class CreateCategoryQuery:
    def __init__(self):
        self.db = Database()

    def execute(self, category: CategoryCreateModel):
        query = """
        INSERT INTO categories (name, description)
        VALUES (%s, %s)
        """
        params = (category.name, category.description)
        result = self.db.execute_query(query, params)
        self.db.close_pool()
        return result
