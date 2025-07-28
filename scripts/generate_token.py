import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
CREDS_PATH = "credentials/gdrive.json"
TOKEN_PATH = "token_drive.pkl"

def generate_token():
    flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
    creds = flow.run_local_server(port=0)
    with open(TOKEN_PATH, "wb") as f:
        pickle.dump(creds, f)
    print("Token 已儲存到 token_drive.pkl")

if __name__ == "__main__":
    generate_token()
