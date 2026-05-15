from database.connection import DatabaseConnection


class AuthService:

    @staticmethod
    def login(username, password):

        db = DatabaseConnection()

        user = db.fetchone(
            """
            SELECT *
            FROM users
            WHERE username = ?
            AND password = ?
            """,
            (username, password)
        )

        db.close()

        return user
