#### MAIN FILE
from admin_page import admin_login
from misc_funs import *
import json
import os

# File paths
USERS_FILE = "users.json"


# Ensure JSON files exist
def initialize_files():
    if not os.path.exists("admin.json"):
        with open("admin.json", "w") as f:
            json.dump({"admin": {"username": "admin", "password": "admin123"}}, f)

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)


# Load JSON data
def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


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
    fresh()
    initialize_files()
    while True:
        print("\nGym Management System")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Exit\n")

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
            wait()
            fresh()


# Run the system
if __name__ == "__main__":
    main_menu()
