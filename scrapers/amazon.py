import re
from playwright.sync_api import Page

def amazon_get_price(page: Page) -> float:
    page.wait_for_selector('span.a-price', timeout=10000)

    whole_el = page.query_selector('span.a-price-whole')
    fraction_el = page.query_selector('span.a-price-fraction')

    if not whole_el or not fraction_el:
        raise ValueError("Nu am gasit tag-urile a-price-whole / a-price-fraction pe Amazon")

    whole_text = re.sub(r'[^\d]', '', whole_el.inner_text())
    fraction_text = re.sub(r'[^\d]', '', fraction_el.inner_text())

    price_str = f"{whole_text}.{fraction_text}"
    try:
        return float(price_str)
    except ValueError:
        raise ValueError(f"Conversia float a eșuat pentru: '{price_str}'")