from dataclasses import dataclass

@dataclass
class Tenant:
    tenant_id: int | None
    ni_number: str
    name: str
    phone: str
    email: str
    occupation: str
    references_text: str
    status: str = "Active"
