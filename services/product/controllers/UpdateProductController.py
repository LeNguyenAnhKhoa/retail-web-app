from queries import UpdateProductQuery
from models import ProductUpdateModel
from shared_config.custom_exception import InvalidDataException, NotFoundException

class UpdateProductController:
    def __init__(self):
        self.query = UpdateProductQuery()
        
    def execute(self, updated_product: ProductUpdateModel):
        if updated_product.product_id <= 0:
            self.query.db.close_pool()
            raise InvalidDataException("Invalid product ID")
        if updated_product.name is not None and not updated_product.name:
            self.query.db.close_pool()
            raise InvalidDataException("Name cannot be empty")
        if updated_product.description is not None and not updated_product.description:
            self.query.db.close_pool()
            raise InvalidDataException("Description cannot be empty")
        if updated_product.price is not None and updated_product.price <= 0:
            self.query.db.close_pool()
            raise InvalidDataException("Price must be greater than zero")
        if updated_product.selling_price is not None and updated_product.selling_price <= 0:
            self.query.db.close_pool()
            raise InvalidDataException("Selling price must be greater than zero")
        if updated_product.import_price is not None and updated_product.import_price <= 0:
            self.query.db.close_pool()
            raise InvalidDataException("Import price must be greater than zero")

        # Validate import_price <= selling_price
        selling_price = updated_product.selling_price if updated_product.selling_price is not None else updated_product.price
        if updated_product.import_price is not None and selling_price is not None:
            if updated_product.import_price > selling_price:
                self.query.db.close_pool()
                raise InvalidDataException("Import price must be less than or equal to selling price")
            
        if updated_product.quantity is not None and updated_product.quantity < 0:
            self.query.db.close_pool()
            raise InvalidDataException("Quantity must be zero or greater")
        if updated_product.stock_quantity is not None and updated_product.stock_quantity < 0:
            self.query.db.close_pool()
            raise InvalidDataException("Stock quantity must be zero or greater")
            
        if updated_product.image_url is not None and not updated_product.image_url:
            self.query.db.close_pool()
            raise InvalidDataException("Image URL cannot be empty")
        if updated_product.category_id is not None and updated_product.category_id <= 0:
            self.query.db.close_pool()
            raise InvalidDataException("Invalid category ID")
        if updated_product.supplier_id is not None and updated_product.supplier_id <= 0:
            self.query.db.close_pool()
            raise InvalidDataException("Invalid supplier ID")
        
        if not self.query.check_product_exists(updated_product.product_id):
            self.query.db.close_pool()
            raise NotFoundException("Product does not exist")
        
        response = self.query.update_product(updated_product)
        self.query.db.close_pool()
        if not response:
            raise Exception("Failed to update product")
        return True