from typing import Optional, Tuple

from playwright.sync_api import Page

from utils.price import parse_price


def get_price_and_stock(page: Page) -> Tuple[Optional[float], Optional[str]]:
    page.wait_for_timeout(4000)

    price_container = page.query_selector("div.text-red-brand:has(.Price-int)")
    price = parse_price(price_container.inner_text()) if price_container else None

    stock_el = page.query_selector("div.flex.items-center.text-13px.leading-tight")
    stock = stock_el.inner_text().strip() if stock_el else None

    return price, stock
