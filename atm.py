import os
import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ---------------- DATABASE ----------------
class Database:
    def __init__(self):
        db_password = os.getenv("DB_PASSWORD")
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",          # CHANGE if needed
    
             password=db_password,
            # password="------",  # 👈 CHANGE THIS
            database="atm_db"
        )
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.seed_users()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            customer_no INT PRIMARY KEY,
            pin INT,
            current_balance DOUBLE,
            saving_balance DOUBLE
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_no INT,
            account_type VARCHAR(20),
            transaction_type VARCHAR(20),
            amount DOUBLE,
            timestamp VARCHAR(30)
        )
        """)
        self.conn.commit()

    def seed_users(self):
        users = [
            (11111, 111, 2000, 1000),
            (11112, 222, 2000, 1000),
            (11113, 333, 2000, 1000)
        ]
        for u in users:
            self.cursor.execute("""
            INSERT IGNORE INTO users
            (customer_no, pin, current_balance, saving_balance)
            VALUES (%s, %s, %s, %s)
            """, u)
        self.conn.commit()


# ---------------- ATM APP ----------------
class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("420x550")
        self.root.title("ATM Management System")

        self.db = Database()
        self.customer_no = None

        self.login_screen()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------- LOGIN ----------
    def login_screen(self):
        self.clear()

        ctk.CTkLabel(self.root, text="🏦 ATM LOGIN",
                     font=("Arial", 22, "bold")).pack(pady=30)

        self.cust_entry = ctk.CTkEntry(
            self.root, placeholder_text="Customer Number")
        self.cust_entry.pack(pady=10)

        self.pin_entry = ctk.CTkEntry(
            self.root, placeholder_text="PIN", show="*")
        self.pin_entry.pack(pady=10)

        ctk.CTkButton(self.root, text="Login",
                      command=self.login).pack(pady=20)

    def login(self):
        try:
            cust = int(self.cust_entry.get())
            pin = int(self.pin_entry.get())

            self.db.cursor.execute(
                "SELECT * FROM users WHERE customer_no=%s AND pin=%s",
                (cust, pin))
            user = self.db.cursor.fetchone()

            if user:
                self.customer_no = cust
                self.dashboard()
            else:
                messagebox.showerror("Error", "Invalid Customer Number or PIN")

        except ValueError:
            messagebox.showerror("Error", "Enter numbers only")

    # ---------- DASHBOARD ----------
    def dashboard(self):
        self.clear()

        ctk.CTkLabel(self.root, text="Select Option",
                     font=("Arial", 20, "bold")).pack(pady=20)

        ctk.CTkButton(self.root, text="Current Account",
                      command=lambda: self.account_menu("current")).pack(pady=10)

        ctk.CTkButton(self.root, text="Saving Account",
                      command=lambda: self.account_menu("saving")).pack(pady=10)

        ctk.CTkButton(self.root, text="Transaction History",
                      command=self.show_history).pack(pady=10)

        ctk.CTkButton(self.root, text="Logout",
                      fg_color="red",
                      command=self.login_screen).pack(pady=10)

    # ---------- ACCOUNT MENU ----------
    def account_menu(self, acc_type):
        self.clear()

        ctk.CTkLabel(self.root, text=f"{acc_type.upper()} ACCOUNT",
                     font=("Arial", 18, "bold")).pack(pady=20)

        ctk.CTkButton(self.root, text="Balance Enquiry",
                      command=lambda: self.balance(acc_type)).pack(pady=8)

        ctk.CTkButton(self.root, text="Deposit",
                      command=lambda: self.transaction(acc_type, "Deposit")).pack(pady=8)

        ctk.CTkButton(self.root, text="Withdraw",
                      command=lambda: self.transaction(acc_type, "Withdraw")).pack(pady=8)

        ctk.CTkButton(self.root, text="Back",
                      command=self.dashboard).pack(pady=10)

    # ---------- BALANCE ----------
    def balance(self, acc_type):
        col = "current_balance" if acc_type == "current" else "saving_balance"

        self.db.cursor.execute(
            f"SELECT {col} FROM users WHERE customer_no=%s",
            (self.customer_no,))
        bal = self.db.cursor.fetchone()[0]

        messagebox.showinfo(
            "Balance", f"Available Balance:\n₹ {bal:,.2f}")

    # ---------- TRANSACTION ----------
    def transaction(self, acc_type, t_type):
        self.clear()

        ctk.CTkLabel(self.root, text=f"{t_type} - {acc_type.upper()}",
                     font=("Arial", 18)).pack(pady=20)

        amount_entry = ctk.CTkEntry(
            self.root, placeholder_text="Enter Amount")
        amount_entry.pack(pady=10)

        def submit():
            try:
                amt = float(amount_entry.get())
                if amt <= 0:
                    raise ValueError

                col = "current_balance" if acc_type == "current" else "saving_balance"

                self.db.cursor.execute(
                    f"SELECT {col} FROM users WHERE customer_no=%s",
                    (self.customer_no,))
                bal = self.db.cursor.fetchone()[0]

                if t_type == "Withdraw" and amt > bal:
                    messagebox.showerror("Error", "Insufficient Balance")
                    return

                new_bal = bal + amt if t_type == "Deposit" else bal - amt

                self.db.cursor.execute(
                    f"UPDATE users SET {col}=%s WHERE customer_no=%s",
                    (new_bal, self.customer_no))

                self.db.cursor.execute("""
                    INSERT INTO transactions
                    (customer_no, account_type, transaction_type, amount, timestamp)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    self.customer_no,
                    acc_type,
                    t_type,
                    amt,
                    datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                ))

                self.db.conn.commit()
                messagebox.showinfo("Success", "Transaction Successful")
                self.account_menu(acc_type)

            except ValueError:
                messagebox.showerror("Error", "Enter valid amount")

        ctk.CTkButton(self.root, text="Submit",
                      command=submit).pack(pady=10)

        ctk.CTkButton(self.root, text="Back",
                      command=lambda: self.account_menu(acc_type)).pack(pady=10)

    # ---------- TRANSACTION HISTORY ----------
    def show_history(self):
        self.clear()

        ctk.CTkLabel(self.root, text="Transaction History",
                     font=("Arial", 18, "bold")).pack(pady=10)

        self.db.cursor.execute("""
            SELECT account_type, transaction_type, amount, timestamp
            FROM transactions
            WHERE customer_no=%s
            ORDER BY id DESC
            LIMIT 10
        """, (self.customer_no,))

        rows = self.db.cursor.fetchall()

        if not rows:
            ctk.CTkLabel(self.root, text="No transactions yet").pack(pady=20)

        for r in rows:
            ctk.CTkLabel(
                self.root,
                text=f"{r[3]} | {r[0]} | {r[1]} | ₹{r[2]}"
            ).pack(anchor="w", padx=20)

        ctk.CTkButton(self.root, text="Back",
                      command=self.dashboard).pack(pady=15)


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = ctk.CTk()
    ATMApp(root)
    root.mainloop()
