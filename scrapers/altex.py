from typing import Optional
import re
from playwright.sync_api import Page


def altex_get_price_playwright(page: Page) -> Optional[float]:
    page.wait_for_timeout(4000)
    price_container = page.query_selector('div.text-red-brand:has(.Price-int)')

    if not price_container:
        raise ValueError("Nu am gasit tag-ul pentru pret pe altex")

    full_text: str = price_container.inner_text()
    price_clean: str = re.sub(r'[^\d,.]', '', full_text)
    if not price_clean:
        raise ValueError(f"Tag-ul a fost gasit, dar nu am putut extrage un numar din: '{full_text}'")
    price_clean = price_clean.replace('.', '').replace(',', '.')

    try:
        return float(price_clean)
    except ValueError:
        raise ValueError(f"Conversia la float a esuat pentru {price_clean}")

