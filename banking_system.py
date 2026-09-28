"""
Banking System - Mini Project
A menu-driven console application simulating basic banking operations.

Features:
- Create account
- Login with Account Number & PIN
- Check balance
- Deposit / Withdraw
- Transfer money between accounts
- View transaction history
- Change PIN
- Logout
"""

import random
from datetime import datetime

# ---------------------------------------------------------
# In-memory "database" of accounts.
# Structure:
# accounts = {
#     "123456": {
#         "name": "John Doe",
#         "phone": "9876543210",
#         "pin": "1234",
#         "balance": 5000.0,
#         "history": [ "2026-09-27 10:00:00 | Deposit | +5000" ]
#     }
# }
# ---------------------------------------------------------
accounts = {}


def generate_account_number():
    """Generate a unique 6-digit account number."""
    while True:
        acc_no = str(random.randint(100000, 999999))
        if acc_no not in accounts:
            return acc_no


def log_transaction(acc_no, description):
    """Add a timestamped entry to the account's transaction history."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    accounts[acc_no]["history"].append(f"{timestamp} | {description}")


def create_account():
    print("\n--- Create New Account ---")
    name = input("Enter your name: ").strip()
    phone = input("Enter your phone number: ").strip()

    while True:
        pin = input("Set a 4-digit PIN: ").strip()
        if pin.isdigit() and len(pin) == 4:
            break
        print("Invalid PIN. Please enter exactly 4 digits.")

    acc_no = generate_account_number()
    accounts[acc_no] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0.0,
        "history": []
    }
    log_transaction(acc_no, "Account created")

    print("\nAccount created successfully!")
    print(f"Your Account Number is: {acc_no}")
    print("Please save this number, you'll need it to log in.")


def login():
    print("\n--- Login ---")
    acc_no = input("Enter Account Number: ").strip()
    pin = input("Enter PIN: ").strip()

    account = accounts.get(acc_no)
    if account and account["pin"] == pin:
        print(f"\nWelcome back, {account['name']}!")
        account_menu(acc_no)
    else:
        print("Invalid Account Number or PIN.")


def check_balance(acc_no):
    balance = accounts[acc_no]["balance"]
    print(f"\nYour current balance is: {balance:.2f}")


def deposit(acc_no):
    try:
        amount = float(input("\nEnter amount to deposit: "))
    except ValueError:
        print("Invalid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    accounts[acc_no]["balance"] += amount
    log_transaction(acc_no, f"Deposit | +{amount:.2f}")
    print(f"Deposited {amount:.2f} successfully.")
    print(f"New balance: {accounts[acc_no]['balance']:.2f}")


def withdraw(acc_no):
    try:
        amount = float(input("\nEnter amount to withdraw: "))
    except ValueError:
        print("Invalid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    if amount > accounts[acc_no]["balance"]:
        print("Insufficient balance.")
        return

    accounts[acc_no]["balance"] -= amount
    log_transaction(acc_no, f"Withdraw | -{amount:.2f}")
    print(f"Withdrew {amount:.2f} successfully.")
    print(f"New balance: {accounts[acc_no]['balance']:.2f}")


def transfer(acc_no):
    receiver_acc = input("\nEnter receiver's Account Number: ").strip()

    if receiver_acc == acc_no:
        print("You cannot transfer money to your own account.")
        return

    if receiver_acc not in accounts:
        print("Receiver account does not exist.")
        return

    try:
        amount = float(input("Enter amount to transfer: "))
    except ValueError:
        print("Invalid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    if amount > accounts[acc_no]["balance"]:
        print("Insufficient balance.")
        return

    accounts[acc_no]["balance"] -= amount
    accounts[receiver_acc]["balance"] += amount

    log_transaction(acc_no, f"Transfer to {receiver_acc} | -{amount:.2f}")
    log_transaction(receiver_acc, f"Transfer from {acc_no} | +{amount:.2f}")

    print(f"Transferred {amount:.2f} to account {receiver_acc} successfully.")
    print(f"New balance: {accounts[acc_no]['balance']:.2f}")


def view_transaction_history(acc_no):
    history = accounts[acc_no]["history"]
    print("\n--- Transaction History ---")
    if not history:
        print("No transactions yet.")
        return
    for entry in history:
        print(entry)


def change_pin(acc_no):
    old_pin = input("\nEnter current PIN: ").strip()
    if old_pin != accounts[acc_no]["pin"]:
        print("Incorrect current PIN.")
        return

    new_pin = input("Enter new 4-digit PIN: ").strip()
    confirm_pin = input("Confirm new PIN: ").strip()

    if not (new_pin.isdigit() and len(new_pin) == 4):
        print("Invalid PIN format. Must be 4 digits.")
        return

    if new_pin != confirm_pin:
        print("PINs do not match.")
        return

    accounts[acc_no]["pin"] = new_pin
    log_transaction(acc_no, "PIN changed")
    print("PIN changed successfully.")


def account_menu(acc_no):
    while True:
        print("\n===== ACCOUNT MENU =====")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            check_balance(acc_no)
        elif choice == "2":
            deposit(acc_no)
        elif choice == "3":
            withdraw(acc_no)
        elif choice == "4":
            transfer(acc_no)
        elif choice == "5":
            view_transaction_history(acc_no)
        elif choice == "6":
            change_pin(acc_no)
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 7.")


def main_menu():
    while True:
        print("\n===== BANKING SYSTEM =====")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Thank you for using the Banking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 3.")


if __name__ == "__main__":
    main_menu()
