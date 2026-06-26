from typing import Optional

from bs4 import BeautifulSoup

from utils.price import parse_price


def get_price(soup: BeautifulSoup) -> Optional[float]:
    meta_tag = soup.find("meta", attrs={"itemprop": "price"})
    if meta_tag and meta_tag.get("content"):
        price = parse_price(str(meta_tag["content"]))
        if price is not None:
            return price

    price_tag = soup.find("span", class_="price_num")
    if price_tag:
        return parse_price(price_tag.get_text())
    return None


def get_stock(soup: BeautifulSoup) -> Optional[str]:
    stock_tag = soup.find("p", id="pi_availability")
    if stock_tag:
        return stock_tag.get_text(strip=True)
    return None
