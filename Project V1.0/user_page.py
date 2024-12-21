#### User PAGE
from misc_funs import *
users = load_json(USERS_FILE)

# User login
def user_login():
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
            user_panel(user_id)
        else:
            print("\nInvalid credentials. Try again.")
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

        phone = input(f"Enter new phone number for {users[user_id]['username']} (Blank ENTER to skip): ")
        if not phone: phone = users[user_id]["phone"]


        user.update({
            "password": new_password,
            "age": age,
            "phone": phone
        })

        save_json(USERS_FILE, users)

        print("Data edited Successfully!")
        wait()
        fresh()
        user_panel(user_id)

# User panel
def user_panel(user_id):
    print(f"\nUser Panel - {users[user_id]['username']}")
    print("1. View Profile")
    print("2. Edit Profile")
    print("3. Logout")

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
    elif choice == "3":
        print("Logging out...")
        fresh()
    else:
        print("Invalid choice. Please try again.")
        user_panel(user_id)