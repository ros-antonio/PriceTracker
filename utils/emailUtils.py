from smtplib import SMTP
from data import Alert
from typing import List, Optional
from collections import defaultdict
from logs.logger import Logger

def send_mails(alerts: List[Alert], logger: Logger, sender: Optional[str] = None, password: Optional[str] = None) -> None:
    if not sender or not password:
        print("Eroare: Lipsesc credențialele de email din variabilele de mediu.")
        return
        
    grouped_alerts = defaultdict(list)
    for alert in alerts:
        grouped_alerts[alert['email']].append(alert['link'])

    with SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender, password)
        
        for to_address, links in grouped_alerts.items():
            logger.log("INFO: Sending mail")
            send_email(smtp, sender, to_address, links)


def send_email(smtp_connection: SMTP, sender: str, to_address: str, product_links: List[str]) -> None:
    subject: str = 'Price Tracker Update'
    
    formatted_links: str = "\n".join([f"- {link}" for link in product_links])
    body: str = f"The price dropped under threshold for {len(product_links)} of your tracked products!\n\nCheck them out now:\n{formatted_links}"
    msg: str = f"Subject: {subject}\n\n{body}"
    
    smtp_connection.sendmail(sender, to_address, msg.encode('utf-8'))