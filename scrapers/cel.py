from typing import Optional

from bs4 import BeautifulSoup

from utils.price import parse_price


def get_price(soup: BeautifulSoup) -> Optional[float]:
    price_span = soup.find("span", id="product-price")
    if price_span:
        return parse_price(price_span.get_text())
    return None


def get_stock(soup: BeautifulSoup) -> Optional[str]:
    stock_span = soup.find("span", id="info_stoc")
    if not stock_span:
        return None

    strong_tag = stock_span.find(
        "strong",
        class_=lambda value: value and "info_stoc" in value,
    )
    return (strong_tag or stock_span).get_text(strip=True)
