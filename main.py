import os
from typing import List, Optional, Tuple

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

from data import Alert, FoundProduct, PriceMovement, ProductEntry
from data.store import get_last_price, init_db, insert_price
from logs import Logger
from scrapers import HTML_SCRAPERS, altex
from utils import get_store, parse_entries, send_mails

load_dotenv()

DEFAULT_RESULT_FILE = "results.md"
DEFAULT_LOG_FILE = "logs/runtime.log"
DEFAULT_JSON_INPUT = "data.json"


def process_data(input_file_path: str, logger: Optional[Logger] = None) -> None:
    entries = parse_entries(input_file_path)
    alerts: List[Alert] = []

    if logger is None:
        logger = Logger(os.getenv("OUTPUT_FILEPATH", DEFAULT_RESULT_FILE), DEFAULT_LOG_FILE)
        logger.init()

    with Stealth().use_sync(sync_playwright()) as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()

        for entry in entries:
            store = get_store(entry["link"])
            if store is None:
                print(f'Skipping {entry["tag"]}: unsupported store in URL "{entry["link"]}".')
                logger.log(f'WARNING: unsupported store for {entry["tag"]}: {entry["link"]}')
                continue

            try:
                page.goto(entry["link"], wait_until="domcontentloaded", timeout=60000)
                current_price, current_stock = scrape_product(page, store)
            except Exception as error:
                print(f'Skipping {entry["tag"]}: could not load "{entry["link"]}" ({error}).')
                logger.log(f'ERROR: {entry["tag"]} failed: {error}')
                continue

            if current_price is None:
                print(f'Skipping {entry["tag"]}: could not find a price for "{entry["link"]}".')
                logger.log(f'WARNING: price not found for {entry["tag"]}')
                continue

            movement = record_price(entry, store, current_price, current_stock)
            found_product = FoundProduct(
                tag=entry["tag"],
                link=entry["link"],
                current_price=current_price,
                target_price=entry["target_price"],
                stock=current_stock,
                movement=movement,
            )
            logger.write_result(found_product.to_markdown_row())
            logger.log(
                f'INFO: {entry["tag"]} {current_price:.2f} '
                f"(target {entry['target_price']:.2f}, {movement.value})"
            )

            if entry["target_price"] > 0 and current_price < entry["target_price"]:
                alerts.append(
                    {
                        "email": entry["email"],
                        "link": entry["link"],
                        "tag": entry["tag"],
                        "current_price": current_price,
                        "target_price": entry["target_price"],
                    }
                )

        browser.close()

    send_mails(
        alerts,
        sender=os.getenv("EMAIL_ADDRESS"),
        password=os.getenv("EMAIL_PASSWORD"),
    )


def scrape_product(page, store: str) -> Tuple[Optional[float], Optional[str]]:
    if store == "altex":
        return altex.get_price_and_stock(page)

    soup = BeautifulSoup(page.content(), "html.parser")
    scraper = HTML_SCRAPERS[store]
    return scraper.get_price(soup), scraper.get_stock(soup)


def record_price(
    entry: ProductEntry,
    store: str,
    current_price: float,
    current_stock: Optional[str],
) -> PriceMovement:
    last_price = get_last_price(entry["tag"], entry["link"])
    insert_price(entry["tag"], entry["link"], store, current_price, current_stock)

    if last_price is None:
        return PriceMovement.FIRST_PRICE_FOUND
    if current_price < last_price:
        return PriceMovement.LOWER_THAN_LAST
    if current_price > last_price:
        return PriceMovement.HIGHER_THAN_LAST
    return PriceMovement.EQUAL_TO_LAST


def get_input_file() -> Optional[str]:
    configured_path = os.getenv("INPUT_FILEPATH")
    if configured_path and os.path.exists(configured_path):
        return configured_path
    if os.path.exists(DEFAULT_JSON_INPUT):
        return DEFAULT_JSON_INPUT
    return None


def main() -> None:
    input_file = get_input_file()
    if input_file is None:
        print("No input file found. Create data.json.")
        return

    init_db()
    logger = Logger(os.getenv("OUTPUT_FILEPATH", DEFAULT_RESULT_FILE), DEFAULT_LOG_FILE)
    logger.init()
    process_data(input_file, logger)


if __name__ == "__main__":
    main()
