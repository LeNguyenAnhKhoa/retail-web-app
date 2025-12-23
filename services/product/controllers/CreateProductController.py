from queries import CreateProductQuery
from models import ProductCreateModel
from shared_utils import logger
from shared_config.custom_exception import InvalidDataException
import time


class CreateProductController:
    def __init__(self):
        self.query = CreateProductQuery()
    
    def execute(self, product: ProductCreateModel, user_info: dict = None):
        # Map simple fields to complex model fields
        if product.price is not None:
            product.selling_price = product.price
            if product.import_price is None:
                product.import_price = product.price * 0.7 # Estimate import price
        
        if product.quantity is not None:
            product.stock_quantity = product.quantity
            
        if not product.code:
            product.code = f"P{int(time.time())}"
            
        if not product.unit:
            product.unit = "Cái" # Default unit
            
        if user_info and 'user_id' in user_info:
            product.created_by = user_info['user_id']

        if not isinstance(product, ProductCreateModel):
            self.query.close()
            raise InvalidDataException("Invalid product data")
            
        if not product.name:
            self.query.close()
            raise InvalidDataException("Name cannot be empty")
            
        if product.selling_price is None or product.selling_price <= 0:
            self.query.close()
            raise InvalidDataException("Price must be greater than zero")
            
        if product.stock_quantity is None or product.stock_quantity < 0:
            self.query.close()
            raise InvalidDataException("Quantity must be zero or greater")
            
        # if not product.image_url:
        #     self.query.close()
        #     raise InvalidDataException("Image URL cannot be empty")
            
        if not product.category_id or product.category_id <= 0:
            self.query.close()
            raise InvalidDataException("Invalid category ID")
            
        if not product.supplier_id or product.supplier_id <= 0:
            self.query.close()
            raise InvalidDataException("Invalid supplier ID")

        response = self.query.create_product(product)
        if not response:
            self.query.close()
            raise Exception("Failed to create product")

        logger.info(f"Product created with name: {product.name}")
        return True


