class ApartmentService:
    def __init__(self, db_manager) -> None:
        self.db = db_manager

    def add_apartment(self, city: str, address: str, apartment_type: str, rooms: int, monthly_rent: float) -> None:
        if not city or not address or not apartment_type:
            raise ValueError("All apartment fields are required.")
        if rooms <= 0:
            raise ValueError("Rooms must be greater than zero.")
        if monthly_rent < 0:
            raise ValueError("Monthly rent cannot be negative.")
        with self.db.get_connection() as conn:
            conn.execute(
                """INSERT INTO apartments(city, address, apartment_type, rooms, monthly_rent, occupancy_status)
                   VALUES (?, ?, ?, ?, ?, 'Vacant')""",
                (city, address, apartment_type, rooms, monthly_rent)
            )
            conn.commit()

    def list_apartments(self):
        with self.db.get_connection() as conn:
            rows = conn.execute("SELECT * FROM apartments ORDER BY apartment_id").fetchall()
            return [dict(row) for row in rows]
