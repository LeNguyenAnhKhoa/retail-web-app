from shared_utils import Database


class GetAllUsersQuery:
    def __init__(self):
        self.db = Database()

    def get_all_users(self):
        """
        Get all users from the database.
        """
        query = """
            SELECT
                user_id,
                username,
                email,
                role,
                is_active,
                created_at,
                image_url
            FROM users
            LIMIT 100
        """
        result = self.db.execute_query(query)
        if result is None:
            return []
        result = [
            {
                "user_id": row[0],
                "username": row[1],
                "email": row[2],
                "role_name": row[3],
                "is_active": row[4],
                "created_time": row[5],
                "image_url": row[6],
            }
            for row in result
        ]
        return result

    def close(self):
        """
        Close the database connection.
        """
        self.db.close_pool()