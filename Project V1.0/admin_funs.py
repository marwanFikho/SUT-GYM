from misc_funs import *
from payments import *
# Generate a unique ID (5 digits)
def generate_unique_id(existing_ids):
    while True:
        new_id = random.randint(10000, 99999)  # Generate a random 5-digit ID
        if new_id not in existing_ids:  # Check if ID is unique
            return new_id

#########################

# Search for users via ID, Phone, username
def view_or_search_users():
    fresh()
    users = load_json(USERS_FILE)
    if not users:
        print("\nNo users found.")
        wait()
        fresh()
        return

    print("Search Options:")
    print("1. Search by User ID")
    print("2. Search by Phone Number")
    print("3. Search by Username")
    print("4. View All Users")
    choice = input("Enter your choice (1, 2, 3, or 4): ")

    if choice in ["1", "2", "3"]:
        search_term = input("Enter your search term: ")
        user = search_user(users, choice, search_term)

        if user:
            print("\nUser Found:")
            print(f"User ID: {user['id']}")
            for key, value in user.items():
                if key not in ["id", "amount_to_pay", "paid_amount"]:
                    print(f"    {key.capitalize()}: {value}")
            print(f"    Paid Amount: {user['paid_amount']} / {user['amount_to_pay']} EGP")
        else:
            print("\nNo user found with the provided search term.")

    elif choice == "4":
        print("\nRegistered Users:")
        for user_id, details in users.items():
            print(f"User ID: {user_id}")
            for key, value in details.items():
                if key not in ["amount_to_pay", "paid_amount"]:
                    print(f"    {key.capitalize()}: {value}")
            print(f"    Paid Amount: {details['paid_amount']} / {details['amount_to_pay']} EGP")
            print()

    else:
        print("\nInvalid choice. Please try again.")

    wait()
    fresh()
##################

# Adding user to the database
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
    while True:
        age = input("Enter user's age: ")
        try:
            age = int(age)
            break
        except ValueError:
            print("The age must be a number!!!")
            wait()
            fresh()

    gender = input("Enter user's gender: ")
    phone = input("Enter user's phone number: ")
    activity = input("Enter user's activity: ")
    while True:
        amount_to_pay = input("Enter the amount the user should pay: ")
        try:
            amount_to_pay = int(amount_to_pay)
            break
        except ValueError:
            print("This value must be a number!!")
    while True:
        paid_amount = input("Enter the amount the user paid: ")
        try:
            paid_amount = int(paid_amount)
            break
        except ValueError:
            print("This value must be a number!!")

    while True:
        re_paid_amount = input("Re-Enter the amount the user paid: ")
        try:
            re_paid_amount = int(re_paid_amount)
            break
        except ValueError:
            print("This value must be a number!!")

    while paid_amount != re_paid_amount :
        print("Amounts don't match!!\n")
        while True:
            paid_amount = input("Enter the amount the user paid: ")
            try:
                paid_amount = int(paid_amount)
                break
            except ValueError:
                print("This value must be a number!!")

        while True:
            re_paid_amount = input("Re-Enter the amount the user paid: ")
            try:
                re_paid_amount = int(re_paid_amount)
                break
            except ValueError:
                print("This value must be a number!!")

    user_id = generate_unique_id(users)

    # Subscription date start/expiry
    subscription_date = input("Enter subscription start date (YYYY-MM-DD): ")
    try:
        subscription_date_obj = datetime.strptime(subscription_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        wait()
        fresh()
        return

    subscription_duration = input("Enter subscription duration (in months): ")
    if not subscription_duration.isdigit():
        print("Duration must be a valid number of months.")
        wait()
        fresh()
        return
    subscription_duration = int(subscription_duration)
    expiry_date_obj = subscription_date_obj + timedelta(days=subscription_duration * 30)
    expiry_date = expiry_date_obj.strftime("%Y-%m-%d")

    # Determine active status
    current_date = datetime.now()
    active_status = "Active" if expiry_date_obj >= current_date else "Inactive"
    ########

    users[user_id] = {
        "username": username,
        "password": password,
        "age": age,
        "gender": gender,
        "phone": phone,
        "activity": activity,
        "amount_to_pay": amount_to_pay,
        "paid_amount": paid_amount,
        "subscription_date": subscription_date,
        "subscription_duration": subscription_duration,
        "expiry_date": expiry_date,
        "active_status": active_status,
    }

    save_json(USERS_FILE, users)
    print(f"User added successfully. Assigned ID: {user_id}.")
    wait()
    fresh()
#######

# Edit user from the database
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

        ### Add months
        add_months = input("Enter number of months to extend subscription (0 to skip): ")
        if add_months.isdigit() and int(add_months) > 0:
            add_months = int(add_months)
            current_expiry_date = datetime.strptime(users[user_id]["expiry_date"], "%Y-%m-%d")
            extended_expiry_date = current_expiry_date + timedelta(days=add_months * 30)
            users[user_id]["expiry_date"] = extended_expiry_date.strftime("%Y-%m-%d")
            print(f"New Expiry Date: {users[user_id]['expiry_date']}")

        # Recalculate active status
        current_date = datetime.now()
        users[user_id]["active_status"] = "Active" if datetime.strptime(users[user_id]["expiry_date"],"%Y-%m-%d") >= current_date else "Inactive"


        users[user_id].update({
            "password": new_password,
            "age": age,
            "phone": phone
        })

        save_json(USERS_FILE, users)
        print("User updated successfully.")
        wait()
        fresh()
#######

def renew_user():
    users = load_json(USERS_FILE)
    user_id = input("Enter the User ID (x to EXIT): ")
    if user_id == 'x':
        fresh()
        return
    if user_id not in users:
        print("User not found!!!")
        wait()
        fresh()
        return
    user = users[user_id]

    print(f"User found: {user['username']}\n")

    while True:
        subscription_date = input("Enter subscription start date (YYYY-MM-DD): ")
        try:
            subscription_date_obj = datetime.strptime(subscription_date, "%Y-%m-%d")
            break
        except ValueError:
            print("\nInvalid date format. Please use YYYY-MM-DD.")
            wait()
            fresh()

    subscription_duration = input("Enter subscription duration (in months): ")
    while not subscription_duration.isdigit():
        print("\nDuration must be a valid number of months.")
        wait()
        fresh()
        subscription_duration = input("Enter subscription duration (in months): ")

    subscription_duration = int(subscription_duration)
    expiry_date_obj = subscription_date_obj + timedelta(days=subscription_duration * 30)
    expiry_date = expiry_date_obj.strftime("%Y-%m-%d")

    # Determine active status
    current_date = datetime.now()
    active_status = "Active" if expiry_date_obj >= current_date else "Inactive"

    user.update({
        "subscription_date": subscription_date,
        "subscription_duration": subscription_duration,
        "expiry_date": expiry_date,
        "active_status": active_status
    })

    save_json(USERS_FILE, users)

    print("User renewed Successfully!!")
    print("<<->> Please add user payment details <<->>")
    wait()
    fresh()
    edit_payment(user_id)
    ########

# Delete a user from the Database
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
    ###########