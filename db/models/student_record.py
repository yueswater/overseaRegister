from dataclasses import dataclass
from db.models.student import Student
from db.models.payment import Payment
from typing import Dict, Any

@dataclass
class StudentRecord:
    student: Student
    payment: Payment

    def to_dict(self) -> Dict[str, Any]:
        return {
            "student": self.student.to_dict(),
            "payment": self.student.to_dict()
        }
    
    def total(self) -> int:
        return self.payment.total()
    
    def summary(self) -> str:
        return self.payment.render_summary()