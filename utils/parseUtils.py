import json
from typing import List
from data import ProductEntry

def parse_entries(file_path: str) -> List[ProductEntry]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            
        entries: List[ProductEntry] = []
        for item in raw_data:
            try:
                entry: ProductEntry = {
                    "tag": str(item.get("tag", "")),
                    "email": str(item.get("email", "")),
                    "link": str(item.get("link", "")),
                    "target_price": float(item.get("target_price", 0))
                }
                entries.append(entry)
            except (ValueError, TypeError):
                continue
                
        return entries

    except FileNotFoundError:
        print(f"Eroare: Fisierul {file_path} nu a fost gasit.")
        return []
    except json.JSONDecodeError:
        print(f"Eroare: Fisierul {file_path} nu are un format JSON valid.")
        return []