import os
from typing import Dict

from db.models.payment import Payment
from db.models.student import Student
from db.models.student_record import StudentRecord

REGISTERED_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "registered_students.xlsx"
)


def from_form(form: Dict) -> StudentRecord:
    student_data = {
        "series_id": form.get("series_id", ""),
        "name": form.get("name", ""),
        "is_pass_exam": form.get("is_pass_exam", "false") in ("true", "1", "on"),
        "class_id": form.get("class_id", ""),
        "student_id": form.get("student_id", ""),
    }

    payment_data = {
        key[len("payment[") : -1]: int(value) if value.strip() else 0
        for key, value in form.items()
        if key.startswith("payment[")
    }

    student = Student.from_dict(student_data)
    payment = Payment.from_dict(payment_data)
    return StudentRecord(student=student, payment=payment)
