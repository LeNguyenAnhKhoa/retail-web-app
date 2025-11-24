from queries import CountTotalProductsQuery

class CountTotalProductsController:
    def __init__(self):
        self.query = CountTotalProductsQuery()

    def execute(self, user_info, search: str = None):
        # Validate user_info is a dict
        if not isinstance(user_info, dict):
            self.query.close()
            raise ValueError("user_info must be a dictionary")
        # Validate role_name
        role = user_info.get('role_name', '').lower()
        if not role:
            self.query.close()
            raise ValueError("Missing 'role_name' in user_info")
        try:
            result = self.query.count_all_products(search=search)
            self.query.close()
            return {'total_products': result}
        finally:
            self.query.close()
