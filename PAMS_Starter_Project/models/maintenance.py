from dataclasses import dataclass

@dataclass
class MaintenanceRequest:
    request_id: int | None
    tenant_id: int
    apartment_id: int
    issue_type: str
    description: str
    priority: str
    assigned_staff: str | None
    request_date: str
    completion_date: str | None
    status: str
    cost: float = 0.0
    hours_taken: float = 0.0
