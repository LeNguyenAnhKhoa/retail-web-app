from pydantic import BaseModel, Field
from typing import Optional

class ProductCreateModel(BaseModel):
    code: str = Field(..., title="Product Code", description="Unique code/SKU for the product")
    name: str = Field(..., title="Product Name", description="Name of the product")
    category_id: int = Field(..., title="Category ID", description="ID of the category")
    unit: str = Field(..., title="Unit", description="Unit of measurement (Hộp, Lon, Gói, etc.)")
    import_price: float = Field(..., title="Import Price", description="Import/cost price")
    selling_price: float = Field(..., title="Selling Price", description="Selling price")
    stock_quantity: int = Field(0, title="Stock Quantity", description="Current stock quantity")
    image_url: Optional[str] = Field(None, title="Product Image URL", description="URL of the product image")
    created_by: int = Field(..., title="Created By", description="User ID who created this product")
    is_active: bool = Field(True, title="Is Active", description="Whether product is active")
    description: Optional[str] = Field(None, title="Product Description", description="Description of the product")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "code": "CC001",
                "name": "Coca Cola 330ml",
                "category_id": 1,
                "unit": "Lon",
                "import_price": 6000,
                "selling_price": 8000,
                "stock_quantity": 100,
                "image_url": "http://example.com/coca.jpg",
                "created_by": 3,
                "is_active": True,
                "description": "Nước ngọt Coca Cola lon 330ml"
            }
        }
        
class ProductUpdateModel(BaseModel):
    product_id: int = Field(..., title="Product ID", description="Unique identifier for the product")
    code: Optional[str] = Field(None, title="Product Code", description="Unique code/SKU")
    name: Optional[str] = Field(None, title="Product Name", description="Name of the product")
    category_id: Optional[int] = Field(None, title="Category ID", description="ID of the category")
    unit: Optional[str] = Field(None, title="Unit", description="Unit of measurement")
    import_price: Optional[float] = Field(None, title="Import Price", description="Import/cost price")
    selling_price: Optional[float] = Field(None, title="Selling Price", description="Selling price")
    stock_quantity: Optional[int] = Field(None, title="Stock Quantity", description="Current stock quantity")
    image_url: Optional[str] = Field(None, title="Product Image URL", description="URL of the product image")
    is_active: Optional[bool] = Field(None, title="Is Active", description="Whether product is active")
    description: Optional[str] = Field(None, title="Product Description", description="Description of the product")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "product_id": 1,
                "code": "CC001",
                "name": "Coca Cola 330ml",
                "category_id": 1,
                "unit": "Lon",
                "import_price": 6000,
                "selling_price": 8000,
                "stock_quantity": 100,
                "image_url": "http://example.com/coca.jpg",
                "is_active": True,
                "description": "Nước ngọt Coca Cola lon 330ml"
            }
        }

class ProductModel(BaseModel):
    product_id: int = Field(..., title="Product ID", description="Unique identifier for the product")
    code: str = Field(..., title="Product Code", description="Unique code/SKU")
    name: str = Field(..., title="Product Name", description="Name of the product")
    category_id: int = Field(..., title="Category ID", description="ID of the category")
    category_name: str = Field(..., title="Category Name", description="Name of the category")
    unit: str = Field(..., title="Unit", description="Unit of measurement")
    import_price: float = Field(..., title="Import Price", description="Import/cost price")
    selling_price: float = Field(..., title="Selling Price", description="Selling price")
    stock_quantity: int = Field(..., title="Stock Quantity", description="Current stock quantity")
    image_url: Optional[str] = Field(None, title="Product Image URL", description="URL of the product image")
    created_by: int = Field(..., title="Created By", description="User ID who created")
    is_active: bool = Field(..., title="Is Active", description="Whether product is active")
    description: Optional[str] = Field(None, title="Product Description", description="Description of the product")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "product_id": 1,
                "code": "CC001",
                "name": "Coca Cola 330ml",
                "category_id": 1,
                "category_name": "Nước ngọt",
                "unit": "Lon",
                "import_price": 6000,
                "selling_price": 8000,
                "stock_quantity": 100,
                "image_url": "http://example.com/coca.jpg",
                "created_by": 3,
                "is_active": True,
                "description": "Nước ngọt Coca Cola lon 330ml"
            }
        }
        
class ProductListModel(BaseModel):
    products: list[ProductModel] = Field(..., title="List of Products", description="List of products")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "products": [
                    {
                        "product_id": 1,
                        "code": "CC001",
                        "name": "Coca Cola 330ml",
                        "category_id": 1,
                        "category_name": "Nước ngọt",
                        "unit": "Lon",
                        "import_price": 6000,
                        "selling_price": 8000,
                        "stock_quantity": 100,
                        "image_url": "http://example.com/coca.jpg",
                        "created_by": 3,
                        "is_active": True,
                        "description": "Nước ngọt Coca Cola lon 330ml"
                    }
                ]
            }
        }