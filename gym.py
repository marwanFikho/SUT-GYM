import json
import os

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
        print("3. Edit User")
        print("4. Delete User")
        print("5. Add Payment")
        print("6. Logout")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            view_users()
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
                print(f"  {key.capitalize()}: {value}")
            print()  # Blank line for readability

# Add a new user
def add_user():
    users = load_json(USERS_FILE)
    username = input("Enter new username: ")
    if username in users:
        print("User already exists.")
        return
    password = input("Enter password for new user: ")
    age = input("Enter user's age: ")
    gender = input("Enter user's gender: ")
    phone = input("Enter user's phone number: ")
    
    users[username] = {
        "password": password,
        "age": age,
        "gender": gender,
        "phone": phone,
        "payment": 0  # Default payment
    }
    save_json(USERS_FILE, users)
    print("User added successfully.")

# Edit user details
def edit_user():
    users = load_json(USERS_FILE)
    if not users:
        print("\nNo users found!")
    else:
        username = input("Enter username to edit: ")
        if username not in users:
            print("User not found.")
            return
        new_password = input(f"Enter new password for {username}: ")
        age = input(f"Enter new age for {username}: ")
        gender = input(f"Enter new gender for {username}: ")
        phone = input(f"Enter new phone number for {username}: ")
        
        users[username].update({
            "password": new_password,
            "age": age,
            "gender": gender,
            "phone": phone
        })
        save_json(USERS_FILE, users)
        print("User updated successfully.")

# Delete a user
def delete_user():
    users = load_json(USERS_FILE)
    username = input("Enter username to delete: ")
    if username not in users:
        print("User not found.")
        return
    del users[username]
    save_json(USERS_FILE, users)
    print("User deleted successfully.")

# Add payment
def add_payment():
    users = load_json(USERS_FILE)
    username = input("Enter username to add payment for: ")
    if username not in users:
        print("User not found.")
        return
    payment = float(input(f"Enter payment amount for {username}: "))
    users[username]["payment"] += payment
    save_json(USERS_FILE, users)
    print(f"Payment of {payment} added successfully for {username}.")

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
    print(f"\nUser Panel - {username}")
    print("1. View Profile")
    print("2. Logout")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        details = load_json(USERS_FILE)[username]
        print("\nYour Details:")
        for key, value in details.items():
            print(f"  {key.capitalize()}: {value}")
    elif choice == "2":
        print("Logging out...")
    else:
        print("Invalid choice. Please try again.")
        user_panel(username)

# Main menu
def main_menu():
    initialize_files()
    while True:
        print("\nGym Management System")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            admin_login()
        elif choice == "2":
            user_login()
        elif choice == "3":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the system
if __name__ == "__main__":
    main_menu()
