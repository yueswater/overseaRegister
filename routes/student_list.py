import math
import os

import gspread
from dotenv import load_dotenv
from flask import Blueprint, render_template, request
from google.oauth2.service_account import Credentials

from utils.formatters import format_phone_number

load_dotenv()

student_list_bp = Blueprint("student_list", __name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file(
    "credentials/service_account.json", scopes=SCOPES
)
gc = gspread.authorize(CREDS)

SHEET_ID_STUDENT = os.getenv("SHEET_ID_LOOKUP")  # .env 中設定學生名單 ID
SHEET_NAME = "114"  # 預設工作表名稱


@student_list_bp.route("/students")
def students():
    sheet = gc.open_by_key(SHEET_ID_STUDENT).worksheet(SHEET_NAME)
    data = sheet.get_all_values()

    headers = data[0]
    rows = data[1:]

    per_page = int(request.args.get("per_page", 20))
    page = int(request.args.get("page", 1))
    total = len(rows)
    total_pages = math.ceil(total / per_page)

    start = (page - 1) * per_page
    end = start + per_page
    page_data = rows[start:end]

    students = [dict(zip(headers, row)) for row in page_data]

    for s in students:
        if "聯絡電話" in s:
            s["聯絡電話"] = format_phone_number(s["聯絡電話"])

    return render_template(
        "students.html",
        students=students,
        total_pages=total_pages,
        current_page=page,
        per_page=per_page,
    )
