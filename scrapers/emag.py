from typing import Optional

from bs4 import BeautifulSoup

from utils.price import parse_price


def get_price(soup: BeautifulSoup) -> Optional[float]:
    price_tag = soup.find("p", class_="product-new-price")
    if price_tag:
        return parse_price(price_tag.get_text())
    return None


def get_stock(soup: BeautifulSoup) -> Optional[str]:
    stock_tag = soup.find(
        "span",
        class_=lambda value: value
        and any(
            marker in value
            for marker in ["label-limited_stock_qty", "label-in_stock", "label-out_of_stock"]
        ),
    )
    if stock_tag:
        return stock_tag.get_text(strip=True)
    return None
