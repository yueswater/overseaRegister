from dataclasses import dataclass
from typing import Any, Dict

from db.models.payment import Payment
from db.models.student import Student


@dataclass
class StudentRecord:
    student: Student
    payment: Payment

    def to_dict(self) -> Dict[str, Any]:
        return {"student": self.student.to_dict(), "payment": self.student.to_dict()}

    def total(self) -> int:
        return self.payment.total()

    def summary(self) -> str:
        return self.payment.render_summary()
