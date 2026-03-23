# PAMS UML Content

## Use Case Diagram (PlantUML)
```plantuml
@startuml
left to right direction
actor FrontDeskStaff
actor FinanceManager
actor MaintenanceStaff
actor Administrator
actor Manager

rectangle PAMS {
  usecase "Register Tenant" as UC1
  usecase "Update Tenant Record" as UC2
  usecase "View Tenant Information" as UC3
  usecase "Register Complaint" as UC4
  usecase "Log Maintenance Request" as UC5
  usecase "Generate Invoice" as UC6
  usecase "Record Payment" as UC7
  usecase "View Late Payments" as UC8
  usecase "Generate Financial Report" as UC9
  usecase "View Assigned Requests" as UC10
  usecase "Update Maintenance Status" as UC11
  usecase "Log Cost and Time" as UC12
  usecase "Manage User Accounts" as UC13
  usecase "Manage Apartments" as UC14
  usecase "Track Lease End Dates" as UC15
  usecase "Generate Location Reports" as UC16
  usecase "View Occupancy Report" as UC17
  usecase "View Performance Report" as UC18
  usecase "Add New City" as UC19
}

FrontDeskStaff --> UC1
FrontDeskStaff --> UC2
FrontDeskStaff --> UC3
FrontDeskStaff --> UC4
FrontDeskStaff --> UC5

FinanceManager --> UC6
FinanceManager --> UC7
FinanceManager --> UC8
FinanceManager --> UC9

MaintenanceStaff --> UC10
MaintenanceStaff --> UC11
MaintenanceStaff --> UC12

Administrator --> UC13
Administrator --> UC14
Administrator --> UC15
Administrator --> UC16

Manager --> UC17
Manager --> UC18
Manager --> UC19
@enduml
```

## Class Diagram (PlantUML)
```plantuml
@startuml
class User {
  -user_id: int
  -full_name: str
  -username: str
  -password_hash: str
  -role: str
  -location: str
}

class Tenant {
  -tenant_id: int
  -ni_number: str
  -name: str
  -phone: str
  -email: str
  -occupation: str
  -references_text: str
  -status: str
}

class Apartment {
  -apartment_id: int
  -city: str
  -address: str
  -apartment_type: str
  -rooms: int
  -monthly_rent: float
  -occupancy_status: str
}

class Lease {
  -lease_id: int
  -start_date: str
  -end_date: str
  -deposit_amount: float
  -monthly_rent: float
  -active: int
  +calculate_early_exit_penalty(): float
}

class Payment {
  -payment_id: int
  -amount: float
  -due_date: str
  -payment_date: str
  -status: str
  -receipt_no: str
  +is_late(today): bool
}

class MaintenanceRequest {
  -request_id: int
  -issue_type: str
  -description: str
  -priority: str
  -assigned_staff: str
  -request_date: str
  -completion_date: str
  -status: str
  -cost: float
  -hours_taken: float
}

class Complaint {
  -complaint_id: int
  -description: str
  -complaint_date: str
  -status: str
}

Tenant "1" -- "0..*" Lease
Apartment "1" -- "0..*" Lease
Tenant "1" -- "0..*" Payment
Lease "1" -- "0..*" Payment
Tenant "1" -- "0..*" MaintenanceRequest
Apartment "1" -- "0..*" MaintenanceRequest
Tenant "1" -- "0..*" Complaint
User "1" -- "0..*" MaintenanceRequest : assigned_staff
@enduml
```

## Sequence Diagram 1: Register New Tenant
```plantuml
@startuml
actor FrontDeskStaff
participant "GUI" as GUI
participant "TenantService" as TS
participant "Database" as DB

FrontDeskStaff -> GUI: Enter tenant details
GUI -> TS: validate_tenant_data(...)
TS -> DB: INSERT tenant
DB --> TS: success
TS --> GUI: tenant created
GUI --> FrontDeskStaff: Show confirmation
@enduml
```

## Sequence Diagram 2: Record Rent Payment
```plantuml
@startuml
actor FinanceManager
participant "GUI" as GUI
participant "PaymentService" as PS
participant "Database" as DB

FinanceManager -> GUI: Select payment and submit payment
GUI -> PS: record_payment(payment_id, payment_date)
PS -> DB: UPDATE payments status='Paid'
DB --> PS: success
PS --> GUI: receipt number
GUI --> FinanceManager: Show receipt and success message
@enduml
```

## Sequence Diagram 3: Log and Resolve Maintenance Request
```plantuml
@startuml
actor FrontDeskStaff
actor MaintenanceStaff
participant "GUI" as GUI
participant "MaintenanceService" as MS
participant "Database" as DB

FrontDeskStaff -> GUI: Submit issue
GUI -> MS: create_request(...)
MS -> DB: INSERT maintenance request
DB --> MS: success
MS --> GUI: request logged

MaintenanceStaff -> GUI: Update request
GUI -> MS: update_request(...)
MS -> DB: UPDATE maintenance request
DB --> MS: success
MS --> GUI: request resolved
@enduml
```
