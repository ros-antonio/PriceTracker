from dataclasses import dataclass
from enum import Enum
from typing import Optional, TypedDict


class ProductEntry(TypedDict):
    tag: str
    email: str
    link: str
    target_price: float


class Alert(TypedDict):
    email: str
    link: str
    tag: str
    current_price: float
    target_price: float


class PriceMovement(Enum):
    FIRST_PRICE_FOUND = "first"
    LOWER_THAN_LAST = "lower"
    HIGHER_THAN_LAST = "higher"
    EQUAL_TO_LAST = "equal"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class FoundProduct:
    tag: str
    link: str
    current_price: float
    target_price: float
    stock: Optional[str] = None
    movement: PriceMovement = PriceMovement.UNKNOWN

    def to_markdown_row(self) -> str:
        stock = self.stock or "unknown"
        movement = {
            PriceMovement.LOWER_THAN_LAST: "down",
            PriceMovement.HIGHER_THAN_LAST: "up",
            PriceMovement.EQUAL_TO_LAST: "same",
            PriceMovement.FIRST_PRICE_FOUND: "new",
            PriceMovement.UNKNOWN: "",
        }[self.movement]
        movement_text = f" ({movement})" if movement else ""
        return (
            f"| [{self.tag}]({self.link}) | {stock} | "
            f"{self.current_price:.2f}{movement_text} | {self.target_price:.2f} |"
        )
