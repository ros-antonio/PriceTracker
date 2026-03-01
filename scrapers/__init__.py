from .emag import emag_get_price, emag_get_stock
from .amazon import amazon_get_price, amazon_get_stock
from .altex import altex_get_price_playwright, altex_get_stock_playwright
from .pcgarage import pcgarage_get_price, pcgarage_get_stock

__all__ = ["emag_get_price", "emag_get_stock", "amazon_get_price", "amazon_get_stock", "altex_get_price_playwright", "altex_get_stock_playwright", "pcgarage_get_price", "pcgarage_get_stock"]
