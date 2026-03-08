from typing import Optional
import re
from bs4 import BeautifulSoup


def expertcompany_get_price(soup: BeautifulSoup) -> float:
    price_div = soup.find('div', class_=re.compile(r'^price\s+cm-reload-'))
    if not price_div:
        raise ValueError("Nu am gasit tag-ul pentru pret pe expertcompany")

    span_tag = price_div.find('bdi')
    if span_tag is None:
        span_tag = price_div

    price_text: str = span_tag.get_text().strip()
    price_text = re.sub(r'[^\d,.]', '', price_text)
    if not price_text:
        raise ValueError(f"Tag-ul a fost gasit, dar nu am putut extrage un numar din: '{price_text}'")
    price_text = price_text.replace(',', '.')

    try:
        return float(price_text)
    except ValueError:
        raise ValueError(f"Conversia la float a esuat pentru '{price_text}'")


def expertcompany_get_stock(soup: BeautifulSoup) -> Optional[str]:
    stock_div = soup.find('div', class_=re.compile(r'^stoc\s+cm-reload-'))
    if stock_div:
        stock_span = stock_div.find('span', class_=re.compile(r'in-stock|out-of-stock'))
        if stock_span:
            return stock_span.get_text().strip()
        return stock_div.get_text().strip()
    return None
