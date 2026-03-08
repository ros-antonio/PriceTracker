from .emag import emag_get_price, emag_get_stock
from .amazon import amazon_get_price, amazon_get_stock
from .altex import altex_get_price_playwright, altex_get_stock_playwright
from .pcgarage import pcgarage_get_price, pcgarage_get_stock
from .expertcompany import expertcompany_get_price, expertcompany_get_stock
from .optimusdigital import optimusdigital_get_price, optimusdigital_get_stock
from .cel import cel_get_price, cel_get_stock

__all__ = ["emag_get_price", "emag_get_stock", "amazon_get_price", "amazon_get_stock", "altex_get_price_playwright", "altex_get_stock_playwright", "pcgarage_get_price", "pcgarage_get_stock", "expertcompany_get_price", "expertcompany_get_stock", "optimusdigital_get_price", "optimusdigital_get_stock", "cel_get_price", "cel_get_stock"]
