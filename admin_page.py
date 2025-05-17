from admin_funs import *
from payments import *

# Admin login
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
######

# Admin Panel
def admin_panel():
    fresh()
    log("Admin", "Login")
    while True:
        print("\nAdmin Panel:")
        print("1. View/Search Users")
        print("2. Add User")
        print("3. Edit User")
        print("4. Delete User")
        print("5. Add Payment")
        print("6. Renew Subscription")
        print("7. Export USERS as CSV")
        print("8. Logout")

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
            renew_user()
        elif choice == "7":
            export_users()
        elif choice == "8":
            print("Logging out...")
            log("Admin", "Logout")
            break
        else:
            print("Invalid choice. Please try again.")
            wait()
            fresh()

##################