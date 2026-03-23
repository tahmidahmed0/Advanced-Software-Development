from database.db_manager import DatabaseManager
from gui.login_window import LoginWindow

def main() -> None:
    db = DatabaseManager()
    db.setup_database()
    db.seed_mock_data()
    app = LoginWindow(db)
    app.run()

if __name__ == "__main__":
    main()
