from fastapi import APIRouter, Query, Depends
from models.inventory import InventoryTicketCreate
from controllers.inventory_controller import (
    GetTicketsController,
    GetTicketByIdController,
    CreateTicketController,
    GetStockMovementController,
    GetLowStockProductsController
)
from shared_config.standard_response import standard_response
from shared_config.response_model import StandardResponse
from shared_utils.middleware import login_required

router = APIRouter()

@router.get("/tickets", response_model=StandardResponse)
@standard_response
def get_tickets(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    type: str = Query(None, description="IMPORT, EXPORT_CANCEL, STOCK_CHECK"),
    supplier_id: int = Query(None),
    user_id: int = Query(None),
    from_date: str = Query(None),
    to_date: str = Query(None),
    user_info: dict = Depends(login_required)
):
    """Get inventory tickets with filters"""
    filters = {
        "type": type,
        "supplier_id": supplier_id,
        "user_id": user_id,
        "from_date": from_date,
        "to_date": to_date
    }
    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None}
    
    controller = GetTicketsController()
    response = controller.execute(filters, page, page_size)
    return response

@router.get("/tickets/{ticket_id}", response_model=StandardResponse)
@standard_response
def get_ticket(ticket_id: int, user_info: dict = Depends(login_required)):
    """Get ticket by ID with details"""
    controller = GetTicketByIdController()
    response = controller.execute(ticket_id)
    return response

@router.post("/tickets", response_model=StandardResponse)
@standard_response
def create_ticket(ticket: InventoryTicketCreate, user_info: dict = Depends(login_required)):
    """
    Create new inventory ticket
    - IMPORT: Nhập hàng từ NCC (cần supplier_id)
    - EXPORT_CANCEL: Xuất hủy hàng hỏng
    - STOCK_CHECK: Kiểm kê điều chỉnh tồn kho
    """
    controller = CreateTicketController()
    response = controller.execute(ticket)
    return response

@router.get("/stock-movement/{product_id}", response_model=StandardResponse)
@standard_response
def get_stock_movement(product_id: int, user_info: dict = Depends(login_required)):
    """Get stock movement history for a product"""
    controller = GetStockMovementController()
    response = controller.execute(product_id)
    return response

@router.get("/low-stock", response_model=StandardResponse)
@standard_response
def get_low_stock(threshold: int = Query(10, ge=0), user_info: dict = Depends(login_required)):
    """Get products with stock below threshold"""
    controller = GetLowStockProductsController()
    response = controller.execute(threshold)
    return response
