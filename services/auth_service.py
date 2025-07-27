import os
from werkzeug.security import check_password_hash
from dotenv import load_dotenv

load_dotenv()

def get_admin_accounts() -> dict:
    accounts_env = os.getenv("ACCOUNTS", "")
    accounts = {}
    for pair in accounts_env.split(","):
        if ":" not in pair:
            continue
        user, pwd_hash = pair.split(":", 1)
        accounts[user] = pwd_hash
    return accounts

def verify_login(username, password):
    accounts = get_admin_accounts()
    if username not in accounts:
        return False
    return check_password_hash(accounts[username], password)
