from queries import DeleteCategoryQuery, CheckCategoryHasProductsQuery
from shared_utils import logger
from shared_config.custom_exception import InvalidDataException

class DeleteCategoryController:
    def __init__(self):
        self.delete_query = DeleteCategoryQuery()
        self.check_query = CheckCategoryHasProductsQuery()

    def execute(self, category_id: int):
        if self.check_query.execute(category_id):
            raise InvalidDataException("Cannot delete category because it has associated products")
            
        self.delete_query.execute(category_id)
        logger.info(f"Category deleted: {category_id}")
        return True
