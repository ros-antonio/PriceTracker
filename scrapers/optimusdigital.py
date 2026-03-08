from typing import Optional
import re
from bs4 import BeautifulSoup


def optimusdigital_get_price(soup: BeautifulSoup) -> float:
    price_span = soup.find('span', id='our_price_display', itemprop='price')
    if price_span and price_span.get('content'):
        try:
            return float(str(price_span['content']))
        except ValueError:
            pass

    if not price_span:
        raise ValueError("Nu am gasit tag-ul pentru pret pe optimusdigital")

    price_text: str = price_span.get_text().strip()
    price_text = re.sub(r'[^\d,.]', '', price_text)
    if not price_text:
        raise ValueError(f"Tag-ul a fost gasit, dar nu am putut extrage un numar din: '{price_text}'")
    price_text = price_text.replace('.', '').replace(',', '.')

    try:
        return float(price_text)
    except ValueError:
        raise ValueError(f"Conversia la float a esuat pentru '{price_text}'")


def optimusdigital_get_stock(soup: BeautifulSoup) -> Optional[str]:
    qty_container = soup.find('p', id='pQuantityAvailable')
    if not qty_container:
        return None

    qty_span = qty_container.find('span', id='quantityAvailable')
    quantity = qty_span.get_text().strip() if qty_span else None

    txt_span = qty_container.find('span', id='quantityAvailableTxtMultiple')
    if txt_span and txt_span.get('style') and 'display:none' in str(txt_span['style']).replace(' ', ''):
        txt_span = None
    if not txt_span:
        txt_span = qty_container.find('span', id='quantityAvailableTxt')
        if txt_span and txt_span.get('style') and 'display:none' in str(txt_span['style']).replace(' ', ''):
            txt_span = None

    label = txt_span.get_text().strip() if txt_span else "in stoc"

    if quantity:
        return f"{quantity} {label}"
    return label
