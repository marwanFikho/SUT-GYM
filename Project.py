import json
import os
from datetime import datetime, timedelta

# File paths
ADMIN_FILE = "admin.json"
USERS_FILE = "users.json"

# Ensure JSON files exist
def initialize_files():
    if not os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, "w") as f:
            json.dump({"admin": {"username": "admin", "password": "admin123"}}, f)
    
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)

# Load JSON data
def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Save JSON data
def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# Admin login
def admin_login():
    admin_data = load_json(ADMIN_FILE)["admin"]
    username = input("Enter Admin Username: ")
    password = input("Enter Admin Password: ")
    
    if username == admin_data["username"] and password == admin_data["password"]:
        print("\nLogin successful! Welcome, Admin.")
        admin_panel()
    else:
        print("\nInvalid credentials. Try again.")
        admin_login()

# Admin panel
def admin_panel():
    while True:
        print("\nAdmin Panel:")
        print("1. View Users")
        print("2. Add User")
        print("3. Add Payment")
        print("4. View Payments")
        print("5. Logout")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            view_users()
        elif choice == "2":
            add_user()
        elif choice == "3":
            add_payment()
        elif choice == "4":
            view_user_payments()
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

# View all users
def view_users():
    users = load_json(USERS_FILE)
    if not users:
        print("\nNo users found.")
    else:
        print("\nRegistered Users:")
        for username, details in users.items():
            print(f"Username: {username}")
            for key, value in details.items():
                if key != "payments":
                    print(f"  {key.capitalize()}: {value}")
            print()

# Add a new user
def add_user():
    users = load_json(USERS_FILE)
    username = input("Enter new username: ")
    if username in users:
        print("User already exists.")
        return
    password = input("Enter password for new user: ")
    gender = input("Enter gender: ")
    phone = input("Enter phone number: ")
    age = input("Enter age: ")
    activity = input("Enter activity: ")
    users[username] = {
        "password": password,
        "gender": gender,
        "phone": phone,
        "age": age,
        "activity": activity,
        "payments": []  # To store payment records
    }
    save_json(USERS_FILE, users)
    print("User added successfully.")

# Admin adds a payment for a user
def add_payment():
    users = load_json(USERS_FILE)
    username = input("Enter username to add payment: ")
    if username not in users:
        print("User not found.")
        return

    # Ensure the 'payments' key exists
    if "payments" not in users[username]:
        users[username]["payments"] = []

    print("\nPayment Options:")
    print("1. One-time Payment")
    print("2. Installment Payment")
    
    payment_choice = input("Choose payment option (1 or 2): ")
    amount = float(input("Enter total payment amount: "))
    
    remaining_balance = sum(payment.get("remaining", 0) for payment in users[username]["payments"])

    if payment_choice == "1":
        date_paid = datetime.now().strftime("%Y-%m-%d")
        new_remaining = max(0, remaining_balance - amount)
        users[username]["payments"].append({
            "type": "one-time",
            "amount_paid": amount,
            "remaining": new_remaining,
            "date_paid": date_paid
        })
        print(f"Payment of {amount} recorded for {username}.")
    
    elif payment_choice == "2":
        installments = int(input("Enter number of installments: "))
        installment_amount = amount / installments
        remaining = amount
        first_deadline = datetime.now() + timedelta(days=30)

        payment_plan = {
            "type": "installment",
            "total_amount": amount,
            "installment_amount": installment_amount,
            "remaining": remaining,
            "paid_amount": 0,
            "deadlines": []
        }
        for i in range(installments):
            deadline = (first_deadline + timedelta(days=30 * i)).strftime("%Y-%m-%d")
            payment_plan["deadlines"].append({
                "installment_number": i + 1,
                "due_date": deadline,
                "status": "unpaid"
            })
        users[username]["payments"].append(payment_plan)
        print(f"Installment plan set for {username}: {installments} installments of {installment_amount} each.")
    else:
        print("Invalid choice.")
    save_json(USERS_FILE, users)

# Admin views payment records of all users
def view_user_payments():
    users = load_json(USERS_FILE)
    print("\nUser Payment Records:")
    for username, details in users.items():
        print(f"\nUser ID: {username}")
        payments = details.get("payments", [])
        total_paid = sum(payment.get("amount_paid", 0) for payment in payments)
        remaining = sum(payment.get("remaining", 0) for payment in payments)
        print(f"  Total Paid: {total_paid}")
        print(f"  Remaining Balance: {remaining}")
        for payment in payments:
            print(f"    - Type: {payment['type']}")
            print(f"      Amount Paid: {payment.get('amount_paid', 0)}")
            print(f"      Remaining: {payment.get('remaining', 0)}")
            print(f"      Date Paid: {payment.get('date_paid', '-')}")
            if payment['type'] == 'installment':
                for deadline in payment['deadlines']:
                    print(f"        Installment {deadline['installment_number']} - Due: {deadline['due_date']} Status: {deadline['status']}")

# User login
def user_login():
    users = load_json(USERS_FILE)
    if not users:
        print("\nNo users found!")
    else:
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        
        if username in users and users[username]["password"] == password:
            print(f"\nWelcome, {username}!")
            user_panel(username)
        else:
            print("\nInvalid credentials. Try again.")
            user_login()

# User panel
def user_panel(username):
    users = load_json(USERS_FILE)
    print("\nUser Panel")
    print("1. View Payments")
    print("2. View User Info")
    print("3. Logout")
    
    choice = input("Enter your choice: ")
    if choice == "1":
        view_payments(username, users)
    elif choice == "2":
        view_user_info(username, users)
    elif choice == "3":
        print("Logging out...")
    else:
        print("Invalid choice. Please try again.")
        user_panel(username)

# View user payments
def view_payments(username, users):
    print("\nYour Payments:")
    payments = users[username].get("payments", [])
    total_paid = sum(payment.get("amount_paid", 0) for payment in payments)
    remaining = sum(payment.get("remaining", 0) for payment in payments)
    print(f"  Total Paid: {total_paid}")
    print(f"  Remaining Balance: {remaining}")
    if not payments:
        print("No payment history found.")
    else:
        for idx, payment in enumerate(payments):
            print(f"Payment {idx + 1}:")
            print(f"  Type: {payment['type']}")
            print(f"  Amount Paid: {payment.get('amount_paid', 0)}")
            print(f"  Remaining: {payment.get('remaining', 0)}")
            print(f"  Date Paid: {payment.get('date_paid', '-')}")

# View user information
def view_user_info(username, users):
    print("\nYour Information:")
    user_info = users.get(username, {})
    for key, value in user_info.items():
        if key != "password" and key != "payments":
            print(f"  {key.capitalize()}: {value}")

# Main menu
def main_menu():
    initialize_files()
    while True:
        print("\nGym Management")