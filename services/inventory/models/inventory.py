from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Inventory Ticket Models
class InventoryTicketDetailCreate(BaseModel):
    product_id: int = Field(..., title="Product ID")
    quantity: int = Field(..., title="Quantity", description="Positive for import, negative for export")
    price: Optional[float] = Field(None, title="Price", description="Import price (for IMPORT type)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_id": 1,
                "quantity": 100,
                "price": 6000
            }
        }

class InventoryTicketCreate(BaseModel):
    code: str = Field(..., title="Ticket Code")
    type: str = Field(..., title="Type", description="IMPORT, EXPORT_CANCEL, or STOCK_CHECK")
    supplier_id: Optional[int] = Field(None, title="Supplier ID", description="Required for IMPORT")
    user_id: int = Field(..., title="User ID", description="User creating the ticket")
    note: Optional[str] = Field(None, title="Note")
    details: List[InventoryTicketDetailCreate] = Field(..., title="Ticket Details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "NK001",
                "type": "IMPORT",
                "supplier_id": 1,
                "user_id": 3,
                "note": "Nhập hàng đợt 1",
                "details": [
                    {"product_id": 1, "quantity": 100, "price": 6000},
                    {"product_id": 2, "quantity": 150, "price": 5500}
                ]
            }
        }

class InventoryTicketDetail(BaseModel):
    id: int
    ticket_id: int
    product_id: int
    product_code: str
    product_name: str
    quantity: int
    price: Optional[float]
    
    class Config:
        from_attributes = True

class InventoryTicket(BaseModel):
    ticket_id: int
    code: str
    type: str
    supplier_id: Optional[int]
    supplier_name: Optional[str]
    user_id: int
    user_name: str
    note: Optional[str]
    created_at: datetime
    details: List[InventoryTicketDetail] = []
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "ticket_id": 1,
                "code": "NK001",
                "type": "IMPORT",
                "supplier_id": 1,
                "supplier_name": "Coca Cola VN",
                "user_id": 3,
                "user_name": "Lê Văn Thủ Kho",
                "note": "Nhập hàng đợt 1",
                "created_at": "2024-11-20T10:00:00",
                "details": []
            }
        }
