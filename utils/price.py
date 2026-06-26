import re
from typing import Optional


def parse_price(price_text: str) -> Optional[float]:
    price_clean = re.sub(r"[^\d,.]", "", price_text)
    if not price_clean:
        return None

    last_comma = price_clean.rfind(",")
    last_dot = price_clean.rfind(".")

    if last_comma > -1 and last_dot > -1:
        decimal_separator = "," if last_comma > last_dot else "."
        thousands_separator = "." if decimal_separator == "," else ","
        price_clean = price_clean.replace(thousands_separator, "")
        price_clean = price_clean.replace(decimal_separator, ".")
    elif "," in price_clean:
        price_clean = normalize_single_separator_price(price_clean, ",")
    elif "." in price_clean:
        price_clean = normalize_single_separator_price(price_clean, ".")

    try:
        return float(price_clean)
    except ValueError:
        return None


def normalize_single_separator_price(price_text: str, separator: str) -> str:
    whole, fraction = price_text.rsplit(separator, 1)
    if len(fraction) == 3 and whole:
        return whole.replace(separator, "") + fraction
    return price_text.replace(separator, ".")
