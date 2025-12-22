from queries import MonthlySalesQuery

class MonthlySalesController:
    def __init__(self):
        self.query = MonthlySalesQuery()
    
    def execute(self, user_info):
        """Get monthly sales data based on user role"""
        try:
            # Get monthly sales data (no warehouse filtering needed)
            monthly_sales_data = self.query.get_monthly_sales_summary()
            self.query.close()
            if not monthly_sales_data:
                return {"message": "No sales data available for the specified period."}
            
            return monthly_sales_data
            
        except Exception as e:
            raise Exception(f"Error fetching monthly sales data: {str(e)}")
        finally:
            self.query.close()
