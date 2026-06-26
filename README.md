# Price Tracker

Tracks product prices from eMAG, Amazon, Altex, PC Garage, and CEL.

The app reads products from `data.json`, scrapes current price and stock with
Playwright, writes a markdown report, stores price history in SQLite, and sends
grouped email alerts when a product drops below its target price.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

Create `.env`:

```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_google_app_password
OUTPUT_FILEPATH=results.md
INPUT_FILEPATH=data.json
```

Create `data.json`:

```json
[
  {
    "tag": "Monitor",
    "email": "you@example.com",
    "link": "https://www.emag.ro/example-product",
    "target_price": 700
  }
]
```

## Run

```powershell
python main.py
```

## Files

- `data.json`: products to track.
- `results.md`: latest markdown report.
- `logs/runtime.log`: run log.
- `data/prices.db`: SQLite price history, created automatically.

`target_price` set to `0` disables email alerts for that product but still
tracks and records its price.
