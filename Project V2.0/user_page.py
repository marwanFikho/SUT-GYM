#### User PAGE
from misc_funs import *
from log_maker import log

# User login
def user_login():
    users = load_json(USERS_FILE)
    if not users:
        print("\nNo users found!")
    else:
        user_id = input("Enter User ID (x to exit): ")
        if user_id == 'x':
            fresh()
            return
        password = input("Enter Password: ")
        fresh()
        if user_id in users and users[user_id]["password"] == password:
            print(f"\nWelcome, {users[user_id]['username']}!")
            log(user_id, "Login")
            user_panel(user_id)
        else:
            print("\nInvalid credentials. Try again.")
            log(user_id, "Access Denied")
            user_login()


def user_user_edit(user_id):
    users = load_json(USERS_FILE)
    user = users[user_id]
    user_pas = input("Enter your password: ")
    if user['password'] != user_pas:
        print("Wrong password please try again later!!")
        wait()
        fresh()
        user_panel(user_id)
    else:
        new_password = input(f"Enter new password for {users[user_id]['username']} (Blank ENTER to skip): ")
        if not new_password: new_password = users[user_id]["password"]
        while True:
            age = input(f"Enter new age for {users[user_id]['username']} (Blank ENTER to skip): ")
            if not age:
                age = users[user_id]["age"]
                break
            try:
                age = int(age)
                break
            except ValueError:
                print("This value must be a number!!")

        patter = r"^01[0125]\d{8}$"
        while True:
            phone = input(f"Enter new phone number for {users[user_id]['username']} (Blank ENTER to skip): ")
            if not phone:
                phone = users[user_id]["phone"]
                break
            if re.match(patter, phone):
                break
            else:
                print("Please enter a valid phone number!!")
                wait()

        user.update({
            "password": new_password,
            "age": age,
            "phone": phone
        })

        save_json(USERS_FILE, users)
        log(user_id, "edit")
        print("Data edited Successfully!")
        wait()
        fresh()
        user_panel(user_id)

def user_delete(user_id):
    users = load_json(USERS_FILE)
    user_pass = input("Enter your password to confirm Deletion: ")
    if user_pass == users[user_id]['password']:
        print("The user will be permanently delete!!")
        x = input("Enter Y to continue or X to exit: ")
        if x.lower() == 'y':
            log(user_id, "Deleted")
            del users[user_id]
            print("User deleted Successfully!")
            save_json(USERS_FILE, users)
            wait()
            fresh()
            return
        else:
            user_panel(user_id)
    else:
        print("Wrong Password, Returning to User Panel")
        wait()
        fresh()
        user_panel(user_id)

# User panel
def user_panel(user_id):
    users = load_json(USERS_FILE)
    print(f"\nUser Panel - {users[user_id]['username']}")
    print("1. View Profile")
    print("2. Edit Profile")
    print("3. Delete User")
    print("4. Logout")

    choice = input("Enter your choice: ")
    fresh()

    if choice == "1":
        details = load_json(USERS_FILE)[user_id]
        print("\nYour Details:")
        for key, value in details.items():
            if key not in ["id", "amount_to_pay", "paid_amount"]:
                print(f"    {key.capitalize()}: {value}")
        print(f"    Paid Amount: {details['paid_amount']} / {details['amount_to_pay']} EGP")
        wait()
        fresh()
        user_panel(user_id)
    elif choice == '2':
        user_user_edit(user_id)
    elif choice == '3':
        user_delete(user_id)
    elif choice == "4":
        print("Logging out...")
        log(user_id, "Logout")
        fresh()
    else:
        print("Invalid choice. Please try again.")
        user_panel(user_id)