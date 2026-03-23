import hashlib
import os
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "pams.db"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

class DatabaseManager:
    def __init__(self) -> None:
        self.db_path = DB_PATH

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def setup_database(self) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                location TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS tenants (
                tenant_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ni_number TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                occupation TEXT NOT NULL,
                references_text TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Active'
            );

            CREATE TABLE IF NOT EXISTS apartments (
                apartment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                address TEXT NOT NULL UNIQUE,
                apartment_type TEXT NOT NULL,
                rooms INTEGER NOT NULL CHECK(rooms > 0),
                monthly_rent REAL NOT NULL CHECK(monthly_rent >= 0),
                occupancy_status TEXT NOT NULL DEFAULT 'Vacant'
            );

            CREATE TABLE IF NOT EXISTS leases (
                lease_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_id INTEGER NOT NULL,
                apartment_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                deposit_amount REAL NOT NULL CHECK(deposit_amount >= 0),
                monthly_rent REAL NOT NULL CHECK(monthly_rent >= 0),
                active INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE,
                FOREIGN KEY (apartment_id) REFERENCES apartments(apartment_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS payments (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_id INTEGER NOT NULL,
                lease_id INTEGER NOT NULL,
                amount REAL NOT NULL CHECK(amount >= 0),
                due_date TEXT NOT NULL,
                payment_date TEXT,
                status TEXT NOT NULL,
                receipt_no TEXT,
                FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE,
                FOREIGN KEY (lease_id) REFERENCES leases(lease_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS maintenance_requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_id INTEGER NOT NULL,
                apartment_id INTEGER NOT NULL,
                issue_type TEXT NOT NULL,
                description TEXT NOT NULL,
                priority TEXT NOT NULL,
                assigned_staff TEXT,
                request_date TEXT NOT NULL,
                completion_date TEXT,
                status TEXT NOT NULL,
                cost REAL NOT NULL DEFAULT 0 CHECK(cost >= 0),
                hours_taken REAL NOT NULL DEFAULT 0 CHECK(hours_taken >= 0),
                FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE,
                FOREIGN KEY (apartment_id) REFERENCES apartments(apartment_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS complaints (
                complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                complaint_date TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE
            );
            """)
            conn.commit()

    def seed_mock_data(self) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            existing = cursor.execute("SELECT COUNT(*) AS count FROM users").fetchone()["count"]
            if existing:
                return

            users = [
                ("Alice Admin", "admin", hash_password("Admin123!"), "Administrator", "Bristol"),
                ("Frank Frontdesk", "frontdesk", hash_password("Front123!"), "FrontDeskStaff", "Cardiff"),
                ("Fiona Finance", "finance", hash_password("Finance123!"), "FinanceManager", "London"),
                ("Mandy Maintenance", "maintenance", hash_password("Maint123!"), "MaintenanceStaff", "Manchester"),
                ("Mark Manager", "manager", hash_password("Manager123!"), "Manager", "Bristol"),
            ]
            cursor.executemany(
                "INSERT INTO users(full_name, username, password_hash, role, location) VALUES (?, ?, ?, ?, ?)",
                users
            )

            apartments = [
                ("Bristol", "12 Queen Square", "2-Bed Flat", 2, 1200, "Occupied"),
                ("Cardiff", "3 River View", "Studio", 1, 800, "Vacant"),
                ("London", "8 Park Lane", "1-Bed Flat", 1, 1600, "Occupied"),
                ("Manchester", "25 Oak Street", "3-Bed House", 3, 1450, "Vacant"),
            ]
            cursor.executemany(
                "INSERT INTO apartments(city, address, apartment_type, rooms, monthly_rent, occupancy_status) VALUES (?, ?, ?, ?, ?, ?)",
                apartments
            )

            tenants = [
                ("QQ123456A", "John Carter", "07111111111", "john@example.com", "Engineer", "Employer + landlord reference", "Active"),
                ("AB123456C", "Sarah Lee", "07222222222", "sarah@example.com", "Teacher", "Employer + ID check", "Active"),
            ]
            cursor.executemany(
                "INSERT INTO tenants(ni_number, name, phone, email, occupation, references_text, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                tenants
            )

            cursor.execute("""INSERT INTO leases(tenant_id, apartment_id, start_date, end_date, deposit_amount, monthly_rent, active)
                              VALUES (1, 1, '2026-01-01', '2026-12-31', 1200, 1200, 1)""")
            cursor.execute("""INSERT INTO leases(tenant_id, apartment_id, start_date, end_date, deposit_amount, monthly_rent, active)
                              VALUES (2, 3, '2026-02-01', '2027-01-31', 1600, 1600, 1)""")

            cursor.execute("""INSERT INTO payments(tenant_id, lease_id, amount, due_date, payment_date, status, receipt_no)
                              VALUES (1, 1, 1200, '2026-03-01', '2026-03-01', 'Paid', 'RCT-1001')""")
            cursor.execute("""INSERT INTO payments(tenant_id, lease_id, amount, due_date, payment_date, status, receipt_no)
                              VALUES (2, 2, 1600, '2026-03-01', NULL, 'Pending', NULL)""")

            cursor.execute("""INSERT INTO maintenance_requests(tenant_id, apartment_id, issue_type, description, priority, assigned_staff, request_date, completion_date, status, cost, hours_taken)
                              VALUES (1, 1, 'Plumbing', 'Leaking kitchen tap', 'Medium', 'Mandy Maintenance', '2026-03-05', NULL, 'Open', 0, 0)""")

            conn.commit()
