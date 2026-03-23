class MaintenanceService:
    def __init__(self, db_manager) -> None:
        self.db = db_manager

    def create_request(self, tenant_id: int, apartment_id: int, issue_type: str, description: str, priority: str, request_date: str) -> None:
        if not issue_type or not description or not priority or not request_date:
            raise ValueError("All maintenance fields are required.")
        with self.db.get_connection() as conn:
            conn.execute(
                """INSERT INTO maintenance_requests(
                       tenant_id, apartment_id, issue_type, description, priority,
                       assigned_staff, request_date, completion_date, status, cost, hours_taken
                   ) VALUES (?, ?, ?, ?, ?, NULL, ?, NULL, 'Open', 0, 0)""",
                (tenant_id, apartment_id, issue_type, description, priority, request_date)
            )
            conn.commit()

    def update_request(self, request_id: int, status: str, assigned_staff: str = "", cost: float = 0.0, hours_taken: float = 0.0, completion_date: str | None = None) -> None:
        if cost < 0 or hours_taken < 0:
            raise ValueError("Cost and hours cannot be negative.")
        with self.db.get_connection() as conn:
            conn.execute(
                """UPDATE maintenance_requests
                   SET status = ?, assigned_staff = ?, cost = ?, hours_taken = ?, completion_date = ?
                   WHERE request_id = ?""",
                (status, assigned_staff or None, cost, hours_taken, completion_date, request_id)
            )
            conn.commit()

    def list_requests(self):
        with self.db.get_connection() as conn:
            rows = conn.execute("SELECT * FROM maintenance_requests ORDER BY request_id").fetchall()
            return [dict(row) for row in rows]
