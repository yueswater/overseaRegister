from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Student:
    series_id: str
    student_id: str
    class_id: str
    name: str

    def to_dict(self):
        return {
            "series_id": self.series_id,
            "student_id": self.student_id,
            "class_id": self.class_id,
            "name": self.name
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            series_id=data["series_id"],
            student_id=data.get("student_id", ""),
            class_id=data.get("class_id", ""),
            name=data["name"]
        )