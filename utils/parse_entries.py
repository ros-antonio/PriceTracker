import json
from pathlib import Path
from typing import List

from data import ProductEntry


def parse_entries(file_path: str) -> List[ProductEntry]:
    path = Path(file_path)
    if path.suffix.lower() != ".json":
        raise ValueError(f"{path} must be a JSON file.")
    return parse_json_entries(path)


def parse_json_entries(path: Path) -> List[ProductEntry]:
    with path.open("r", encoding="utf-8") as file:
        raw_data = json.load(file)

    if isinstance(raw_data, dict):
        raw_items = [raw_data]
    elif isinstance(raw_data, list):
        raw_items = raw_data
    else:
        raise ValueError(f"{path} must contain a JSON object or array.")

    entries: List[ProductEntry] = []
    for index, item in enumerate(raw_items, start=1):
        if not isinstance(item, dict):
            print(f"Skipping JSON entry {index}: expected an object.")
            continue

        entry = _coerce_entry(
            tag=item.get("tag") or f"product-{index}",
            email=item.get("email"),
            link=item.get("link"),
            target_price=item.get("target_price"),
            source=f"JSON entry {index}",
        )
        if entry:
            entries.append(entry)

    return entries


def _coerce_entry(tag, email, link, target_price, source: str):
    if not email or not link:
        print(f"Skipping {source}: email and link are required.")
        return None

    try:
        price = float(target_price)
    except (TypeError, ValueError):
        print(f'Skipping {source}: invalid target price "{target_price}".')
        return None

    return {
        "tag": str(tag),
        "email": str(email),
        "link": str(link),
        "target_price": price,
    }
