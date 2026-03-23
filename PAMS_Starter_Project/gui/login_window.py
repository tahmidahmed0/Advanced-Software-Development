import tkinter as tk
from tkinter import messagebox
from services.auth_service import AuthService
from gui.dashboard import DashboardWindow

class LoginWindow:
    def __init__(self, db_manager) -> None:
        self.db = db_manager
        self.auth_service = AuthService(self.db)
        self.root = tk.Tk()
        self.root.title("PAMS Login")
        self.root.geometry("360x220")
        self.build_ui()

    def build_ui(self) -> None:
        tk.Label(self.root, text="Paragon Apartment Management System", font=("Arial", 12, "bold")).pack(pady=12)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack(pady=4)

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*", width=30)
        self.password_entry.pack(pady=4)

        tk.Button(self.root, text="Login", width=18, command=self.attempt_login).pack(pady=16)

    def attempt_login(self) -> None:
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        user = self.auth_service.login(username, password)
        if not user:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            return
        self.root.destroy()
        dashboard = DashboardWindow(self.db, user)
        dashboard.run()

    def run(self) -> None:
        self.root.mainloop()
