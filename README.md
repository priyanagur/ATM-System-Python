# 🏦 ATM Management System (Python)

A modern, GUI-based **ATM Management System** developed using **Python, CustomTkinter, and MySQL**.  
The application simulates real ATM operations such as secure login, account management, transactions, and transaction history with persistent database storage.


## 🚀 Features

- 🔐 Secure login using Customer Number and PIN
- 💳 Current Account & Saving Account support
- 💰 Balance enquiry
- ➕ Deposit money
- ➖ Withdraw money
- 🧾 Transaction history tracking
- 🗄️ Persistent storage using MySQL
- 🌙 Modern dark-themed GUI using CustomTkinter

---

## 🛠️ Tech Stack

- **Programming Language:** Python 3  
- **GUI Framework:** CustomTkinter  
- **Database:** MySQL  
- **Database Connector:** mysql-connector-python  
- **Concepts Used:** OOP, GUI programming, SQL

---

## 📂 Project Structure

ATM-System/
│
├── atm.py # Main application file
├── README.md # Project documentation
├── requirements.txt # Project dependencies
├── .gitignore 


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ATM-System.git
cd ATM-System
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Create MySQL Database
Open MySQL Workbench / MySQL CLI and run:
CREATE DATABASE atm_db;
Tables and default users are created automatically by the application.

4️⃣ Configure Database Credentials
Open atm.py and update:
user="root"
password="YOUR_MYSQL_PASSWORD"

5️⃣ Run the Application
python atm.py

🔑 Default Login Credentials
Customer Number	PIN
11111	            111
11112	            222
11113	            333

🧾 Database Design
Tables Used
1. users

customer_no (Primary Key)
pin
current_balance
saving_balance

2. transactions

id (Auto Increment)
customer_no
account_type
transaction_type
amount
timestamp



🧪 How It Works (Flow)
User logs in using Customer Number and PIN
Selects account type (Current / Saving)
Performs operations like balance check, deposit, or withdraw
Every transaction is stored in the MySQL database
Transaction history can be viewed anytime

🧠 Learning Outcomes
GUI application development in Python
Database connectivity using MySQL
Object-Oriented Programming (OOP)
CRUD operations using SQL
Real-world project structure and GitHub usage

📌 Future Enhancements
PIN encryption / hashing

Admin dashboard

User registration module

Transaction filtering and export

Convert application to .exe

👩‍💻 Author
Priya Nagur
B.Tech (CSE)
GitHub: https://github.com/YOUR_USERNAME

⭐ Acknowledgement
This project was developed for academic and learning purposes to understand GUI development and database integration using Python.

