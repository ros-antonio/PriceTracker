import os
from typing import Optional, List, TypedDict
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Page, BrowserContext, Browser
from playwright_stealth import Stealth
from data import Alert, ProductEntry, FoundProduct
from scrapers import emag_get_price, amazon_get_price, altex_get_price_playwright
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
                elif 'amazon' in entry['link']:
                    current_price = amazon_get_price(page)
                else:
                    soup: BeautifulSoup = BeautifulSoup(page.content(), 'html.parser')
                    if 'emag.ro' in entry['link']:
                        current_price = emag_get_price(soup)
            except Exception as e:
                print(f" Eroare la produsul {entry['tag']}: {e}")
                if logger:
                    logger.log(f"ERROR: produsul {entry['tag']} - {e}")
                continue

            if current_price is not None:
                if entry['target_price'] != 0 and current_price < entry['target_price']:
                    alerts.append(Alert(email=entry['email'], link=entry['link']))

                foundProduct = FoundProduct(entry["tag"], entry["link"], current_price)
                logger.writeResult(str(foundProduct))
            else:
                print(f" Eroare la produsul {entry['tag']}: Nu o fost gasit pret")
                logger.log(f"ERROR: produsul {entry['tag']} - Nu o fost gasit pret")

        browser.close()

    if alerts:
        sender: Optional[str] = os.getenv("EMAIL_ADDRESS")
        password: Optional[str] = os.getenv("EMAIL_PASSWORD")
        send_mails(alerts, sender, password)



def main() -> None:
    resultsRawPath = os.getenv("OUTPUT_FILEPATH", "results.md")

    logger = Logger(resultsRawPath, "logs/runtime.log")
    if os.path.exists("data.json"):
        logger.init()
        process_data("data.json", logger)
    else:
        print(f" Nu exista fisier de input")
        logger.log("ERROR: Nu exista fisier de input")

if __name__ == '__main__':
    main()
