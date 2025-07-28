import logging

from flask import Blueprint, render_template, request

from db.config.payment_schema import ALL_ITEMS, PAYMENT_METADATA
from services.google_drive import upload_pdf_to_drive
from services.google_sheet import append_student_record
from services.receipt_generator import generate_receipt
from services.student_service import from_form

logging.basicConfig(level=logging.DEBUG)

student_bp = Blueprint("student", __name__)


@student_bp.route("/report", methods=["GET"])
def report_form():
    defaults = {item: PAYMENT_METADATA[item]["amount"] for item in ALL_ITEMS}
    return render_template(
        "report.html", payment_items=ALL_ITEMS, default_payments=defaults
    )


@student_bp.route("/register", methods=["POST"])
def register():
    form_data = request.form.to_dict()
    record = from_form(form_data)

    try:
        # save_student_record(record)
        append_student_record(record)

        receipt_path = generate_receipt(record)
        drive_url = upload_pdf_to_drive(receipt_path)

        logging.debug(record.to_dict())
        return render_template("success.html", record=record, receipt_url=drive_url)
    except Exception:
        logging.exception("Failed to register student.")
