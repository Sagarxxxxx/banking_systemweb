"""Flask web app for the Banking System mini project."""
import os
from functools import wraps

from flask import Flask, jsonify, render_template, request, session

import bank

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")


def body():
    return request.get_json(silent=True) or {}


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        no = session.get("acc")
        if no not in bank.accounts:
            session.clear()
            return jsonify(error="Please log in."), 401
        return fn(no, *args, **kwargs)
    return wrapper


@app.errorhandler(bank.BankError)
def handle_bank_error(e):
    return jsonify(error=str(e)), 400


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/register")
def register():
    d = body()
    return jsonify(account_number=bank.create_account(d.get("name"), d.get("phone"), d.get("pin")))


@app.post("/api/login")
def login():
    d = body()
    session["acc"] = bank.authenticate(d.get("account"), d.get("pin"))
    return jsonify(bank.summary(session["acc"]))


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify(ok=True)


@app.get("/api/me")
@login_required
def me(no):
    return jsonify(bank.summary(no))


@app.post("/api/deposit")
@login_required
def deposit(no):
    bank.deposit(no, body().get("amount"))
    return jsonify(bank.summary(no))


@app.post("/api/withdraw")
@login_required
def withdraw(no):
    bank.withdraw(no, body().get("amount"))
    return jsonify(bank.summary(no))


@app.post("/api/transfer")
@login_required
def transfer(no):
    d = body()
    bank.transfer(no, d.get("to"), d.get("amount"))
    return jsonify(bank.summary(no))


@app.post("/api/change-pin")
@login_required
def change_pin(no):
    d = body()
    bank.change_pin(no, d.get("old"), d.get("new"), d.get("confirm"))
    return jsonify(bank.summary(no))


if __name__ == "__main__":
    app.run(debug=True)
