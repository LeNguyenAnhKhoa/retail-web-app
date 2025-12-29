from queries import UpdateUserQuery
from models import AdminUpdateUserModel
from shared_config.custom_exception import InvalidDataException, BadRequestException, ForbiddenException
from shared_utils import logger
import re

class UpdateUserByAdminController:
    def __init__(self):
        self.query = UpdateUserQuery()
        
    def execute(self, update_user: AdminUpdateUserModel, user_info: dict):
        # Check if requester is MANAGER
        requester_role = user_info.get("role_name")
        if requester_role != "MANAGER":
            self.query.close()
            raise ForbiddenException("Only MANAGER can perform this action")

        if not update_user.user_id or not isinstance(update_user.user_id, int) or update_user.user_id <= 0:
            self.query.close()
            raise InvalidDataException("Invalid user ID")
        
        if update_user.username and (not isinstance(update_user.username, str) or not re.match(r'^[a-zA-Z0-9_]+$', update_user.username)):
            self.query.close()
            raise InvalidDataException("Invalid username")
            
        if update_user.phone and (not isinstance(update_user.phone, str) or not re.match(r'^\d{10,11}$', update_user.phone)):
             self.query.close()
             raise InvalidDataException("Invalid phone number")

        res = self.query.update_user_by_id(update_user)
        logger.info(f"Update user by admin: {user_info.get('email')} updated user {update_user.user_id} with data: {update_user}")
        self.query.close()
        if not res:
            raise BadRequestException("Failed to update user")
        return True
