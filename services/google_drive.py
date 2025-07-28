import os
import base64
import pickle
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
TOKEN_PATH = "token_drive.pkl"
DRIVE_FOLDER_ID = "1rMBOrwxIuM_PllFxbSqzrJWrFcNxS2qx"  # ← 改成你想要上傳的資料夾 ID

def restore_token_from_env():
    if os.path.exists(TOKEN_PATH):
        return
    b64 = os.getenv("GOOGLE_TOKEN_B64")
    if not b64:
        raise RuntimeError("GOOGLE_TOKEN_B64 不存在")
    with open(TOKEN_PATH, "wb") as f:
        f.write(base64.b64decode(b64))

def get_drive_service():
    restore_token_from_env()
    with open(TOKEN_PATH, "rb") as f:
        creds = pickle.load(f)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_PATH, "wb") as f2:
                pickle.dump(creds, f2)
        else:
            raise RuntimeError("Token 無效且無法刷新")
    return build("drive", "v3", credentials=creds)

def upload_pdf_to_drive(file_path: str) -> str:
    service = get_drive_service()

    file_metadata = {
        "name": os.path.basename(file_path),
        "parents": [DRIVE_FOLDER_ID]
    }

    media = MediaFileUpload(file_path, mimetype="application/pdf")
    uploaded = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    file_id = uploaded.get("id")

    # 設定為任何人都可以存取連結
    service.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"},
    ).execute()

    return f"https://drive.google.com/file/d/{file_id}/view"
