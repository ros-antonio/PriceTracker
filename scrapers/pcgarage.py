from typing import Optional
import re
from bs4 import BeautifulSoup


def pcgarage_get_price(soup: BeautifulSoup) -> float:
    # Try the meta tag first (most reliable)
    meta_tag = soup.find('meta', attrs={'itemprop': 'price'})
    if meta_tag and meta_tag.get('content'):
        try:
            return float(str(meta_tag['content']))
        except ValueError:
            pass

    # Fallback: span with class "price_num"
    price_tag = soup.find('span', class_='price_num')
    if not price_tag:
        raise ValueError("Nu am gasit tag-ul pentru pret pe pcgarage")

    price_text: str = price_tag.get_text().strip()
    price_text = re.sub(r'[^\d,.]', '', price_text)
    if not price_text:
        raise ValueError(f"Tag-ul a fost gasit, dar nu am putut extrage un numar din: '{price_text}'")
    price_text = price_text.replace('.', '').replace(',', '.')

    try:
        return float(price_text)
    except ValueError:
        raise ValueError(f"Conversia la float a esuat pentru '{price_text}'")


def pcgarage_get_stock(soup: BeautifulSoup) -> Optional[str]:
    stock_tag = soup.find('p', id='pi_availability')
    if stock_tag:
        return stock_tag.get_text().strip()
    return None
