from werkzeug.security import generate_password_hash

accounts = {
    "nocsh001": generate_password_hash("nocsh001", method="pbkdf2:sha256"),
    "nocsh002": generate_password_hash("nocsh002", method="pbkdf2:sha256"),
    "nocsh003": generate_password_hash("nocsh003", method="pbkdf2:sha256"),
}

for username, hashed_password in accounts.items():
    print(f"{username}:{hashed_password}")
