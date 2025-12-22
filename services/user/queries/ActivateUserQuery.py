from shared_utils import Database

class ActivateUserQuery:
    def __init__(self):
        self.db = Database()
        
    def close(self):
        self.db.close_pool()

    def check_if_user_exists(self, user_id: int):
        """
        Check if a user exists in the database.

        :param user_id: The ID of the user to check.
        :return: True if the user exists, False otherwise.
        """
        query = "SELECT COUNT(*) FROM users WHERE user_id = %s"
        res = self.db.execute_query(query, (user_id,))
        if not res:
            return False
        return res[0][0] > 0

    def activate_user(self, user_id: int):
        """
        Activate a user in the database.

        :param user_id: The ID of the user to activate.
        :return: True if the user was activated successfully, False otherwise.
        """
        query = """
            UPDATE users
            SET is_active = 1
            WHERE user_id = %s
        """
        res = self.db.execute_query(query, (user_id,))
        return res is not None
