from smtplib import SMTP
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

load_dotenv()


def parse_price(price_text):
    price_clean = re.sub(r'[^\d,.]', '', price_text)
    if not price_clean:
        return None

    last_comma = price_clean.rfind(',')
    last_dot = price_clean.rfind('.')

    if last_comma > -1 and last_dot > -1:
        decimal_separator = ',' if last_comma > last_dot else '.'
        thousands_separator = '.' if decimal_separator == ',' else ','
        price_clean = price_clean.replace(thousands_separator, '')
        price_clean = price_clean.replace(decimal_separator, '.')
    elif ',' in price_clean:
        price_clean = normalize_single_separator_price(price_clean, ',')
    elif '.' in price_clean:
        price_clean = normalize_single_separator_price(price_clean, '.')

    try:
        return float(price_clean)
    except ValueError:
        return None


def normalize_single_separator_price(price_text, separator):
    whole, fraction = price_text.rsplit(separator, 1)
    if len(fraction) == 3 and whole:
        return whole.replace(separator, '') + fraction
    return price_text.replace(separator, '.')


def get_hostname(link):
    return urlparse(link).netloc.lower()


def get_store(link):
    hostname = get_hostname(link)

    if hostname == 'emag.ro' or hostname.endswith('.emag.ro'):
        return 'emag'
    if hostname == 'altex.ro' or hostname.endswith('.altex.ro'):
        return 'altex'
    if hostname == 'amazon' or '.amazon.' in hostname or hostname.startswith('amazon.'):
        return 'amazon'

    return None


def emag_get_price(soup):
    price_tag = soup.find('p', class_='product-new-price')
    if price_tag:
        return parse_price(price_tag.get_text())
    return None


def amazon_get_price(soup):
    price_tag = soup.find('span', class_='a-price')
    if price_tag:
        offscreen_price = price_tag.find(class_='a-offscreen')
        if offscreen_price:
            return parse_price(offscreen_price.get_text())

        whole = price_tag.find(class_='a-price-whole')
        fraction = price_tag.find(class_='a-price-fraction')
        if whole and fraction:
            whole_text = re.sub(r'[^\d,.]', '', whole.get_text()).rstrip(',.')
            fraction_text = re.sub(r'\D', '', fraction.get_text())
            return parse_price(f'{whole_text}.{fraction_text}')

        return parse_price(price_tag.get_text())
    return None


def altex_get_price_playwright(page):
    try:
        page.wait_for_timeout(4000)

        price_container = page.query_selector('div.text-red-brand:has(.Price-int)')

        if price_container:
            full_text = price_container.inner_text()

            return parse_price(full_text)

        return None

    except Exception as error:
        print(f'Could not parse Altex price: {error}')
        return None


def process_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
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

        for line_number, line in enumerate(lines[1:], start=2):
            parts = line.strip().split()
            if len(parts) != 3:
                print(f'Skipping line {line_number}: expected 3 fields.')
                continue

            email = parts[0]
            link = parts[1]

            try:
                target_price = float(parts[2])
            except ValueError:
                print(f'Skipping line {line_number}: invalid target price "{parts[2]}".')
                continue

            current_price = None
            store = get_store(link)

            if store is None:
                print(f'Skipping line {line_number}: unsupported store in URL "{link}".')
                continue

            try:
                page.goto(link, wait_until="domcontentloaded", timeout=60000)

                if store == 'altex':
                    current_price = altex_get_price_playwright(page)
                else:
                    soup = BeautifulSoup(page.content(), 'html.parser')
                    if store == 'emag':
                        current_price = emag_get_price(soup)
                    elif store == 'amazon':
                        current_price = amazon_get_price(soup)
            except Exception as error:
                print(f'Skipping line {line_number}: could not load "{link}" ({error}).')
                continue

            if current_price is None:
                print(f'Skipping line {line_number}: could not find a price for "{link}".')
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
