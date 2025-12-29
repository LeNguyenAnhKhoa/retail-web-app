from queries import UpdateCategoryQuery
from models import CategoryUpdateModel
from shared_utils import logger
from shared_config.custom_exception import InvalidDataException

class UpdateCategoryController:
    def __init__(self):
        self.query = UpdateCategoryQuery()

    def execute(self, category_id: int, category: CategoryUpdateModel):
        if not category.name:
            raise InvalidDataException("Category name is required")
            
        self.query.execute(category_id, category)
        logger.info(f"Category updated: {category_id}")
        return True
