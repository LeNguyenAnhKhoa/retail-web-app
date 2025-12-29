from shared_utils import Database
from models import RegisterModel

class RegisterQuery:
    def __init__(self):
        self.db = Database()
        
    
    def check_email_exists(self, email: str):
        query = '''SELECT 
            user_id, 
            username, 
            email, 
            password_hash 
            FROM users 
            WHERE email = %s
        '''
        params = (email,)
        result = self.db.execute_query(query, params)
        if not result:
            return False
        return True
    
    def create_user(self, payload: RegisterModel):
        query = """
            INSERT INTO
                users (username, email, password_hash, full_name, phone, role, image_url, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        # dicebear 
        random_image_url = "https://api.dicebear.com/9.x/identicon/svg?seed=" + payload.username
        params = (
            payload.username,
            payload.email,
            payload.password,
            payload.username,  # Use username as full_name for now
            payload.phone,
            "STAFF",  # Default role
            random_image_url,
            False
        )
        result = self.db.execute_query(query, params)
        if result is None:
            return False
        return True
    
    def close(self):
        self.db.close_pool()