import unittest
from pathlib import Path
from database.db_manager import DatabaseManager
from services.maintenance_service import MaintenanceService

class TestMaintenanceService(unittest.TestCase):
    def setUp(self):
        db_file = Path("database/pams.db")
        if db_file.exists():
            db_file.unlink()
        self.db = DatabaseManager()
        self.db.setup_database()
        with self.db.get_connection() as conn:
            conn.execute("INSERT INTO tenants(ni_number, name, phone, email, occupation, references_text, status) VALUES ('AA123456A', 'T User', '07123456789', 't@example.com', 'Tester', 'Ref', 'Active')")
            conn.execute("INSERT INTO apartments(city, address, apartment_type, rooms, monthly_rent, occupancy_status) VALUES ('Bristol', 'Flat 1', '1-Bed Flat', 1, 900, 'Vacant')")
            conn.commit()
        self.service = MaintenanceService(self.db)

    def test_create_request(self):
        self.service.create_request(1, 1, "Electrical", "Light not working", "Low", "2026-03-01")
        self.assertEqual(len(self.service.list_requests()), 1)

    def test_negative_cost_raises(self):
        self.service.create_request(1, 1, "Electrical", "Light not working", "Low", "2026-03-01")
        with self.assertRaises(ValueError):
            self.service.update_request(1, "Closed", cost=-5)

if __name__ == "__main__":
    unittest.main()
