# Banking System – Mini Project

A Python banking application with two ways to run it:

- `banking_system.py` – the original menu-driven console version
- `app.py` – a Flask web version with an interactive page (same rules, PINs stored hashed)

Features: create account, login with account number and PIN, balance, deposit, withdraw,
transfer, transaction history, change PIN, logout.

Python concepts: variables, conditionals, loops, functions, lists and dictionaries,
string operations, modules (`random`, `datetime`), plus Flask for the web layer.

## Run locally

```bash
python3 banking_system.py          # console version

pip install -r requirements.txt    # web version
python3 app.py                     # open http://127.0.0.1:5000
```

## Deploy on Render

1. Push this repo to GitHub.
2. On Render: New → Web Service → connect the repo (or New → Blueprint to use `render.yaml`).
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app --workers 1 --threads 4`
5. Add an environment variable `SECRET_KEY` with any long random value.

## Notes

- Data lives in memory, so accounts reset when the server restarts or sleeps
  (Render's free tier sleeps when idle). Keep `--workers 1` so all requests share the same data.
- Live demo: _add your Render link here_
