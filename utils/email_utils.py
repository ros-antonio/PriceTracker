from collections import defaultdict
from smtplib import SMTP
from typing import Iterable, List, Optional

from data import Alert


def send_mails(
    alerts: Iterable[Alert],
    sender: Optional[str] = None,
    password: Optional[str] = None,
) -> None:
    grouped_alerts = defaultdict(list)
    for alert in alerts:
        grouped_alerts[alert["email"]].append(alert)

    if not grouped_alerts:
        return

    if not sender or not password:
        print("Skipping email alerts: missing EMAIL_ADDRESS or EMAIL_PASSWORD.")
        return

    with SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(sender, password)

        for to_address, recipient_alerts in grouped_alerts.items():
            send_email(smtp, sender, to_address, recipient_alerts)


def send_email(
    smtp_connection: SMTP,
    sender: str,
    to_address: str,
    alerts: List[Alert],
) -> None:
    subject = "Price Tracker Update"
    formatted_alerts = "\n".join(
        [
            f"- {alert['tag']}: {alert['current_price']:.2f} "
            f"(target {alert['target_price']:.2f}) - {alert['link']}"
            for alert in alerts
        ]
    )
    body = (
        f"The price dropped under threshold for {len(alerts)} tracked product(s).\n\n"
        f"{formatted_alerts}"
    )
    msg = f"Subject: {subject}\n\n{body}"

    smtp_connection.sendmail(sender, to_address, msg.encode("utf-8"))
