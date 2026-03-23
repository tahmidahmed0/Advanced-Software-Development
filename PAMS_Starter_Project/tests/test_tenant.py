import unittest
from pathlib import Path
from database.db_manager import DatabaseManager
from services.tenant_service import TenantService

class TestTenantService(unittest.TestCase):
    def setUp(self):
        db_file = Path("database/pams.db")
        if db_file.exists():
            db_file.unlink()
        self.db = DatabaseManager()
        self.db.setup_database()
        self.service = TenantService(self.db)

    def test_add_valid_tenant(self):
        self.service.add_tenant("AA123456A", "Test User", "07123456789", "test@example.com", "Engineer", "Reference")
        tenants = self.service.list_tenants()
        self.assertEqual(len(tenants), 1)

    def test_invalid_email_raises(self):
        with self.assertRaises(ValueError):
            self.service.add_tenant("AA123456A", "Test User", "07123456789", "bademail", "Engineer", "Reference")

if __name__ == "__main__":
    unittest.main()
