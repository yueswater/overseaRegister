from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Student:
    series_id: str
    name: str
    is_pass_exam: bool
    class_id: str = ""
    student_id: str = ""

    def to_dict(self):
        return {
            "series_id": self.series_id,
            "name": self.name,
            "is_pass_exam": self.is_pass_exam,
            "class_id": self.class_id,
            "student_id": self.student_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            series_id=data["series_id"],
            name=data["name"],
            is_pass_exam=str(data.get("is_pass_exam", "false")).lower()
            in ("1", "true", "yes"),
            class_id=data.get("class_id", ""),
            student_id=data.get("student_id", ""),
        )

    def __repr__(self):
        return f"<Student {self.name} - {self.student_id}>"
