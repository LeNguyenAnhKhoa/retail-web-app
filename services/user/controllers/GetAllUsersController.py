from queries import GetAllUsersQuery

class GetAllUsersController:
    def __init__(self):
        self.query = GetAllUsersQuery()
        
    def execute(self, user_info: dict):
        """
        Execute the GetAllUsersQuery and return the result.
        """
        role_name = user_info.get("role_name", "").lower()
        if role_name not in ("admin", "manager"):
            return []
        result = self.query.get_all_users()
        self.query.close()
        return result