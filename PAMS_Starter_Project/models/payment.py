from dataclasses import dataclass
from datetime import date

@dataclass
class Payment:
    payment_id: int | None
    tenant_id: int
    lease_id: int
    amount: float
    due_date: str
    payment_date: str | None
    status: str
    receipt_no: str | None = None

    def is_late(self, today: str | None = None) -> bool:
        check_date = today or date.today().isoformat()
        return self.status != "Paid" and check_date > self.due_date
