import re
from typing import Optional

from bs4 import BeautifulSoup

from utils.price import parse_price


def get_price(soup: BeautifulSoup) -> Optional[float]:
    price_tag = soup.find("span", class_="a-price")
    if not price_tag:
        return None

    offscreen_price = price_tag.find(class_="a-offscreen")
    if offscreen_price:
        return parse_price(offscreen_price.get_text())

    whole = price_tag.find(class_="a-price-whole")
    fraction = price_tag.find(class_="a-price-fraction")
    if whole and fraction:
        whole_text = re.sub(r"[^\d,.]", "", whole.get_text()).rstrip(",.")
        fraction_text = re.sub(r"\D", "", fraction.get_text())
        return parse_price(f"{whole_text}.{fraction_text}")

    return parse_price(price_tag.get_text())


def get_stock(soup: BeautifulSoup) -> Optional[str]:
    stock_tag = soup.select_one("#availability span")
    if stock_tag:
        return stock_tag.get_text(strip=True)
    return None
