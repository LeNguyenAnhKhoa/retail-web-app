from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Union
from datetime import datetime

class OrderResponse(BaseModel):
    status: str
    data: Union[Dict[str, Any], List[Dict[str, Any]]]
    message: str

class OrderDetailData(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    cost_price: float

class OrderCreateData(BaseModel):
    code: str
    customer_id: Optional[int] = None
    user_id: int
    payment_method: str = "CASH"  # CASH, TRANSFER, CARD
    status: str = "COMPLETED"
    details: List[OrderDetailData]

class OrderDetail(BaseModel):
    id: int
    order_id: int
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    cost_price: float
    created_at: datetime
    updated_at: datetime

class Order(BaseModel):
    order_id: int
    code: str
    customer_id: Optional[int]
    customer_name: Optional[str]
    user_id: int
    staff_name: str
    total_amount: float
    payment_method: str
    status: str
    created_at: datetime
    updated_at: datetime
    details: List[OrderDetail] = []
 