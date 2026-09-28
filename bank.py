"""Core banking logic (same rules as the console version), used by the web app."""
import math
import random
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

accounts = {}  # account_number -> {name, phone, pin_hash, balance, history}


class BankError(Exception):
    """Raised for any user-facing banking problem."""


def _log(no, kind, text, amount=0.0):
    accounts[no]["history"].append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "kind": kind, "text": text, "amount": amount,
    })


def _amount(value):
    try:
        amt = round(float(value), 2)
    except (TypeError, ValueError):
        raise BankError("Enter a valid amount.")
    if not math.isfinite(amt) or amt <= 0:
        raise BankError("Amount must be greater than zero.")
    return amt


def _valid_pin(pin):
    return isinstance(pin, str) and pin.isdigit() and len(pin) == 4


def create_account(name, phone, pin):
    name, phone = (name or "").strip(), (phone or "").strip()
    if not name:
        raise BankError("Name is required.")
    if not phone.isdigit() or not 7 <= len(phone) <= 15:
        raise BankError("Enter a valid phone number (digits only).")
    if not _valid_pin(pin):
        raise BankError("PIN must be exactly 4 digits.")
    while True:
        no = str(random.randint(100000, 999999))
        if no not in accounts:
            break
    accounts[no] = {"name": name, "phone": phone, "balance": 0.0,
                    "pin_hash": generate_password_hash(pin), "history": []}
    _log(no, "info", "Account created")
    return no


def authenticate(no, pin):
    acc = accounts.get((no or "").strip())
    if not acc or not check_password_hash(acc["pin_hash"], pin or ""):
        raise BankError("Invalid account number or PIN.")
    return no.strip()


def deposit(no, amount):
    amt = _amount(amount)
    accounts[no]["balance"] += amt
    _log(no, "in", "Deposit", amt)


def withdraw(no, amount):
    amt = _amount(amount)
    if amt > accounts[no]["balance"]:
        raise BankError("Insufficient balance.")
    accounts[no]["balance"] -= amt
    _log(no, "out", "Withdrawal", amt)


def transfer(no, to, amount):
    to = (to or "").strip()
    if to == no:
        raise BankError("You cannot transfer money to your own account.")
    if to not in accounts:
        raise BankError("Receiver account does not exist.")
    amt = _amount(amount)
    if amt > accounts[no]["balance"]:
        raise BankError("Insufficient balance.")
    accounts[no]["balance"] -= amt
    accounts[to]["balance"] += amt
    _log(no, "out", f"Transfer to {to}", amt)
    _log(to, "in", f"Transfer from {no}", amt)


def change_pin(no, old, new, confirm):
    if not check_password_hash(accounts[no]["pin_hash"], old or ""):
        raise BankError("Incorrect current PIN.")
    if not _valid_pin(new):
        raise BankError("New PIN must be exactly 4 digits.")
    if new != confirm:
        raise BankError("PINs do not match.")
    accounts[no]["pin_hash"] = generate_password_hash(new)
    _log(no, "info", "PIN changed")


def summary(no):
    a = accounts[no]
    return {"name": a["name"], "account_number": no,
            "balance": round(a["balance"], 2), "history": a["history"][::-1]}
