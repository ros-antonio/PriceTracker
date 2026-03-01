import os
from typing import Optional, List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Page, BrowserContext, Browser
from playwright_stealth import Stealth
from data import Alert, ProductEntry, FoundProduct
from data.store import init_db, get_last_price, insert_price
from enums import FoundPriceType
from scrapers import emag_get_price, emag_get_stock, amazon_get_price, amazon_get_stock, altex_get_price_playwright, altex_get_stock_playwright, pcgarage_get_price, pcgarage_get_stock
from utils import send_mails, parse_entries
from logs.logger import Logger

load_dotenv()

DEFAULT_RESULT_FILE = "results.md"
DEFAULT_LOG_FILE = "logs/runtime.log"

def process_data(input_file_path: str, logger: Optional[Logger] = None) -> None:
    entries: List[ProductEntry] = parse_entries(input_file_path)
    alerts: List[Alert] = []

    if logger is None:
        logger = Logger(DEFAULT_RESULT_FILE, DEFAULT_LOG_FILE)
        logger.init()

    with Stealth().use_sync(sync_playwright()) as p:
        browser: Browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context: BrowserContext = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page: Page = context.new_page()

        for entry in entries:
            current_price: Optional[float] = None
            current_stoc: Optional[str] = None

            try:
                page.goto(entry['link'], wait_until="domcontentloaded", timeout=60000)

                if 'altex.ro' in entry['link']:
                    current_price = altex_get_price_playwright(page)
                    current_stoc = altex_get_stock_playwright(page)
                    logger.log(f"DEBUG: {entry['tag']} cautare pe altex")
                elif 'amazon' in entry['link']:
                    current_price = amazon_get_price(page)
                    current_stoc = amazon_get_stock(page)
                    logger.log(f"DEBUG: {entry['tag']} cautare pe amazon")
                else:
                    soup: BeautifulSoup = BeautifulSoup(page.content(), 'html.parser')
                    if 'emag.ro' in entry['link']:
                        current_price = emag_get_price(soup)
                        current_stoc = emag_get_stock(soup)
                        logger.log(f"DEBUG: {entry['tag']} cautare pe emag")
                    elif 'pcgarage.ro' in entry['link']:
                        current_price = pcgarage_get_price(soup)
                        current_stoc = pcgarage_get_stock(soup)
                        logger.log(f"DEBUG: {entry['tag']} cautare pe pcgarage")
            except Exception as e:
                print(f" Eroare la produsul {entry['tag']}: {e}")
                if logger:
                    logger.log(f"ERROR: produsul {entry['tag']} - {e}")
                continue

            if current_price is not None:
                if entry['target_price'] != 0 and current_price < entry['target_price']:
                    alerts.append(Alert(email=entry['email'], link=entry['link']))
                    logger.log(f"DEBUG: pending mail for {entry['tag']} to {entry['email']}")

                last_price = get_last_price(entry['tag'])
                if last_price is None:
                    price_type = FoundPriceType.FIRST_PRICE_FOUND
                    logger.log(f"INFO: {entry['tag']} - primul pret inregistrat: {int(current_price)} RON")
                elif int(current_price) < last_price:
                    price_type = FoundPriceType.LOWER_THAN_LAST
                    logger.log(f"INFO: {entry['tag']} - pretul a scazut: {last_price} -> {int(current_price)} RON")
                elif int(current_price) > last_price:
                    price_type = FoundPriceType.HIGHER_THAN_LAST
                    logger.log(f"INFO: {entry['tag']} - pretul a crescut: {last_price} -> {int(current_price)} RON")
                else:
                    price_type = FoundPriceType.EQUAL_TO_LAST
                    logger.log(f"INFO: {entry['tag']} - pretul a ramas neschimbat: {int(current_price)} RON")

                insert_price(entry['tag'], int(current_price))

                foundProduct = FoundProduct(entry["tag"], entry["link"], current_price, foundPriceType=price_type, stoc=current_stoc if current_stoc else "unknown")
                logger.writeResult(str(foundProduct))
                logger.log(f"INFO: s-a gasit si s-a scris pretul curent al produsului {entry['tag']}")
            else:
                print(f" Eroare la produsul {entry['tag']}: Nu o fost gasit pret")
                logger.log(f"ERROR: produsul {entry['tag']} - Nu o fost gasit pret")

        browser.close()

    if alerts:
        sender: Optional[str] = os.getenv("EMAIL_ADDRESS")
        password: Optional[str] = os.getenv("EMAIL_PASSWORD")
        try:
            send_mails(alerts, logger, sender, password)
        except Exception as e:
            logger.log(f"ERROR: {e}")



def main() -> None:
    resultsRawPath = os.getenv("OUTPUT_FILEPATH", "results.md")

    logger = Logger(resultsRawPath, "logs/runtime.log")
    if os.path.exists("data.json"):
        init_db()
        logger.init()
        process_data("data.json", logger)
    else:
        print(f" Nu exista fisier de input")
        logger.log("ERROR: Nu exista fisier de input")

if __name__ == '__main__':
    main()
