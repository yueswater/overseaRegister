from dataclasses import dataclass, field
from typing import Any, Dict

from db.config.payment_schema import ALL_ITEMS, PAYMENT_METADATA


@dataclass
class Payment:
    items: Dict[str, int] = field(
        default_factory=lambda: {
            item: PAYMENT_METADATA[item]["amount"] for item in ALL_ITEMS
        }
    )

    def total(self) -> int:
        return sum(self.items.values())

    @classmethod
    def from_dict(cls, data: Dict[str, int]):
        items = {
            item: data.get(item, PAYMENT_METADATA[item]["amount"]) for item in ALL_ITEMS
        }
        return cls(items=items)

    def to_dict(self):
        return dict(self.items)

    def apply_reduction(self, key: str) -> None:
        if key in self.items and PAYMENT_METADATA[key]["reducible"]:
            self.items[key] = 0

    def render_summary(self) -> str:
        lines = [f"{k}: 新臺幣 {v} 元" for k, v in self.items.items()]
        lines.append(f"合計：新臺幣 {self.total()} 元")
        return "\n".join(lines)

    def to_form_data(self) -> Dict[str, str]:
        return {f"payment[{k}]": str(v) for k, v in self.items.items()}

    def __getitem__(self, key: str) -> Any:
        return self.items.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.items[key] = value
