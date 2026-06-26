from . import altex, amazon, cel, emag, pcgarage

HTML_SCRAPERS = {
    "amazon": amazon,
    "cel": cel,
    "emag": emag,
    "pcgarage": pcgarage,
}

__all__ = ["HTML_SCRAPERS", "altex"]
