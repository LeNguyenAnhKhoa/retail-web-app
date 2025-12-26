from shared_utils.database import Database
from queries.supplier_queries import SupplierQueries
from models.supplier import SupplierResponse, SupplierData
from shared_utils.logger import logger
from shared_config.custom_exception import InvalidDataException, NotFoundException

class SupplierController:
    def __init__(self):
        self.db = Database()

    def get_all_suppliers(self, user_info: dict, search: str = None) -> list:
        # Validate user_info is a dict
        if not isinstance(user_info, dict):
            self.db.close_pool()
            raise InvalidDataException("User info must be a dictionary")
        role_name = user_info.get("role_name", "").lower()
        if not role_name:
            self.db.close_pool()
            raise InvalidDataException("Role name must be provided in user info")
        if role_name not in ("admin", "staff", "manager", "stockkeeper"):
            self.db.close_pool()
            raise InvalidDataException("User role must be either 'admin', 'staff', 'manager', or 'stockkeeper'")
        
        # Prepare search parameter
        search = search.strip() if search else None
        if search and not isinstance(search, str):
            raise InvalidDataException("Search must be a string")
        
        # All roles can access all suppliers since there's only one warehouse
        if search:
            search_param = f"%{search}%"
            result = self.db.execute_query(SupplierQueries.GET_ALL_SUPPLIERS_BY_SEARCH, 
                                         (search_param, search_param, search_param, search_param))
        else:
            result = self.db.execute_query(SupplierQueries.GET_ALL_SUPPLIERS)
        self.db.close_pool()
        suppliers = []
        for row in result:
            supplier = {
                "supplier_id": row[0],
                "supplier_name": row[1],
                "contact_name": row[2],
                "contact_email": row[5],
                "phone": row[3],
                "address": row[4],
                "total_products": row[6],
                "total_product_quantity": row[7],
                "avg_product_price": row[8],
                "earliest_product_created": None,
                "latest_product_updated": None,
                "supplier_created_time": row[9],
                "supplier_updated_time": row[10]
            }
            if suppliers and suppliers[-1]["supplier_id"] == supplier["supplier_id"]:
                # If the supplier already exists in the list, skip adding it again
                continue
            suppliers.append(supplier)
        return suppliers

    def get_supplier(self, supplier_id: int, user_info: dict) -> dict:
        # Validate user_info is a dict
        if not isinstance(user_info, dict):
            self.db.close_pool()
            raise InvalidDataException("User info must be a dictionary")
        role_name = user_info.get("role_name", "").lower()
        if not role_name:
            self.db.close_pool()
            raise InvalidDataException("Role name must be provided in user info")
        if role_name not in ("admin", "staff", "manager", "stockkeeper"):
            self.db.close_pool()
            raise InvalidDataException("User role must be either 'admin', 'staff', 'manager', or 'stockkeeper'")
        # Check if supplier_id is valid
        if not isinstance(supplier_id, int) or supplier_id <= 0:
            self.db.close_pool()
            raise InvalidDataException("Invalid supplier ID")
        # Fetch supplier by ID - all roles have same access
        result = self.db.execute_query(SupplierQueries.GET_ALL_SUPPLIERS_WITH_PRODUCTS, (supplier_id,))
        
        if not result:
            self.db.close_pool()
            raise NotFoundException(f"Supplier with ID {supplier_id} not found")
            
        # Fetch products for the supplier
        products_result = self.db.execute_query(SupplierQueries.GET_PRODUCTS_BY_SUPPLIER_ID, (supplier_id,))
        self.db.close_pool()
        
        products = []
        for prod_row in products_result:
            products.append({
                "product_id": prod_row[0],
                "product_name": prod_row[1],
                "description": prod_row[2],
                "price": float(prod_row[3]) if prod_row[3] is not None else 0.0,
                "quantity": prod_row[4],
                "category_name": prod_row[5] if prod_row[5] else "Uncategorized",
                "product_created_time": prod_row[6],
                "product_updated_time": prod_row[7]
            })

        row = result[0]
        supplier = {
            "supplier_id": row[0],
            "supplier_name": row[1],
            "contact_name": row[2],
            "contact_email": row[5],
            "phone": row[3],
            "address": row[4],
            "products": products
        }
        return supplier

    def create_supplier(self, supplier: dict):
        # Handle backward compatibility
        name = supplier.get("name")
        contact_email = supplier.get("contact_email")
        contact_name = supplier.get("contact_name")
        phone = supplier.get("phone")
        address = supplier.get("address")
        
        # at least one of contact_email or phone must be provided
        if not contact_email and not phone:
            raise InvalidDataException("At least one of contact_email or phone must be provided")
        if not contact_name:
            raise InvalidDataException("Contact name must be provided")
        
        # Create new supplier
        res = self.db.execute_query(
            SupplierQueries.CREATE_SUPPLIER,
            (name, contact_name, contact_email, phone, address)
        )
        self.db.close_pool()
        if  res:
            raise Exception("Failed to create supplier")
        return {}
        
        
    def update_supplier(self, supplier_id: int, supplier: SupplierData):
        # Check if supplier exists
        existing = self.db.execute_query(SupplierQueries.CHECK_SUPPLIER_EXISTS, (supplier_id,))
        if not existing:
            self.db.close_pool()
            raise NotFoundException(f"Supplier with ID {supplier_id} not found")

        current = existing[0]
        
        # Update only provided fields
        name = supplier.name if supplier.name is not None else current[1]
        contact_name = supplier.contact_name if supplier.contact_name is not None else current[2]
        
        # Handle backward compatibility for email
        contact_email = supplier.contact_email
        if contact_email is None and supplier.email is not None:
            contact_email = supplier.email
        if contact_email is None:
            contact_email = current[5]
            
        phone = supplier.phone if supplier.phone is not None else current[3]
        address = supplier.address if supplier.address is not None else current[4]

        # Update supplier
        res = self.db.execute_query(
            SupplierQueries.UPDATE_SUPPLIER,
            (name, contact_name, contact_email, phone, address, supplier_id)
        )

        self.db.close_pool() 
        if res is None:
            raise Exception("Failed to update supplier")       
        return {}
        

    def delete_supplier(self, supplier_id: int):
        # Check if supplier exists
        existing = self.db.execute_query(SupplierQueries.GET_ALL_SUPPLIERS_WITH_PRODUCTS, (supplier_id,))
        if not existing:
            self.db.close_pool()
            raise NotFoundException(f"Supplier with ID {supplier_id} not found")

        # Check for active products
        active_products_count = self.db.execute_query(SupplierQueries.COUNT_ACTIVE_PRODUCTS_BY_SUPPLIER_ID, (supplier_id,))
        if active_products_count and active_products_count[0][0] > 0:
            self.db.close_pool()
            raise InvalidDataException("Cannot delete supplier with existing products")
       
        # Nullify references in other tables to avoid foreign key constraints
        self.db.execute_query(SupplierQueries.NULLIFY_PRODUCT_SUPPLIER, (supplier_id,))
        self.db.execute_query(SupplierQueries.NULLIFY_INVENTORY_TICKET_SUPPLIER, (supplier_id,))

        # Delete supplier
        res = self.db.execute_query(SupplierQueries.DELETE_SUPPLIER, (supplier_id,))
        self.db.close_pool()
        if res is None:
            raise Exception("Failed to delete supplier")
        return {}
    
    def count_suppliers(self, user_info: dict) -> int:
        # Validate user_info is a dict
        if not isinstance(user_info, dict):
            self.db.close_pool()
            raise InvalidDataException("User info must be a dictionary")
        role_name = user_info.get("role_name", "").lower()
        if not role_name:
            self.db.close_pool()
            raise InvalidDataException("Role name must be provided in user info")
        if role_name not in ("admin", "staff", "manager", "stockkeeper"):
            self.db.close_pool()
            raise InvalidDataException("User role must be either 'admin', 'staff', 'manager', or 'stockkeeper'")
        
        # All roles have same access now
        result = self.db.execute_query(SupplierQueries.GET_ALL_SUPPLIERS)
        suppliers = []
        if not result:
            self.db.close_pool()
            return 0
        # Count unique suppliers
        unique_supplier_ids = set(row[0] for row in result)
        self.db.close_pool()
        return len(unique_supplier_ids)