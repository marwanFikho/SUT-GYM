#### MAIN FILE
from misc_funs import *
from user_page import user_login
from admin_page import admin_login

# Ensure JSON files exist
def initialize_files():
    if not os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, "w") as f:
            json.dump({"admin": {"username": "admin", "password": "admin123"}}, f)

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)

    if not os.path.exists(PAYMENT_LOG_FILE):
        with open(PAYMENT_LOG_FILE, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["User ID", "Paid Amount", "Payment Date"])

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Who", "Action", "What", "When"])

######



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
if __name__ == "__main__": # int main()
    main_menu()
