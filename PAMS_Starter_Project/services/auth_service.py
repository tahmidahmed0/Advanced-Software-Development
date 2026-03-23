from database.db_manager import hash_password

class AuthService:
    def __init__(self, db_manager) -> None:
        self.db = db_manager

    def login(self, username: str, password: str):
        with self.db.get_connection() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            ).fetchone()
            if not user:
                return None
            if user["password_hash"] != hash_password(password):
                return None
            return dict(user)
