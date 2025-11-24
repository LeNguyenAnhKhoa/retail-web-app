"""
Inventory Controller - Warehouse management
"""

from shared_utils.database import Database
from shared_config.custom_exception import InvalidDataException
from queries.inventory_queries import *
from models.inventory import InventoryTicketCreate
from shared_utils.logger import logger

class GetTicketsController:
    def __init__(self):
        self.db = Database()
    
    def execute(self, filters: dict, page: int = 1, page_size: int = 20):
        """Get list of inventory tickets with pagination and filters"""
        if not isinstance(page, int) or not isinstance(page_size, int):
            self.db.close_pool()
            raise InvalidDataException("Page and page_size must be integers")
        
        if page_size > 100:
            self.db.close_pool()
            raise InvalidDataException("Max page_size is 100")
        
        offset = (page - 1) * page_size
        
        # Build filter query
        filter_parts = []
        filter_values = []
        
        if filters.get('type'):
            filter_parts.append("AND it.type = %s")
            filter_values.append(filters['type'])
        
        if filters.get('supplier_id'):
            filter_parts.append("AND it.supplier_id = %s")
            filter_values.append(filters['supplier_id'])
        
        if filters.get('user_id'):
            filter_parts.append("AND it.user_id = %s")
            filter_values.append(filters['user_id'])
        
        if filters.get('from_date'):
            filter_parts.append("AND DATE(it.created_at) >= %s")
            filter_values.append(filters['from_date'])
        
        if filters.get('to_date'):
            filter_parts.append("AND DATE(it.created_at) <= %s")
            filter_values.append(filters['to_date'])
        
        filter_query = " ".join(filter_parts)
        query = GET_INVENTORY_TICKETS.format(filters=filter_query)
        
        filter_values.extend([page_size, offset])
        
        tickets = self.db.execute_query(query, tuple(filter_values))
        self.db.close_pool()
        
        return {"tickets": tickets, "page": page, "page_size": page_size}

class GetTicketByIdController:
    def __init__(self):
        self.db = Database()
    
    def execute(self, ticket_id: int):
        """Get ticket detail by ID"""
        if not isinstance(ticket_id, int):
            self.db.close_pool()
            raise InvalidDataException("Ticket ID must be an integer")
        
        # Get ticket info
        ticket = self.db.execute_query(GET_INVENTORY_TICKET_BY_ID, (ticket_id,))
        
        if not ticket or len(ticket) == 0:
            self.db.close_pool()
            raise InvalidDataException("Ticket not found")
        
        ticket_data = ticket[0]
        
        # Get ticket details
        details = self.db.execute_query(GET_TICKET_DETAILS, (ticket_id,))
        ticket_data['details'] = details
        
        self.db.close_pool()
        
        return ticket_data

class CreateTicketController:
    def __init__(self):
        self.db = Database()
    
    def execute(self, ticket_data: InventoryTicketCreate):
        """Create new inventory ticket with details"""
        # Validate ticket code
        existing = self.db.execute_query(CHECK_TICKET_CODE_EXISTS, (ticket_data.code,))
        if existing and existing[0].get('count', 0) > 0:
            self.db.close_pool()
            raise InvalidDataException("Ticket code already exists")
        
        # Validate supplier for IMPORT type
        if ticket_data.type == 'IMPORT' and not ticket_data.supplier_id:
            self.db.close_pool()
            raise InvalidDataException("Supplier required for IMPORT ticket")
        
        # Validate stock for EXPORT_CANCEL
        if ticket_data.type == 'EXPORT_CANCEL':
            for detail in ticket_data.details:
                if detail.quantity > 0:
                    detail.quantity = -detail.quantity  # Make it negative
                
                stock = self.db.execute_query(GET_PRODUCT_STOCK, (detail.product_id,))
                if stock and stock[0].get('stock_quantity', 0) < abs(detail.quantity):
                    self.db.close_pool()
                    raise InvalidDataException(
                        f"Insufficient stock for product ID {detail.product_id}"
                    )
        
        # Create ticket
        ticket_id = self.db.execute_query(
            CREATE_INVENTORY_TICKET,
            (ticket_data.code, ticket_data.type, ticket_data.supplier_id, 
             ticket_data.user_id, ticket_data.note)
        )
        
        # Create ticket details and update stock
        for detail in ticket_data.details:
            # Insert detail
            self.db.execute_query(
                CREATE_TICKET_DETAIL,
                (ticket_id, detail.product_id, detail.quantity, detail.price)
            )
            
            # Update product stock
            self.db.execute_query(
                UPDATE_PRODUCT_STOCK,
                (detail.quantity, detail.product_id)
            )
            
            # Update import price for IMPORT tickets
            if ticket_data.type == 'IMPORT' and detail.price:
                self.db.execute_query(
                    UPDATE_PRODUCT_IMPORT_PRICE,
                    (detail.price, detail.product_id)
                )
        
        self.db.close_pool()
        
        return {"ticket_id": ticket_id}

class GetStockMovementController:
    def __init__(self):
        self.db = Database()
    
    def execute(self, product_id: int):
        """Get stock movement for a product"""
        if not isinstance(product_id, int):
            self.db.close_pool()
            raise InvalidDataException("Product ID must be an integer")
        
        movement = self.db.execute_query(GET_STOCK_MOVEMENT, (product_id,))
        self.db.close_pool()
        
        if not movement or len(movement) == 0:
            raise InvalidDataException("Product not found")
        
        return movement[0]

class GetLowStockProductsController:
    def __init__(self):
        self.db = Database()
    
    def execute(self, threshold: int = 10):
        """Get products with low stock"""
        if not isinstance(threshold, int):
            self.db.close_pool()
            raise InvalidDataException("Threshold must be an integer")
        
        products = self.db.execute_query(GET_LOW_STOCK_PRODUCTS, (threshold,))
        self.db.close_pool()
        
        return {"products": products, "threshold": threshold}
