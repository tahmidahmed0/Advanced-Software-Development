class ReportService:
    def __init__(self, db_manager) -> None:
        self.db = db_manager

    def occupancy_report(self):
        query = """
        SELECT city,
               COUNT(*) AS total_apartments,
               SUM(CASE WHEN occupancy_status = 'Occupied' THEN 1 ELSE 0 END) AS occupied,
               SUM(CASE WHEN occupancy_status = 'Vacant' THEN 1 ELSE 0 END) AS vacant
        FROM apartments
        GROUP BY city
        ORDER BY city
        """
        with self.db.get_connection() as conn:
            return [dict(row) for row in conn.execute(query).fetchall()]

    def financial_report(self):
        query = """
        SELECT
            SUM(CASE WHEN status = 'Paid' THEN amount ELSE 0 END) AS collected,
            SUM(CASE WHEN status != 'Paid' THEN amount ELSE 0 END) AS pending
        FROM payments
        """
        with self.db.get_connection() as conn:
            row = conn.execute(query).fetchone()
            return dict(row)

    def maintenance_cost_report(self):
        query = """
        SELECT status, COUNT(*) AS total_requests, SUM(cost) AS total_cost
        FROM maintenance_requests
        GROUP BY status
        ORDER BY status
        """
        with self.db.get_connection() as conn:
            return [dict(row) for row in conn.execute(query).fetchall()]
