from datetime import date
import uuid

class PaymentService:
    def __init__(self, db_manager) -> None:
        self.db = db_manager

    def generate_invoice(self, tenant_id: int, lease_id: int, amount: float, due_date: str) -> None:
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        with self.db.get_connection() as conn:
            conn.execute(
                """INSERT INTO payments(tenant_id, lease_id, amount, due_date, payment_date, status, receipt_no)
                   VALUES (?, ?, ?, ?, NULL, 'Pending', NULL)""",
                (tenant_id, lease_id, amount, due_date)
            )
            conn.commit()

    def record_payment(self, payment_id: int, payment_date: str | None = None) -> str:
        paid_on = payment_date or date.today().isoformat()
        receipt_no = f"RCT-{uuid.uuid4().hex[:8].upper()}"
        with self.db.get_connection() as conn:
            conn.execute(
                """UPDATE payments
                   SET payment_date = ?, status = 'Paid', receipt_no = ?
                   WHERE payment_id = ?""",
                (paid_on, receipt_no, payment_id)
            )
            conn.commit()
        return receipt_no

    def list_payments(self):
        with self.db.get_connection() as conn:
            rows = conn.execute("SELECT * FROM payments ORDER BY payment_id").fetchall()
            return [dict(row) for row in rows]

    def late_payments(self, today: str):
        with self.db.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM payments WHERE status != 'Paid' AND due_date < ? ORDER BY due_date",
                (today,)
            ).fetchall()
            return [dict(row) for row in rows]
