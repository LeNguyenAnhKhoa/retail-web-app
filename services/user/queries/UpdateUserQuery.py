from shared_utils import Database
from models import UpdateUserModel, AdminUpdateUserModel

class UpdateUserQuery:
    def __init__(self):
        self.db = Database()
        
    def update_user_by_email(self, update_user: UpdateUserModel, user_email: str):
        query = """
            UPDATE users
            SET username = %s,
                image_url = %s
            WHERE email = %s
        """
        params = (
            update_user.username,
            update_user.image_url,
            user_email
        )
        res = self.db.execute_query(query, params)
        if res is None:
            return False
        return True

    def update_user_by_id(self, update_user: AdminUpdateUserModel):
        # Build query dynamically based on provided fields
        fields = []
        params = []

        if update_user.username:
            fields.append("username = %s")
            params.append(update_user.username)
        
        if update_user.full_name:
            fields.append("full_name = %s")
            params.append(update_user.full_name)
            
        if update_user.phone:
            fields.append("phone = %s")
            params.append(update_user.phone)
            
        if update_user.role:
            fields.append("role = %s")
            params.append(update_user.role)

        if not fields:
            return True # Nothing to update

        query = f"UPDATE users SET {', '.join(fields)} WHERE user_id = %s"
        params.append(update_user.user_id)

        res = self.db.execute_query(query, tuple(params))
        if res is None:
            return False
        return True
    
    def check_phone_exists_exclude_user(self, phone: str, user_id: int):
        query = '''SELECT 
            user_id
            FROM users 
            WHERE phone = %s AND user_id != %s
        '''
        params = (phone, user_id)
        result = self.db.execute_query(query, params)
        if not result:
            return False
        return True
    
    def close(self):
        self.db.close_pool()