from misc_funs import *
import csv
PAYMENT_LOG_FILE = 'payment_log.csv'

def log_payment(user_id, paid_amount):

    payment_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(PAYMENT_LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, paid_amount, payment_date])

def add_payment():
    users = load_json(USERS_FILE)
    user_id = input("Enter User ID to add payment (x to Exit): ")
    if user_id == 'x':
        fresh()
        return
    if user_id not in users:
        print("\nUser not found!!")
        wait()
        fresh()
        return

    else:
        print(f"User found --> {users[user_id]['username']}")
        print(f"User payment: {users[user_id]['paid_amount']} / {users[user_id]['amount_to_pay']}")
        amount = int(input("Enter amount to pay: "))
        reamount = int(input("Re-Enter amount to pay: "))
        while amount != reamount:
            print("\nAmounts don't match!!\n")
            amount = int(input("Enter amount to pay: "))
            reamount = int(input("Re-Enter amount to pay: "))


        users[user_id]['paid_amount'] += amount
        print("Payment Succeeded!!")
        print(f"Updated user payment: {users[user_id]['paid_amount']} / {users[user_id]['amount_to_pay']}")
        wait()
        fresh()
        log_payment(user_id, amount)
        save_json(USERS_FILE, users)

def edit_payment(user_id):
        users = load_json(USERS_FILE)
        user = users[user_id]
        print(f"Username: {user['username']}")
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

        while paid_amount != re_paid_amount:
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

        user.update({
            "amount_to_pay" : amount_to_pay,
            "paid_amount": paid_amount
        })

        log_payment(user_id, paid_amount)
        save_json(USERS_FILE, users)

        print("Payment Edited Successfully!!")
        wait()
        fresh()