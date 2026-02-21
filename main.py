from smtplib import SMTP
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import re

load_dotenv()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}


def get_soup(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException:
        return None


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


def process_data(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    alerts = []

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

        soup = get_soup(link)
        if not soup:
            continue

        current_price = None
        if 'emag.ro' in link:
            current_price = emag_get_price(soup)
        elif 'amazon.it' in link:
            current_price = amazon_get_price(soup)

        if current_price is not None and current_price < target_price:
            alerts.append((email, link))

    if alerts:
        sender = os.getenv("EMAIL_ADDRESS")
        password = os.getenv("EMAIL_PASSWORD")

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
    process_data("data.txt")


if __name__ == '__main__':
    main()
