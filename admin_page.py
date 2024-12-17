import json
import random
from misc_funs import *

ADMIN_FILE = "admin.json"
USERS_FILE = "users.json"

# Load and save databases
def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

#########################

# Generate a unique ID (5 digits)
def generate_unique_id(existing_ids):
    while True:
        new_id = random.randint(10000, 99999)  # Generate a random 5-digit ID
        if new_id not in existing_ids:  # Check if ID is unique
            return new_id

#########################


def admin_login():
    admin_data = load_json(ADMIN_FILE)["admin"]
    username = input("\nEnter Admin Username (or x to exit): ")
    if username == 'x':
        fresh()
        return
    password = input("Enter Admin Password: ")

    if username == admin_data["username"] and password == admin_data["password"]:
        input("\nLogin successful! Welcome, Admin.\nPress ENTER to continue...")
        admin_panel()
    else:
        input("\nInvalid credentials. Try again. Press ENTER to continue... ")
        fresh()
        admin_login()


def admin_panel():
    fresh()
    while True:
        print("\nAdmin Panel:")
        print("1. View/Search Users")
        print("2. Add User")
        print("3. Edit User")
        print("4. Delete User")
        print("5. Add Payment")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_or_search_users()

        elif choice == "2":
            add_user()
        elif choice == "3":
            edit_user()
        elif choice == "4":
            delete_user()
        elif choice == "5":
            add_payment()
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")
            wait()

def view_or_search_users():
    fresh()
    users = load_json(USERS_FILE)
    if not users:
        print("\nNo users found.")
        wait()
        fresh()
        return

    user_id = input("Enter User ID to search (or press ENTER to view all users): ")

    if user_id:
        if user_id in users:
            user = users[user_id]
            print("\nUser Found:")
            print(f"User ID: {user_id}")
            for key, value in user.items():
                if key not in ["amount_to_pay", "paid_amount"]:
                    print(f"    {key.capitalize()}: {value}")
            print(f"    Paid Amount: {user['paid_amount']} / {user['amount_to_pay']} EGP")
        else:
            print("No user found with that ID.")
    else:  # If no ID is provided, show all users
        print("\nRegistered Users:")
        for user_id, details in users.items():
            print(f"User ID: {user_id}")
            for key, value in details.items():
                if key not in ["amount_to_pay", "paid_amount"]:
                    print(f"    {key.capitalize()}: {value}")
            print(f"    Paid Amount: {details['paid_amount']} / {details['amount_to_pay']} EGP")
            print()

    wait()
    fresh()


def add_user():
    fresh()
    users = load_json(USERS_FILE)
    username = input("Enter new username (or x to exit): ")
    if username == 'x':
        fresh()
        return
    if username in users:
        print("User already exists.")
        wait()
        fresh()
        return

    password = input("Enter password for new user: ")
    age = input("Enter user's age: ")
    gender = input("Enter user's gender: ")
    phone = input("Enter user's phone number: ")
    activity = input("Enter user's activity: ")
    amount_to_pay = input("Enter the amount the user should pay: ")
    user_id = generate_unique_id(users)

    users[user_id] = {
        "username": username,
        "password": password,
        "age": age,
        "gender": gender,
        "phone": phone,
        "activity": activity,
        "amount_to_pay": amount_to_pay,
        "paid_amount": 0
    }

    save_json(USERS_FILE, users)
    print(f"User added successfully. Assigned ID: {user_id}.")
    wait()
    fresh()


def edit_user():
    fresh()
    users = load_json(USERS_FILE)
    if not users:
        print("\nNo users found!\n")
        wait()
        fresh()
    else:
        user_id = input("Enter User ID to edit (or x to exit):  ")
        if user_id == 'x':
            fresh()
            return
        if user_id not in users:
            print("User not found.")
            wait()
            fresh()
            return
        new_password = input(f"Enter new password for {users[user_id]['username']} (Blank ENTER to skip): ")
        if not new_password: new_password = users[user_id]["password"]
        age = input(f"Enter new age for {users[user_id]['username']} (Blank ENTER to skip): ")
        if not age: age = users[user_id]["age"]
        gender = input(f"Enter new gender for {users[user_id]['username']} (Blank ENTER to skip): ")
        if not gender: gender = users[user_id]["gender"]
        phone = input(f"Enter new phone number for {users[user_id]['username']} (Blank ENTER to skip): ")
        if not phone: phone = users[user_id]["phone"]

        users[user_id].update({
            "password": new_password,
            "age": age,
            "gender": gender,
            "phone": phone
        })
        save_json(USERS_FILE, users)
        print("User updated successfully.")
        wait()
        fresh()


def delete_user():
    fresh()
    users = load_json(USERS_FILE)
    user_id = input("Enter User ID to delete (or x to exit): ")
    if user_id == 'x': return
    if user_id not in users:
        print("User not found.")
        wait()
        fresh()
        return
    del users[user_id]
    save_json(USERS_FILE, users)
    print("User deleted successfully.")
    wait()
    fresh()