from typing import TypedDict

class ProductEntry(TypedDict):
    tag: str
    email: str
    link: str
    target_price: float #0 means ignore