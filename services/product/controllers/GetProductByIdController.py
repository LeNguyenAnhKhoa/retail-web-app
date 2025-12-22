from queries import GetProductByIdQuery
from models import ProductModel
from shared_config.custom_exception import NotFoundException, InvalidDataException

class GetProductByIdController:
    def __init__(self):
        self.query = GetProductByIdQuery()
    
    def execute(self, product_id: int) -> ProductModel:
        if not isinstance(product_id, int) or product_id <= 0:
            self.query.close()
            raise InvalidDataException("Invalid product ID")
        response = self.query.execute(product_id=product_id)
        self.query.close()
        if not response:
            raise NotFoundException("Product not found")
        
        return ProductModel(
            product_id=response.get("product_id"),
            code=response.get("code"),
            name=response.get("name"),
            category_id=response.get("category_id"),
            category_name=response.get("category_name"),
            unit=response.get("unit"),
            import_price=response.get("import_price"),
            selling_price=response.get("selling_price"),
            stock_quantity=response.get("stock_quantity"),
            image_url=response.get("image_url"),
            is_active=response.get("is_active"),
            description=response.get("description"),
            created_by=response.get("created_by")
        )

