from smtplib import SMTP
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

load_dotenv()


def emag_get_price(soup):
    price_tag = soup.find('p', class_='product-new-price')
    if price_tag:
        price_text = price_tag.get_text().strip()
        price_text = re.sub(r'[^\d,.]', '', price_text)
        price_text = price_text.replace('.', '').replace(',', '.')
        try:
            return float(price_text)
        except ValueError:
            return None
    return None


def amazon_get_price(soup):
    price_tag = soup.find('span', class_='a-price')
    if price_tag:
        price_text = price_tag.get_text().strip()
        match = re.search(r'\d+[.,]?\d*', price_text)
        if match:
            return float(match.group(0).replace(',', '.'))
    return None


def altex_get_price_playwright(page):
    try:
        page.wait_for_timeout(4000)

        price_container = page.query_selector('div.text-red-brand:has(.Price-int)')

        if price_container:
            full_text = price_container.inner_text()

            price_clean = re.sub(r'[^\d,.]', '', full_text)
            price_clean = price_clean.replace('.', '').replace(',', '.')

            return float(price_clean)

        return None

    except Exception:
        return None


def process_data(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    alerts = []

    with Stealth().use_sync(sync_playwright()) as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) != 3:
                continue

            email = parts[0]
            link = parts[1]

            try:
                target_price = float(parts[2])
            except ValueError:
                continue

            current_price = None

            try:
                page.goto(link, wait_until="domcontentloaded", timeout=60000)

                if 'altex.ro' in link:
                    current_price = altex_get_price_playwright(page)
                else:
                    soup = BeautifulSoup(page.content(), 'html.parser')
                    if 'emag.ro' in link:
                        current_price = emag_get_price(soup)
                    elif 'amazon' in link:
                        current_price = amazon_get_price(soup)
            except Exception:
                continue

            if current_price is not None and current_price < target_price:
                alerts.append((email, link))

        browser.close()

    if alerts:
        sender = os.getenv("EMAIL_ADDRESS")
        password = os.getenv("EMAIL_PASSWORD")

        if sender and password:
            with SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(sender, password)
                for recipient, product_link in alerts:
                    send_email(smtp, sender, recipient, product_link)


def send_email(smtp_connection, sender, to_address, product_link):
    subject = 'Price Tracker Update'
    body = f'The price of a product has dropped! Check it out now: {product_link}'
    msg = f'Subject: {subject}\n\n{body}'
    smtp_connection.sendmail(sender, to_address, msg)


def main():
    if os.path.exists("data.txt"):
        process_data("data.txt")


if __name__ == '__main__':
    main()
