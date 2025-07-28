import logging
import os

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

from utils.restore_from_env import restore_from_env

load_dotenv()
restore_from_env("SERVICE_ACCOUNT_BASE64", "credentials/service_account.json")

logging.basicConfig(level=logging.DEBUG)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file(
    "credentials/service_account.json", scopes=SCOPES
)
gc = gspread.authorize(CREDS)

SHEET_ID_LOOKUP = os.getenv("SHEET_ID_LOOKUP")
SHEET_ID_REGISTER = os.getenv("SHEET_ID_REGISTER")
SHEET_NAME = "114"


def append_student_record(record):
    sheet = gc.open_by_key(SHEET_ID_REGISTER).worksheet(SHEET_NAME)
    existing_values = sheet.col_values(1)  # 第一欄為 series_id

    if record.student.series_id in existing_values:
        logging.error(f"序號 {record.student.series_id} 已存在，略過寫入")
        return  # 已存在就不寫入

    # 準備 row 資料
    row = (
        [
            record.student.series_id,
            record.student.name,
            record.student.class_id,
            record.student.student_id,
            record.student.is_pass_exam,
        ]
        + [
            record.payment.items.get(key, 0)
            for key in sorted(record.payment.items.keys())
        ]
        + [record.payment.total()]
    )

    sheet.append_row(row, value_input_option="USER_ENTERED")
    logging.info(f"[WRITE] 已寫入序號 {record.student.series_id}")


def get_name_by_series_id(series_id: str) -> str | None:
    sheet = gc.open_by_key(SHEET_ID_LOOKUP).worksheet(SHEET_NAME)
    records = sheet.get_all_values()

    for _, row in enumerate(records[1:], start=2):  # Skip header
        cell_value = row[0].strip() if row else ""
        if cell_value == series_id:
            return row[1] if len(row) > 1 else None
    return None
