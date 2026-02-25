from typing import Optional
import re
from bs4 import BeautifulSoup


def emag_get_price(soup: BeautifulSoup) -> float:
    price_tag = soup.find('p', class_='product-new-price')
    
    if not price_tag:
        raise ValueError("Nu am gasit tag-ul pentru pret pe emag")
    
    price_text: str = price_tag.get_text().strip()
    price_text = re.sub(r'[^\d,.]', '', price_text)
    if not price_text:
        raise ValueError(f"Tag-ul a fost gasit, dar nu am putut extrage un numar din: '{price_text}'")
    price_text = price_text.replace('.', '').replace(',', '.')
    
    try:
        return float(price_text)
    except ValueError:
        raise ValueError(f"Conversia la float a esuat pentru '{price_text}'")

