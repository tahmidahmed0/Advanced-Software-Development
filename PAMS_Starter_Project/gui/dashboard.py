import tkinter as tk
from tkinter import ttk, messagebox
from services.tenant_service import TenantService
from services.apartment_service import ApartmentService
from services.payment_service import PaymentService
from services.maintenance_service import MaintenanceService
from services.report_service import ReportService

class DashboardWindow:
    def __init__(self, db_manager, user: dict) -> None:
        self.db = db_manager
        self.user = user
        self.root = tk.Tk()
        self.root.title("PAMS Dashboard")
        self.root.geometry("900x550")
        self.tenant_service = TenantService(self.db)
        self.apartment_service = ApartmentService(self.db)
        self.payment_service = PaymentService(self.db)
        self.maintenance_service = MaintenanceService(self.db)
        self.report_service = ReportService(self.db)
        self.build_ui()

    def build_ui(self) -> None:
        top = tk.Frame(self.root)
        top.pack(fill="x", pady=10)
        tk.Label(
            top,
            text=f"Welcome {self.user['full_name']} ({self.user['role']}, {self.user['location']})",
            font=("Arial", 12, "bold")
        ).pack()

        self.output = tk.Text(self.root, width=110, height=28)
        self.output.pack(padx=10, pady=10)

        button_bar = tk.Frame(self.root)
        button_bar.pack(fill="x")

        role = self.user["role"]
        if role in {"FrontDeskStaff", "Administrator"}:
            tk.Button(button_bar, text="List Tenants", command=self.show_tenants).pack(side="left", padx=4)
            tk.Button(button_bar, text="List Apartments", command=self.show_apartments).pack(side="left", padx=4)
        if role in {"FinanceManager", "Administrator", "Manager"}:
            tk.Button(button_bar, text="Payments", command=self.show_payments).pack(side="left", padx=4)
            tk.Button(button_bar, text="Financial Report", command=self.show_financial_report).pack(side="left", padx=4)
        if role in {"MaintenanceStaff", "FrontDeskStaff", "Administrator"}:
            tk.Button(button_bar, text="Maintenance", command=self.show_maintenance).pack(side="left", padx=4)
        if role in {"Manager", "Administrator"}:
            tk.Button(button_bar, text="Occupancy Report", command=self.show_occupancy_report).pack(side="left", padx=4)
            tk.Button(button_bar, text="Maintenance Cost Report", command=self.show_maintenance_cost_report).pack(side="left", padx=4)

    def clear_output(self) -> None:
        self.output.delete("1.0", tk.END)

    def write_lines(self, title: str, rows) -> None:
        self.clear_output()
        self.output.insert(tk.END, title + "\n" + ("=" * len(title)) + "\n\n")
        if not rows:
            self.output.insert(tk.END, "No data found.\n")
            return
        for row in rows:
            self.output.insert(tk.END, f"{row}\n")

    def show_tenants(self) -> None:
        self.write_lines("Tenants", self.tenant_service.list_tenants())

    def show_apartments(self) -> None:
        self.write_lines("Apartments", self.apartment_service.list_apartments())

    def show_payments(self) -> None:
        self.write_lines("Payments", self.payment_service.list_payments())

    def show_maintenance(self) -> None:
        self.write_lines("Maintenance Requests", self.maintenance_service.list_requests())

    def show_occupancy_report(self) -> None:
        self.write_lines("Occupancy Report", self.report_service.occupancy_report())

    def show_financial_report(self) -> None:
        report = self.report_service.financial_report()
        self.write_lines("Financial Report", [report])

    def show_maintenance_cost_report(self) -> None:
        self.write_lines("Maintenance Cost Report", self.report_service.maintenance_cost_report())

    def run(self) -> None:
        self.root.mainloop()
