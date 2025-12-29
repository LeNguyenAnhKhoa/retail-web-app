from queries import CreateCategoryQuery
from models import CategoryCreateModel
from shared_utils import logger
from shared_config.custom_exception import InvalidDataException

class CreateCategoryController:
    def __init__(self):
        self.query = CreateCategoryQuery()

    def execute(self, category: CategoryCreateModel):
        if not category.name:
            raise InvalidDataException("Category name is required")
        
        self.query.execute(category)
        logger.info(f"Category created: {category.name}")
        return True
