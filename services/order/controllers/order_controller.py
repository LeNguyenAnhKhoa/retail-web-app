from fastapi import HTTPException
from shared_utils.database import Database
from queries.order_queries import OrderQueries
from models.order import OrderResponse, OrderCreateData, OrderDetailData, Order, OrderDetail
from typing import Dict, List
from shared_utils.logger import logger
from shared_config.custom_exception import BadRequestException, NotFoundException
import datetime
import uuid

class OrderController:
    def __init__(self):
        self.db = Database()

    def _format_order_with_items(self, rows: List[tuple]) -> Dict:
        if not rows:
            logger.info("No rows to format")
            return {}
        
        # First row contains order data
        order_data = {
            "order_id": rows[0][0],
            "customer_id": rows[0][1],
            "status": rows[0][2],
            "order_date": rows[0][3],
            "created_time": rows[0][4],
            "updated_time": rows[0][5],
            "items": []
        }

        # Process all rows for order items
        for row in rows:
            if row[6] is not None:  # Check if there's an order item
                # Check if we already have this item
                item_id = row[6]
                existing_item = next((item for item in order_data["items"] if item["order_item_id"] == item_id), None)
                
                if existing_item:
                    continue  # Skip duplicate items
                
                item = {
                    "order_item_id": row[6],
                    "order_id": row[0],
                    "product_id": row[7],
                    "quantity": row[8],
                    "total_price": row[9]
                }
                order_data["items"].append(item)

        logger.info(f"Formatted order {order_data['order_id']} with {len(order_data['items'])} items")
        return order_data

    def get_all_orders(self, user_info, search=None):
        role_name = user_info.get("role_name", "").lower()
        if role_name not in ["admin", "staff", "manager", "stockkeeper"]:
            raise BadRequestException("Only admin, manager, staff, and stockkeeper can retrieve orders")
        
        # Handle search parameter - extract number from ORD-1000 format
        search_param = None
        if search:
            if search.startswith("ORD-"):
                search_param = f"%{search[4:]}%"  # Extract number part
            else:
                search_param = f"%{search}%"
        
        # All roles can see all orders since there's only one warehouse
        if search_param:
            result = self.db.execute_query(OrderQueries.GET_ALL_ORDERS_WITH_SEARCH, (search_param, search_param))
        else:
            result = self.db.execute_query(OrderQueries.GET_ALL_ORDERS)
        if result is None:
            raise Exception("Failed to retrieve orders from the database")
        
        orders = []
        for row in result:
            order_data = {
                "order_id": row[0],
                "order_code": row[1],
                "customer_id": row[2],
                "customer_name": row[3],
                "customer_phone": row[4],
                "user_id": row[5],
                "staff_name": row[6],
                "staff_role": row[7],
                "total_amount": row[8],
                "payment_method": row[9],
                "status": row[10],
                "total_items": row[11],
                "total_quantity": row[12],
                "total_profit": row[13],
                "created_at": row[14],
                "updated_at": row[15],
                "username": row[16],
            }
            if orders and orders[-1].get("order_id") == order_data.get("order_id"):
                continue
            orders.append(order_data)
        return orders

    def get_order(self, order_id: int, user_info: dict):
        role_name = user_info.get("role_name", "").lower()
        
        if not role_name:
            raise BadRequestException("Role Name is required")

        if role_name not in ["admin", "staff", "manager", "stockkeeper"]:
            raise BadRequestException("Only admin, manager, staff, and stockkeeper can retrieve orders")
        
        # All roles can see all orders since there's only one warehouse
        result = self.db.execute_query(OrderQueries.GET_ORDER_DETAIL, (order_id,))
        logger.info(f"Got result from database: {bool(result)}")
        if not result:
            raise NotFoundException(f"Cannot found order with ID {order_id}")
        order_data = {
            "order_id": result[0][0],
            "order_date": result[0][1],
            "order_status": result[0][2],
            "customer_id": result[0][3],
            "customer_name": result[0][4],
            "customer_email": result[0][5],
            "customer_phone": result[0][6],
            "items": [],
            "total_items": 0,
            "total_price": 0
        }
        for row in result:
            item = {
                "order_item_id": row[7],
                "product_id": row[8],
                "product_name": row[9],
                "product_price": row[10],
                "quantity_ordered": row[11],
                "price": row[12]
            }
            order_data["items"].append(item)
            order_data["total_items"] += 1
            order_data["total_price"] += item["price"]
        if order_data and order_data.get("order_id") is None:
            return {}
        return order_data

    def create_order(self, order: dict, user_info: dict):
        user_id = user_info.get("user_id")
        if not user_id:
            raise BadRequestException("User ID is required")

        # Generate order code
        order_code = f"ORD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        product_ids = []
        quantities = []
        prices = []
        receives = []
        give_backs = []
        
        for item in order["items"]:
            product_ids.append(str(item["product_id"]))
            quantities.append(str(item["quantity"]))
            prices.append(str(item["price"]))
            
            receive = float(item.get("receive", 0))
            quantity = int(item["quantity"])
            price = float(item["price"])
            
            if receive < quantity * price:
                 raise BadRequestException(f"Receive amount {receive} is less than total price {quantity * price} for product {item['product_id']}")
            
            give_back = receive - (quantity * price)
            
            receives.append(str(receive))
            give_backs.append(str(give_back))
            
        if not product_ids:
             raise BadRequestException("No items in order")

        # Fetch cost prices (import_price) for products
        placeholders = ','.join(['%s'] * len(product_ids))
        query = f"SELECT product_id, import_price FROM products WHERE product_id IN ({placeholders})"
        
        products_result = self.db.execute_query(query, tuple(product_ids))
        if not products_result:
             raise BadRequestException("Products not found")
             
        cost_map = {str(row[0]): row[1] for row in products_result}
        
        cost_prices = []
        for pid in product_ids:
            cost = cost_map.get(pid)
            if cost is None:
                raise BadRequestException(f"Product {pid} not found")
            cost_prices.append(str(cost))
        
        # Convert lists to comma-separated strings
        product_ids_str = ','.join(product_ids)
        quantities_str = ','.join(quantities)
        prices_str = ','.join(prices)
        cost_prices_str = ','.join(cost_prices)
        receives_str = ','.join(receives)
        give_backs_str = ','.join(give_backs)
        
        logger.info(f"Calling CreateOrderWithDetails procedure with: customer_id={order['customer_id']}, "
                    f"product_ids={product_ids_str}, quantities={quantities_str}, prices={prices_str}")
        
        # Call the CreateOrder stored procedure
        res = self.db.execute_query(OrderQueries.CREATE_ORDER_PROCEDURE, (
            order_code,
            order["customer_id"],
            user_id,
            order.get("payment_method", "CASH"),
            product_ids_str,
            quantities_str,
            prices_str,
            cost_prices_str,
            receives_str,
            give_backs_str
        ))
        if res is None:
            logger.error("Failed to create order in the database")
            raise Exception("Failed to create order in the database")
        
        return {}
      

    def update_order(self, order_id: int, order: OrderCreateData, user_info: dict = None):
        result = self.db.execute_query(OrderQueries.GET_ORDER_BY_ID, (order_id,))
        if not result:
            raise NotFoundException(f"Order with ID {order_id} not found")
        
        # We'll just update the order status for simplicity
        # In a real application, you might want to update items as well
        
        # Start transaction
        self.db.execute_query("START TRANSACTION;")
        logger.info(f"Updating order with ID {order_id}")
        
        # Update order status
        update_query = """
            UPDATE orders SET status = %s WHERE order_id = %s
        """
        res = self.db.execute_query(update_query, (order.status, order_id))
        
        logger.info(f"Updated order {order_id} status to {order.status}")
        if res is None:
            raise Exception("Failed to update order status in the database")
        return {}
        
            
    def delete_order(self, order_id: int):
        result = self.db.execute_query(OrderQueries.GET_ORDER_BY_ID, (order_id,))
        if not result:
            raise NotFoundException(f"Order with ID {order_id} not found")
        
        # We need to delete in the correct order due to foreign key constraints
        # First, delete from order_details
        res = self.db.execute_query(OrderQueries.DELETE_ORDER_ITEMS, (order_id,))
        logger.info(f"Deleted all items for order {order_id}")
        if res is None:
            raise Exception("Failed to delete order items from the database")
            
        # Finally delete the order
        res = self.db.execute_query(OrderQueries.DELETE_ORDER, (order_id,))
        logger.info(f"Deleted order {order_id}")
        if res is None:
            raise Exception("Failed to delete order from the database")

        return {}


    def update_order_status(self, order_id: int, status: str):
        # Validate input
        if order_id <= 0:
            raise BadRequestException("Invalid order ID")
        if not status:
            raise BadRequestException("Status cannot be empty")
        
        # Check if order exists and get current status
        check_result = self.db.execute_query("SELECT status FROM orders WHERE order_id = %s", (order_id,))
        if not check_result:
            raise NotFoundException("Order does not exist")
        
        current_status = check_result[0][0]
        
        # If cancelling an order that was previously active, restore stock quantities
        if status.lower() == "cancelled" and current_status.lower() != "cancelled":
            logger.info(f"Cancelling order {order_id}, restoring stock quantities")
            
            # Get all order items with their quantities
            order_items_result = self.db.execute_query(OrderQueries.GET_ORDER_ITEMS_FOR_CANCELLATION, (order_id,))
            
            if order_items_result:
                # For each product in the order, restore the quantity
                for row in order_items_result:
                    product_id = row[0]
                    quantity = row[1]
                    
                    # Call UpdateProductQuantity procedure to add back the quantity
                    logger.info(f"Restoring {quantity} units for product {product_id}")
                    restore_result = self.db.execute_query(OrderQueries.UPDATE_PRODUCT_QUANTITY_PROCEDURE, (product_id, quantity))
                    
                    if restore_result is None:
                        logger.error(f"Failed to restore quantity for product {product_id}")
                        raise Exception(f"Failed to restore stock quantity for product {product_id}")

        # If reactivating a cancelled order, deduct stock quantities
        elif current_status.lower() == "cancelled" and status.lower() != "cancelled":
            logger.info(f"Reactivating order {order_id}, deducting stock quantities")
            
            # Get all order items with their quantities
            order_items_result = self.db.execute_query(OrderQueries.GET_ORDER_ITEMS_FOR_CANCELLATION, (order_id,))
            
            if order_items_result:
                # For each product in the order, deduct the quantity
                for row in order_items_result:
                    product_id = row[0]
                    quantity = row[1]
                    
                    # Call UpdateProductQuantity procedure to deduct the quantity (pass negative value)
                    logger.info(f"Deducting {quantity} units for product {product_id}")
                    restore_result = self.db.execute_query(OrderQueries.UPDATE_PRODUCT_QUANTITY_PROCEDURE, (product_id, -quantity))
                    
                    if restore_result is None:
                        logger.error(f"Failed to deduct quantity for product {product_id}")
                        raise Exception(f"Failed to deduct stock quantity for product {product_id}")
        
        # Update the order status
        result = self.db.execute_query(OrderQueries.UPDATE_ORDER_STATUS, (status, order_id))
        
        if result is None:
            raise Exception("Failed to update order status")
        
        return f"Order {order_id} status updated to {status}"

    def get_recent_completed_orders(self, user_info):
        user_id = user_info.get("user_id")
        role_name = user_info.get("role_name", "").lower()
        
        if not user_id:
            raise BadRequestException("User ID is required to retrieve orders")
        if role_name not in ["admin", "staff", "manager", "stockkeeper"]:
            raise BadRequestException("Only admin, manager, staff, and stockkeeper can retrieve orders")
        
        # Admin/Manager can see all recent completed orders, staff/stockkeeper only sees their own orders
        if role_name in ("admin", "manager"):
            result = self.db.execute_query(OrderQueries.GET_RECENT_COMPLETED_ORDERS)
        else:  # staff, stockkeeper
            result = self.db.execute_query(OrderQueries.GET_RECENT_COMPLETED_ORDERS_BY_USER, (user_id,))
        
        if result is None:
            raise Exception("Failed to retrieve recent completed orders from the database")
        
        orders = []
        for row in result:
            order_data = {
                "order_id": row[0],
                "customer_name": row[1] if row[1] else "Khách vãng lai",
                "total_order_value": float(row[2]) if row[2] else 0.0,
                "order_date": row[3].strftime('%Y-%m-%d') if row[3] else None
            }
            orders.append(order_data)
        
        return orders
