from queries import DeleteUserQuery
from shared_config.custom_exception import ForbiddenException, NotFoundException, InvalidDataException

class DeleteUserController:
    def __init__(self):
        self.query = DeleteUserQuery()
        
    def execute(self, user_id: int, user_info: dict):
        # Check if the requester is a manager
        # print(f"DEBUG: user_info={user_info}")
        role_name = user_info.get("role_name")
        if not role_name:
            role_name = user_info.get("role")
            
        if not role_name:
            self.query.close()
            raise ForbiddenException("You are not authorized to perform this action")
            
        role_name = str(role_name).lower()
        if role_name not in ("admin", "manager"):
            self.query.close()
            raise ForbiddenException("You are not authorized to perform this action")
            
        # Check if the user to be deleted exists and get their role
        target_user_role = self.query.get_user_role(user_id)
        
        if not target_user_role:
            self.query.close()
            raise NotFoundException("User not found")
            
        # Cannot delete a manager
        if target_user_role == "MANAGER":
            self.query.close()
            raise ForbiddenException("Cannot delete a manager")
            
        # Delete the user
        res = self.query.delete_user(user_id)
        self.query.close()
        
        if not res:
            raise InvalidDataException("Failed to delete user")
            
        return True
