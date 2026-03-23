import unittest
from pathlib import Path
from database.db_manager import DatabaseManager
from services.apartment_service import ApartmentService

class TestApartmentService(unittest.TestCase):
    def setUp(self):
        db_file = Path("database/pams.db")
        if db_file.exists():
            db_file.unlink()
        self.db = DatabaseManager()
        self.db.setup_database()
        self.service = ApartmentService(self.db)

    def test_add_valid_apartment(self):
        self.service.add_apartment("Bristol", "10 High Street", "Studio", 1, 800)
        self.assertEqual(len(self.service.list_apartments()), 1)

    def test_negative_rent_raises(self):
        with self.assertRaises(ValueError):
            self.service.add_apartment("Bristol", "10 High Street", "Studio", 1, -1)

if __name__ == "__main__":
    unittest.main()
