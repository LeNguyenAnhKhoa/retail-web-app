from shared_utils import Database
from models import UserModel

class GetUserDetailQuery:
    def __init__(self):
        self.db = Database()
        
    
    def execute(self, user_id: str):
        query = """
            SELECT 
                user_id,
                username,
                email,
                full_name,
                phone,
                role,
                image_url,
                is_active
            FROM users 
            WHERE user_id = %s
            AND is_active = TRUE
        """
        params = (user_id,)
        result = self.db.execute_query(query, params)
        if not result:
            return None
        user = result[0]
        res = UserModel(
            user_id=user[0],
            username=user[1],
            full_name=user[3],
            phone=user[4],
            role=user[5],
            is_active=user[7]
        )
        
        return res
    
    def close(self):
        self.db.close_pool()