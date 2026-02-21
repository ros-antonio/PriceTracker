from smtplib import SMTP

import os
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup

import re

load_dotenv()

sender = os.getenv("EMAIL_ADDRESS")
password = os.getenv("EMAIL_PASSWORD")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}


def send_email(to_address, product_name):
    with SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender, password)
        subject = f'Price Tracker Update'
        body = f'The price of a product has dropped! Check it out now: {product_name}'
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(sender, to_address, msg)


def process_data(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    for line in lines[1:]:
        parts = line.strip().split(" ")
        if len(parts) != 3:
            continue

        email = parts[0]
        link = parts[1]
        target_price = float(parts[2])

        if 'emag.ro' in link:
            current_price = emag_get_price(link)
            if current_price is not None and current_price < target_price:
                send_email(email, link)
        elif 'amazon.it' in link:
            current_price = amazon_get_price(link)
            if current_price is not None and current_price < target_price:
                send_email(email, link)

def emag_get_price(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
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


def amazon_get_price(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    price_tag = soup.find('span', class_='a-price')
    if price_tag:
        price_text = price_tag.get_text().strip()
        match = re.search(r'\d+[.,]?\d*', price_text)
        if match:
            return float(match.group(0).replace(',', '.'))
    return None


def main():
    process_data("data.txt")


if __name__ == '__main__':
    main()
