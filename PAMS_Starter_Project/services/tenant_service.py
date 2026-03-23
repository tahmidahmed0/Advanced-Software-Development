import re

class TenantService:
    def __init__(self, db_manager) -> None:
        self.db = db_manager

    def validate_tenant_data(self, ni_number: str, name: str, phone: str, email: str, occupation: str, references_text: str) -> None:
        if not all([ni_number.strip(), name.strip(), phone.strip(), email.strip(), occupation.strip(), references_text.strip()]):
            raise ValueError("All tenant fields are required.")
        if len(phone) < 10 or not phone.replace("+", "").isdigit():
            raise ValueError("Phone number is invalid.")
        if "@" not in email or "." not in email:
            raise ValueError("Email is invalid.")

    def add_tenant(self, ni_number: str, name: str, phone: str, email: str, occupation: str, references_text: str) -> None:
        self.validate_tenant_data(ni_number, name, phone, email, occupation, references_text)
        with self.db.get_connection() as conn:
            conn.execute(
                """INSERT INTO tenants(ni_number, name, phone, email, occupation, references_text, status)
                   VALUES (?, ?, ?, ?, ?, ?, 'Active')""",
                (ni_number, name, phone, email, occupation, references_text)
            )
            conn.commit()

    def list_tenants(self):
        with self.db.get_connection() as conn:
            rows = conn.execute("SELECT * FROM tenants ORDER BY tenant_id").fetchall()
            return [dict(row) for row in rows]
