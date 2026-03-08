from typing import Optional
import re
from bs4 import BeautifulSoup


def cel_get_price(soup: BeautifulSoup) -> float:
    price_span = soup.find('span', id='product-price')
    if not price_span:
        raise ValueError("Nu am gasit tag-ul pentru pret pe cel.ro")

    price_text: str = price_span.get_text().strip()
    price_text = re.sub(r'[^\d,.]', '', price_text)
    if not price_text:
        raise ValueError(f"Tag-ul a fost gasit, dar nu am putut extrage un numar din: '{price_text}'")
    price_text = price_text.replace('.', '').replace(',', '.')

    try:
        return float(price_text)
    except ValueError:
        raise ValueError(f"Conversia la float a esuat pentru '{price_text}'")


def cel_get_stock(soup: BeautifulSoup) -> Optional[str]:
    stock_span = soup.find('span', id='info_stoc')
    if stock_span:
        strong_tag = stock_span.find('strong', class_=re.compile(r'info_stoc'))
        if strong_tag:
            return strong_tag.get_text().strip()
        return stock_span.get_text().strip()
    return None
