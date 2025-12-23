from shared_utils import Database
from models import ProductCreateModel

class CreateProductQuery:
    def __init__(self):
        self.db = Database()

    def create_product(self, params: ProductCreateModel):
        query = """
        INSERT INTO products (code, name, category_id, unit, import_price, selling_price, stock_quantity, created_by, is_active, description, supplier_id, image_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        query_params = (
            params.code,
            params.name,
            params.category_id,
            params.unit,
            params.import_price,
            params.selling_price,
            params.stock_quantity,
            params.created_by,
            params.is_active,
            params.description,
            params.supplier_id,
            params.image_url
        )
        res = self.db.execute_query(query, query_params)
        self.db.close_pool()
        return True if res is not None else False
    
    def close(self):
        self.db.close_pool()