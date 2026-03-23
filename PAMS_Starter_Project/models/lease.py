from dataclasses import dataclass

@dataclass
class Lease:
    lease_id: int | None
    tenant_id: int
    apartment_id: int
    start_date: str
    end_date: str
    deposit_amount: float
    monthly_rent: float
    active: int = 1

    def calculate_early_exit_penalty(self) -> float:
        return round(self.monthly_rent * 0.05, 2)
