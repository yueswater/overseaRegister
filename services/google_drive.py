import base64
import os
import pickle

from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
TOKEN_PATH = "token_drive.pkl"
DRIVE_FOLDER_ID = (
    "1rMBOrwxIuM_PllFxbSqzrJWrFcNxS2qx"  # ← Change to the folder you want to upload ID
)


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


# def upload_pdf_to_drive(file_path: str) -> str:
#     service = get_drive_service()

#     file_metadata = {"name": os.path.basename(file_path), "parents": [DRIVE_FOLDER_ID]}

#     media = MediaFileUpload(file_path, mimetype="application/pdf")
#     uploaded = (
#         service.files()
#         .create(body=file_metadata, media_body=media, fields="id")
#         .execute()
#     )
#     file_id = uploaded.get("id")

# # Set to access the link by anyone
# service.permissions().create(
# fileId=file_id,
# body={"type": "anyone", "role": "reader"},
# ).execute()

#     return f"https://drive.google.com/file/d/{file_id}/view"


def upload_pdf_to_drive(file_path: str) -> str:
    service = get_drive_service()

    # Get the pure file name (you can add a time stamp by yourself)
    base_name = os.path.basename(file_path)

    # Search for whether the file of the same name already exists in this folder
    query = (
        f"'{DRIVE_FOLDER_ID}' in parents and "
        f"name = '{base_name}' and trashed = false"
    )
    response = (
        service.files().list(q=query, spaces="drive", fields="files(id)").execute()
    )
    files = response.get("files", [])

    media = MediaFileUpload(file_path, mimetype="application/pdf")

    if files:
        # File already exists: overwrite with update
        file_id = files[0]["id"]
        service.files().update(fileId=file_id, media_body=media).execute()
    else:
        # Nothing exists: Create a new file
        file_metadata = {"name": base_name, "parents": [DRIVE_FOLDER_ID]}
        uploaded = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        file_id = uploaded.get("id")

        # Set to be read by anyone
        service.permissions().create(
            fileId=file_id,
            body={"type": "anyone", "role": "reader"},
        ).execute()

    return f"https://drive.google.com/file/d/{file_id}/view"
