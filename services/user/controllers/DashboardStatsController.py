from queries import DashboardStatsQuery
from shared_config.custom_exception import InvalidDataException, BadRequestException

class DashboardStatsController:
    def __init__(self):
        self.query = DashboardStatsQuery()
        
    def execute(self, user_info: dict):
        """
        Get comprehensive dashboard statistics based on user role
        """
        try:
            # Validate user info
            if not isinstance(user_info, dict):
                raise InvalidDataException("User info must be a dictionary")
                
            role_name = user_info.get("role_name")
            
            if not role_name:
                raise InvalidDataException("Role name must be provided in user info")
            
            # Convert role_name to lowercase for comparison
            role_name_lower = role_name.lower()
                
            if role_name_lower not in ("admin", "staff", "manager", "stockkeeper"):
                raise InvalidDataException("User role must be either 'admin', 'staff', 'manager', or 'stockkeeper'")
            
            # Get all statistics (no warehouse filtering needed)
            revenue_stats = self.query.get_revenue_stats()
            products_stats = self.query.get_products_stats()
            orders_stats = self.query.get_orders_stats()
            customers_stats = self.query.get_customers_stats()
            self.query.close()
            return {
                "revenue": {
                    "total": revenue_stats['total_revenue'],
                    "current_month": revenue_stats['current_month_revenue'],
                    "previous_month": revenue_stats['previous_month_revenue'],
                    "month_over_month_change": revenue_stats['month_over_month_change']
                },
                "products": {
                    "total": products_stats['total_products'],
                    "current_month": products_stats['current_month_products'],
                    "previous_month": products_stats['previous_month_products'],
                    "month_over_month_change": products_stats['month_over_month_change']
                },
                "orders": {
                    "total": orders_stats['total_orders'],
                    "current_month": orders_stats['current_month_orders'],
                    "previous_month": orders_stats['previous_month_orders'],
                    "month_over_month_change": orders_stats['month_over_month_change']
                },
                "customers": {
                    "total": customers_stats['total_customers'],
                    "current_month": customers_stats['current_month_customers'],
                    "previous_month": customers_stats['previous_month_customers'],
                    "month_over_month_change": customers_stats['month_over_month_change']
                }
            }
            
        except Exception as e:
            raise e
        finally:
            self.query.close()
