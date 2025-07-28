import logging
import math
import os

import gspread
from dotenv import load_dotenv
from flask import Blueprint, render_template, request
from google.oauth2.service_account import Credentials

from db.config.payment_schema import ALL_ITEMS
from utils.restore_from_env import restore_from_env

load_dotenv()
restore_from_env("SERVICE_ACCOUNT_BASE64", "credentials/service_account.json")

registered_list_bp = Blueprint("registered_list", __name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file(
    "credentials/service_account.json", scopes=SCOPES
)
gc = gspread.authorize(CREDS)

SHEET_ID_REGISTER = os.getenv("SHEET_ID_REGISTER")
SHEET_NAME = "114"  # 可視情況抽成變數


@registered_list_bp.route("/registered")
def registered_students():
    try:
        sheet = gc.open_by_key(SHEET_ID_REGISTER).worksheet(SHEET_NAME)
        data = sheet.get_all_values()
    except Exception:
        logging.exception("讀取 Google Sheet 失敗")
        return "Server Error: Google Sheet 無法存取", 500

    headers = data[0]
    rows = data[1:]

    per_page = int(request.args.get("per_page", 20))
    page = int(request.args.get("page", 1))
    total = len(rows)
    total_pages = math.ceil(total / per_page)

    start = (page - 1) * per_page
    end = start + per_page
    page_data = rows[start:end]

    students = []
    for row in page_data:
        s = dict(zip(headers, row))
        total_paid = 0
        for item in ALL_ITEMS:
            value = s.get(item, "0").replace(",", "").strip()
            try:
                total_paid += int(value)
            except ValueError:
                continue
        s["繳交總額"] = total_paid
        students.append(s)

    return render_template(
        "registered.html",
        students=students,
        total_pages=total_pages,
        current_page=page,
        per_page=per_page,
    )
