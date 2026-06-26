from typing import Optional
from urllib.parse import urlparse


SUPPORTED_STORES = {
    "altex",
    "amazon",
    "cel",
    "emag",
    "pcgarage",
}


def get_hostname(link: str) -> str:
    return urlparse(link).netloc.lower()


def host_matches(hostname: str, domain: str) -> bool:
    return hostname == domain or hostname.endswith(f".{domain}")


def get_store(link: str) -> Optional[str]:
    hostname = get_hostname(link)

    if host_matches(hostname, "emag.ro"):
        return "emag"
    if host_matches(hostname, "altex.ro"):
        return "altex"
    if hostname == "amazon" or ".amazon." in hostname or hostname.startswith("amazon."):
        return "amazon"
    if host_matches(hostname, "pcgarage.ro"):
        return "pcgarage"
    if host_matches(hostname, "cel.ro"):
        return "cel"

    return None
