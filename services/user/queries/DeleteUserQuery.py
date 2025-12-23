from shared_utils import Database

class DeleteUserQuery:
    def __init__(self):
        self.db = Database()
        
    def get_user_role(self, user_id: int):
        query = "SELECT role FROM users WHERE user_id = %s"
        params = (user_id,)
        result = self.db.execute_query(query, params)
        if not result:
            return None
        return result[0][0]
        
    def delete_user(self, user_id: int):
        query = "DELETE FROM users WHERE user_id = %s"
        params = (user_id,)
        result = self.db.execute_query(query, params)
        if result is None:
            return False
        return True
        
    def close(self):
        self.db.close_pool()
