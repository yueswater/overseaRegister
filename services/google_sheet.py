import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file(
    "credentials/service_account.json", scopes=SCOPES
)
gc = gspread.authorize(CREDS)

SPREADSHEET_ID = "15SxzEWQKwx3hlBPQVMyJObQUPhRpzrrmuzdNUeMEa1Y"
SHEET_NAME = "114"

def append_student_record(record):
    sheet = gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    row = [
        record.student.series_id,
        record.student.name,
        record.student.class_id,
        record.student.student_id,
        record.student.is_pass_exam,
    ] + [record.payment.items.get(key, 0) for key in sorted(record.payment.items.keys())]
    sheet.append_row(row, value_input_option="USER_ENTERED")
